# MCP Core Verification and Testing Plan

## Step 1: Verify MCP Core Models and Logic
- [ ] Review MCP models (MCPConfig, DemandData, ContextData, ShortagePrediction, PredictionAlert) for completeness
- [ ] Check prediction engine calculations (demand trend, supply levels, context factors, confidence scoring)
- [ ] Verify views and serializers for correct API endpoints
- [ ] Ensure URLs are properly configured

## Step 2: Test Data Integration
- [ ] Create sample data script for inventory, EHR prescriptions, DemandData, and ContextData
- [ ] Verify DemandData can be populated from EHR prescriptions (check signals)
- [ ] Test ContextData integration (weather, disease trends, alerts)

## Step 3: Run Prediction Tests
- [ ] Set up Django test environment
- [ ] Execute predictions via API endpoints
- [ ] Verify prediction outputs and database saves
- [ ] Test different scenarios (high demand, low supply, context impacts)

## Step 4: Check Alert Generation
- [ ] Ensure PredictionAlert models are created correctly
- [ ] Verify integration with notifications system
- [ ] Test alert sending logic

## Step 5: Identify and Implement Fixes
- [ ] Add automatic DemandData creation from prescriptions (signals)
- [ ] Enhance prediction logic if needed
- [ ] Integrate alerts with notification services
- [ ] Add comprehensive tests to mcp/tests.py

## Followup Steps
- [ ] Create test data population script
- [ ] Run Django server and test all endpoints
- [ ] Fix any identified issues
- [ ] Run full integration test with real data flow
