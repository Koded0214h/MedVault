from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Patient, MedicalRecord, Prescription, LabResult

User = get_user_model()

class PatientSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_phone = serializers.CharField(source='user.phone_number', read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('user',)

class PrescriptionSerializer(serializers.ModelSerializer):
    medication_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Prescription
        fields = '__all__'
    
    def get_medication_details(self, obj):
        # This could be enhanced to include medication info from inventory
        return {
            'name': obj.medication_name,
            'dosage': obj.dosage,
            'frequency': obj.frequency
        }

class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = '__all__'

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    lab_results = LabResultSerializer(many=True, read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = '__all__'

class MedicalRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'

class PatientDetailSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_phone = serializers.CharField(source='user.phone_number', read_only=True)
    medical_records = MedicalRecordSerializer(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'

# Serializer for creating prescriptions with lab results
class MedicalRecordWithDetailsSerializer(serializers.Serializer):
    record_data = MedicalRecordCreateSerializer()
    prescriptions = PrescriptionSerializer(many=True, required=False)
    lab_results = LabResultSerializer(many=True, required=False)