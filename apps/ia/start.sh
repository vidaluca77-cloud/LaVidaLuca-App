#!/bin/bash

# Start script for the FastAPI application
# This script can be used for development or production deployment

echo "Starting La Vida Luca FastAPI Application..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Please copy .env.example to .env and configure your settings."
    exit 1
fi

# Start the application
echo "Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload