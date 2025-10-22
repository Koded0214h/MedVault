import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum, Avg, Count, Q
from django.db import transaction
from .models import MCPConfig, DemandData, ContextData, ShortagePrediction, PredictionAlert
from inventory.models import MedicalItem, Inventory

logger = logging.getLogger(__name__)

class MCPPredictionEngine:
    def __init__(self, config_name="default"):
        try:
            self.config = MCPConfig.objects.get(name=config_name, is_active=True)
        except MCPConfig.DoesNotExist:
            # Create default config if none exists
            self.config = MCPConfig.objects.create(
                name=config_name,
                description="Default MCP Configuration"
            )
    
    def calculate_demand_trend(self, medical_item, region, days_back=30):
        """
        Calculate demand trend for a medical item in a region
        """
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days_back)
        
        demand_data = DemandData.objects.filter(
            medical_item=medical_item,
            region=region,
            period_start__gte=start_date,
            period_end__lte=end_date
        ).order_by('period_start')
        
        if not demand_data:
            return 0, 0  # No trend data
        
        # Calculate trend using linear regression (simplified)
        demands = [data.demand_count for data in demand_data]
        if len(demands) > 1:
            trend = (demands[-1] - demands[0]) / len(demands)
        else:
            trend = 0
        
        avg_demand = sum(demands) / len(demands)
        
        return avg_demand, trend
    
    def get_current_supply(self, medical_item, region):
        """
        Get current supply levels for a medical item in a region
        """
        total_supply = Inventory.objects.filter(
            medical_item=medical_item,
            vendor__city=region,  # Using city as region for simplicity
            current_stock__gt=0,
            is_available=True
        ).aggregate(total_stock=Sum('current_stock'))['total_stock'] or 0
        
        return total_supply
    
    def get_context_factors(self, region, days_ahead=14):
        """
        Get contextual factors affecting demand
        """
        end_date = timezone.now() + timedelta(days=days_ahead)
        
        context_factors = ContextData.objects.filter(
            region=region,
            effective_date__lte=end_date,
            expiry_date__gte=timezone.now()
        )
        
        impact_score = 1.0  # Base impact
        
        for context in context_factors:
            if context.data_type == 'disease_trend' and context.trend_direction == 'up':
                impact_score *= 1.3  # 30% increase in demand
            elif context.data_type == 'public_health_alert' and context.alert_level == 'high':
                impact_score *= 1.5  # 50% increase in demand
            elif context.data_type == 'weather' and context.rainfall > 50:  # Heavy rainfall
                impact_score *= 1.2  # 20% increase in demand
        
        return impact_score
    
    def predict_shortage(self, medical_item, region, prediction_days=14):
        """
        Predict shortage for a specific medical item in a region
        """
        try:
            # Get demand data
            avg_demand, demand_trend = self.calculate_demand_trend(medical_item, region)
            
            # Get current supply
            current_supply = self.get_current_supply(medical_item, region)
            
            # Get context impact
            context_impact = self.get_context_factors(region, prediction_days)
            
            # Calculate predicted demand
            predicted_demand = (avg_demand + demand_trend * prediction_days) * context_impact
            
            # Calculate days until shortage
            if current_supply <= 0:
                days_until_shortage = 0
            elif predicted_demand <= 0:
                days_until_shortage = float('inf')
            else:
                days_until_shortage = current_supply / (predicted_demand / prediction_days)
            
            # Calculate confidence score
            confidence_score = self.calculate_confidence(
                avg_demand, demand_trend, context_impact
            )
            
            # Determine severity level
            severity_level = self.determine_severity(days_until_shortage, confidence_score)
            
            return {
                'medical_item': medical_item,
                'region': region,
                'predicted_demand': predicted_demand,
                'current_supply': current_supply,
                'days_until_shortage': days_until_shortage,
                'confidence_score': confidence_score,
                'severity_level': severity_level,
                'predicted_shortage_date': timezone.now() + timedelta(days=min(days_until_shortage, 365)),
                'predicted_shortage_duration': max(1, int(predicted_demand - current_supply) // max(1, int(avg_demand))),
                'demand_increase_reason': self.get_demand_increase_reason(context_impact, demand_trend),
                'supply_constraint_reason': self.get_supply_constraint_reason(current_supply)
            }
            
        except Exception as e:
            logger.error(f"Error predicting shortage for {medical_item.name} in {region}: {str(e)}")
            return None
    
    def calculate_confidence(self, avg_demand, demand_trend, context_impact):
        """
        Calculate prediction confidence score (0.0 to 1.0)
        """
        confidence = 0.7  # Base confidence
        
        # Adjust based on data quality
        if avg_demand > 10:  # Good historical data
            confidence += 0.2
        
        if abs(demand_trend) < 5:  # Stable trend
            confidence += 0.1
        
        if 0.8 <= context_impact <= 1.2:  # Normal context
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def determine_severity(self, days_until_shortage, confidence_score):
        """
        Determine shortage severity level
        """
        if days_until_shortage <= 7 and confidence_score >= self.config.critical_alert_threshold:
            return 'critical'
        elif days_until_shortage <= 14 and confidence_score >= self.config.shortage_alert_threshold:
            return 'high'
        elif days_until_shortage <= 30:
            return 'medium'
        else:
            return 'low'
    
    def get_demand_increase_reason(self, context_impact, demand_trend):
        reasons = []
        
        if context_impact > 1.2:
            reasons.append("Increased demand due to contextual factors")
        if demand_trend > 5:
            reasons.append("Rising demand trend observed")
        
        return "; ".join(reasons) if reasons else "Normal demand patterns"
    
    def get_supply_constraint_reason(self, current_supply):
        if current_supply == 0:
            return "Current stock depleted"
        elif current_supply < 10:
            return "Very low current stock levels"
        else:
            return "Adequate current stock"
    
    def run_predictions(self, regions=None, medical_items=None, prediction_days=14):
        """
        Run shortage predictions for multiple regions and items
        """
        predictions = []
        
        # Get regions to analyze
        if not regions:
            regions = DemandData.objects.values_list('region', flat=True).distinct()
        
        # Get medical items to analyze
        if not medical_items:
            medical_items = MedicalItem.objects.filter(
                inventory__current_stock__gt=0
            ).distinct()
        
        for region in regions:
            for medical_item in medical_items:
                prediction = self.predict_shortage(medical_item, region, prediction_days)
                if prediction and prediction['confidence_score'] >= 0.5:  # Only store reasonable predictions
                    predictions.append(prediction)
        
        return predictions
    
    @transaction.atomic
    def save_predictions(self, predictions):
        """
        Save predictions to database and create alerts if needed
        """
        saved_predictions = []
        
        for prediction_data in predictions:
            # Create or update prediction
            prediction, created = ShortagePrediction.objects.update_or_create(
                medical_item=prediction_data['medical_item'],
                region=prediction_data['region'],
                predicted_shortage_date=prediction_data['predicted_shortage_date'],
                defaults={
                    'confidence_score': prediction_data['confidence_score'],
                    'severity_level': prediction_data['severity_level'],
                    'predicted_shortage_duration': prediction_data['predicted_shortage_duration'],
                    'demand_increase_reason': prediction_data['demand_increase_reason'],
                    'supply_constraint_reason': prediction_data['supply_constraint_reason'],
                    'is_active': True
                }
            )
            
            # Create alert if threshold met
            if prediction_data['confidence_score'] >= self.config.shortage_alert_threshold:
                self.create_prediction_alert(prediction)
            
            saved_predictions.append(prediction)
        
        return saved_predictions
    
    def create_prediction_alert(self, prediction):
        """
        Create alert for a prediction
        """
        alert_type = 'shortage_imminent' if prediction.severity_level in ['high', 'critical'] else 'shortage_predicted'
        
        message = self.generate_alert_message(prediction)
        recommended_actions = self.generate_recommended_actions(prediction)
        
        alert = PredictionAlert.objects.create(
            prediction=prediction,
            alert_type=alert_type,
            message=message,
            recommended_actions=recommended_actions,
            notify_vendors=True,
            notify_health_authorities=prediction.severity_level in ['high', 'critical'],
            notify_public=prediction.severity_level == 'critical'
        )
        
        return alert
    
    def generate_alert_message(self, prediction):
        """Generate alert message based on prediction"""
        return (
            f"Potential {prediction.medical_item.name} shortage predicted in {prediction.region}. "
            f"Severity: {prediction.severity_level}. "
            f"Confidence: {prediction.confidence_score:.1%}"
        )
    
    def generate_recommended_actions(self, prediction):
        """Generate recommended actions based on prediction"""
        actions = []
        
        if prediction.severity_level == 'critical':
            actions.extend([
                "Immediate restocking required",
                "Contact emergency suppliers",
                "Notify health authorities"
            ])
        elif prediction.severity_level == 'high':
            actions.extend([
                "Accelerate restocking process",
                "Identify alternative suppliers",
                "Monitor stock levels daily"
            ])
        else:
            actions.extend([
                "Plan for restocking",
                "Monitor demand patterns",
                "Check with regional suppliers"
            ])
        
        return "\n".join(actions)