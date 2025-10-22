from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Vendor(models.Model):
    VENDOR_TYPE_CHOICES = (
        ('pharmacy', 'Pharmacy'),
        ('laboratory', 'Laboratory'),
        ('hospital', 'Hospital'),
        ('supplier', 'Supplier'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_profile')
    vendor_type = models.CharField(max_length=20, choices=VENDOR_TYPE_CHOICES)
    business_name = models.CharField(max_length=255)
    business_license = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    # Location without GDAL - using simple lat/lng fields
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Nigeria')
    
    # Simple latitude/longitude fields instead of PointField
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    
    contact_person = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    operating_hours = models.TextField(blank=True, null=True)
    services_offered = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.business_name} ({self.vendor_type})"

    @property
    def has_coordinates(self):
        return self.latitude is not None and self.longitude is not None

    def get_distance(self, lat, lng):
        """Calculate approximate distance using Haversine formula"""
        if not self.has_coordinates:
            return None
            
        from math import radians, sin, cos, sqrt, atan2
            
        R = 6371  # Earth radius in kilometers
        
        lat1 = radians(float(self.latitude))
        lon1 = radians(float(self.longitude))
        lat2 = radians(float(lat))
        lon2 = radians(float(lng))
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c

class MedicalItem(models.Model):
    ITEM_CATEGORY_CHOICES = (
        ('medication', 'Medication'),
        ('vaccine', 'Vaccine'),
        ('medical_supply', 'Medical Supply'),
        ('lab_equipment', 'Lab Equipment'),
        ('blood_type', 'Blood Type'),
        ('diagnostic_tool', 'Diagnostic Tool'),
    )
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=ITEM_CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    unit_of_measure = models.CharField(max_length=50)
    default_shelf_life = models.IntegerField(blank=True, null=True)
    
    generic_name = models.CharField(max_length=255, blank=True, null=True)
    strength = models.CharField(max_length=100, blank=True, null=True)
    
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    rh_factor = models.CharField(max_length=5, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['name', 'category', 'strength']

    def __str__(self):
        if self.category == 'blood_type' and self.blood_group:
            return f"Blood {self.blood_group}{self.rh_factor}"
        return f"{self.name} ({self.category})"

class Inventory(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='inventory_items')
    medical_item = models.ForeignKey(MedicalItem, on_delete=models.CASCADE)
    
    current_stock = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=10)
    maximum_stock = models.IntegerField(default=1000)
    
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    
    last_restocked = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['vendor', 'medical_item', 'batch_number']
        verbose_name_plural = 'Inventories'

    def __str__(self):
        return f"{self.medical_item.name} at {self.vendor.business_name}"

class StockTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
        ('return', 'Return'),
    )
    
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.IntegerField()
    previous_stock = models.IntegerField()
    new_stock = models.IntegerField()
    
    reason = models.TextField(blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    
    prescription = models.ForeignKey('ehr.Prescription', on_delete=models.SET_NULL, blank=True, null=True)
    
    transaction_date = models.DateTimeField(auto_now_add=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.previous_stock = self.inventory.current_stock
            
            if self.transaction_type == 'in':
                self.new_stock = self.previous_stock + self.quantity
            elif self.transaction_type in ['out', 'return']:
                self.new_stock = self.previous_stock - self.quantity
            
            self.inventory.current_stock = self.new_stock
            self.inventory.save()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.inventory.medical_item.name} ({self.quantity})"