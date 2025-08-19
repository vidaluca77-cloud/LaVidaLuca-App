#!/bin/bash

# Deployment script for La Vida Luca application
# This script deploys the frontend to Vercel and backend to Render

set -e

echo "🚀 Starting La Vida Luca deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed"
        exit 1
    fi
    
    if ! command -v vercel &> /dev/null; then
        print_warning "Vercel CLI not found. Install with: npm i -g vercel"
    fi
    
    if ! command -v git &> /dev/null; then
        print_error "git is not installed"
        exit 1
    fi
}

# Build and test frontend
deploy_frontend() {
    print_status "Building and testing frontend..."
    
    cd apps/web
    
    # Install dependencies
    npm install
    
    # Build the application
    npm run build
    
    # Deploy to Vercel if CLI is available
    if command -v vercel &> /dev/null; then
        print_status "Deploying frontend to Vercel..."
        vercel --prod
    else
        print_warning "Vercel CLI not found. Please deploy manually or install CLI."
        print_status "Build completed. Upload 'out' directory to your hosting provider."
    fi
    
    cd ../..
}

# Deploy backend
deploy_backend() {
    print_status "Preparing backend deployment..."
    
    cd apps/ia
    
    # Check if virtual environment exists
    if [ ! -d ".venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv .venv
    fi
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Run tests
    print_status "Running backend tests..."
    python -m pytest tests/ -v
    
    print_status "Backend is ready for deployment to Render."
    print_warning "Please configure Render with the following:"
    echo "  - Build Command: pip install -r requirements.txt"
    echo "  - Start Command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
    echo "  - Environment: Python 3.11+"
    
    cd ../..
}

# Setup database
setup_database() {
    print_status "Database setup instructions:"
    print_warning "Please manually execute the following in your Supabase dashboard:"
    echo "  1. Create a new Supabase project"
    echo "  2. Execute infra/supabase/schema.sql in the SQL editor"
    echo "  3. Execute infra/supabase/seeds.sql in the SQL editor"
    echo "  4. Configure the environment variables with your database URL"
}

# Main deployment flow
main() {
    print_status "La Vida Luca Deployment Script"
    echo "======================================"
    
    check_dependencies
    
    # Ask what to deploy
    echo ""
    echo "What would you like to deploy?"
    echo "1) Frontend only"
    echo "2) Backend only"  
    echo "3) Full application"
    echo "4) Database setup info"
    echo ""
    read -p "Choose option (1-4): " choice
    
    case $choice in
        1)
            deploy_frontend
            ;;
        2)
            deploy_backend
            ;;
        3)
            deploy_frontend
            deploy_backend
            setup_database
            ;;
        4)
            setup_database
            ;;
        *)
            print_error "Invalid option selected"
            exit 1
            ;;
    esac
    
    print_status "Deployment process completed!"
    echo ""
    print_warning "Don't forget to configure your environment variables:"
    echo "Frontend (.env.local):"
    echo "  NEXT_PUBLIC_SUPABASE_URL=your_supabase_url"
    echo "  NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key"
    echo "  NEXT_PUBLIC_IA_API_URL=your_render_api_url"
    echo ""
    echo "Backend (.env):"
    echo "  DATABASE_URL=your_supabase_database_url"
    echo "  SECRET_KEY=your_secret_key"
    echo "  ALLOWED_ORIGINS=your_frontend_domains"
}

# Run main function
main "$@"