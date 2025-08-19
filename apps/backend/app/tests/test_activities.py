import pytest
from fastapi.testclient import TestClient


def test_list_activities(test_client: TestClient):
    """Test GET /api/v1/activities"""
    response = test_client.get("/api/v1/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert "activities" in data
    assert "total" in data
    assert isinstance(data["activities"], list)
    assert data["total"] >= 0


def test_list_activities_with_category_filter(test_client: TestClient):
    """Test GET /api/v1/activities with category filter"""
    response = test_client.get("/api/v1/activities?category=agri")
    assert response.status_code == 200
    
    data = response.json()
    assert "activities" in data
    for activity in data["activities"]:
        assert activity["category"] == "agri"


def test_list_activities_invalid_category(test_client: TestClient):
    """Test GET /api/v1/activities with invalid category"""
    response = test_client.get("/api/v1/activities?category=invalid")
    assert response.status_code == 400


def test_get_activity_by_slug(test_client: TestClient):
    """Test GET /api/v1/activities/{slug}"""
    response = test_client.get("/api/v1/activities/test-activity")
    assert response.status_code == 200
    
    data = response.json()
    assert data["slug"] == "test-activity"
    assert data["title"] == "Test Activity"
    assert data["category"] == "agri"


def test_get_activity_by_slug_not_found(test_client: TestClient):
    """Test GET /api/v1/activities/{slug} with non-existent slug"""
    response = test_client.get("/api/v1/activities/non-existent-slug")
    assert response.status_code == 404


def test_register_for_activity_without_auth(test_client: TestClient):
    """Test POST /api/v1/activities/{id}/register without authentication"""
    response = test_client.post("/api/v1/activities/1/register")
    assert response.status_code == 401