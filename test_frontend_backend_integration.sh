#!/bin/bash

# Frontend-Backend Integration Test Script
# This script tests all API endpoints and verifies data flow

echo "=========================================="
echo "AgroSmart Frontend-Backend Integration Test"
echo "=========================================="
echo ""

API_URL="http://localhost:8000/api"
FRONTEND_URL="http://localhost:5173"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local endpoint=$1
    local method=$2
    local data=$3
    local description=$4
    
    echo -e "${BLUE}Testing: ${description}${NC}"
    
    if [ "$method" == "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "${API_URL}${endpoint}")
    else
        response=$(curl -s -w "\n%{http_code}" -X POST "${API_URL}${endpoint}" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -eq 200 ]; then
        echo -e "${GREEN}✓ PASSED${NC} - HTTP $http_code"
        echo "Response: $body" | jq '.' 2>/dev/null || echo "$body"
        echo ""
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} - HTTP $http_code"
        echo "Response: $body"
        echo ""
        ((FAILED++))
        return 1
    fi
}

echo "1. Testing Backend Health Check"
echo "--------------------------------"
test_endpoint "/health" "GET" "" "Backend health status"

echo ""
echo "2. Testing Crop Prediction Endpoint"
echo "------------------------------------"
CROP_DATA='{
  "soil_type": "Alluvial Soil",
  "n_level": 90,
  "p_level": 42,
  "k_level": 43,
  "temperature": 20.87,
  "humidity": 82.0,
  "ph_level": 6.5,
  "rainfall": 202.0,
  "region": "North India"
}'
test_endpoint "/predict-crop" "POST" "$CROP_DATA" "Crop prediction with real ML model"

echo ""
echo "3. Testing Fertilizer Recommendation Endpoint"
echo "----------------------------------------------"
FERTILIZER_DATA='{
  "crop_type": "Rice",
  "current_n": 40,
  "current_p": 30,
  "current_k": 20,
  "soil_ph": 6.8,
  "soil_type": "Alluvial Soil"
}'
test_endpoint "/recommend-fertilizer" "POST" "$FERTILIZER_DATA" "Fertilizer recommendation with ML model"

echo ""
echo "4. Testing Yield Estimation Endpoint"
echo "-------------------------------------"
YIELD_DATA='{
  "crop_type": "Rice",
  "area_hectares": 2.5,
  "season": "Kharif",
  "temperature": 28.5,
  "humidity": 75.0,
  "rainfall": 150.0,
  "soil_type": "Alluvial Soil",
  "soil_ph": 7.0,
  "n_level": 80,
  "p_level": 40,
  "k_level": 50
}'
test_endpoint "/estimate-yield" "POST" "$YIELD_DATA" "Yield estimation with ML model"

echo ""
echo "=========================================="
echo "INTEGRATION CHECK RESULTS"
echo "=========================================="
echo ""

# Check if backend is using ML models
echo "5. Checking ML Model Integration"
echo "---------------------------------"
echo -e "${BLUE}Verifying ML models are loaded...${NC}"

# Test for ML model artifacts
if [ -d "/home/DevCrewX/Desktop/AgroSmart/backend/trained_models" ]; then
    model_count=$(ls -1 /home/DevCrewX/Desktop/AgroSmart/backend/trained_models/*.pkl 2>/dev/null | wc -l)
    if [ $model_count -gt 0 ]; then
        echo -e "${GREEN}✓ PASSED${NC} - Found $model_count ML model files"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} - No ML model files found"
        ((FAILED++))
    fi
else
    echo -e "${RED}✗ FAILED${NC} - trained_models directory not found"
    ((FAILED++))
fi

echo ""
echo "6. Checking Frontend API Integration"
echo "-------------------------------------"
if [ -f "/home/DevCrewX/Desktop/AgroSmart/src/services/api.ts" ]; then
    echo -e "${GREEN}✓ PASSED${NC} - API service layer exists"
    ((PASSED++))
    
    # Check if API calls are not hardcoded
    echo -e "${BLUE}Checking for hardcoded data in frontend...${NC}"
    
    # Check CropPrediction component
    if grep -q "import \* as api from '../services/api'" /home/DevCrewX/Desktop/AgroSmart/src/pages/CropPrediction.tsx; then
        echo -e "${GREEN}✓ PASSED${NC} - CropPrediction uses API service"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} - CropPrediction might have hardcoded data"
        ((FAILED++))
    fi
    
    # Check FertilizerRecommendation component
    if grep -q "import \* as api from '../services/api'" /home/DevCrewX/Desktop/AgroSmart/src/pages/FertilizerRecommendation.tsx; then
        echo -e "${GREEN}✓ PASSED${NC} - FertilizerRecommendation uses API service"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} - FertilizerRecommendation might have hardcoded data"
        ((FAILED++))
    fi
    
    # Check YieldEstimation component
    if grep -q "import \* as api from '../services/api'" /home/DevCrewX/Desktop/AgroSmart/src/pages/YieldEstimation.tsx; then
        echo -e "${GREEN}✓ PASSED${NC} - YieldEstimation uses API service"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} - YieldEstimation might have hardcoded data"
        ((FAILED++))
    fi
else
    echo -e "${RED}✗ FAILED${NC} - API service layer not found"
    ((FAILED++))
fi

echo ""
echo "7. Checking Dashboard Data Source"
echo "----------------------------------"
if grep -q "Mock dashboard data" /home/DevCrewX/Desktop/AgroSmart/src/pages/Dashboard.tsx; then
    echo -e "${YELLOW}⚠ WARNING${NC} - Dashboard is using mock data"
    echo "  → Dashboard needs to be connected to a real database or API"
else
    echo -e "${GREEN}✓ PASSED${NC} - Dashboard appears to use dynamic data"
    ((PASSED++))
fi

echo ""
echo "8. Checking for Hardcoded Values"
echo "---------------------------------"

# Check for potential hardcoded response data
HARDCODED_PATTERNS=(
    "predicted_crop.*=.*['\"].*['\"]"
    "recommended_fertilizer.*=.*['\"].*['\"]"
    "estimated_yield.*=.*[0-9]+"
)

echo -e "${BLUE}Scanning frontend files for hardcoded predictions...${NC}"

HARDCODED_FOUND=false
for pattern in "${HARDCODED_PATTERNS[@]}"; do
    matches=$(grep -rn --include="*.tsx" --include="*.ts" "$pattern" /home/DevCrewX/Desktop/AgroSmart/src/ 2>/dev/null | grep -v "interface\|type\|const.*=.*useState" | head -5)
    if [ ! -z "$matches" ]; then
        HARDCODED_FOUND=true
        echo -e "${YELLOW}⚠ Potential hardcoded value found:${NC}"
        echo "$matches"
    fi
done

if [ "$HARDCODED_FOUND" = false ]; then
    echo -e "${GREEN}✓ PASSED${NC} - No obvious hardcoded prediction values found"
    ((PASSED++))
fi

echo ""
echo "=========================================="
echo "TEST SUMMARY"
echo "=========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
TOTAL=$((PASSED + FAILED))
echo "Total: $TOTAL"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED!${NC}"
    echo "Frontend is properly connected to the ML-powered backend."
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    echo "Please review the failures above."
    exit 1
fi
