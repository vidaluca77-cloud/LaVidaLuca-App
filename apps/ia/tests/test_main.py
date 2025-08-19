import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestMain:
    """Test main application endpoints."""

    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "environment" in data

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert data["message"] == "LaVidaLuca API"
        assert "version" in data
        assert "docs" in data
        assert "redoc" in data

    def test_docs_accessible(self, client: TestClient):
        """Test that API documentation is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_spec(self, client: TestClient):
        """Test that OpenAPI specification is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "LaVidaLuca API"