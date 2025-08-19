import pytest
from fastapi.testclient import TestClient

def create_test_user(client: TestClient):
    """Helper function to create a test user and return auth token"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    client.post("/auth/register", json=user_data)
    
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    response = client.post("/auth/login", json=login_data)
    return response.json()["access_token"]

def test_create_activity(client: TestClient):
    # Create superuser first (we'll need to modify the user creation to make them superuser)
    token = create_test_user(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    activity_data = {
        "slug": "test-activity",
        "title": "Test Activity",
        "category": "agri",
        "summary": "A test activity for agriculture",
        "description": "Detailed description of the test activity",
        "duration_min": 90,
        "skill_tags": ["soil", "plants"],
        "seasonality": ["spring", "summer"],
        "safety_level": 1,
        "materials": ["gloves", "boots"]
    }
    
    # This will fail because regular user is not superuser
    response = client.post("/api/activities/", json=activity_data, headers=headers)
    assert response.status_code == 403

def test_get_activities(client: TestClient):
    """Test getting activities list without authentication"""
    response = client.get("/api/activities/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_activities_with_category_filter(client: TestClient):
    """Test filtering activities by category"""
    response = client.get("/api/activities/?category=agri")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, list)

def test_get_activity_not_found(client: TestClient):
    """Test getting non-existent activity"""
    response = client.get("/api/activities/999")
    assert response.status_code == 404

def test_get_activity_by_slug_not_found(client: TestClient):
    """Test getting activity by non-existent slug"""
    response = client.get("/api/activities/slug/non-existent-slug")
    assert response.status_code == 404