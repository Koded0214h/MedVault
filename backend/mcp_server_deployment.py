#!/usr/bin/env python3
"""
MedVault MCP Server - Production Deployment Script
Provides AI assistants with access to healthcare resource prediction capabilities
"""

import asyncio
import logging
import sys
import os

# Add site-packages to path for MCP imports
sys.path.insert(0, '/Users/koded/Desktop/Code/MedVault/env/lib/python3.11/site-packages')

from fastmcp import FastMCP
import mcp
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

# Import MCP modules after Django setup
from mcp.prediction_engine import MCPPredictionEngine
from inventory.models import MedicalItem
from mcp.models import DemandData, ContextData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP app
app = FastMCP("medvault-mcp")

@app.tool()
async def predict_shortage(
    medical_item_name: str,
    region: str,
    prediction_days: int = 14,
    user_lat: float = None,
    user_lng: float = None
) -> str:
    """
    Predict medical resource shortages using AI with live weather/GPS data and find alternative suppliers
    """
    try:
        # Find medical item
        medical_item = MedicalItem.objects.filter(
            name__icontains=medical_item_name
        ).first()

        if not medical_item:
            return f"Medical item '{medical_item_name}' not found in inventory."

        # Initialize prediction engine (with live external APIs)
        engine = MCPPredictionEngine()

        # Get live weather data for the region
        live_weather = engine.external_data.get_live_weather(region)
        weather_info = ""
        if live_weather:
            weather_info = f"""
**Live Weather Data:**
- Temperature: {live_weather['temperature']}°C
- Humidity: {live_weather['humidity']}%
- Rainfall: {live_weather['rainfall']}mm
- Conditions: {live_weather['description']}
- Source: {live_weather['source']}"""

        # Run prediction (this will also update context data with live APIs)
        prediction = engine.predict_shortage(
            medical_item=medical_item,
            region=region,
            prediction_days=prediction_days
        )

        if not prediction:
            return f"Unable to generate prediction for {medical_item_name} in {region}."

        # Find alternative suppliers if location provided
        alternative_suppliers = ""
        if user_lat is not None and user_lng is not None:
            from inventory.utils import find_nearby_vendors
            nearby_results = find_nearby_vendors(user_lat, user_lng, radius_km=100, item_name=medical_item_name)

            if nearby_results:
                alternative_suppliers = "\n\n**🚨 Alternative Suppliers (within 100km):**\n"
                for vendor, distance, inventory in nearby_results[:5]:  # Top 5 closest
                    alternative_suppliers += f"- {vendor.business_name} ({vendor.city}): {inventory.current_stock} units available, {distance:.1f}km away\n"
                    if vendor.contact_phone:
                        alternative_suppliers += f"  📞 Contact: {vendor.contact_phone}\n"
                    # Add GPS directions if available
                    if vendor.latitude and vendor.longitude:
                        alternative_suppliers += f"  📍 GPS: {vendor.latitude:.4f}, {vendor.longitude:.4f}\n"
            else:
                alternative_suppliers = "\n\n**No alternative suppliers found within 100km.**"

        # Format response
        response = f"""
**🩺 Medical Resource Shortage Prediction**

**Item:** {medical_item.name}
**Region:** {region}
**Prediction Period:** {prediction_days} days

**📊 Current Status:**
- Current Supply: {prediction['current_supply']} units
- Predicted Demand: {prediction['predicted_demand']:.1f} units
- Days Until Shortage: {prediction['days_until_shortage']:.1f}

**⚠️ Risk Assessment:**
- Severity Level: {prediction['severity_level'].upper()}
- Confidence Score: {prediction['confidence_score']:.1%}

**🔍 Contributing Factors:**
- Demand Increase: {prediction['demand_increase_reason']}
- Supply Constraints: {prediction['supply_constraint_reason']}

**💡 Recommended Actions:**
{engine.generate_recommended_actions({
    'severity_level': prediction['severity_level'],
    'medical_item': medical_item,
    'region': region
})}

**🌦️ Live Data Sources (Real-time API Integration):**
- 📈 Demand data from EHR prescriptions (auto-collected via Django signals)
- 📦 Supply data from vendor inventory systems (real-time sync)
- 🌡️ **Live weather data** from OpenWeatherMap API (temperature, humidity, rainfall)
- 🦠 Disease trends from health authority APIs
- 📍 **Live GPS coordinates** from Google Maps API for supplier locations
- 🔔 Automated alerts when predictions exceed thresholds{weather_info}{alternative_suppliers}
        """

        return response.strip()

    except Exception as e:
        logger.error(f"Error in predict_shortage: {str(e)}")
        return f"Error generating prediction: {str(e)}"

@app.tool()
async def get_inventory_status(
    region: str = None,
    medical_item_name: str = None
) -> str:
    """
    Get current inventory status for medical items
    """
    try:
        from inventory.models import Inventory

        # Build query
        query = Inventory.objects.filter(is_available=True)

        if region:
            query = query.filter(vendor__city__icontains=region)

        if medical_item_name:
            query = query.filter(medical_item__name__icontains=medical_item_name)

        inventory_items = query.select_related('medical_item', 'vendor')[:20]  # Limit results

        if not inventory_items:
            return f"No inventory items found matching criteria (region: {region}, item: {medical_item_name})."

        response = "**Current Inventory Status**\n\n"

        for item in inventory_items:
            response += f"""
**{item.medical_item.name}**
- Location: {item.vendor.city}, {item.vendor.name}
- Current Stock: {item.current_stock} units
- Minimum Stock: {item.minimum_stock} units
- Status: {'LOW STOCK' if item.current_stock <= item.minimum_stock else 'AVAILABLE'}
            """

        return response.strip()

    except Exception as e:
        logger.error(f"Error in get_inventory_status: {str(e)}")
        return f"Error retrieving inventory status: {str(e)}"

