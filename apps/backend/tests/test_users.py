"""
User API tests.
"""
import pytest
from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    """Test user creation."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User",
        "skills": ["agriculture", "animals"],
        "availability": ["weekend", "afternoon"],
        "preferences": ["outdoor"]
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data
    assert "hashed_password" not in data  # Password should not be returned


def test_create_duplicate_user(client: TestClient):
    """Test creating user with duplicate email/username."""
    user_data = {
        "email": "duplicate@example.com",
        "username": "duplicate",
        "password": "testpass123"
    }
    
    # Create first user
    response1 = client.post("/api/v1/users/", json=user_data)
    assert response1.status_code == 200
    
    # Try to create duplicate
    response2 = client.post("/api/v1/users/", json=user_data)
    assert response2.status_code == 400


def test_get_user_profile(client: TestClient):
    """Test getting public user profile."""
    # First create a user
    user_data = {
        "email": "profile@example.com",
        "username": "profileuser",
        "password": "testpass123",
        "first_name": "Profile",
        "last_name": "User"
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    
    # Get profile
    response = client.get("/api/v1/users/profile/profileuser")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "profileuser"
    assert data["first_name"] == "Profile"
    assert "email" not in data  # Email should not be in public profile


def test_get_nonexistent_user_profile(client: TestClient):
    """Test getting profile for non-existent user."""
    response = client.get("/api/v1/users/profile/nonexistent")
    assert response.status_code == 404