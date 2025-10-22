from django.contrib import admin
from .models import Patient, MedicalRecord, Prescription, LabResult

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_type', 'height', 'weight')
    list_filter = ('blood_type',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email')

class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 1

class LabResultInline(admin.TabularInline):
    model = LabResult
    extra = 1

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'record_type', 'title', 'date_occurred', 'doctor')
    list_filter = ('record_type', 'date_occurred')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'title', 'diagnosis')
    inlines = [PrescriptionInline, LabResultInline]

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'medication_name', 'dosage', 'frequency', 'is_active')
    list_filter = ('is_active', 'prescribed_date')
    search_fields = ('medication_name', 'medical_record__patient__user__first_name')

@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'test_name', 'result_value', 'date_tested')
    list_filter = ('test_name', 'date_tested')
    search_fields = ('test_name', 'medical_record__patient__user__first_name')