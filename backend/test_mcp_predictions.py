#!/usr/bin/env python
"""
Test script for MCP Core predictions
"""
import os
import sys
import django
import json
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from inventory.models import MedicalItem, Inventory, Vendor
from mcp.models import MCPConfig, DemandData, ContextData, ShortagePrediction, PredictionAlert
from mcp.prediction_engine import MCPPredictionEngine

def test_prediction_engine():
    """Test the prediction engine directly"""
    print("Testing MCP Prediction Engine...")

    engine = MCPPredictionEngine()

    # Get test data
    insulin = MedicalItem.objects.get(name='Insulin')
    tetanus_vaccine = MedicalItem.objects.get(name='Tetanus Vaccine')

    print(f"Testing predictions for {insulin.name} in Lagos...")

    # Run prediction for Insulin
    prediction = engine.predict_shortage(insulin, 'Lagos', prediction_days=14)

    if prediction:
        print("✓ Prediction generated successfully")
        print(f"  - Predicted demand: {prediction['predicted_demand']:.1f}")
        print(f"  - Current supply: {prediction['current_supply']}")
        print(f"  - Days until shortage: {prediction['days_until_shortage']:.1f}")
        print(f"  - Confidence score: {prediction['confidence_score']:.2%}")
        print(f"  - Severity level: {prediction['severity_level']}")
    else:
        print("✗ No prediction generated")

    # Test bulk predictions
    print("\nTesting bulk predictions...")
    predictions = engine.run_predictions(regions=['Lagos'], prediction_days=14)

    print(f"Generated {len(predictions)} predictions")

    # Save predictions
    saved_predictions = engine.save_predictions(predictions)
    print(f"Saved {len(saved_predictions)} predictions to database")

    return predictions, saved_predictions

def test_api_endpoints():
    """Test MCP API endpoints"""
    print("\nTesting MCP API endpoints...")

    client = APIClient()

    # Create test user and authenticate
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        test_user = User.objects.get(username='admin')
        client.force_authenticate(user=test_user)

        # Test config endpoint
        print("Testing MCP config endpoint...")
        response = client.get('/api/mcp/config/')
        print(f"Config endpoint status: {response.status_code}")

        if response.status_code == 200:
            configs = response.json()
            print(f"Found {len(configs)} MCP configurations")

        # Test demand data endpoint
        print("Testing demand data endpoint...")
        response = client.get('/api/mcp/demand-data/')
        print(f"Demand data endpoint status: {response.status_code}")

        if response.status_code == 200:
            demand_data = response.json()
            print(f"Found {demand_data['count']} demand data entries")

        # Test context data endpoint
        print("Testing context data endpoint...")
        response = client.get('/api/mcp/context-data/')
        print(f"Context data endpoint status: {response.status_code}")

        if response.status_code == 200:
            context_data = response.json()
            print(f"Found {context_data['count']} context data entries")

        # Test run predictions endpoint
        print("Testing run predictions endpoint...")
        prediction_request = {
            'region': 'Lagos',
            'prediction_days': 14
        }
        response = client.post('/api/mcp/predictions/run/', prediction_request, format='json')
        print(f"Run predictions endpoint status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"API generated {len(result['predictions'])} predictions")

        # Test predictions list endpoint
        print("Testing predictions list endpoint...")
        response = client.get('/api/mcp/predictions/')
        print(f"Predictions list endpoint status: {response.status_code}")

        if response.status_code == 200:
            predictions = response.json()
            print(f"Found {predictions['count']} total predictions in database")

        # Test critical shortages endpoint
        print("Testing critical shortages endpoint...")
        response = client.get('/api/mcp/predictions/critical/')
        print(f"Critical shortages endpoint status: {response.status_code}")

        if response.status_code == 200:
            critical = response.json()
            print(f"Found {len(critical)} critical shortages")

        # Test stats endpoint
        print("Testing stats endpoint...")
        response = client.get('/api/mcp/stats/')
        print(f"Stats endpoint status: {response.status_code}")

        if response.status_code == 200:
            stats = response.json()
            print("Prediction stats:")
            for key, value in stats.items():
                print(f"  {key}: {value}")

        return True

    except User.DoesNotExist:
        print("✗ Test user not found")
        return False
    except Exception as e:
        print(f"✗ API test error: {e}")
        return False

def test_alert_generation():
    """Test alert generation"""
    print("\nTesting alert generation...")

    # Check if alerts were created during prediction run
    alerts = PredictionAlert.objects.all()
    print(f"Found {alerts.count()} prediction alerts in database")

    for alert in alerts[:3]:  # Show first 3 alerts
        print(f"Alert: {alert.alert_type} - {alert.prediction.medical_item.name}")
        print(f"  Message: {alert.message}")
        print(f"  Notify vendors: {alert.notify_vendors}")
        print(f"  Notify authorities: {alert.notify_health_authorities}")
        print(f"  Notify public: {alert.notify_public}")

    return alerts.count() > 0

def test_data_integrity():
    """Test data integrity and relationships"""
    print("\nTesting data integrity...")

    issues = []

    # Check that demand data exists
    demand_count = DemandData.objects.count()
    if demand_count == 0:
        issues.append("No demand data found")
    else:
        print(f"✓ Found {demand_count} demand data entries")

    # Check that context data exists
    context_count = ContextData.objects.count()
    if context_count == 0:
        issues.append("No context data found")
    else:
        print(f"✓ Found {context_count} context data entries")

    # Check that inventory exists
    inventory_count = Inventory.objects.count()
    if inventory_count == 0:
        issues.append("No inventory data found")
    else:
        print(f"✓ Found {inventory_count} inventory items")

    # Check that predictions were generated
    prediction_count = ShortagePrediction.objects.count()
    if prediction_count == 0:
        issues.append("No predictions generated")
    else:
        print(f"✓ Found {prediction_count} predictions")

    # Check for critical predictions
    critical_count = ShortagePrediction.objects.filter(severity_level='critical').count()
    high_count = ShortagePrediction.objects.filter(severity_level='high').count()
    print(f"✓ Found {critical_count} critical and {high_count} high severity predictions")

    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  ✗ {issue}")
        return False
    else:
        print("✓ All data integrity checks passed")
        return True

def main():
    """Main test function"""
    print("Starting MCP Core verification tests...\n")

    try:
        # Test prediction engine
        predictions, saved_predictions = test_prediction_engine()

        # Test API endpoints
        api_success = test_api_endpoints()

        # Test alert generation
        alerts_created = test_alert_generation()

        # Test data integrity
        data_integrity = test_data_integrity()

        print("\n" + "="*50)
        print("MCP CORE VERIFICATION RESULTS")
        print("="*50)

        results = {
            'Prediction Engine': len(predictions) > 0,
            'API Endpoints': api_success,
            'Alert Generation': alerts_created,
            'Data Integrity': data_integrity
        }

        all_passed = True
        for test_name, passed in results.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{test_name}: {status}")
            if not passed:
                all_passed = False

        print("\n" + "="*50)
        if all_passed:
            print("🎉 ALL MCP CORE TESTS PASSED!")
            print("The MCP Core is working as expected.")
        else:
            print("⚠️  SOME TESTS FAILED - Review output above for details.")

        return all_passed

    except Exception as e:
        print(f"✗ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
