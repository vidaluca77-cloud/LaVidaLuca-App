"""
Test module for the basic FastAPI backend implementation.

Tests the main endpoints and configuration to ensure proper functionality.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns expected information."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "Bienvenue sur l'API La Vida Luca"
    assert data["version"] == "1.0.0"
    assert data["description"] == "API pour l'assistant agricole La Vida Luca"
    assert data["docs"] == "/docs"
    assert data["status"] == "healthy"


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert data["api_version"] == "1.0.0"
    assert data["service"] == "agricultural_assistant"
    
    # Database will be unhealthy without actual DB connection
    assert data["status"] in ["healthy", "degraded"]
    assert data["database"] in ["healthy", "unhealthy"]


def test_docs_endpoint():
    """Test that the documentation endpoint is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_redoc_endpoint():
    """Test that the ReDoc documentation endpoint is accessible."""
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]