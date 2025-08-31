#!/bin/bash

# LaVidaLuca Development Accelerator
# This script sets up the enhanced development environment for 100x faster development

set -e

echo "🚀 LaVidaLuca Development Accelerator - Setting up 100x faster development"
echo "============================================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -d "apps" ]; then
    print_error "Please run this script from the LaVidaLuca-App root directory"
    exit 1
fi

print_step "1. Installing enhanced development dependencies..."
npm install
if [ $? -eq 0 ]; then
    print_success "Root dependencies installed"
else
    print_error "Failed to install root dependencies"
    exit 1
fi

print_step "2. Installing frontend dependencies..."
cd apps/web
npm install
if [ $? -eq 0 ]; then
    print_success "Frontend dependencies installed"
else
    print_error "Failed to install frontend dependencies"
    exit 1
fi
cd ../..

print_step "3. Installing enhanced backend dependencies..."
cd apps/backend
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    print_success "Backend dependencies installed"
else
    print_error "Failed to install backend dependencies"
    exit 1
fi
cd ../..

print_step "4. Setting up development environment files..."
if [ ! -f "apps/backend/.env" ]; then
    if [ -f "apps/backend/.env.example" ]; then
        cp apps/backend/.env.example apps/backend/.env
        print_success "Backend .env file created from example"
    else
        print_warning "No backend .env.example found"
    fi
fi

if [ ! -f "apps/web/.env.local" ]; then
    if [ -f "apps/web/.env.local.example" ]; then
        cp apps/web/.env.local.example apps/web/.env.local
        print_success "Frontend .env.local file created from example"
    else
        print_warning "No frontend .env.local.example found"
    fi
fi

print_step "5. Running validation checks..."
npm run validate
if [ $? -eq 0 ]; then
    print_success "All validation checks passed!"
else
    print_warning "Some validation checks failed - see output above"
fi

echo ""
echo "🎉 Development Accelerator Setup Complete!"
echo "=========================================="
echo ""
echo -e "${CYAN}Available Development Commands:${NC}"
echo ""
echo -e "  ${GREEN}npm run dev:turbo${NC}     - Start everything with live testing and linting"
echo -e "  ${GREEN}npm run dev:full${NC}      - Start web, API, and watch tests"
echo -e "  ${GREEN}npm run test:watch${NC}    - Run tests in watch mode"
echo -e "  ${GREEN}npm run status${NC}        - Check build, test, and type status"
echo -e "  ${GREEN}npm run validate${NC}      - Run full validation (lint, type-check, test, build)"
echo ""
echo -e "${YELLOW}For 100x faster development:${NC}"
echo -e "  1. Use ${GREEN}npm run dev:turbo${NC} for continuous development"
echo -e "  2. Keep tests running with live feedback"
echo -e "  3. Automatic linting and type checking"
echo -e "  4. Instant reload on file changes"
echo ""
echo -e "${PURPLE}Access Points:${NC}"
echo -e "  • Frontend: http://localhost:3000"
echo -e "  • API Docs: http://localhost:8000/docs"
echo -e "  • API: http://localhost:8000"
echo ""
print_success "Ready for 100x accelerated development! 🚀"