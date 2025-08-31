#!/bin/bash

# LaVidaLuca Super-Fast Development Starter
# Ultimate 100x development acceleration - starts everything in optimal configuration

set -e

# Colors for better UX
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Unicode symbols for better visual feedback
CHECK="✅"
CROSS="❌"
ROCKET="🚀"
GEAR="⚙️"
LIGHTNING="⚡"
ROBOT="🤖"

clear

echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                LaVidaLuca Super Development Mode                 ║${NC}"
echo -e "${PURPLE}║                  🚀 100x ACCELERATED DEVELOPMENT 🚀             ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to show step progress
show_step() {
    echo -e "${CYAN}${GEAR} $1${NC}"
}

show_success() {
    echo -e "${GREEN}${CHECK} $1${NC}"
}

show_error() {
    echo -e "${RED}${CROSS} $1${NC}"
}

show_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -d "apps" ]; then
    show_error "Please run this script from the LaVidaLuca-App root directory"
    exit 1
fi

show_step "Running AI health check and auto-fixes..."
npm run ai:auto > /dev/null 2>&1
show_success "AI assistant completed health check and fixes"

show_step "Setting up environment files..."
# Ensure .env files exist
if [ ! -f "apps/backend/.env" ] && [ -f "apps/backend/.env.example" ]; then
    cp apps/backend/.env.example apps/backend/.env
    show_success "Created backend .env file"
fi

if [ ! -f "apps/web/.env.local" ] && [ -f "apps/web/.env.local.example" ]; then
    cp apps/web/.env.local.example apps/web/.env.local
    show_success "Created frontend .env.local file"
fi

show_step "Starting super development mode..."
echo ""
echo -e "${YELLOW}🎯 SUPER DEVELOPMENT MODE ACTIVATED ${YELLOW}"
echo -e "${YELLOW}====================================${NC}"
echo ""
echo -e "${GREEN}${LIGHTNING} Starting concurrent services:${NC}"
echo -e "  ${CYAN}🌐 Frontend${NC}      - Next.js dev server (port 3000)"
echo -e "  ${CYAN}🔧 Backend${NC}       - FastAPI with auto-reload (port 8000)" 
echo -e "  ${CYAN}🧪 Tests${NC}         - Continuous test watching"
echo -e "  ${CYAN}🔍 Linting${NC}       - Real-time code quality checks"
echo ""
echo -e "${PURPLE}${ROBOT} AI Assistant is monitoring and will auto-fix issues!${NC}"
echo ""
echo -e "${BLUE}📊 Access Points:${NC}"
echo -e "  • Frontend:    http://localhost:3000"
echo -e "  • API Docs:    http://localhost:8000/docs"
echo -e "  • API:         http://localhost:8000"
echo ""
echo -e "${YELLOW}🔥 Performance Tips:${NC}"
echo -e "  • Save any file to trigger instant rebuilds"
echo -e "  • Tests run automatically on code changes"
echo -e "  • Linting fixes issues in real-time"
echo -e "  • AI assistant monitors and auto-fixes problems"
echo ""
echo -e "${GREEN}Press Ctrl+C to stop all services${NC}"
echo ""

# Small delay to let user read the info
sleep 3

# Start the super development mode
npm run dev:turbo