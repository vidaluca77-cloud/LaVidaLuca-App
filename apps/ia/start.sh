#!/bin/bash

# LaVidaLuca API Startup Script

echo "Starting LaVidaLuca API..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "Please edit .env with your configuration before running again."
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations if using Alembic
if [ "$1" == "--migrate" ]; then
    echo "Running database migrations..."
    alembic upgrade head
fi

# Seed database if requested
if [ "$1" == "--seed" ]; then
    echo "Seeding database..."
    python app/db/seed_data.py
fi

echo "Starting API server..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload