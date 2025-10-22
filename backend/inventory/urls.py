from django.urls import path
from . import views

urlpatterns = [
    path('vendors/', views.VendorListView.as_view(), name='vendor-list'),
    path('vendors/<int:pk>/', views.VendorDetailView.as_view(), name='vendor-detail'),
    path('medical-items/', views.MedicalItemListView.as_view(), name='medical-item-list'),
    path('inventory/', views.InventoryListView.as_view(), name='inventory-list'),
    path('inventory/nearby/', views.search_nearby_inventory, name='nearby-inventory'),
]