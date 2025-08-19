"""
Test authentication endpoints
"""

import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "full_name": "New User",
            "password": "newpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data


def test_register_duplicate_user(client: TestClient, test_user):
    """Test registration with duplicate email/username"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": test_user.email,
            "username": "different",
            "full_name": "Different User",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_login_success(client: TestClient, test_user):
    """Test successful login"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": test_user.username, "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient, test_user):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": test_user.username, "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_nonexistent_user(client: TestClient):
    """Test login with nonexistent user"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "nonexistent", "password": "password"}
    )
    assert response.status_code == 401