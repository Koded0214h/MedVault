from rest_framework import serializers
from .models import MCPConfig, DemandData, ContextData, ShortagePrediction, PredictionAlert
from inventory.models import MedicalItem

class MCPConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCPConfig
        fields = '__all__'

class DemandDataSerializer(serializers.ModelSerializer):
    medical_item_name = serializers.CharField(source='medical_item.name', read_only=True)
    medical_item_category = serializers.CharField(source='medical_item.category', read_only=True)
    
    class Meta:
        model = DemandData
        fields = '__all__'

class ContextDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContextData
        fields = '__all__'

class ShortagePredictionSerializer(serializers.ModelSerializer):
    medical_item_name = serializers.CharField(source='medical_item.name', read_only=True)
    medical_item_category = serializers.CharField(source='medical_item.category', read_only=True)
    days_until_shortage = serializers.SerializerMethodField()
    
    class Meta:
        model = ShortagePrediction
        fields = '__all__'
    
    def get_days_until_shortage(self, obj):
        from django.utils import timezone
        if obj.predicted_shortage_date:
            delta = obj.predicted_shortage_date - timezone.now()
            return max(0, delta.days)
        return None

class PredictionAlertSerializer(serializers.ModelSerializer):
    prediction_details = ShortagePredictionSerializer(source='prediction', read_only=True)
    
    class Meta:
        model = PredictionAlert
        fields = '__all__'

# Input serializers for prediction requests
class PredictionRequestSerializer(serializers.Serializer):
    medical_item_id = serializers.IntegerField(required=False)
    region = serializers.CharField(max_length=100, required=False)
    prediction_days = serializers.IntegerField(default=14, min_value=1, max_value=90)

class BulkDemandDataSerializer(serializers.Serializer):
    demand_data = DemandDataSerializer(many=True)

class BulkContextDataSerializer(serializers.Serializer):
    context_data = ContextDataSerializer(many=True)