import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["service"] == "la-vida-luca-ia"


def test_api_status():
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["api"] == "La Vida Luca IA"
    assert data["status"] == "operational"
    assert "endpoints" in data


def test_get_activities():
    response = client.get("/api/v1/activities")
    assert response.status_code == 200
    data = response.json()
    assert "activities" in data
    assert len(data["activities"]) > 0


def test_get_recommendations():
    user_preferences = {
        "skills": ["sol", "plantes"],
        "interests": ["agriculture"],
        "experience_level": 1
    }
    response = client.post("/api/v1/recommendations", json=user_preferences)
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data