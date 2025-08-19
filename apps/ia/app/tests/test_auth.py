"""
Tests for authentication endpoints
"""
import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient, db):
    """Test user registration."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpass123",
            "full_name": "New User"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert data["full_name"] == "New User"
    assert data["is_active"] is True
    assert "id" in data


def test_register_duplicate_email(client: TestClient, test_user):
    """Test registration with duplicate email."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",  # Same as test_user
            "username": "newuser",
            "password": "newpass123"
        }
    )
    
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_register_duplicate_username(client: TestClient, test_user):
    """Test registration with duplicate username."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "new@example.com",
            "username": "testuser",  # Same as test_user
            "password": "newpass123"
        }
    )
    
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]


def test_login_success(client: TestClient, test_user):
    """Test successful login."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "testpass"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 1800  # 30 minutes


def test_login_with_email(client: TestClient, test_user):
    """Test login with email instead of username."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "test@example.com", "password": "testpass"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_wrong_password(client: TestClient, test_user):
    """Test login with wrong password."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "wrongpass"}
    )
    
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_nonexistent_user(client: TestClient):
    """Test login with nonexistent user."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "nonexistent", "password": "somepass"}
    )
    
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_register_invalid_email(client: TestClient):
    """Test registration with invalid email."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "not-an-email",
            "username": "testuser",
            "password": "testpass"
        }
    )
    
    assert response.status_code == 422  # Validation error


def test_register_short_password(client: TestClient):
    """Test registration with too short password."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "123"  # Too short
        }
    )
    
    assert response.status_code == 422  # Validation error