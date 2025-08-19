"""
Test authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient, sample_user_data):
    """Test user registration."""
    response = client.post("/api/v1/auth/register", json=sample_user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user" in data
    assert data["user"]["email"] == sample_user_data["email"]
    assert data["user"]["role"] == "student"


def test_register_duplicate_email(client: TestClient, sample_user_data):
    """Test registration with duplicate email fails."""
    # Register first user
    response = client.post("/api/v1/auth/register", json=sample_user_data)
    assert response.status_code == 200
    
    # Try to register again with same email
    response = client.post("/api/v1/auth/register", json=sample_user_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_register_password_mismatch(client: TestClient, sample_user_data):
    """Test registration with mismatched passwords fails."""
    user_data = sample_user_data.copy()
    user_data["confirm_password"] = "differentpassword"
    
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400
    assert "Passwords do not match" in response.json()["detail"]


def test_login_success(client: TestClient, sample_user_data):
    """Test successful login."""
    # Register user first
    client.post("/api/v1/auth/register", json=sample_user_data)
    
    # Login
    login_data = {
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user" in data


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials fails."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_get_current_user(client: TestClient, auth_headers):
    """Test getting current user information."""
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "role" in data
    assert "id" in data


def test_get_current_user_unauthorized(client: TestClient):
    """Test getting current user without token fails."""
    response = client.get("/api/v1/auth/me")
    
    assert response.status_code == 401


def test_change_password(client: TestClient, auth_headers, sample_user_data):
    """Test password change."""
    password_data = {
        "current_password": sample_user_data["password"],
        "new_password": "newpassword123",
        "confirm_password": "newpassword123"
    }
    
    response = client.post("/api/v1/auth/change-password", json=password_data, headers=auth_headers)
    assert response.status_code == 200
    
    # Test login with new password
    login_data = {
        "email": sample_user_data["email"],
        "password": "newpassword123"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200


def test_change_password_wrong_current(client: TestClient, auth_headers):
    """Test password change with wrong current password fails."""
    password_data = {
        "current_password": "wrongpassword",
        "new_password": "newpassword123",
        "confirm_password": "newpassword123"
    }
    
    response = client.post("/api/v1/auth/change-password", json=password_data, headers=auth_headers)
    assert response.status_code == 400
    assert "Incorrect current password" in response.json()["detail"]