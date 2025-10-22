import math
from typing import List, Tuple, Optional
from .models import Vendor, Inventory

def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate distance between two points using Haversine formula
    Returns distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)

    a = (math.sin(delta_lat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def find_nearby_vendors(
    latitude: float, 
    longitude: float, 
    radius_km: float = 50,
    item_name: Optional[str] = None
) -> List[Tuple[Vendor, float, Inventory]]:
    """
    Find vendors within radius having specified item in stock
    Returns list of tuples: (vendor, distance_km, inventory)
    """
    nearby_vendors = []
    
    # Get all vendors with coordinates
    vendors = Vendor.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False,
        is_active=True,
        is_verified=True
    )
    
    for vendor in vendors:
        distance = calculate_distance(
            latitude, longitude,
            float(vendor.latitude), float(vendor.longitude)
        )
        
        if distance <= radius_km:
            # Check if vendor has the requested item
            inventory_query = vendor.inventory_items.filter(
                current_stock__gt=0,
                is_available=True
            )
            
            if item_name:
                inventory_query = inventory_query.filter(
                    medical_item__name__icontains=item_name
                )
            
            for inventory in inventory_query:
                nearby_vendors.append((vendor, distance, inventory))
    
    # Sort by distance
    nearby_vendors.sort(key=lambda x: x[1])
    
    return nearby_vendors

def get_vendors_within_bounds(
    north: float, south: float, east: float, west: float,
    item_name: Optional[str] = None
) -> List[Vendor]:
    """
    Get vendors within geographic bounds
    """
    vendors = Vendor.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False,
        latitude__gte=south,
        latitude__lte=north,
        longitude__gte=west,
        longitude__lte=east,
        is_active=True,
        is_verified=True
    )
    
    if item_name:
        vendors = vendors.filter(
            inventory_items__medical_item__name__icontains=item_name,
            inventory_items__current_stock__gt=0,
            inventory_items__is_available=True
        ).distinct()
    
    return vendors