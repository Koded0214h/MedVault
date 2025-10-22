from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Patient, MedicalRecord, Prescription, LabResult
from .serializers import (
    PatientSerializer, PatientDetailSerializer, MedicalRecordSerializer,
    MedicalRecordCreateSerializer, PrescriptionSerializer, LabResultSerializer,
    MedicalRecordWithDetailsSerializer
)
from .permissions import IsPatientOrDoctor, IsPatientOwner, IsHealthcareProfessional, CanCreateMedicalRecord

User = get_user_model()

# Patient Views
class PatientListView(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsHealthcareProfessional]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['user__first_name', 'user__last_name', 'created_at']
    
    def get_queryset(self):
        if self.request.user.user_type == 'doctor':
            return Patient.objects.all()
        return Patient.objects.none()

class PatientDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = PatientDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatientOrDoctor]
    
    def get_queryset(self):
        if self.request.user.user_type == 'doctor':
            return Patient.objects.all()
        elif self.request.user.user_type == 'patient':
            return Patient.objects.filter(user=self.request.user)
        return Patient.objects.none()

class MyPatientProfileView(generics.RetrieveUpdateAPIView):
    """
    For patients to view and update their own profile
    """
    serializer_class = PatientDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        # Get or create patient profile for the current user
        patient, created = Patient.objects.get_or_create(user=self.request.user)
        return patient

# Medical Record Views
class MedicalRecordListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, CanCreateMedicalRecord]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['record_type', 'patient', 'doctor']
    search_fields = ['title', 'diagnosis', 'treatment']
    ordering_fields = ['date_occurred', 'date_recorded']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MedicalRecordCreateSerializer
        return MedicalRecordSerializer

    def get_queryset(self):
        user = self.request.user
        
        if user.user_type == 'patient':
            # Patients can only see their own records
            return MedicalRecord.objects.filter(patient__user=user)
        elif user.user_type == 'doctor':
            # Doctors can see records they created or all records if specified
            patient_id = self.request.query_params.get('patient_id')
            if patient_id:
                return MedicalRecord.objects.filter(patient_id=patient_id)
            return MedicalRecord.objects.filter(doctor=user)
        else:
            # Other healthcare professionals have limited access
            return MedicalRecord.objects.filter(patient__user=user)

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

class MedicalRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatientOrDoctor]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patient':
            return MedicalRecord.objects.filter(patient__user=user)
        return MedicalRecord.objects.all()

class PatientMedicalRecordsView(generics.ListAPIView):
    """
    Get medical records for a specific patient
    """
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsHealthcareProfessional]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['record_type']
    ordering_fields = ['date_occurred', 'date_recorded']
    
    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return MedicalRecord.objects.filter(patient_id=patient_id)

# Prescription Views
class PrescriptionListView(generics.ListCreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsHealthcareProfessional]
    
    def get_queryset(self):
        medical_record_id = self.request.query_params.get('medical_record_id')
        if medical_record_id:
            return Prescription.objects.filter(medical_record_id=medical_record_id)
        return Prescription.objects.all()

class PrescriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsHealthcareProfessional]
    queryset = Prescription.objects.all()

class ActivePrescriptionsView(generics.ListAPIView):
    """
    Get active prescriptions for a patient
    """
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatientOrDoctor]
    
    def get_queryset(self):
        patient_id = self.kwargs.get('patient_id')
        user = self.request.user
        
        if user.user_type == 'patient':
            return Prescription.objects.filter(
                medical_record__patient__user=user,
                is_active=True
            )
        elif patient_id:
            return Prescription.objects.filter(
                medical_record__patient_id=patient_id,
                is_active=True
            )
        return Prescription.objects.none()

# Lab Result Views
class LabResultListView(generics.ListCreateAPIView):
    serializer_class = LabResultSerializer
    permission_classes = [permissions.IsAuthenticated, IsHealthcareProfessional]
    
    def get_queryset(self):
        medical_record_id = self.request.query_params.get('medical_record_id')
        if medical_record_id:
            return LabResult.objects.filter(medical_record_id=medical_record_id)
        return LabResult.objects.all()

class LabResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LabResultSerializer
    permission_classes = [permissions.IsAuthenticated, IsHealthcareProfessional]
    queryset = LabResult.objects.all()

# Complex Operations
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsHealthcareProfessional])
def create_complete_medical_record(request):
    """
    Create a medical record with prescriptions and lab results in one request
    """
    serializer = MedicalRecordWithDetailsSerializer(data=request.data)
    
    if serializer.is_valid():
        record_data = serializer.validated_data['record_data']
        prescriptions_data = serializer.validated_data.get('prescriptions', [])
        lab_results_data = serializer.validated_data.get('lab_results', [])
        
        # Create medical record
        medical_record = MedicalRecord.objects.create(**record_data, doctor=request.user)
        
        # Create prescriptions
        for prescription_data in prescriptions_data:
            Prescription.objects.create(medical_record=medical_record, **prescription_data)
        
        # Create lab results
        for lab_result_data in lab_results_data:
            LabResult.objects.create(medical_record=medical_record, **lab_result_data)
        
        return Response(
            MedicalRecordSerializer(medical_record).data,
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def patient_medical_summary(request, patient_id):
    """
    Get a comprehensive medical summary for a patient
    """
    try:
        patient = Patient.objects.get(id=patient_id)
        
        # Check permissions
        if request.user.user_type == 'patient' and patient.user != request.user:
            return Response(
                {'error': 'You can only access your own medical summary'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get recent records
        recent_records = MedicalRecord.objects.filter(patient=patient).order_by('-date_occurred')[:10]
        active_prescriptions = Prescription.objects.filter(
            medical_record__patient=patient, 
            is_active=True
        )
        recent_lab_results = LabResult.objects.filter(
            medical_record__patient=patient
        ).order_by('-date_tested')[:5]
        
        summary = {
            'patient': PatientSerializer(patient).data,
            'recent_records': MedicalRecordSerializer(recent_records, many=True).data,
            'active_prescriptions': PrescriptionSerializer(active_prescriptions, many=True).data,
            'recent_lab_results': LabResultSerializer(recent_lab_results, many=True).data,
            'stats': {
                'total_records': MedicalRecord.objects.filter(patient=patient).count(),
                'active_prescriptions_count': active_prescriptions.count(),
                'recent_lab_results_count': recent_lab_results.count(),
            }
        }
        
        return Response(summary)
    
    except Patient.DoesNotExist:
        return Response(
            {'error': 'Patient not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

# Search endpoints
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_medical_records(request):
    """
    Search medical records across various fields
    """
    query = request.query_params.get('q', '')
    user = request.user
    
    if user.user_type == 'patient':
        # For patients: only their records + search across fields
        records = MedicalRecord.objects.filter(
            Q(patient__user=user) & (
                Q(title__icontains=query) |
                Q(diagnosis__icontains=query) |
                Q(treatment__icontains=query) |
                Q(notes__icontains=query)
            )
        )
    else:
        # For healthcare professionals: all records + broader search
        records = MedicalRecord.objects.filter(
            Q(title__icontains=query) |
            Q(diagnosis__icontains=query) |
            Q(treatment__icontains=query) |
            Q(notes__icontains=query) |
            Q(patient__user__first_name__icontains=query) |
            Q(patient__user__last_name__icontains=query)
        )
    
    serializer = MedicalRecordSerializer(records, many=True)
    return Response(serializer.data)