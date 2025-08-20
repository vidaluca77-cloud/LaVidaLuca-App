#!/bin/bash
# Production Deployment Validation Script
# This script validates that all required configurations are in place

set -e

echo "🚀 La Vida Luca - Production Deployment Validation"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL="${PRODUCTION_API_URL:-https://lavidaluca-backend.onrender.com}"
FRONTEND_URL="${PRODUCTION_FRONTEND_URL:-https://lavidaluca.fr}"
TIMEOUT=10

# Validation functions
check_status() {
    local name="$1"
    local url="$2"
    local expected_status="$3"
    
    echo -n "Checking $name... "
    
    status_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT "$url" || echo "000")
    
    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✓ OK${NC} ($status_code)"
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} ($status_code)"
        return 1
    fi
}

check_json_response() {
    local name="$1"
    local url="$2"
    local field="$3"
    local expected="$4"
    
    echo -n "Checking $name... "
    
    response=$(curl -s --max-time $TIMEOUT "$url" || echo "{}")
    actual=$(echo "$response" | jq -r ".$field" 2>/dev/null || echo "null")
    
    if [ "$actual" = "$expected" ]; then
        echo -e "${GREEN}✓ OK${NC} ($actual)"
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} (expected: $expected, got: $actual)"
        return 1
    fi
}

check_health_endpoint() {
    local name="$1"
    local url="$2"
    
    echo -n "Checking $name health... "
    
    response=$(curl -s --max-time $TIMEOUT "$url" || echo "{}")
    status=$(echo "$response" | jq -r '.status' 2>/dev/null || echo "null")
    
    case "$status" in
        "healthy")
            echo -e "${GREEN}✓ HEALTHY${NC}"
            return 0
            ;;
        "degraded")
            echo -e "${YELLOW}⚠ DEGRADED${NC}"
            return 1
            ;;
        "unhealthy")
            echo -e "${RED}✗ UNHEALTHY${NC}"
            return 1
            ;;
        *)
            echo -e "${RED}✗ UNKNOWN${NC} ($status)"
            return 1
            ;;
    esac
}

# Main validation
echo -e "\n${BLUE}1. Basic Connectivity Tests${NC}"
echo "----------------------------"

errors=0

# Backend basic health
if ! check_status "Backend Basic Health" "$BACKEND_URL/health" "200"; then
    ((errors++))
fi

# Backend liveness probe
if ! check_status "Backend Liveness" "$BACKEND_URL/health/live" "200"; then
    ((errors++))
fi

# Backend readiness probe  
if ! check_status "Backend Readiness" "$BACKEND_URL/health/ready" "200"; then
    ((errors++))
fi

# Frontend
if ! check_status "Frontend" "$FRONTEND_URL" "200"; then
    ((errors++))
fi

echo -e "\n${BLUE}2. Health Status Validation${NC}"
echo "-----------------------------"

# Comprehensive health check
if ! check_health_endpoint "Backend Comprehensive" "$BACKEND_URL/health"; then
    ((errors++))
fi

# Environment validation
if ! check_json_response "Environment" "$BACKEND_URL/health" "environment" "production"; then
    ((errors++))
fi

echo -e "\n${BLUE}3. API Functionality Tests${NC}"
echo "----------------------------"

# Test API endpoint
echo -n "Testing API Guide endpoint... "
api_response=$(curl -s --max-time $TIMEOUT \
    -X POST "$BACKEND_URL/api/v1/guide" \
    -H "Content-Type: application/json" \
    -d '{"question":"test"}' || echo "{}")

if echo "$api_response" | jq -e '.answer' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
    ((errors++))
fi

echo -e "\n${BLUE}4. Deployment Validation${NC}"
echo "-------------------------"

# Deployment validation endpoint
echo -n "Running deployment validation... "
validation_response=$(curl -s --max-time $TIMEOUT "$BACKEND_URL/validate/deployment" || echo "{}")
deployment_valid=$(echo "$validation_response" | jq -r '.deployment_valid' 2>/dev/null || echo "false")

if [ "$deployment_valid" = "true" ]; then
    echo -e "${GREEN}✓ VALID${NC}"
else
    echo -e "${RED}✗ INVALID${NC}"
    echo "Validation details:"
    echo "$validation_response" | jq -r '.checks[] | select(.success == false) | "  - \(.component): \(.message)"' 2>/dev/null || echo "  Could not parse validation response"
    ((errors++))
fi

echo -e "\n${BLUE}5. Security Headers Check${NC}"
echo "-------------------------"

# Check security headers
echo -n "Checking security headers... "
headers=$(curl -s -I --max-time $TIMEOUT "$FRONTEND_URL" 2>/dev/null || echo "")

security_headers=("X-Content-Type-Options" "X-Frame-Options" "X-XSS-Protection")
missing_headers=0

for header in "${security_headers[@]}"; do
    if ! echo "$headers" | grep -qi "$header"; then
        ((missing_headers++))
    fi
done

if [ $missing_headers -eq 0 ]; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${YELLOW}⚠ MISSING $missing_headers HEADERS${NC}"
    # Not counting as error for now, but worth noting
fi

echo -e "\n${BLUE}6. Performance Check${NC}"
echo "--------------------"

# Response time check
echo -n "Checking response times... "
start_time=$(date +%s%N)
curl -s --max-time $TIMEOUT "$BACKEND_URL/health" > /dev/null
end_time=$(date +%s%N)
response_time=$(( (end_time - start_time) / 1000000 )) # Convert to milliseconds

if [ $response_time -lt 2000 ]; then
    echo -e "${GREEN}✓ OK${NC} (${response_time}ms)"
else
    echo -e "${YELLOW}⚠ SLOW${NC} (${response_time}ms)"
fi

# Summary
echo -e "\n${BLUE}Validation Summary${NC}"
echo "=================="

if [ $errors -eq 0 ]; then
    echo -e "${GREEN}✅ All validation checks passed!${NC}"
    echo -e "🚀 Deployment is ready for production traffic"
    exit 0
else
    echo -e "${RED}❌ $errors validation check(s) failed${NC}"
    echo -e "🛑 Deployment issues need to be resolved before production use"
    exit 1
fi