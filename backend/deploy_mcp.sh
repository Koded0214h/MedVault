#!/bin/bash

# MedVault MCP Server Deployment Script
# This script sets up and runs the MCP server for production use

echo "🚀 Starting MedVault MCP Server Deployment..."

# Set environment variables
export DJANGO_SETTINGS_MODULE=backend.settings
export PYTHONPATH="/Users/koded/Desktop/Code/MedVault/backend:$PYTHONPATH"

# Navigate to backend directory
cd /Users/koded/Desktop/Code/MedVault/backend

# Activate virtual environment if it exists
if [ -d "env" ]; then
    source env/bin/activate
    echo "✅ Virtual environment activated"
fi

# Run database migrations (ensure database is ready)
echo "📊 Checking database migrations..."
python manage.py migrate --check
if [ $? -ne 0 ]; then
    echo "⚠️  Running database migrations..."
    python manage.py migrate
fi

# Test MCP server components
echo "🧪 Testing MCP server components..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()
import sys
sys.path.insert(0, '/Users/koded/Desktop/Code/MedVault/backend')

from fastmcp import FastMCP
from mcp.prediction_engine import MCPPredictionEngine
from inventory.models import MedicalItem

print('✅ All imports successful')
print('✅ MCP server ready for deployment')
"

if [ $? -eq 0 ]; then
    echo "🎉 MCP server components verified successfully!"
    echo ""
    echo "📋 Deployment Instructions:"
    echo "1. The MCP server is ready to run"
    echo "2. Use the following command to start the server:"
    echo "   python mcp_server_deployment.py"
    echo ""
    echo "3. For production deployment, consider:"
    echo "   - Setting up a process manager (systemd/pm2)"
    echo "   - Configuring environment variables"
    echo "   - Setting up monitoring and logging"
    echo "   - Using a production database"
    echo ""
    echo "4. The server will listen for MCP protocol messages"
    echo "   and provide healthcare resource prediction tools"
else
    echo "❌ MCP server verification failed. Please check the errors above."
    exit 1
fi
