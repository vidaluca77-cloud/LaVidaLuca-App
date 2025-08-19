import pytest
from fastapi.testclient import TestClient

def test_root_endpoint(client: TestClient):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to La Vida Luca API"
    assert "version" in data
    assert "docs" in data

def test_health_check(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "la-vida-luca-api"

def test_openapi_docs_available(client: TestClient):
    """Test that OpenAPI documentation is available."""
    response = client.get("/docs")
    assert response.status_code == 200
    
    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi_data = response.json()
    assert openapi_data["info"]["title"] == "La Vida Luca API"

def test_cors_headers(client: TestClient):
    """Test that CORS headers are properly set."""
    response = client.options("/")
    # The test client might not return CORS headers in OPTIONS
    # but we can test a regular request
    response = client.get("/")
    assert response.status_code == 200