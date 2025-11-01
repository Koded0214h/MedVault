from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('shortage_alert', 'Shortage Alert'),
        ('emergency_broadcast', 'Emergency Broadcast'),
        ('appointment_reminder', 'Appointment Reminder'),
        ('prescription_ready', 'Prescription Ready'),
        ('lab_result_ready', 'Lab Result Ready'),
        ('stock_update', 'Stock Update'),
        ('system_alert', 'System Alert'),
        ('health_tip', 'Health Tip'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )

    # Basic notification fields
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    # Target audience
    recipients = models.ManyToManyField(User, through='NotificationRecipient', related_name='notifications')
    target_user_types = models.JSONField(default=list, blank=True)  # ['patient', 'doctor', etc.]
    target_regions = models.JSONField(default=list, blank=True)  # ['Lagos', 'Nairobi', etc.]

    # Related objects (for contextual notifications)
    related_medical_item = models.ForeignKey('inventory.MedicalItem', on_delete=models.SET_NULL, null=True, blank=True)
    related_prediction = models.ForeignKey('mcp.ShortagePrediction', on_delete=models.SET_NULL, null=True, blank=True)
    related_prescription = models.ForeignKey('ehr.Prescription', on_delete=models.SET_NULL, null=True, blank=True)

    # Delivery control
    scheduled_for = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)

    # Actions
    action_url = models.CharField(max_length=500, blank=True, null=True)
    action_text = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.notification_type}: {self.title}"

    def save(self, *args, **kwargs):
        if self.is_sent and not self.sent_at:
            self.sent_at = timezone.now()
        super().save(*args, **kwargs)

class Alert(models.Model):
    ALERT_TYPE_CHOICES = (
        ('shortage_warning', 'Shortage Warning'),
        ('emergency_alert', 'Emergency Alert'),
        ('system_notification', 'System Notification'),
        ('health_advisory', 'Health Advisory'),
    )

    title = models.CharField(max_length=255)
    message = models.TextField()
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=(
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ), default='medium')

    # Related objects
    related_notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='alerts', null=True, blank=True)
    related_medical_item = models.ForeignKey('inventory.MedicalItem', on_delete=models.SET_NULL, null=True, blank=True)
    related_prediction = models.ForeignKey('mcp.ShortagePrediction', on_delete=models.SET_NULL, null=True, blank=True)

    # Target audience
    target_regions = models.JSONField(default=list, blank=True)
    target_user_types = models.JSONField(default=list, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.alert_type}: {self.title}"



class NotificationRecipient(models.Model):
    DELIVERY_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
    )
    
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Delivery status
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='pending')
    read_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    # Delivery channels
    sent_via_push = models.BooleanField(default=False)
    sent_via_sms = models.BooleanField(default=False)
    sent_via_email = models.BooleanField(default=False)
    sent_via_in_app = models.BooleanField(default=False)
    
    # Failure tracking
    failure_reason = models.TextField(blank=True, null=True)
    retry_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['notification', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.notification.title}"

class EmergencyBroadcast(models.Model):
    EMERGENCY_TYPE_CHOICES = (
        ('disease_outbreak', 'Disease Outbreak'),
        ('natural_disaster', 'Natural Disaster'),
        ('security_alert', 'Security Alert'),
        ('health_advisory', 'Health Advisory'),
        ('resource_shortage', 'Resource Shortage'),
    )
    
    URGENCY_LEVEL_CHOICES = (
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
        ('life_threatening', 'Life Threatening'),
    )
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    emergency_type = models.CharField(max_length=50, choices=EMERGENCY_TYPE_CHOICES)
    urgency_level = models.CharField(max_length=20, choices=URGENCY_LEVEL_CHOICES)
    
    # Geographic targeting
    regions = models.JSONField(default=list)  # Specific regions
    radius_km = models.IntegerField(null=True, blank=True)  # Broadcast radius
    coordinates_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    coordinates_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Medical targeting
    target_conditions = models.JSONField(default=list, blank=True)  # ['diabetes', 'asthma', etc.]
    target_blood_types = models.JSONField(default=list, blank=True)  # ['A+', 'O-', etc.]
    target_medications = models.JSONField(default=list, blank=True)  # ['insulin', 'ventolin', etc.]
    
    # Break Glass features
    break_glass_activated = models.BooleanField(default=False)
    break_glass_reason = models.TextField(blank=True, null=True)
    authorized_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorized_broadcasts')
    
    # Delivery stats
    total_recipients = models.IntegerField(default=0)
    delivered_count = models.IntegerField(default=0)
    read_count = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Emergency: {self.title} ({self.urgency_level})"

class UserNotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Channel preferences
    push_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    in_app_notifications = models.BooleanField(default=True)
    
    # Notification type preferences
    receive_shortage_alerts = models.BooleanField(default=True)
    receive_emergency_broadcasts = models.BooleanField(default=True)
    receive_appointment_reminders = models.BooleanField(default=True)
    receive_prescription_alerts = models.BooleanField(default=True)
    receive_lab_result_alerts = models.BooleanField(default=True)
    receive_stock_updates = models.BooleanField(default=True)
    receive_health_tips = models.BooleanField(default=True)
    
    # Quiet hours
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    
    # Emergency override
    emergency_override = models.BooleanField(default=True)  # Receive critical alerts even during quiet hours
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"

class DeviceToken(models.Model):
    DEVICE_TYPE_CHOICES = (
        ('ios', 'iOS'),
        ('android', 'Android'),
        ('web', 'Web'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device_tokens')
    token = models.CharField(max_length=255)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES)
    device_id = models.CharField(max_length=255, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(auto_now=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'token']

    def __str__(self):
        return f"{self.user.username} - {self.device_type}"