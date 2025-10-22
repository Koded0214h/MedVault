from django.contrib import admin
from .models import (
    Notification, NotificationRecipient, EmergencyBroadcast,
    UserNotificationPreference, DeviceToken
)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'priority', 'is_sent', 'created_at')
    list_filter = ('notification_type', 'priority', 'is_sent', 'created_at')
    search_fields = ('title', 'message')
    readonly_fields = ('sent_at',)

@admin.register(NotificationRecipient)
class NotificationRecipientAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification', 'status', 'read_at', 'created_at')
    list_filter = ('status', 'sent_via_push', 'sent_via_sms', 'sent_via_email')
    search_fields = ('user__username', 'notification__title')

@admin.register(EmergencyBroadcast)
class EmergencyBroadcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'emergency_type', 'urgency_level', 'is_active', 'created_at')
    list_filter = ('emergency_type', 'urgency_level', 'is_active')
    search_fields = ('title', 'message')
    readonly_fields = ('total_recipients', 'delivered_count', 'read_count')

@admin.register(UserNotificationPreference)
class UserNotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'push_notifications', 'sms_notifications', 'email_notifications')
    list_filter = ('push_notifications', 'sms_notifications', 'email_notifications')
    search_fields = ('user__username',)

@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_type', 'is_active', 'last_used')
    list_filter = ('device_type', 'is_active')
    search_fields = ('user__username', 'token')