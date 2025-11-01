#!/usr/bin/env python3
"""
MedVault MCP Server - Model Context Protocol Implementation
Provides AI assistants with access to healthcare resource prediction capabilities
"""

import asyncio
import logging
from typing import Any, Sequence
from mcp import Tool
from mcp.server import Server
from mcp.types import TextContent, PromptMessage
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from mcp.prediction_engine import MCPPredictionEngine
from inventory.models import MedicalItem
from mcp.models import DemandData, ContextData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
server = Server("medvault-mcp")

@server.tool()
async def predict_shortage(
    medical_item_name: str,
    region: str,
    prediction_days: int = 14
) -> str:
    """
    Predict medical resource shortages using AI

    Args:
        medical_item_name: Name of the medical item (e.g., "Insulin", "Paracetamol")
        region: Geographic region (e.g., "Lagos", "Nairobi")
        prediction_days: Number of days to predict ahead (default: 14)

    Returns:
        Prediction results including shortage risk, confidence score, and recommendations
    """
    try:
        # Find medical item
        medical_item = MedicalItem.objects.filter(
            name__icontains=medical_item_name
        ).first()

        if not medical_item:
            return f"Medical item '{medical_item_name}' not found in inventory."

        # Initialize prediction engine
        engine = MCPPredictionEngine()

        # Run prediction
        prediction = engine.predict_shortage(
            medical_item=medical_item,
            region=region,
            prediction_days=prediction_days
        )

        if not prediction:
            return f"Unable to generate prediction for {medical_item_name} in {region}."

        # Format response
        response = f"""
**Medical Resource Shortage Prediction**

**Item:** {medical_item.name}
**Region:** {region}
**Prediction Period:** {prediction_days} days

**Current Status:**
- Current Supply: {prediction['current_supply']} units
- Predicted Demand: {prediction['predicted_demand']:.1f} units
- Days Until Shortage: {prediction['days_until_shortage']:.1f}

**Risk Assessment:**
- Severity Level: {prediction['severity_level'].upper()}
- Confidence Score: {prediction['confidence_score']:.1%}

**Contributing Factors:**
- Demand Increase: {prediction['demand_increase_reason']}
- Supply Constraints: {prediction['supply_constraint_reason']}

**Recommended Actions:**
{engine.generate_recommended_actions({
    'severity_level': prediction['severity_level'],
    'medical_item': medical_item,
    'region': region
})}
        """

        return response.strip()

    except Exception as e:
        logger.error(f"Error in predict_shortage: {str(e)}")
        return f"Error generating prediction: {str(e)}"

@server.tool()
async def get_inventory_status(
    region: str = None,
    medical_item_name: str = None
) -> str:
    """
    Get current inventory status for medical items

    Args:
        region: Filter by geographic region (optional)
        medical_item_name: Filter by medical item name (optional)

    Returns:
        Current inventory levels and availability
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

@server.tool()
async def analyze_demand_trends(
    medical_item_name: str,
    region: str,
    days_back: int = 30
) -> str:
    """
    Analyze historical demand trends for medical items

    Args:
        medical_item_name: Name of the medical item
        region: Geographic region
        days_back: Number of days to analyze (default: 30)

    Returns:
        Demand trend analysis and insights
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

@server.tool()
async def get_contextual_factors(
    region: str,
    days_ahead: int = 14
) -> str:
    """
    Get contextual factors affecting healthcare demand

    Args:
        region: Geographic region
        days_ahead: Number of days to look ahead (default: 14)

    Returns:
        Current and upcoming contextual factors
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

@server.tool()
async def generate_shortage_alert(
    medical_item_name: str,
    region: str,
    severity_level: str = "medium"
) -> str:
    """
    Generate and send shortage alerts to relevant stakeholders

    Args:
        medical_item_name: Name of the medical item
        region: Geographic region
        severity_level: Alert severity (low/medium/high/critical)

    Returns:
        Alert generation status and details
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
    import mcp.server.stdio

    logger.info("Starting MedVault MCP Server...")
    logger.info("Available tools:")
    logger.info("- predict_shortage: Predict medical resource shortages")
    logger.info("- get_inventory_status: Check current inventory levels")
    logger.info("- analyze_demand_trends: Analyze historical demand patterns")
    logger.info("- get_contextual_factors: Get factors affecting demand")
    logger.info("- generate_shortage_alert: Create and send shortage alerts")

    # Run the server using stdio transport
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
