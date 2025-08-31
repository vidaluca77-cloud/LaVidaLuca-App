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
    response = client.post("/api/v1/guide", json={"question": test_question})
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
    response = client.post("/api/v1/guide", json={"question": test_question})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "jardinage" in data["answer"].lower() or "plante" in data["answer"].lower()


def test_guide_endpoint_compost_question():
    """Test the guide endpoint with compost question."""
    test_question = "Comment faire du compost ?"
    response = client.post("/api/v1/guide", json={"question": test_question})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "compost" in data["answer"].lower()


def test_guide_endpoint_general_question():
    """Test the guide endpoint with general question."""
    test_question = "Bonjour, que peux-tu faire ?"
    response = client.post("/api/v1/guide", json={"question": test_question})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "jardinage" in data["answer"].lower()


def test_guide_endpoint_invalid_request():
    """Test the guide endpoint with invalid request."""
    response = client.post(
        "/api/v1/guide", json={}  # Missing required 'question' field
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


def test_activities_endpoint():
    """Test the activities endpoint."""
    response = client.get("/api/v1/activities")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "activities" in data["data"]
    assert "total" in data["data"]
    assert "categories" in data["data"]
    assert isinstance(data["data"]["activities"], list)
    assert data["data"]["total"] == 30
    assert len(data["data"]["activities"]) == 30


def test_activities_endpoint_with_search():
    """Test the activities endpoint with search parameter."""
    response = client.get("/api/v1/activities?search=mouton")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    activities = data["data"]["activities"]
    # Should find activities containing "mouton"
    if len(activities) > 0:
        assert any("mouton" in activity["title"].lower() for activity in activities)


def test_activities_endpoint_with_category_filter():
    """Test the activities endpoint with category filter."""
    response = client.get("/api/v1/activities?category=agri")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    activities = data["data"]["activities"]
    # All returned activities should be in the "agri" category
    if len(activities) > 0:
        assert all(activity["category"] == "agri" for activity in activities)


def test_activities_categories_endpoint():
    """Test the activities categories endpoint."""
    response = client.get("/api/v1/activities/categories")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    categories = data["data"]
    expected_categories = ["agri", "transfo", "artisanat", "nature", "social"]
    for cat in expected_categories:
        assert cat in categories
    assert categories["agri"] == "Agriculture"
    assert categories["transfo"] == "Transformation"


def test_contact_endpoint_valid_submission():
    """Test the contact endpoint with valid data."""
    contact_data = {
        "nom": "Jean Dupont",
        "email": "jean@example.com",
        "telephone": "0123456789",
        "typeAide": "Formation",
        "message": "Je souhaite participer aux formations",
    }
    response = client.post("/api/v1/contact", json=contact_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "message" in data
    assert "contact_id" in data


def test_contact_endpoint_missing_required_fields():
    """Test the contact endpoint with missing required fields."""
    contact_data = {
        "nom": "Jean Dupont"
        # Missing email and message (required fields)
    }
    response = client.post("/api/v1/contact", json=contact_data)
    assert response.status_code == 422  # Validation error


def test_contact_health_endpoint():
    """Test the contact health endpoint."""
    response = client.get("/api/v1/contact/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "contact"
