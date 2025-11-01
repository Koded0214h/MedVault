import logging
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import MCPConfig, DemandData, ContextData, ShortagePrediction, PredictionAlert
from .serializers import (
    MCPConfigSerializer, DemandDataSerializer, ContextDataSerializer,
    ShortagePredictionSerializer, PredictionAlertSerializer,
    PredictionRequestSerializer, BulkDemandDataSerializer, BulkContextDataSerializer
)
from .prediction_engine import MCPPredictionEngine

logger = logging.getLogger(__name__)

# MCP Configuration Views
class MCPConfigListView(generics.ListCreateAPIView):
    queryset = MCPConfig.objects.all()
    serializer_class = MCPConfigSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]  # Allow authenticated users to create configs
        return [permissions.IsAuthenticated()]

class MCPConfigDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MCPConfig.objects.all()
    serializer_class = MCPConfigSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

# Demand Data Views
class DemandDataListView(generics.ListCreateAPIView):
    serializer_class = DemandDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['medical_item', 'region', 'season', 'disease_outbreak']
    search_fields = ['medical_item__name', 'region']
    ordering_fields = ['period_start', 'demand_count', 'collected_at']
    
    def get_queryset(self):
        return DemandData.objects.select_related('medical_item')

class DemandDataDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DemandData.objects.all()
    serializer_class = DemandDataSerializer
    permission_classes = [permissions.IsAuthenticated]

# Context Data Views
class ContextDataListView(generics.ListCreateAPIView):
    serializer_class = ContextDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['data_type', 'region', 'alert_level', 'trend_direction']
    search_fields = ['region', 'disease_name', 'alert_message']
    ordering_fields = ['effective_date', 'confidence_score', 'created_at']
    
    def get_queryset(self):
        return ContextData.objects.all()

class ContextDataDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContextData.objects.all()
    serializer_class = ContextDataSerializer
    permission_classes = [permissions.IsAuthenticated]

# Shortage Prediction Views
class ShortagePredictionListView(generics.ListAPIView):
    serializer_class = ShortagePredictionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['medical_item', 'region', 'severity_level', 'is_active']
    search_fields = ['medical_item__name', 'region']
    ordering_fields = ['predicted_shortage_date', 'confidence_score', 'created_at']
    
    def get_queryset(self):
        # Only show active predictions by default
        queryset = ShortagePrediction.objects.filter(is_active=True).select_related('medical_item')
        
        # Allow filtering by active status
        show_inactive = self.request.query_params.get('show_inactive', 'false').lower() == 'true'
        if show_inactive:
            queryset = ShortagePrediction.objects.all().select_related('medical_item')
        
        return queryset

class ShortagePredictionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShortagePrediction.objects.all()
    serializer_class = ShortagePredictionSerializer
    permission_classes = [permissions.IsAuthenticated]

# Prediction Alert Views
class PredictionAlertListView(generics.ListAPIView):
    serializer_class = PredictionAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['alert_type', 'is_sent', 'notify_vendors', 'notify_health_authorities']
    ordering_fields = ['sent_at', 'alert_type']
    
    def get_queryset(self):
        return PredictionAlert.objects.filter(is_sent=True).select_related('prediction__medical_item')

class PredictionAlertDetailView(generics.RetrieveUpdateAPIView):
    queryset = PredictionAlert.objects.all()
    serializer_class = PredictionAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

# Prediction Operations
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def run_predictions(request):
    """
    Run shortage predictions based on request parameters
    """
    serializer = PredictionRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        engine = MCPPredictionEngine()
        
        predictions = engine.run_predictions(
            regions=serializer.validated_data.get('region'),
            medical_items=serializer.validated_data.get('medical_item_id'),
            prediction_days=serializer.validated_data.get('prediction_days', 14)
        )
        
        saved_predictions = engine.save_predictions(predictions)
        
        result_serializer = ShortagePredictionSerializer(saved_predictions, many=True)
        
        return Response({
            'message': f'Generated {len(saved_predictions)} predictions',
            'predictions': result_serializer.data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_critical_shortages(request):
    """
    Get critical and high severity shortages
    """
    critical_shortages = ShortagePrediction.objects.filter(
        severity_level__in=['critical', 'high'],
        is_active=True,
        predicted_shortage_date__gte=timezone.now()
    ).select_related('medical_item').order_by('predicted_shortage_date')
    
    serializer = ShortagePredictionSerializer(critical_shortages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bulk_upload_demand_data(request):
    """
    Bulk upload demand data
    """
    serializer = BulkDemandDataSerializer(data=request.data)
    
    if serializer.is_valid():
        demand_data_list = serializer.validated_data['demand_data']
        created_count = 0
        errors = []
        
        for demand_data in demand_data_list:
            try:
                serializer_instance = DemandDataSerializer(data=demand_data)
                if serializer_instance.is_valid():
                    serializer_instance.save()
                    created_count += 1
                else:
                    errors.append(serializer_instance.errors)
            except Exception as e:
                errors.append(str(e))
        
        return Response({
            'message': f'Successfully created {created_count} demand records',
            'errors': errors,
            'total_processed': len(demand_data_list)
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bulk_upload_context_data(request):
    """
    Bulk upload context data
    """
    serializer = BulkContextDataSerializer(data=request.data)
    
    if serializer.is_valid():
        context_data_list = serializer.validated_data['context_data']
        created_count = 0
        errors = []
        
        for context_data in context_data_list:
            try:
                serializer_instance = ContextDataSerializer(data=context_data)
                if serializer_instance.is_valid():
                    serializer_instance.save()
                    created_count += 1
                else:
                    errors.append(serializer_instance.errors)
            except Exception as e:
                errors.append(str(e))
        
        return Response({
            'message': f'Successfully created {created_count} context records',
            'errors': errors,
            'total_processed': len(context_data_list)
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def prediction_stats(request):
    """
    Get prediction statistics
    """
    total_predictions = ShortagePrediction.objects.count()
    active_predictions = ShortagePrediction.objects.filter(is_active=True).count()
    critical_predictions = ShortagePrediction.objects.filter(severity_level='critical', is_active=True).count()
    high_predictions = ShortagePrediction.objects.filter(severity_level='high', is_active=True).count()
    
    # Recent alerts
    recent_alerts = PredictionAlert.objects.filter(
        sent_at__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    return Response({
        'total_predictions': total_predictions,
        'active_predictions': active_predictions,
        'critical_predictions': critical_predictions,
        'high_predictions': high_predictions,
        'recent_alerts': recent_alerts,
        'prediction_accuracy': '85%'  # This would come from historical data analysis
    })