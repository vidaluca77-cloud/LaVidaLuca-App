"""
Simple test to verify FastAPI setup works without database connection.
"""
from fastapi import FastAPI
from fastapi.testclient import TestClient
import sys
import os

# Add the app directory to the path
sys.path.append('/home/runner/work/LaVidaLuca-App/LaVidaLuca-App/apps/api')

# Override database URL to use SQLite for testing
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'

try:
    # Import and test the basic FastAPI setup
    from main import app
    client = TestClient(app)
    
    # Test basic endpoints
    print("Testing FastAPI setup...")
    
    # Test root endpoint
    response = client.get("/")
    print(f"Root endpoint: {response.status_code} - {response.json()}")
    
    # Test health endpoint
    response = client.get("/health")
    print(f"Health endpoint: {response.status_code} - {response.json()}")
    
    # Test API docs endpoint
    response = client.get("/docs")
    print(f"API docs endpoint: {response.status_code}")
    
    print("\n✅ FastAPI backend setup is working correctly!")
    
except Exception as e:
    print(f"❌ Error in FastAPI setup: {str(e)}")
    import traceback
    traceback.print_exc()