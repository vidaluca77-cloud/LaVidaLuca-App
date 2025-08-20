#!/bin/bash
# Health Check Script for LaVidaLuca Production Deployment
# Verifies that both frontend and backend are properly deployed and accessible

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL=${BACKEND_URL:-"https://lavidaluca-backend.onrender.com"}
FRONTEND_URL=${FRONTEND_URL:-"https://lavidaluca.vercel.app"}
TIMEOUT=30
MAX_RETRIES=3

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "SUCCESS")
            echo -e "${GREEN}✅ $message${NC}"
            ;;
        "ERROR")
            echo -e "${RED}❌ $message${NC}"
            ;;
        "WARNING")
            echo -e "${YELLOW}⚠️  $message${NC}"
            ;;
        "INFO")
            echo -e "ℹ️  $message"
            ;;
    esac
}

# Function to check HTTP endpoint
check_endpoint() {
    local url=$1
    local expected_status=${2:-200}
    local retries=0
    
    while [ $retries -lt $MAX_RETRIES ]; do
        # Simple connectivity check
        status_code=$(curl -s --max-time $TIMEOUT -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
        if [[ "$status_code" =~ ^[23] ]]; then
            return 0
        fi
        retries=$((retries + 1))
        if [ $retries -lt $MAX_RETRIES ]; then
            print_status "WARNING" "Attempt $retries failed for $url (status: $status_code), retrying..."
            sleep 5
        fi
    done
    return 1
}

# Function to check JSON API endpoint
check_json_endpoint() {
    local url=$1
    local retries=0
    
    while [ $retries -lt $MAX_RETRIES ]; do
        response=$(curl -s --max-time $TIMEOUT "$url" 2>/dev/null || echo "")
        if [ -n "$response" ] && echo "$response" | grep -q "{"; then
            return 0
        fi
        retries=$((retries + 1))
        if [ $retries -lt $MAX_RETRIES ]; then
            print_status "WARNING" "Attempt $retries failed for $url, retrying..."
            sleep 5
        fi
    done
    return 1
}

print_status "INFO" "Starting health checks for LaVidaLuca production deployment..."
print_status "INFO" "Backend URL: $BACKEND_URL"
print_status "INFO" "Frontend URL: $FRONTEND_URL"

# Backend Health Checks
print_status "INFO" "Checking backend health..."

# Check if backend is accessible
if check_endpoint "$BACKEND_URL"; then
    print_status "SUCCESS" "Backend is accessible"
else
    print_status "ERROR" "Backend is not accessible at $BACKEND_URL"
    exit 1
fi

# Check backend health endpoint
if check_json_endpoint "$BACKEND_URL/health"; then
    print_status "SUCCESS" "Backend health endpoint is responding"
else
    print_status "WARNING" "Backend health endpoint not available (this is expected if not implemented yet)"
fi

# Check backend API documentation
if check_endpoint "$BACKEND_URL/docs"; then
    print_status "SUCCESS" "Backend API documentation is accessible"
else
    print_status "WARNING" "Backend API documentation not accessible"
fi

# Frontend Health Checks
print_status "INFO" "Checking frontend health..."

# Check if frontend is accessible
if check_endpoint "$FRONTEND_URL"; then
    print_status "SUCCESS" "Frontend is accessible"
else
    print_status "ERROR" "Frontend is not accessible at $FRONTEND_URL"
    exit 1
fi

# Check if frontend loads properly (look for HTML content)
frontend_content=$(curl -s --max-time $TIMEOUT "$FRONTEND_URL" 2>/dev/null || echo "")
if echo "$frontend_content" | grep -qi "html\|<!doctype"; then
    print_status "SUCCESS" "Frontend is serving HTML content"
else
    print_status "ERROR" "Frontend is not serving proper HTML content"
    exit 1
fi

# Additional checks
print_status "INFO" "Running additional checks..."

# Check if backend API endpoints are accessible
api_endpoints=("/api/v1" "/api/v1/health")
for endpoint in "${api_endpoints[@]}"; do
    if check_endpoint "$BACKEND_URL$endpoint"; then
        print_status "SUCCESS" "Backend endpoint $endpoint is accessible"
    else
        print_status "WARNING" "Backend endpoint $endpoint is not accessible"
    fi
done

print_status "SUCCESS" "Health checks completed successfully!"
print_status "INFO" "Deployment verification finished"

exit 0