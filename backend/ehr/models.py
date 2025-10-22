from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    blood_type = models.CharField(max_length=5, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # in cm
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # in kg
    allergies = models.TextField(blank=True, null=True)
    chronic_conditions = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Patient: {self.user.get_full_name()}"

class MedicalRecord(models.Model):
    RECORD_TYPE_CHOICES = (
        ('consultation', 'Consultation'),
        ('lab_result', 'Lab Result'),
        ('prescription', 'Prescription'),
        ('immunization', 'Immunization'),
        ('surgery', 'Surgery'),
        ('allergy', 'Allergy'),
        ('vital', 'Vital Signs'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_recorded = models.DateTimeField(auto_now_add=True)
    date_occurred = models.DateTimeField()
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'user_type': 'doctor'})
    
    # Medical specific fields
    diagnosis = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.record_type}: {self.title} - {self.patient}"

class Prescription(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True, null=True)
    prescribed_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.medication_name} for {self.medical_record.patient}"

class LabResult(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='lab_results')
    test_name = models.CharField(max_length=255)
    result_value = models.CharField(max_length=255)
    normal_range = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    lab_name = models.CharField(max_length=255)
    date_tested = models.DateTimeField()
    date_received = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.test_name} - {self.medical_record.patient}"