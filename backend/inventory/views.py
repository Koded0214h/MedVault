from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import Vendor, MedicalItem, Inventory
from .serializers import VendorSerializer, MedicalItemSerializer, InventorySerializer
from .utils import find_nearby_vendors, get_vendors_within_bounds

class VendorListView(generics.ListCreateAPIView):
    queryset = Vendor.objects.filter(is_active=True)
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

class MedicalItemListView(generics.ListCreateAPIView):
    queryset = MedicalItem.objects.all()
    serializer_class = MedicalItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class InventoryListView(generics.ListAPIView):
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Inventory.objects.filter(
            current_stock__gt=0,
            is_available=True
        ).select_related('medical_item', 'vendor')
        
        # Filter by item name
        item_name = self.request.query_params.get('item_name')
        if item_name:
            queryset = queryset.filter(
                Q(medical_item__name__icontains=item_name) |
                Q(medical_item__generic_name__icontains=item_name)
            )
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(medical_item__category=category)
        
        return queryset

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_nearby_inventory(request):
    """
    Search for inventory items near a location
    """
    lat = request.query_params.get('lat')
    lng = request.query_params.get('lng')
    item_name = request.query_params.get('item_name')
    radius = float(request.query_params.get('radius', 50))
    
    if not lat or not lng:
        return Response(
            {'error': 'Latitude and longitude parameters are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        latitude = float(lat)
        longitude = float(lng)
    except ValueError:
        return Response(
            {'error': 'Invalid latitude or longitude format'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Find nearby vendors with inventory
    results = find_nearby_vendors(latitude, longitude, radius, item_name)
    
    response_data = []
    for vendor, distance, inventory in results:
        response_data.append({
            'vendor': VendorSerializer(vendor, context={'request': request}).data,
            'inventory': InventorySerializer(inventory).data,
            'distance_km': round(distance, 2)
        })
    
    return Response(response_data)