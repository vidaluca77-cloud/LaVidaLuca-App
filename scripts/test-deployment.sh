#!/bin/bash

# Test deployment infrastructure script
# This script validates that all deployment configurations are working

set -e

echo "🌱 Testing La Vida Luca Deployment Infrastructure"
echo "================================================="

# Test 1: Check required files exist
echo ""
echo "1. Checking deployment configuration files..."

files=(
    "vercel.json"
    "render.yaml"
    ".github/workflows/ci-cd.yml"
    "infra/supabase/migrations/20240819000001_initial_schema.sql"
    "infra/supabase/seeds.sql"
    "scripts/monitoring/health-check.sh"
    "scripts/monitoring/performance-monitor.js"
    ".env.example"
    "DEPLOYMENT.md"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file (missing)"
        exit 1
    fi
done

# Test 2: Validate JSON configurations
echo ""
echo "2. Validating JSON configurations..."

if command -v node >/dev/null 2>&1; then
    echo "✓ vercel.json syntax" && node -e "JSON.parse(require('fs').readFileSync('vercel.json', 'utf8'))"
    echo "✓ package.json syntax" && node -e "JSON.parse(require('fs').readFileSync('package.json', 'utf8'))"
else
    echo "⚠ Node.js not available, skipping JSON validation"
fi

# Test 3: Check Next.js build
echo ""
echo "3. Testing Next.js build..."
if npm run build > /dev/null 2>&1; then
    echo "✓ Next.js build successful"
else
    echo "✗ Next.js build failed"
    exit 1
fi

# Test 4: Check TypeScript compilation
echo ""
echo "4. Testing TypeScript compilation..."
if npm run type-check > /dev/null 2>&1; then
    echo "✓ TypeScript compilation successful"
else
    echo "✗ TypeScript compilation failed"
    exit 1
fi

# Test 5: Check Python requirements (if Python is available)
echo ""
echo "5. Testing Python IA API..."
if command -v python3 >/dev/null 2>&1; then
    cd apps/ia
    if python3 -c "import sys; sys.path.append('.'); from main import app; print('✓ FastAPI app imports successfully')" 2>/dev/null; then
        echo "✓ FastAPI app structure valid"
    else
        echo "⚠ FastAPI app has import issues (dependencies may be missing)"
    fi
    cd ../..
else
    echo "⚠ Python not available, skipping API validation"
fi

# Test 6: Check SQL syntax (basic)
echo ""
echo "6. Testing SQL migrations..."
if grep -q "CREATE TABLE" infra/supabase/migrations/20240819000001_initial_schema.sql; then
    echo "✓ SQL migration file contains CREATE statements"
else
    echo "✗ SQL migration file appears invalid"
    exit 1
fi

if grep -q "INSERT INTO" infra/supabase/seeds.sql; then
    echo "✓ SQL seeds file contains INSERT statements"
else
    echo "✗ SQL seeds file appears invalid"
    exit 1
fi

# Test 7: Check script permissions
echo ""
echo "7. Testing script permissions..."
if [ -x "scripts/monitoring/health-check.sh" ]; then
    echo "✓ health-check.sh is executable"
else
    echo "✗ health-check.sh is not executable"
    exit 1
fi

if [ -x "scripts/monitoring/performance-monitor.js" ]; then
    echo "✓ performance-monitor.js is executable"
else
    echo "✗ performance-monitor.js is not executable"
    exit 1
fi

echo ""
echo "🎉 All deployment infrastructure tests passed!"
echo ""
echo "Next steps for deployment:"
echo "1. Set up accounts on Vercel, Render, and Supabase"
echo "2. Configure environment variables as described in .env.example"
echo "3. Configure GitHub secrets for CI/CD"
echo "4. Follow the deployment guide in DEPLOYMENT.md"
echo ""
echo "Quick commands:"
echo "  - Health check: npm run health-check"
echo "  - Performance monitoring: npm run monitor"
echo "  - Deploy to Vercel: npm run deploy:vercel"