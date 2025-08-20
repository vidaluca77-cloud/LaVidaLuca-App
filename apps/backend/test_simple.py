"""
Test health and guide endpoints for the simple app.
"""

import pytest
from fastapi.testclient import TestClient
from app_simple import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to La Vida Luca API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "healthy"


def test_health_endpoint():
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert "environment" in data


def test_guide_endpoint_soil_question():
    """Test the guide endpoint with soil question."""
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
    assert "sol" in data["answer"].lower() or "argileux" in data["answer"].lower()


def test_guide_endpoint_gardening_question():
    """Test the guide endpoint with gardening question."""
    test_question = "Quels sont les meilleurs légumes à planter ?"
    response = client.post(
        "/api/v1/guide",
        json={"question": test_question}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "jardinage" in data["answer"].lower() or "plante" in data["answer"].lower()


def test_guide_endpoint_compost_question():
    """Test the guide endpoint with compost question."""
    test_question = "Comment faire du compost ?"
    response = client.post(
        "/api/v1/guide",
        json={"question": test_question}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "compost" in data["answer"].lower()


def test_guide_endpoint_general_question():
    """Test the guide endpoint with general question."""
    test_question = "Bonjour, que peux-tu faire ?"
    response = client.post(
        "/api/v1/guide",
        json={"question": test_question}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "jardinage" in data["answer"].lower()


def test_guide_endpoint_invalid_request():
    """Test the guide endpoint with invalid request."""
    response = client.post(
        "/api/v1/guide",
        json={}  # Missing required 'question' field
    )
    assert response.status_code == 422  # Validation error


def test_guide_health_endpoint():
    """Test the guide health endpoint."""
    response = client.get("/api/v1/guide/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "guide"
    assert "ai_enabled" in data