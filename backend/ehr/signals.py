from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Patient, Prescription
from mcp.models import DemandData

User = get_user_model()

@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    """
    Automatically create a patient profile when a user with patient type is created
    """
    if created and instance.user_type == 'patient':
        Patient.objects.get_or_create(user=instance)

@receiver(post_save, sender=Prescription)
def create_demand_data_from_prescription(sender, instance, created, **kwargs):
    """
    Automatically create demand data when a prescription is created
    """
    if created:
        try:
            # Extract medical item name from prescription
            medication_name = instance.medication_name

            # Try to find matching medical item (simplified matching)
            from inventory.models import MedicalItem
            medical_item = None

            # Exact match first
            try:
                medical_item = MedicalItem.objects.get(name__iexact=medication_name)
            except MedicalItem.DoesNotExist:
                # Fuzzy matching for common medications
                if 'insulin' in medication_name.lower():
                    medical_item = MedicalItem.objects.filter(name__icontains='insulin').first()
                elif 'paracetamol' in medication_name.lower() or 'acetaminophen' in medication_name.lower():
                    medical_item = MedicalItem.objects.filter(name__icontains='paracetamol').first()

            if medical_item:
                # Get patient location (simplified - using default region)
                region = 'Lagos'  # Default region, could be enhanced with actual location data

                # Calculate period (current day)
                today = timezone.now().date()
                period_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
                period_end = period_start + timedelta(days=1)

                # Create or update demand data
                demand_data, created = DemandData.objects.get_or_create(
                    medical_item=medical_item,
                    region=region,
                    period_start=period_start,
                    period_end=period_end,
                    defaults={
                        'demand_count': 1,  # Start with 1, will be aggregated
                        'season': 'unknown',  # Could be enhanced with actual season data
                        'disease_outbreak': False
                    }
                )

                if not created:
                    # Increment demand count if entry already exists
                    demand_data.demand_count += 1
                    demand_data.save()

        except Exception as e:
            # Log error but don't break prescription creation
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error creating demand data from prescription: {e}")

# Connect the signal
def ready(self):
    import ehr.signals
