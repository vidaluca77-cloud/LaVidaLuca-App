import pytest
from fastapi.testclient import TestClient
from app.core.auth import create_access_token


def test_get_current_user_without_auth(test_client: TestClient):
    """Test GET /api/v1/users/me without authentication"""
    response = test_client.get("/api/v1/users/me")
    assert response.status_code == 401


def test_get_current_user_with_auth(test_client: TestClient):
    """Test GET /api/v1/users/me with authentication"""
    # Create token for test user
    token = create_access_token(data={"sub": "test@example.com"})
    headers = {"Authorization": f"Bearer {token}"}
    
    response = test_client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "elevage" in data["skills"]
    assert "weekend" in data["availability"]


def test_update_user_profile(test_client: TestClient):
    """Test PUT /api/v1/users/me"""
    # Create token for test user
    token = create_access_token(data={"sub": "test@example.com"})
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {
        "full_name": "Updated Test User",
        "skills": ["elevage", "soil", "creativite"],
        "location": "Updated Location"
    }
    
    response = test_client.put("/api/v1/users/me", json=update_data, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["full_name"] == "Updated Test User"
    assert "creativite" in data["skills"]
    assert data["location"] == "Updated Location"


def test_get_user_activities(test_client: TestClient):
    """Test GET /api/v1/users/me/activities"""
    # Create token for test user
    token = create_access_token(data={"sub": "test@example.com"})
    headers = {"Authorization": f"Bearer {token}"}
    
    response = test_client.get("/api/v1/users/me/activities", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "activities" in data
    assert "total" in data
    assert isinstance(data["activities"], list)


def test_update_user_profile_without_auth(test_client: TestClient):
    """Test PUT /api/v1/users/me without authentication"""
    update_data = {"full_name": "Should Not Work"}
    
    response = test_client.put("/api/v1/users/me", json=update_data)
    assert response.status_code == 401