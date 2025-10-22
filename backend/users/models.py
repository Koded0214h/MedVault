from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('pharmacist', 'Pharmacist'),
        ('lab_technician', 'Lab Technician'),
        ('vendor', 'Vendor'),
        ('admin', 'System Admin'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='patient')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    user_groups = models.ManyToManyField(Group, related_name='user_related_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_realted_permissions')

    def __str__(self):
        return f"{self.username} ({self.user_type})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Medical professional specific fields
    license_number = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=200, blank=True, null=True)
    hospital_affiliation = models.CharField(max_length=255, blank=True, null=True)
    
    # Vendor specific fields
    company_name = models.CharField(max_length=255, blank=True, null=True)
    business_license = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"