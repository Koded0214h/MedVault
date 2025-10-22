from django.urls import path
from . import views

urlpatterns = [
    # User notifications
    path('my-notifications/', views.UserNotificationsView.as_view(), name='my-notifications'),
    path('my-notifications/unread/', views.UnreadNotificationsView.as_view(), name='unread-notifications'),
    path('my-notifications/<int:notification_recipient_id>/read/', views.mark_notification_read, name='mark-notification-read'),
    path('my-notifications/mark-all-read/', views.mark_all_notifications_read, name='mark-all-read'),
    
    # Preferences
    path('preferences/', views.UserNotificationPreferencesView.as_view(), name='notification-preferences'),
    
    # Device tokens
    path('device-tokens/', views.DeviceTokenView.as_view(), name='device-tokens'),
    path('device-tokens/<int:token_id>/remove/', views.remove_device_token, name='remove-device-token'),
    
    # Admin management
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    
    # Emergency broadcasts
    path('emergency-broadcasts/', views.EmergencyBroadcastListView.as_view(), name='emergency-broadcast-list'),
    path('emergency-broadcasts/<int:pk>/', views.EmergencyBroadcastDetailView.as_view(), name='emergency-broadcast-detail'),
    
    # Bulk operations
    path('bulk/send/', views.send_bulk_notification, name='bulk-send'),
    
    # Stats
    path('stats/', views.notification_stats, name='notification-stats'),
    
    # Integrations
    path('shortage-alerts/<int:prediction_id>/', views.create_shortage_alert, name='create-shortage-alert'),
]