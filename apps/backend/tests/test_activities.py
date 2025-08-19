import pytest
from fastapi.testclient import TestClient


def test_get_activities(client: TestClient):
    """Test getting activities list"""
    response = client.get("/api/activities/")
    assert response.status_code == 200
    data = response.json()
    assert "activities" in data
    assert "total" in data
    assert "page" in data
    assert "per_page" in data


def test_get_activities_with_filters(client: TestClient):
    """Test getting activities with filters"""
    response = client.get("/api/activities/?category=agri&search=test")
    assert response.status_code == 200
    data = response.json()
    assert "activities" in data


def test_get_activity_not_found(client: TestClient):
    """Test getting non-existent activity"""
    response = client.get("/api/activities/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_get_activity_by_slug_not_found(client: TestClient):
    """Test getting activity by non-existent slug"""
    response = client.get("/api/activities/slug/non-existent")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_activity_matching(client: TestClient):
    """Test activity matching endpoint"""
    user_profile = {
        "skills": ["elevage", "hygiene"],
        "availability": ["weekend"],
        "location": "Paris",
        "preferences": ["agri"]
    }
    
    matching_request = {"user_profile": user_profile}
    response = client.post("/api/activities/match", json=matching_request)
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert "user_profile" in data


def test_get_safety_guide_not_found(client: TestClient):
    """Test getting safety guide for non-existent activity"""
    response = client.get("/api/activities/999/safety-guide")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def create_authenticated_user(client: TestClient, test_user_data, is_superuser=False):
    """Helper function to create and authenticate a user"""
    if is_superuser:
        test_user_data["username"] = "admin"
        test_user_data["email"] = "admin@example.com"
    
    # Register user
    register_response = client.post("/api/auth/register", json=test_user_data)
    token = register_response.json()["token"]["access_token"]
    
    # Make user superuser if needed (simulate database update)
    if is_superuser:
        # This would normally require database access, but for testing we'll skip actual promotion
        pass
    
    return token


def test_create_activity_unauthorized(client: TestClient, test_activity_data):
    """Test creating activity without admin permissions"""
    response = client.post("/api/activities/", json=test_activity_data)
    assert response.status_code == 403


def test_update_activity_unauthorized(client: TestClient, test_user_data):
    """Test updating activity without admin permissions"""
    token = create_authenticated_user(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {"title": "Updated Title"}
    response = client.put("/api/activities/1", json=update_data, headers=headers)
    assert response.status_code == 403


def test_delete_activity_unauthorized(client: TestClient, test_user_data):
    """Test deleting activity without admin permissions"""
    token = create_authenticated_user(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.delete("/api/activities/1", headers=headers)
    assert response.status_code == 403