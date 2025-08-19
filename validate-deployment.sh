#!/usr/bin/env bash

# Deployment Configuration Validation Script
set -e

echo "🚀 Validating La Vida Luca Deployment Configuration"
echo "=================================================="

# Test frontend build
echo "📦 Testing frontend build..."
cd apps/web
npm run build
echo "✅ Frontend build successful!"
cd ../..

# Validate configuration files
echo "🔍 Validating configuration files..."

if [ -f "vercel.json" ]; then
    echo "✅ vercel.json exists"
    # Basic JSON validation
    python -c "import json; json.load(open('vercel.json'))" && echo "✅ vercel.json is valid JSON"
else
    echo "❌ vercel.json not found"
    exit 1
fi

if [ -f "render.yaml" ]; then
    echo "✅ render.yaml exists"
    # Basic YAML validation using Python
    python -c "import yaml; yaml.safe_load(open('render.yaml'))" && echo "✅ render.yaml is valid YAML"
else
    echo "❌ render.yaml not found"
    exit 1
fi

# Test package.json scripts
echo "🧪 Testing package.json scripts..."
if npm run | grep -q "web:build"; then
    echo "✅ web:build script available"
else
    echo "❌ web:build script missing"
    exit 1
fi

if npm run | grep -q "backend:prod"; then
    echo "✅ backend:prod script available"
else
    echo "❌ backend:prod script missing"
    exit 1
fi

# Test backend dependencies
echo "🐍 Testing backend dependencies..."
cd apps/backend
python -c "from config import settings; print('✅ Backend config loads successfully')"
cd ../..

echo ""
echo "🎉 All deployment configurations validated successfully!"
echo ""
echo "Next steps:"
echo "1. Set up environment variables as described in DEPLOYMENT.md"
echo "2. Deploy frontend to Vercel: npm run deploy:vercel"
echo "3. Deploy backend to Render: Connect repository and push to main"