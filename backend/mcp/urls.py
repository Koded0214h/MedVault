from django.urls import path
from . import views

urlpatterns = [
    # Configuration endpoints
    path('config/', views.MCPConfigListView.as_view(), name='mcp-config-list'),
    path('config/<int:pk>/', views.MCPConfigDetailView.as_view(), name='mcp-config-detail'),
    
    # Demand data endpoints
    path('demand-data/', views.DemandDataListView.as_view(), name='demand-data-list'),
    path('demand-data/<int:pk>/', views.DemandDataDetailView.as_view(), name='demand-data-detail'),
    
    # Context data endpoints
    path('context-data/', views.ContextDataListView.as_view(), name='context-data-list'),
    path('context-data/<int:pk>/', views.ContextDataDetailView.as_view(), name='context-data-detail'),
    
    # Prediction endpoints
    path('predictions/', views.ShortagePredictionListView.as_view(), name='prediction-list'),
    path('predictions/<int:pk>/', views.ShortagePredictionDetailView.as_view(), name='prediction-detail'),
    path('predictions/run/', views.run_predictions, name='run-predictions'),
    path('predictions/critical/', views.get_critical_shortages, name='critical-shortages'),
    
    # Alert endpoints
    path('alerts/', views.PredictionAlertListView.as_view(), name='alert-list'),
    path('alerts/<int:pk>/', views.PredictionAlertDetailView.as_view(), name='alert-detail'),
    
    # Bulk operations
    path('bulk/demand-data/', views.bulk_upload_demand_data, name='bulk-demand-data'),
    path('bulk/context-data/', views.bulk_upload_context_data, name='bulk-context-data'),
    
    # Statistics
    path('stats/', views.prediction_stats, name='prediction-stats'),
]