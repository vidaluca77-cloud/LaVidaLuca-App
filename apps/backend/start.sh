#!/bin/bash

# Render.com deployment script for LaVidaLuca Backend
# This script is executed when deploying to Render

echo "Starting LaVidaLuca Backend deployment..."

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run database migrations if needed (when using Alembic)
# echo "Running database migrations..."
# alembic upgrade head

echo "Starting FastAPI server..."
# Use gunicorn for production deployment
if [ "$DEBUG" = "true" ]; then
    echo "Starting development server..."
    uvicorn main:app --host 0.0.0.0 --port $PORT --reload
else
    echo "Starting production server..."
    # Install gunicorn for production
    pip install gunicorn
    gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
fi