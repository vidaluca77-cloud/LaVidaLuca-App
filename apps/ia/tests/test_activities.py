"""
Test activities endpoints
"""
import pytest
from fastapi.testclient import TestClient

def get_auth_headers(client: TestClient, test_user_data):
    """Helper to get authentication headers"""
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post("/api/v1/auth/login", json={
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    })
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_activities(client: TestClient):
    """Test getting activities list"""
    response = client.get("/api/v1/activities/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data

def test_create_activity(client: TestClient, test_user_data, test_activity_data):
    """Test creating a new activity"""
    headers = get_auth_headers(client, test_user_data)
    
    response = client.post(
        "/api/v1/activities/",
        json=test_activity_data,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "activity_id" in data["data"]

def test_get_activity_by_id(client: TestClient, test_user_data, test_activity_data):
    """Test getting activity by ID"""
    headers = get_auth_headers(client, test_user_data)
    
    # Create activity first
    create_response = client.post(
        "/api/v1/activities/",
        json=test_activity_data,
        headers=headers
    )
    activity_id = create_response.json()["data"]["activity_id"]
    
    # Get activity
    response = client.get(f"/api/v1/activities/{activity_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_activity_data["title"]
    assert data["slug"] == test_activity_data["slug"]

def test_get_activity_by_slug(client: TestClient, test_user_data, test_activity_data):
    """Test getting activity by slug"""
    headers = get_auth_headers(client, test_user_data)
    
    # Create activity first
    client.post(
        "/api/v1/activities/",
        json=test_activity_data,
        headers=headers
    )
    
    # Get activity by slug
    response = client.get(f"/api/v1/activities/slug/{test_activity_data['slug']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_activity_data["title"]

def test_get_nonexistent_activity(client: TestClient):
    """Test getting non-existent activity"""
    response = client.get("/api/v1/activities/99999")
    assert response.status_code == 404

def test_get_activity_categories(client: TestClient):
    """Test getting activity categories"""
    response = client.get("/api/v1/activities/categories/list")
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)
    assert "agri" in categories
    assert "transfo" in categories