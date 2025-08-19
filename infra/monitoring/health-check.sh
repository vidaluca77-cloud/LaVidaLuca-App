#!/bin/bash

# Health check script for La Vida Luca application
# This script checks the health of frontend and backend services

# Configuration
FRONTEND_URL="${FRONTEND_URL:-https://la-vida-luca.vercel.app}"
BACKEND_URL="${BACKEND_URL:-https://la-vida-luca-api.onrender.com}"
WEBHOOK_URL="${WEBHOOK_URL:-}"  # Discord/Slack webhook for notifications

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

check_service() {
    local name="$1"
    local url="$2"
    local expected_status="${3:-200}"
    
    log "Checking $name at $url..."
    
    response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 --max-time 30 "$url")
    
    if [ "$response" = "$expected_status" ]; then
        log "${GREEN}✓ $name is healthy (HTTP $response)${NC}"
        return 0
    else
        log "${RED}✗ $name is unhealthy (HTTP $response)${NC}"
        return 1
    fi
}

send_notification() {
    local message="$1"
    local color="${2:-16711680}"  # Red color in decimal
    
    if [ -n "$WEBHOOK_URL" ]; then
        curl -s -X POST "$WEBHOOK_URL" \
            -H "Content-Type: application/json" \
            -d "{
                \"embeds\": [{
                    \"title\": \"La Vida Luca - Health Check Alert\",
                    \"description\": \"$message\",
                    \"color\": $color,
                    \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%S.000Z)\"
                }]
            }" > /dev/null
    fi
}

main() {
    log "Starting health check for La Vida Luca services..."
    
    local all_healthy=true
    local failed_services=""
    
    # Check frontend
    if ! check_service "Frontend" "$FRONTEND_URL"; then
        all_healthy=false
        failed_services+="Frontend "
    fi
    
    # Check backend health endpoint
    if ! check_service "Backend Health" "$BACKEND_URL/health"; then
        all_healthy=false
        failed_services+="Backend "
    fi
    
    # Check backend API endpoint
    if ! check_service "Backend API" "$BACKEND_URL/activities"; then
        all_healthy=false
        failed_services+="API "
    fi
    
    if [ "$all_healthy" = true ]; then
        log "${GREEN}All services are healthy!${NC}"
        # Send success notification only if previous check failed
        if [ -f "/tmp/lavidaluca_health_failed" ]; then
            send_notification "✅ All services are now healthy!" "65280"  # Green
            rm -f "/tmp/lavidaluca_health_failed"
        fi
    else
        log "${RED}Some services are unhealthy: $failed_services${NC}"
        send_notification "🚨 Health check failed for: $failed_services" "16711680"  # Red
        touch "/tmp/lavidaluca_health_failed"
        exit 1
    fi
}

main "$@"