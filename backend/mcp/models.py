from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class MCPConfig(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    
    # Alert thresholds
    shortage_alert_threshold = models.FloatField(default=0.8)  # 80% confidence
    critical_alert_threshold = models.FloatField(default=0.9)  # 90% confidence
    
    # Data source weights
    demand_data_weight = models.FloatField(default=0.4)
    supply_data_weight = models.FloatField(default=0.4)
    context_data_weight = models.FloatField(default=0.2)
    
    prediction_horizon_days = models.IntegerField(default=14)  # Predict 14 days ahead
    retraining_frequency_hours = models.IntegerField(default=24)  # Retrain every 24 hours
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class DemandData(models.Model):
    medical_item = models.ForeignKey('inventory.MedicalItem', on_delete=models.CASCADE)
    region = models.CharField(max_length=100)  # e.g., "Lagos", "Nairobi"
    
    demand_count = models.IntegerField()  # Number of prescriptions/requests
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    
    # Context factors
    season = models.CharField(max_length=50, blank=True, null=True)  # "rainy", "dry"
    disease_outbreak = models.BooleanField(default=False)
    outbreak_disease = models.CharField(max_length=100, blank=True, null=True)
    
    collected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['medical_item', 'region', 'period_start']

class ContextData(models.Model):
    DATA_TYPE_CHOICES = (
        ('weather', 'Weather'),
        ('disease_trend', 'Disease Trend'),
        ('public_health_alert', 'Public Health Alert'),
        ('seasonal', 'Seasonal'),
        ('economic', 'Economic'),
    )
    
    region = models.CharField(max_length=100)
    data_type = models.CharField(max_length=30, choices=DATA_TYPE_CHOICES)
    
    # Weather data
    temperature = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    rainfall = models.FloatField(blank=True, null=True)
    
    # Disease trends
    disease_name = models.CharField(max_length=100, blank=True, null=True)
    case_count = models.IntegerField(blank=True, null=True)
    trend_direction = models.CharField(max_length=10, choices=(('up', 'Up'), ('down', 'Down'), ('stable', 'Stable')), blank=True, null=True)
    
    # Public health alerts
    alert_level = models.CharField(max_length=20, choices=(('low', 'Low'), ('medium', 'Medium'), ('high', 'High')), blank=True, null=True)
    alert_message = models.TextField(blank=True, null=True)
    
    effective_date = models.DateTimeField()
    expiry_date = models.DateTimeField(blank=True, null=True)
    
    confidence_score = models.FloatField(default=1.0)  # Data reliability
    source = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

class ShortagePrediction(models.Model):
    medical_item = models.ForeignKey('inventory.MedicalItem', on_delete=models.CASCADE)
    region = models.CharField(max_length=100)
    
    predicted_shortage_date = models.DateTimeField()
    confidence_score = models.FloatField()  # 0.0 to 1.0
    severity_level = models.CharField(max_length=20, choices=(
        ('low', 'Low'),
        ('medium', 'Medium'), 
        ('high', 'High'),
        ('critical', 'Critical')
    ))
    
    predicted_shortage_duration = models.IntegerField()  # in days
    affected_population_estimate = models.IntegerField(blank=True, null=True)
    
    # Contributing factors
    demand_increase_reason = models.TextField(blank=True, null=True)
    supply_constraint_reason = models.TextField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['medical_item', 'region', 'predicted_shortage_date']

class PredictionAlert(models.Model):
    ALERT_TYPE_CHOICES = (
        ('shortage_predicted', 'Shortage Predicted'),
        ('shortage_imminent', 'Shortage Imminent'),
        ('shortage_resolved', 'Shortage Resolved'),
    )
    
    prediction = models.ForeignKey(ShortagePrediction, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPE_CHOICES)
    
    message = models.TextField()
    recommended_actions = models.TextField(blank=True, null=True)
    
    # Target recipients
    notify_vendors = models.BooleanField(default=True)
    notify_health_authorities = models.BooleanField(default=True)
    notify_public = models.BooleanField(default=False)
    
    sent_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.alert_type} - {self.prediction.medical_item.name}"