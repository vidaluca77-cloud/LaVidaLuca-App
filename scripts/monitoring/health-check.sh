#!/bin/bash

# Health Check Script for La Vida Luca Infrastructure
# This script checks the health of all deployed services

set -e

# Configuration
WEB_URL="${VERCEL_PRODUCTION_URL:-https://la-vida-luca.vercel.app}"
API_URL="${RENDER_SERVICE_URL:-https://lavidaluca-ia-api.onrender.com}"
SUPABASE_URL="${NEXT_PUBLIC_SUPABASE_URL}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check HTTP endpoint
check_endpoint() {
    local url=$1
    local name=$2
    local expected_status=${3:-200}
    
    echo -n "Checking $name ($url)... "
    
    if response=$(curl -s -w "%{http_code}" -o /dev/null --max-time 30 "$url"); then
        if [ "$response" -eq "$expected_status" ]; then
            echo -e "${GREEN}✓ OK${NC} (HTTP $response)"
            return 0
        else
            echo -e "${RED}✗ FAILED${NC} (HTTP $response)"
            return 1
        fi
    else
        echo -e "${RED}✗ UNREACHABLE${NC}"
        return 1
    fi
}

# Function to check API endpoint with JSON response
check_api_endpoint() {
    local url=$1
    local name=$2
    
    echo -n "Checking $name API ($url)... "
    
    if response=$(curl -s --max-time 30 -H "Accept: application/json" "$url"); then
        if echo "$response" | jq -e '.status == "healthy"' > /dev/null 2>&1; then
            echo -e "${GREEN}✓ OK${NC}"
            return 0
        else
            echo -e "${YELLOW}⚠ DEGRADED${NC} (Response: $response)"
            return 1
        fi
    else
        echo -e "${RED}✗ UNREACHABLE${NC}"
        return 1
    fi
}

# Function to check database connectivity
check_database() {
    if [ -z "$SUPABASE_URL" ]; then
        echo -e "Database check: ${YELLOW}⚠ SKIPPED${NC} (SUPABASE_URL not set)"
        return 0
    fi
    
    echo -n "Checking Supabase database... "
    
    if response=$(curl -s --max-time 30 "$SUPABASE_URL/rest/v1/" -H "apikey: $NEXT_PUBLIC_SUPABASE_ANON_KEY"); then
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ OK${NC}"
            return 0
        else
            echo -e "${RED}✗ FAILED${NC}"
            return 1
        fi
    else
        echo -e "${RED}✗ UNREACHABLE${NC}"
        return 1
    fi
}

# Main health check
echo "======================================"
echo "La Vida Luca - Health Check"
echo "======================================"
echo "Timestamp: $(date)"
echo ""

# Initialize counters
total_checks=0
failed_checks=0

# Check web application
total_checks=$((total_checks + 1))
if ! check_endpoint "$WEB_URL" "Web Application"; then
    failed_checks=$((failed_checks + 1))
fi

# Check web application health endpoint
total_checks=$((total_checks + 1))
if ! check_endpoint "$WEB_URL/api/health" "Web Health API" 200; then
    failed_checks=$((failed_checks + 1))
fi

# Check IA API
total_checks=$((total_checks + 1))
if ! check_endpoint "$API_URL" "IA API"; then
    failed_checks=$((failed_checks + 1))
fi

# Check IA API health endpoint
total_checks=$((total_checks + 1))
if ! check_api_endpoint "$API_URL/health" "IA Health API"; then
    failed_checks=$((failed_checks + 1))
fi

# Check database
total_checks=$((total_checks + 1))
if ! check_database; then
    failed_checks=$((failed_checks + 1))
fi

# Summary
echo ""
echo "======================================"
echo "Health Check Summary"
echo "======================================"

if [ $failed_checks -eq 0 ]; then
    echo -e "Status: ${GREEN}ALL SYSTEMS OPERATIONAL${NC}"
    echo "✓ $total_checks/$total_checks services healthy"
    exit 0
elif [ $failed_checks -lt $total_checks ]; then
    echo -e "Status: ${YELLOW}PARTIAL OUTAGE${NC}"
    echo "⚠ $((total_checks - failed_checks))/$total_checks services healthy"
    exit 1
else
    echo -e "Status: ${RED}MAJOR OUTAGE${NC}"
    echo "✗ All services are down"
    exit 2
fi