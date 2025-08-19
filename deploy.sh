#!/bin/bash

# La Vida Luca - Deployment Script
# This script handles deployment to both Vercel (frontend) and Render (backend)

set -e  # Exit on any error

echo "🚀 Starting La Vida Luca deployment process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Install dependencies
print_status "Installing dependencies..."
npm install
cd apps/web && npm install && cd ../..

# Lint and type check
print_status "Running linting and type checks..."
cd apps/web
npm run lint
cd ../..

# Run tests
print_status "Running tests..."
npm run test

# Build the frontend
print_status "Building frontend..."
cd apps/web
npm run build
cd ../..

print_status "Frontend build successful!"

# Check backend requirements
print_status "Checking backend configuration..."
if [ -f "apps/backend/requirements.txt" ]; then
    print_status "Backend requirements.txt found"
else
    print_error "Backend requirements.txt not found"
    exit 1
fi

if [ -f "apps/backend/render.yaml" ]; then
    print_status "Render configuration found"
else
    print_error "Render configuration not found"
    exit 1
fi

# Deployment instructions
echo ""
print_status "Deployment preparation complete!"
echo ""
echo "📋 Next steps for deployment:"
echo ""
echo "🌐 Frontend (Vercel):"
echo "   1. Connect your GitHub repository to Vercel"
echo "   2. Vercel will automatically use the vercel.json configuration"
echo "   3. Set environment variables in Vercel dashboard if needed"
echo "   4. Deploy: git push to main branch"
echo ""
echo "🔧 Backend (Render):"
echo "   1. Connect your GitHub repository to Render"
echo "   2. Create a new Web Service using apps/backend/render.yaml"
echo "   3. Set the OPENAI_API_KEY in Render dashboard"
echo "   4. Deploy: git push to main branch"
echo ""
echo "🔗 Configure API endpoints:"
echo "   - Update NEXT_PUBLIC_API_URL in Vercel to point to your Render backend"
echo "   - Update CORS_ORIGINS in Render to include your Vercel domain"
echo ""
print_status "All deployment configurations are ready!"