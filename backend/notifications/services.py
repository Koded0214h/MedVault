import logging
from datetime import datetime, time
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import (
    Notification, NotificationRecipient, EmergencyBroadcast,
    UserNotificationPreference, DeviceToken
)
from inventory.models import MedicalItem
from ehr.models import Patient

User = get_user_model()
logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    def create_notification(notification_data, send_immediately=True):
        """
        Create a notification and optionally send it immediately
        """
        try:
            notification = Notification.objects.create(**notification_data)
            
            if send_immediately and not notification.scheduled_for:
                NotificationService.deliver_notification(notification)
            
            return notification
            
        except Exception as e:
            logger.error(f"Error creating notification: {str(e)}")
            raise
    
    @staticmethod
    def get_recipients_for_notification(notification):
        """
        Get recipients based on notification targeting
        """
        base_query = User.objects.filter(is_active=True)
        
        # Filter by user types
        if notification.target_user_types:
            base_query = base_query.filter(user_type__in=notification.target_user_types)
        
        # Filter by regions
        if notification.target_regions:
            # This would need to be enhanced with actual location data
            base_query = base_query.filter(
                Q(city__in=notification.target_regions) |
                Q(vendor_profile__city__in=notification.target_regions)
            ).distinct()
        
        # Additional filtering for medical conditions
        if notification.related_medical_item:
            # Find users who might need this medication
            patients_with_condition = Patient.objects.filter(
                current_medications__icontains=notification.related_medical_item.name
            ).values_list('user_id', flat=True)
            base_query = base_query.filter(id__in=patients_with_condition)
        
        return base_query
    
    @staticmethod
    def deliver_notification(notification):
        """
        Deliver notification to all recipients
        """
        try:
            recipients = NotificationService.get_recipients_for_notification(notification)
            
            for user in recipients:
                NotificationService.deliver_to_user(notification, user)
            
            notification.is_sent = True
            notification.sent_at = timezone.now()
            notification.save()
            
            logger.info(f"Notification {notification.id} delivered to {recipients.count()} users")
            
        except Exception as e:
            logger.error(f"Error delivering notification {notification.id}: {str(e)}")
    
    @staticmethod
    def deliver_to_user(notification, user):
        """
        Deliver notification to a specific user via preferred channels
        """
        try:
            # Get or create recipient record
            recipient, created = NotificationRecipient.objects.get_or_create(
                notification=notification,
                user=user
            )
            
            # Check user preferences
            preferences = NotificationService.get_user_preferences(user)
            
            # Check quiet hours
            if NotificationService.is_quiet_hours(preferences) and notification.priority != 'critical':
                logger.info(f"Quiet hours active for {user.username}, skipping delivery")
                return
            
            # Deliver via preferred channels
            delivery_success = False
            
            if preferences.push_notifications:
                if NotificationService.send_push_notification(notification, user):
                    recipient.sent_via_push = True
                    delivery_success = True
            
            if preferences.sms_notifications and user.phone_number:
                if NotificationService.send_sms_notification(notification, user):
                    recipient.sent_via_sms = True
                    delivery_success = True
            
            if preferences.email_notifications and user.email:
                if NotificationService.send_email_notification(notification, user):
                    recipient.sent_via_email = True
                    delivery_success = True
            
            if preferences.in_app_notifications:
                recipient.sent_via_in_app = True
                delivery_success = True
            
            if delivery_success:
                recipient.status = 'sent'
                recipient.delivered_at = timezone.now()
            else:
                recipient.status = 'failed'
                recipient.failure_reason = "All delivery channels failed"
            
            recipient.save()
            
        except Exception as e:
            logger.error(f"Error delivering to user {user.username}: {str(e)}")
    
    @staticmethod
    def get_user_preferences(user):
        """
        Get user notification preferences, create default if not exists
        """
        preferences, created = UserNotificationPreference.objects.get_or_create(user=user)
        return preferences
    
    @staticmethod
    def is_quiet_hours(preferences):
        """
        Check if current time is within user's quiet hours
        """
        if not preferences.quiet_hours_start or not preferences.quiet_hours_end:
            return False
        
        now = timezone.now().time()
        return preferences.quiet_hours_start <= now <= preferences.quiet_hours_end
    
    @staticmethod
    def send_push_notification(notification, user):
        """
        Send push notification (integrate with FCM/APNS)
        """
        try:
            # Get user's device tokens
            device_tokens = DeviceToken.objects.filter(user=user, is_active=True)
            
            for device_token in device_tokens:
                # Integration with Firebase Cloud Messaging or Apple Push Notification Service
                # This is a placeholder - implement actual push service integration
                logger.info(f"Push sent to {user.username} via {device_token.device_type}: {notification.title}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending push to {user.username}: {str(e)}")
            return False
    
    @staticmethod
    def send_sms_notification(notification, user):
        """
        Send SMS notification (integrate with SMS gateway)
        """
        try:
            # Integration with SMS gateway like Twilio, Africa's Talking, etc.
            # This is a placeholder - implement actual SMS service integration
            logger.info(f"SMS sent to {user.phone_number}: {notification.title}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending SMS to {user.phone_number}: {str(e)}")
            return False
    
    @staticmethod
    def send_email_notification(notification, user):
        """
        Send email notification
        """
        try:
            # Integration with email service
            # This is a placeholder - implement actual email service integration
            logger.info(f"Email sent to {user.email}: {notification.title}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email to {user.email}: {str(e)}")
            return False

