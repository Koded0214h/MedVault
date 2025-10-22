from rest_framework import serializers
from .models import Vendor, MedicalItem, Inventory, StockTransaction

class MedicalItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalItem
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()
    
    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ('distance',)
    
    def get_distance(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'query_params'):
            lat = request.query_params.get('lat')
            lng = request.query_params.get('lng')
            if lat and lng and obj.has_coordinates:
                return obj.get_distance(float(lat), float(lng))
        return None

class InventorySerializer(serializers.ModelSerializer):
    medical_item = MedicalItemSerializer(read_only=True)
    vendor = VendorSerializer(read_only=True)
    is_low_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Inventory
        fields = '__all__'
    
    def get_is_low_stock(self, obj):
        return obj.current_stock <= obj.minimum_stock

class StockTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransaction
        fields = '__all__'