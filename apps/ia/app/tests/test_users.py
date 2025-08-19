"""
Tests for user and profile endpoints
"""
import pytest
from fastapi.testclient import TestClient


def test_get_current_user(client: TestClient, test_user, auth_headers):
    """Test getting current user info."""
    response = client.get("/api/v1/users/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert data["full_name"] == "Test User"


def test_get_current_user_unauthorized(client: TestClient):
    """Test getting current user without authentication."""
    response = client.get("/api/v1/users/me")
    
    assert response.status_code == 401


def test_update_current_user(client: TestClient, test_user, auth_headers):
    """Test updating current user info."""
    response = client.put(
        "/api/v1/users/me",
        headers=auth_headers,
        json={"full_name": "Updated Name"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"


def test_create_user_profile(client: TestClient, test_user, auth_headers):
    """Test creating a user profile."""
    profile_data = {
        "skills": ["elevage", "hygiene"],
        "preferences": ["agri", "transfo"],
        "availability": ["weekend", "semaine"],
        "location": "Test Location",
        "experience_level": "debutant",
        "bio": "Test bio"
    }
    
    response = client.post(
        "/api/v1/users/me/profile",
        headers=auth_headers,
        json=profile_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["skills"] == ["elevage", "hygiene"]
    assert data["preferences"] == ["agri", "transfo"]
    assert data["location"] == "Test Location"
    assert data["experience_level"] == "debutant"
    assert data["user_id"] == test_user.id


def test_get_user_profile(client: TestClient, test_user_profile, auth_headers):
    """Test getting user profile."""
    response = client.get("/api/v1/users/me/profile", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["skills"] == ["elevage", "hygiene"]
    assert data["preferences"] == ["agri", "transfo"]
    assert data["location"] == "Test Location"


def test_get_profile_not_found(client: TestClient, test_user, auth_headers):
    """Test getting profile that doesn't exist."""
    response = client.get("/api/v1/users/me/profile", headers=auth_headers)
    
    assert response.status_code == 404
    assert "Profile not found" in response.json()["detail"]


def test_update_user_profile(client: TestClient, test_user_profile, auth_headers):
    """Test updating user profile."""
    update_data = {
        "skills": ["elevage", "hygiene", "organization"],
        "experience_level": "intermediaire"
    }
    
    response = client.put(
        "/api/v1/users/me/profile",
        headers=auth_headers,
        json=update_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["skills"]) == 3
    assert "organization" in data["skills"]
    assert data["experience_level"] == "intermediaire"


def test_delete_user_profile(client: TestClient, test_user_profile, auth_headers):
    """Test deleting user profile."""
    response = client.delete("/api/v1/users/me/profile", headers=auth_headers)
    
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    
    # Verify profile is deleted
    get_response = client.get("/api/v1/users/me/profile", headers=auth_headers)
    assert get_response.status_code == 404


def test_create_duplicate_profile(client: TestClient, test_user_profile, auth_headers):
    """Test creating profile when one already exists."""
    profile_data = {
        "skills": ["new_skill"],
        "preferences": ["agri"],
        "availability": ["weekend"]
    }
    
    response = client.post(
        "/api/v1/users/me/profile",
        headers=auth_headers,
        json=profile_data
    )
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]