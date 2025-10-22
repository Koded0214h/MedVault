from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Notification, NotificationRecipient, EmergencyBroadcast,
    UserNotificationPreference, DeviceToken
)

User = get_user_model()

class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'last_used')

class UserNotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotificationPreference
        fields = '__all__'
        read_only_fields = ('user', 'updated_at')

class NotificationRecipientSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = NotificationRecipient
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    recipients_count = serializers.SerializerMethodField()
    read_count = serializers.SerializerMethodField()
    delivery_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = '__all__'
    
    def get_recipients_count(self, obj):
        return obj.recipients.count()
    
    def get_read_count(self, obj):
        return obj.notificationrecipient_set.filter(status='read').count()
    
    def get_delivery_status(self, obj):
        return {
            'pending': obj.notificationrecipient_set.filter(status='pending').count(),
            'sent': obj.notificationrecipient_set.filter(status='sent').count(),
            'delivered': obj.notificationrecipient_set.filter(status='delivered').count(),
            'read': obj.notificationrecipient_set.filter(status='read').count(),
            'failed': obj.notificationrecipient_set.filter(status='failed').count(),
        }

class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'title', 'message', 'notification_type', 'priority',
            'target_user_types', 'target_regions', 'related_medical_item',
            'related_prediction', 'related_prescription', 'scheduled_for',
            'expires_at', 'action_url', 'action_text'
        )

class EmergencyBroadcastSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='authorized_by.get_full_name', read_only=True)
    delivery_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = EmergencyBroadcast
        fields = '__all__'
        read_only_fields = ('total_recipients', 'delivered_count', 'read_count')
    
    def get_delivery_rate(self, obj):
        if obj.total_recipients > 0:
            return (obj.delivered_count / obj.total_recipients) * 100
        return 0

class EmergencyBroadcastCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyBroadcast
        fields = (
            'title', 'message', 'emergency_type', 'urgency_level',
            'regions', 'radius_km', 'coordinates_lat', 'coordinates_lng',
            'target_conditions', 'target_blood_types', 'target_medications',
            'break_glass_activated', 'break_glass_reason', 'expires_at'
        )

class UserNotificationSerializer(serializers.ModelSerializer):
    notification_details = NotificationSerializer(source='notification', read_only=True)
    
    class Meta:
        model = NotificationRecipient
        fields = (
            'id', 'notification', 'notification_details', 'status',
            'read_at', 'delivered_at', 'sent_via_push', 'sent_via_sms',
            'sent_via_email', 'sent_via_in_app', 'created_at'
        )

# Dashboard serializers
class NotificationStatsSerializer(serializers.Serializer):
    total_notifications = serializers.IntegerField()
    unread_count = serializers.IntegerField()
    emergency_alerts = serializers.IntegerField()
    shortage_alerts = serializers.IntegerField()
    delivery_success_rate = serializers.FloatField()

class BulkNotificationSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField())
    title = serializers.CharField(max_length=255)
    message = serializers.CharField()
    notification_type = serializers.ChoiceField(choices=Notification.NOTIFICATION_TYPE_CHOICES)
    priority = serializers.ChoiceField(choices=Notification.PRIORITY_CHOICES, default='medium')