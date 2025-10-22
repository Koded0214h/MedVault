from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Patient

User = get_user_model()

@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    """
    Automatically create a patient profile when a user with patient type is created
    """
    if created and instance.user_type == 'patient':
        Patient.objects.get_or_create(user=instance)

# Connect the signal
def ready(self):
    import ehr.signals