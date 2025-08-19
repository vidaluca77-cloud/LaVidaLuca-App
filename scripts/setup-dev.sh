#!/bin/bash

# LaVidaLuca Development Setup Script
# This script sets up the local development environment

set -e

echo "🚀 Setting up LaVidaLuca development environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual configuration values"
fi

# Create necessary directories
mkdir -p logs
mkdir -p data/postgres

echo "🐳 Starting services with Docker Compose..."
cd infra
docker-compose up -d postgres

echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 10

echo "🎯 PostgreSQL is ready!"

# Install backend dependencies (if Python is available)
if command -v python3 &> /dev/null; then
    echo "🐍 Installing backend dependencies..."
    cd ../apps/backend
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    source venv/bin/activate
    pip install -r requirements.txt
    cd ../..
fi

# Install frontend dependencies (if Node.js is available)
if command -v npm &> /dev/null; then
    echo "📦 Installing frontend dependencies..."
    cd apps/frontend
    npm install
    cd ../..
fi

echo "✅ Development environment setup complete!"
echo ""
echo "🔗 Available services:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - PostgreSQL: localhost:5432"
echo "   - pgAdmin: http://localhost:5050 (run with --profile dev)"
echo ""
echo "🚀 To start all services:"
echo "   cd infra && docker-compose up"
echo ""
echo "🔧 To run services individually:"
echo "   Backend: cd apps/backend && source venv/bin/activate && uvicorn main:app --reload"
echo "   Frontend: cd apps/frontend && npm run dev"