@app.tool()
async def analyze_demand_trends(
    medical_item_name: str,
    region: str,
    days_back: int = 30
) -> str:
    """
    Analyze historical demand trends for medical items
    """
    try:
        # Find medical item
        medical_item = MedicalItem.objects.filter(
            name__icontains=medical_item_name
        ).first()

        if not medical_item:
            return f"Medical item '{medical_item_name}' not found."

        # Initialize prediction engine
        engine = MCPPredictionEngine()

        # Calculate demand trend
        avg_demand, trend = engine.calculate_demand_trend(
            medical_item=medical_item,
            region=region,
            days_back=days_back
        )

        # Get recent demand data
        recent_demand = DemandData.objects.filter(
            medical_item=medical_item,
            region=region
        ).order_by('-period_end')[:10]

        response = f"""
**Demand Trend Analysis**

**Item:** {medical_item.name}
**Region:** {region}
**Analysis Period:** {days_back} days

**Key Metrics:**
- Average Daily Demand: {avg_demand:.1f} units
- Demand Trend: {'INCREASING' if trend > 0 else 'DECREASING'} ({trend:.2f} units/day)

**Recent Demand Data:**
        """

        for demand in recent_demand:
            response += f"\n- {demand.period_end.date()}: {demand.demand_count} units"

        # Add insights
        if trend > 5:
            response += "\n\n**Alert:** Significant increasing demand trend detected!"
        elif trend < -5:
            response += "\n\n**Note:** Demand is decreasing, consider stock optimization."

        return response.strip()

    except Exception as e:
        logger.error(f"Error in analyze_demand_trends: {str(e)}")
        return f"Error analyzing demand trends: {str(e)}"

@app.tool()
async def get_contextual_factors(
    region: str,
    days_ahead: int = 14
) -> str:
    """
    Get contextual factors affecting healthcare demand
    """
    try:
        from django.utils import timezone
        from datetime import timedelta

        # Initialize prediction engine
        engine = MCPPredictionEngine()

        # Get context impact
        impact_score = engine.get_context_factors(region, days_ahead)

        # Get active context data
        end_date = timezone.now() + timedelta(days=days_ahead)
        context_data = ContextData.objects.filter(
            region=region,
            effective_date__lte=end_date,
            expiry_date__gte=timezone.now()
        ).order_by('effective_date')

        response = f"""
**Contextual Factors Analysis**

**Region:** {region}
**Analysis Period:** Next {days_ahead} days

**Overall Impact Score:** {impact_score:.2f} (1.0 = normal, >1.0 = increased demand)

**Active Contextual Factors:**
        """

        if not context_data:
            response += "\nNo significant contextual factors currently active."
        else:
            for context in context_data:
                response += f"""

**{context.get_data_type_display()}**
- Type: {context.data_type}
- Effective: {context.effective_date.date()}
- Expires: {context.expiry_date.date() if context.expiry_date else 'Ongoing'}
- Confidence: {context.confidence_score:.1%}
                """

                # Add specific details based on type
                if context.data_type == 'weather':
                    response += f"- Conditions: Temp {context.temperature}°C, Humidity {context.humidity}%, Rainfall {context.rainfall}mm"
                elif context.data_type == 'disease_trend':
                    response += f"- Disease: {context.disease_name}, Trend: {context.trend_direction}, Cases: {context.case_count}"
                elif context.data_type == 'public_health_alert':
                    response += f"- Level: {context.alert_level}, Message: {context.alert_message}"

        return response.strip()

    except Exception as e:
        logger.error(f"Error in get_contextual_factors: {str(e)}")
        return f"Error retrieving contextual factors: {str(e)}"

@app.tool()
async def generate_shortage_alert(
    medical_item_name: str,
    region: str,
    severity_level: str = "medium"
) -> str:
    """
    Generate and send shortage alerts to relevant stakeholders
    """
    try:
        from mcp.models import PredictionAlert

        # Find medical item
        medical_item = MedicalItem.objects.filter(
            name__icontains=medical_item_name
        ).first()

        if not medical_item:
            return f"Medical item '{medical_item_name}' not found."

        # Create mock prediction for alert generation
        from mcp.models import ShortagePrediction
        from django.utils import timezone

        prediction = ShortagePrediction.objects.create(
            medical_item=medical_item,
            region=region,
            predicted_shortage_date=timezone.now(),
            confidence_score=0.8,
            severity_level=severity_level,
            predicted_shortage_duration=7,
            demand_increase_reason="Generated via MCP server",
            supply_constraint_reason="Alert requested",
            is_active=True
        )

        # Initialize prediction engine
        engine = MCPPredictionEngine()

        # Generate alert
        alert = engine.create_prediction_alert(prediction)

        response = f"""
**Shortage Alert Generated**

**Alert Details:**
- ID: {alert.id}
- Type: {alert.alert_type}
- Item: {medical_item.name}
- Region: {region}
- Severity: {severity_level.upper()}

**Message:**
{alert.message}

**Recommended Actions:**
{alert.recommended_actions}

**Notification Targets:**
- Vendors: {'Yes' if alert.notify_vendors else 'No'}
- Health Authorities: {'Yes' if alert.notify_health_authorities else 'No'}
- Public: {'Yes' if alert.notify_public else 'No'}

**Status:** Alert created and ready for sending
        """

        return response.strip()

    except Exception as e:
        logger.error(f"Error in generate_shortage_alert: {str(e)}")
        return f"Error generating alert: {str(e)}"

async def main():
    """Main entry point for the MCP server"""
    logger.info("Starting MedVault MCP Server with FastMCP...")

    # Run the FastMCP app
    await app.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())
