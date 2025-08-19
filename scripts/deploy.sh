#!/bin/bash

# LaVidaLuca Deployment Script for Production
# This script prepares the application for deployment

set -e

echo "🚀 Preparing LaVidaLuca for deployment..."

# Build backend for production
echo "🐍 Building backend..."
cd apps/backend
docker build -t lavidaluca-backend:latest .
echo "✅ Backend built successfully"

# Build frontend for production
echo "⚛️ Building frontend..."
cd ../frontend
npm run build
docker build -t lavidaluca-frontend:latest .
echo "✅ Frontend built successfully"

cd ../..

echo "📋 Deployment checklist:"
echo "  □ Update environment variables in production"
echo "  □ Set up PostgreSQL database (Supabase)"
echo "  □ Configure domain and SSL certificates"
echo "  □ Set up monitoring and logging"
echo "  □ Configure CI/CD pipeline"
echo ""
echo "🔗 Deployment targets:"
echo "  - Frontend: Deploy to Vercel"
echo "  - Backend: Deploy to Render"
echo "  - Database: Supabase PostgreSQL"
echo ""
echo "✅ Build complete! Ready for deployment."