class EmergencyBroadcastService:
    @staticmethod
    def create_emergency_broadcast(broadcast_data, author):
        """
        Create and activate emergency broadcast
        """
        try:
            broadcast = EmergencyBroadcast.objects.create(
                **broadcast_data,
                authorized_by=author
            )
            
            EmergencyBroadcastService.activate_broadcast(broadcast)
            
            return broadcast
            
        except Exception as e:
            logger.error(f"Error creating emergency broadcast: {str(e)}")
            raise
    
    @staticmethod
    def activate_broadcast(broadcast):
        """
        Activate emergency broadcast and deliver to targeted users
        """
        try:
            # Get targeted users based on broadcast criteria
            targeted_users = EmergencyBroadcastService.get_targeted_users(broadcast)
            broadcast.total_recipients = targeted_users.count()
            broadcast.save()
            
            # Create notification for emergency broadcast
            notification_data = {
                'title': f"EMERGENCY: {broadcast.title}",
                'message': broadcast.message,
                'notification_type': 'emergency_broadcast',
                'priority': 'critical',  # Emergency broadcasts are always critical
                'target_user_types': [],  # Already filtered in targeted_users
                'target_regions': broadcast.regions,
                'expires_at': broadcast.expires_at,
            }
            
            notification = Notification.objects.create(**notification_data)
            
            # Deliver to targeted users (bypassing quiet hours)
            for user in targeted_users:
                recipient = NotificationRecipient.objects.create(
                    notification=notification,
                    user=user,
                    status='sent'
                )
                
                # Force delivery regardless of preferences for emergencies
                NotificationService.deliver_to_user(notification, user)
                
                # Update broadcast stats
                if recipient.status == 'delivered':
                    broadcast.delivered_count += 1
            
            broadcast.save()
            logger.info(f"Emergency broadcast activated: {broadcast.title}")
            
        except Exception as e:
            logger.error(f"Error activating emergency broadcast: {str(e)}")
    
    @staticmethod
    def get_targeted_users(broadcast):
        """
        Get users targeted by emergency broadcast based on geographic and medical criteria
        """
        base_query = User.objects.filter(is_active=True)
        
        # Geographic filtering (simplified - would need proper location service)
        if broadcast.regions:
            base_query = base_query.filter(
                Q(city__in=broadcast.regions) |
                Q(vendor_profile__city__in=broadcast.regions)
            ).distinct()
        
        # Medical condition filtering
        if broadcast.target_conditions:
            patients_with_conditions = Patient.objects.filter(
                chronic_conditions__icontains=broadcast.target_conditions[0]  # Simplified
            ).values_list('user_id', flat=True)
            base_query = base_query.filter(id__in=patients_with_conditions)
        
        # Blood type filtering
        if broadcast.target_blood_types:
            patients_with_blood_types = Patient.objects.filter(
                blood_type__in=broadcast.target_blood_types
            ).values_list('user_id', flat=True)
            base_query = base_query.filter(id__in=patients_with_blood_types)
        
        return base_query

class ShortageAlertService:
    @staticmethod
    def create_shortage_alert(prediction):
        """
        Create shortage alert from prediction
        """
        try:
            notification_data = {
                'title': f"Shortage Alert: {prediction.medical_item.name}",
                'message': f"Potential shortage predicted in {prediction.region}. Severity: {prediction.severity_level}",
                'notification_type': 'shortage_alert',
                'priority': 'high' if prediction.severity_level in ['high', 'critical'] else 'medium',
                'target_user_types': ['pharmacist', 'vendor', 'doctor'],
                'target_regions': [prediction.region],
                'related_medical_item': prediction.medical_item,
                'related_prediction': prediction,
            }
            
            return NotificationService.create_notification(notification_data)
            
        except Exception as e:
            logger.error(f"Error creating shortage alert: {str(e)}")
            raise