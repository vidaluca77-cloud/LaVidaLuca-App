#!/bin/bash

# Exit on any error
set -e

echo "Starting LaVidaLuca Backend deployment..."

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application
echo "Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}