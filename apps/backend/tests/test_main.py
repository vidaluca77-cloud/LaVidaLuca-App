import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "La Vida Luca API" in data["message"]

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "service" in data
    assert data["service"] == "La Vida Luca API"

def test_users_endpoint():
    """Test the users endpoint"""
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_activities_endpoint():
    """Test the activities endpoint"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)