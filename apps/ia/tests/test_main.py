"""
Tests for the main application.
"""
import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(test_client: TestClient):
    """Test the root endpoint."""
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Welcome to LaVidaLuca API"


def test_health_check(test_client: TestClient):
    """Test the health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_404_handler(test_client: TestClient):
    """Test custom 404 handler."""
    response = test_client.get("/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data