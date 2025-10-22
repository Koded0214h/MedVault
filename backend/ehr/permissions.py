from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()

class IsPatientOrDoctor(permissions.BasePermission):
    """
    Permission check for patient accessing own data or doctor accessing patient data
    """
    def has_object_permission(self, request, view, obj):
        if request.user.user_type == 'doctor':
            return True
        elif request.user.user_type == 'patient':
            # For Patient model
            if hasattr(obj, 'user'):
                return obj.user == request.user
            # For MedicalRecord model
            elif hasattr(obj, 'patient'):
                return obj.patient.user == request.user
        return False

class IsPatientOwner(permissions.BasePermission):
    """
    Permission check for patient accessing own data only
    """
    def has_object_permission(self, request, view, obj):
        if request.user.user_type == 'patient':
            if hasattr(obj, 'user'):
                return obj.user == request.user
            elif hasattr(obj, 'patient'):
                return obj.patient.user == request.user
        return False

class IsHealthcareProfessional(permissions.BasePermission):
    """
    Permission for doctors, lab technicians, etc.
    """
    def has_permission(self, request, view):
        return request.user.user_type in ['doctor', 'lab_technician', 'pharmacist']

class CanCreateMedicalRecord(permissions.BasePermission):
    """
    Permission for creating medical records
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.user_type in ['doctor', 'lab_technician']
        return True