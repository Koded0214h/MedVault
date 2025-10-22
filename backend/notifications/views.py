from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone
from .models import (
    Notification, NotificationRecipient, EmergencyBroadcast,
    UserNotificationPreference, DeviceToken
)
from .serializers import (
    NotificationSerializer, NotificationCreateSerializer,
    EmergencyBroadcastSerializer, EmergencyBroadcastCreateSerializer,
    UserNotificationPreferenceSerializer, DeviceTokenSerializer,
    UserNotificationSerializer, NotificationStatsSerializer,
    BulkNotificationSerializer
)
from django.contrib.auth import get_user_model
from .services import NotificationService, EmergencyBroadcastService, ShortageAlertService

User = get_user_model()

# User-facing notifications
class UserNotificationsView(generics.ListAPIView):
    serializer_class = UserNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'notification__notification_type']
    ordering_fields = ['created_at', 'notification__priority']
    
    def get_queryset(self):
        return NotificationRecipient.objects.filter(
            user=self.request.user
        ).select_related('notification').order_by('-created_at')

class UnreadNotificationsView(generics.ListAPIView):
    serializer_class = UserNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return NotificationRecipient.objects.filter(
            user=self.request.user,
            status__in=['sent', 'delivered']
        ).select_related('notification').order_by('-created_at')

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, notification_recipient_id):
    """
    Mark a notification as read
    """
    try:
        recipient = NotificationRecipient.objects.get(
            id=notification_recipient_id,
            user=request.user
        )
        
        recipient.status = 'read'
        recipient.read_at = timezone.now()
        recipient.save()
        
        return Response({'message': 'Notification marked as read'})
    
    except NotificationRecipient.DoesNotExist:
        return Response(
            {'error': 'Notification not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    """
    Mark all user notifications as read
    """
    updated_count = NotificationRecipient.objects.filter(
        user=request.user,
        status__in=['sent', 'delivered']
    ).update(status='read', read_at=timezone.now())
    
    return Response({
        'message': f'Marked {updated_count} notifications as read'
    })

# Notification preferences
class UserNotificationPreferencesView(generics.RetrieveUpdateAPIView):
    serializer_class = UserNotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        preferences, created = UserNotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return preferences

# Device token management
class DeviceTokenView(generics.ListCreateAPIView):
    serializer_class = DeviceTokenSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return DeviceToken.objects.filter(user=self.request.user, is_active=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_device_token(request, token_id):
    """
    Remove a device token
    """
    try:
        device_token = DeviceToken.objects.get(
            id=token_id,
            user=request.user
        )
        device_token.delete()
        
        return Response({'message': 'Device token removed'})
    
    except DeviceToken.DoesNotExist:
        return Response(
            {'error': 'Device token not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

# Admin notification management
class NotificationListView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['notification_type', 'priority', 'is_sent']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'scheduled_for', 'sent_at']
    
    def get_queryset(self):
        return Notification.objects.all().prefetch_related('recipients')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NotificationCreateSerializer
        return NotificationSerializer
    
    def perform_create(self, serializer):
        notification = serializer.save()
        # Auto-send if no scheduled time
        if not notification.scheduled_for:
            NotificationService.deliver_notification(notification)

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

# Emergency broadcasts
class EmergencyBroadcastListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['emergency_type', 'urgency_level', 'is_active']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'starts_at', 'expires_at']
    
    def get_queryset(self):
        return EmergencyBroadcast.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmergencyBroadcastCreateSerializer
        return EmergencyBroadcastSerializer
    
    def perform_create(self, serializer):
        broadcast = serializer.save(authorized_by=self.request.user)
        EmergencyBroadcastService.activate_broadcast(broadcast)

class EmergencyBroadcastDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyBroadcast.objects.all()
    serializer_class = EmergencyBroadcastSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

# Bulk operations
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
def send_bulk_notification(request):
    """
    Send notification to specific users
    """
    serializer = BulkNotificationSerializer(data=request.data)
    
    if serializer.is_valid():
        user_ids = serializer.validated_data['user_ids']
        users = User.objects.filter(id__in=user_ids, is_active=True)
        
        notification_data = {
            'title': serializer.validated_data['title'],
            'message': serializer.validated_data['message'],
            'notification_type': serializer.validated_data['notification_type'],
            'priority': serializer.validated_data['priority'],
        }
        
        notification = NotificationService.create_notification(notification_data)
        
        # Manually add recipients
        for user in users:
            NotificationService.deliver_to_user(notification, user)
        
        return Response({
            'message': f'Notification sent to {users.count()} users',
            'notification_id': notification.id
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Stats and dashboard
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notification_stats(request):
    """
    Get notification statistics
    """
    user = request.user
    
    if user.user_type == 'patient':
        # Patient stats
        total_notifications = NotificationRecipient.objects.filter(user=user).count()
        unread_count = NotificationRecipient.objects.filter(
            user=user, 
            status__in=['sent', 'delivered']
        ).count()
        
        stats = {
            'total_notifications': total_notifications,
            'unread_count': unread_count,
            'emergency_alerts': NotificationRecipient.objects.filter(
                user=user,
                notification__notification_type='emergency_broadcast'
            ).count(),
            'shortage_alerts': NotificationRecipient.objects.filter(
                user=user,
                notification__notification_type='shortage_alert'
            ).count(),
            'delivery_success_rate': 95.0,  # This would be calculated from actual delivery data
        }
    else:
        # Admin stats
        stats = {
            'total_notifications': Notification.objects.count(),
            'unread_count': NotificationRecipient.objects.filter(
                status__in=['sent', 'delivered']
            ).count(),
            'emergency_alerts': EmergencyBroadcast.objects.count(),
            'shortage_alerts': Notification.objects.filter(
                notification_type='shortage_alert'
            ).count(),
            'delivery_success_rate': 92.5,
        }
    
    serializer = NotificationStatsSerializer(stats)
    return Response(serializer.data)

# Integration with other services
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_shortage_alert(request, prediction_id):
    """
    Create shortage alert from prediction (called by MCP system)
    """
    from mcp.models import ShortagePrediction
    
    try:
        prediction = ShortagePrediction.objects.get(id=prediction_id)
        notification = ShortageAlertService.create_shortage_alert(prediction)
        
        return Response({
            'message': 'Shortage alert created',
            'notification_id': notification.id
        })
    
    except ShortagePrediction.DoesNotExist:
        return Response(
            {'error': 'Prediction not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )