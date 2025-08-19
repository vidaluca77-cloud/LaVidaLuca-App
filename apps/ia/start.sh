#!/bin/bash

# LaVidaLuca API Startup Script

set -e

echo "🚀 Starting LaVidaLuca API..."

# Check if environment file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration"
fi

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "🐍 Activating virtual environment..."
    source .venv/bin/activate
fi

# Install dependencies if they don't exist
if [ ! -d ".venv" ] || [ ! -f ".venv/pyvenv.cfg" ]; then
    echo "📦 Installing dependencies..."
    python -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Load environment variables
export $(cat .env | grep -v '#' | awk '/=/ {print $1}')

# Run database migrations if DATABASE_URL is set
if [ ! -z "$DATABASE_URL" ]; then
    echo "🗃️  Running database migrations..."
    alembic upgrade head
else
    echo "⚠️  DATABASE_URL not set. Skipping migrations."
fi

# Start the server
echo "🌟 Starting server on http://0.0.0.0:8000"
echo "📚 API Documentation available at http://0.0.0.0:8000/docs"

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload