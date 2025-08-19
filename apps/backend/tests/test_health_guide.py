"""
Test health and guide endpoints.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import create_app


@pytest.fixture
def client():
    """Create test client without database dependency."""
    app = create_app()
    
    # Mock database connection for health endpoint
    async def mock_db_execute(query):
        return True
    
    # We'll override the database dependency in tests that need it
    return TestClient(app)


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to La Vida Luca API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "healthy"


def test_health_endpoint_structure(client):
    """Test the health endpoint returns proper structure."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "environment" in data


def test_guide_endpoint(client):
    """Test the guide endpoint."""
    test_question = "Comment améliorer un sol argileux ?"
    response = client.post(
        "/api/v1/guide",
        json={"question": test_question}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "confidence" in data
    assert "sources" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0


def test_guide_endpoint_different_question(client):
    """Test the guide endpoint with different question."""
    test_question = "Quels sont les meilleurs légumes à planter ?"
    response = client.post(
        "/api/v1/guide",
        json={"question": test_question}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "jardinage" in data["answer"].lower() or "plante" in data["answer"].lower()


def test_guide_endpoint_invalid_request(client):
    """Test the guide endpoint with invalid request."""
    response = client.post(
        "/api/v1/guide",
        json={}  # Missing required 'question' field
    )
    assert response.status_code == 422  # Validation error


def test_guide_health_endpoint(client):
    """Test the guide health endpoint."""
    response = client.get("/api/v1/guide/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "guide"
    assert "ai_enabled" in data