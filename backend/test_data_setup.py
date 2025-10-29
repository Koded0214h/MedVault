#!/usr/bin/env python
"""
Test data setup script for MCP Core verification
"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from inventory.models import Vendor, MedicalItem, Inventory
from ehr.models import Patient, MedicalRecord, Prescription
from mcp.models import MCPConfig, DemandData, ContextData
from users.models import User

User = get_user_model()

def create_test_users():
    """Create test users"""
    print("Creating test users...")

    # Create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@medvault.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
            'user_type': 'admin'
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()

    # Create doctor
    doctor_user, created = User.objects.get_or_create(
        username='doctor1',
        defaults={
            'email': 'doctor@medvault.com',
            'first_name': 'Dr.',
            'last_name': 'Smith',
            'user_type': 'doctor'
        }
    )
    if created:
        doctor_user.set_password('doctor123')
        doctor_user.save()

    # Create patient
    patient_user, created = User.objects.get_or_create(
        username='patient1',
        defaults={
            'email': 'patient@medvault.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'user_type': 'patient'
        }
    )
    if created:
        patient_user.set_password('patient123')
        patient_user.save()

    # Create vendor user
    vendor_user, created = User.objects.get_or_create(
        username='vendor1',
        defaults={
            'email': 'vendor@medvault.com',
            'first_name': 'Vendor',
            'last_name': 'One',
            'user_type': 'vendor'
        }
    )
    if created:
        vendor_user.set_password('vendor123')
        vendor_user.save()

    return admin_user, doctor_user, patient_user, vendor_user

def create_test_vendors(vendor_user):
    """Create test vendors"""
    print("Creating test vendors...")

    vendor, created = Vendor.objects.get_or_create(
        user=vendor_user,
        defaults={
            'vendor_type': 'pharmacy',
            'business_name': 'Test Pharmacy Lagos',
            'business_license': 'PHARM001',
            'address': '123 Pharmacy Street, Lagos',
            'city': 'Lagos',
            'country': 'Nigeria',
            'latitude': Decimal('6.5244'),
            'longitude': Decimal('3.3792'),
            'contact_person': 'Vendor Manager',
            'contact_email': 'contact@testpharmacy.com',
            'contact_phone': '+234123456789',
            'is_verified': True,
            'is_active': True
        }
    )

    return vendor

def create_test_medical_items():
    """Create test medical items"""
    print("Creating test medical items...")

    items_data = [
        {
            'name': 'Insulin',
            'category': 'medication',
            'description': 'Diabetes medication',
            'manufacturer': 'Test Pharma',
            'unit_of_measure': 'vials',
            'generic_name': 'Insulin',
            'strength': '100IU/ml'
        },
        {
            'name': 'Paracetamol',
            'category': 'medication',
            'description': 'Pain relief medication',
            'manufacturer': 'Generic Pharma',
            'unit_of_measure': 'tablets',
            'generic_name': 'Acetaminophen',
            'strength': '500mg'
        },
        {
            'name': 'Tetanus Vaccine',
            'category': 'vaccine',
            'description': 'Tetanus vaccination',
            'manufacturer': 'Vaccine Corp',
            'unit_of_measure': 'doses',
            'generic_name': 'Tetanus Toxoid'
        },
        {
            'name': 'Blood Type O+',
            'category': 'blood_type',
            'description': 'O Positive blood type',
            'unit_of_measure': 'units',
            'blood_group': 'O',
            'rh_factor': '+'
        }
    ]

    items = []
    for item_data in items_data:
        item, created = MedicalItem.objects.get_or_create(
            name=item_data['name'],
            category=item_data['category'],
            defaults=item_data
        )
        items.append(item)

    return items

def create_test_inventory(vendor, medical_items):
    """Create test inventory"""
    print("Creating test inventory...")

    inventory_items = []
    for item in medical_items:
        inventory, created = Inventory.objects.get_or_create(
            vendor=vendor,
            medical_item=item,
            defaults={
                'current_stock': 50 if item.name == 'Insulin' else 100,
                'minimum_stock': 10,
                'maximum_stock': 500,
                'unit_price': Decimal('15.00') if item.category == 'medication' else Decimal('25.00'),
                'batch_number': f'BATCH_{item.name.upper()[:3]}_001',
                'expiry_date': timezone.now().date() + timedelta(days=365),
                'is_available': True
            }
        )
        inventory_items.append(inventory)

    return inventory_items

def create_test_ehr_data(doctor_user, patient_user):
    """Create test EHR data"""
    print("Creating test EHR data...")

    # Create patient profile
    patient, created = Patient.objects.get_or_create(
        user=patient_user,
        defaults={
            'blood_type': 'O+',
            'height': Decimal('175.00'),
            'weight': Decimal('70.00'),
            'allergies': 'None',
            'chronic_conditions': 'Diabetes',
            'current_medications': 'Insulin'
        }
    )

    # Create medical record
    medical_record, created = MedicalRecord.objects.get_or_create(
        patient=patient,
        record_type='consultation',
        title='Diabetes Follow-up',
        description='Regular check-up for diabetes management',
        date_occurred=timezone.now() - timedelta(days=7),
        doctor=doctor_user,
        defaults={
            'diagnosis': 'Type 2 Diabetes',
            'treatment': 'Continue insulin therapy',
            'notes': 'Patient stable, blood sugar controlled'
        }
    )

    # Create prescription
    prescription, created = Prescription.objects.get_or_create(
        medical_record=medical_record,
        medication_name='Insulin',
        dosage='10 units twice daily',
        frequency='BID',
        duration='30 days',
        defaults={
            'instructions': 'Inject subcutaneously before meals',
            'is_active': True
        }
    )

    return patient, medical_record, prescription

def create_test_mcp_config():
    """Create MCP configuration"""
    print("Creating MCP configuration...")

    config, created = MCPConfig.objects.get_or_create(
        name='default',
        defaults={
            'description': 'Default MCP Configuration for testing',
            'shortage_alert_threshold': 0.8,
            'critical_alert_threshold': 0.9,
            'demand_data_weight': 0.4,
            'supply_data_weight': 0.4,
            'context_data_weight': 0.2,
            'prediction_horizon_days': 14,
            'retraining_frequency_hours': 24,
            'is_active': True
        }
    )

    return config

def create_test_demand_data(medical_items):
    """Create test demand data"""
    print("Creating test demand data...")

    demand_entries = []
    base_date = timezone.now() - timedelta(days=60)

    for i in range(60):  # 60 days of data
        date = base_date + timedelta(days=i)

        for item in medical_items:
            # Create demand data with some variation
            base_demand = 5 if item.name == 'Insulin' else 10
            demand_variation = (i % 7) + 1  # Weekly pattern
            demand_count = base_demand + demand_variation

            demand_data, created = DemandData.objects.get_or_create(
                medical_item=item,
                region='Lagos',
                period_start=date.replace(hour=0, minute=0, second=0),
                period_end=date.replace(hour=23, minute=59, second=59),
                defaults={
                    'demand_count': demand_count,
                    'season': 'rainy' if i % 30 < 15 else 'dry',
                    'disease_outbreak': i > 45 and item.name == 'Tetanus Vaccine',  # Recent outbreak
                    'outbreak_disease': 'Tetanus' if i > 45 and item.name == 'Tetanus Vaccine' else None
                }
            )
            demand_entries.append(demand_data)

    return demand_entries

def create_test_context_data():
    """Create test context data"""
    print("Creating test context data...")

    context_entries = []

    # Weather data
    weather_data, created = ContextData.objects.get_or_create(
        region='Lagos',
        data_type='weather',
        effective_date=timezone.now(),
        expiry_date=timezone.now() + timedelta(days=7),
        defaults={
            'temperature': 28.5,
            'humidity': 75.0,
            'rainfall': 15.0,  # Heavy rainfall
            'confidence_score': 0.9,
            'source': 'Weather API'
        }
    )
    context_entries.append(weather_data)

    # Disease trend
    disease_data, created = ContextData.objects.get_or_create(
        region='Lagos',
        data_type='disease_trend',
        effective_date=timezone.now(),
        expiry_date=timezone.now() + timedelta(days=30),
        defaults={
            'disease_name': 'Malaria',
            'case_count': 150,
            'trend_direction': 'up',
            'confidence_score': 0.85,
            'source': 'Health Ministry'
        }
    )
    context_entries.append(disease_data)

    # Public health alert
    alert_data, created = ContextData.objects.get_or_create(
        region='Lagos',
        data_type='public_health_alert',
        effective_date=timezone.now(),
        expiry_date=timezone.now() + timedelta(days=14),
        defaults={
            'alert_level': 'high',
            'alert_message': 'Cholera outbreak reported in Lagos district',
            'confidence_score': 0.95,
            'source': 'Public Health Authority'
        }
    )
    context_entries.append(alert_data)

    return context_entries

def main():
    """Main setup function"""
    print("Starting test data setup for MCP Core verification...")

    try:
        # Create users
        admin_user, doctor_user, patient_user, vendor_user = create_test_users()

        # Create vendors and inventory
        vendor = create_test_vendors(vendor_user)
        medical_items = create_test_medical_items()
        inventory_items = create_test_inventory(vendor, medical_items)

        # Create EHR data
        patient, medical_record, prescription = create_test_ehr_data(doctor_user, patient_user)

        # Create MCP data
        mcp_config = create_test_mcp_config()
        demand_data = create_test_demand_data(medical_items)
        context_data = create_test_context_data()

        print("\nTest data setup completed successfully!")
        print(f"Created {User.objects.count()} users")
        print(f"Created {Vendor.objects.count()} vendors")
        print(f"Created {MedicalItem.objects.count()} medical items")
        print(f"Created {Inventory.objects.count()} inventory items")
        print(f"Created {Patient.objects.count()} patients")
        print(f"Created {MedicalRecord.objects.count()} medical records")
        print(f"Created {Prescription.objects.count()} prescriptions")
        print(f"Created {MCPConfig.objects.count()} MCP configs")
        print(f"Created {DemandData.objects.count()} demand data entries")
        print(f"Created {ContextData.objects.count()} context data entries")

        print("\nReady for MCP Core testing!")

    except Exception as e:
        print(f"Error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
