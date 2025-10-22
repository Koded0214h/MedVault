from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    # Patient endpoints
    path('patients/', views.PatientListView.as_view(), name='patient-list'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
    path('me/patient-profile/', views.MyPatientProfileView.as_view(), name='my-patient-profile'),
    
    # Medical record endpoints
    path('medical-records/', views.MedicalRecordListView.as_view(), name='medical-record-list'),
    path('medical-records/<int:pk>/', views.MedicalRecordDetailView.as_view(), name='medical-record-detail'),
    path('patients/<int:patient_id>/medical-records/', views.PatientMedicalRecordsView.as_view(), name='patient-medical-records'),
    
    # Prescription endpoints
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescription-list'),
    path('prescriptions/<int:pk>/', views.PrescriptionDetailView.as_view(), name='prescription-detail'),
    path('patients/<int:patient_id>/active-prescriptions/', views.ActivePrescriptionsView.as_view(), name='active-prescriptions'),
    
    # Lab result endpoints
    path('lab-results/', views.LabResultListView.as_view(), name='lab-result-list'),
    path('lab-results/<int:pk>/', views.LabResultDetailView.as_view(), name='lab-result-detail'),
    
    # Complex operations
    path('complete-medical-record/', views.create_complete_medical_record, name='complete-medical-record'),
    path('patients/<int:patient_id>/medical-summary/', views.patient_medical_summary, name='patient-medical-summary'),
    path('search/medical-records/', views.search_medical_records, name='search-medical-records'),
]   