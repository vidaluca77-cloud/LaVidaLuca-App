import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    """Test user registration."""
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpass123",
            "full_name": "New User",
            "skills": ["agriculture"],
            "availability": ["weekend"],
            "preferences": ["agri"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data


def test_login_user(client: TestClient, test_user):
    """Test user login."""
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    response = client.post(
        "/auth/login",
        json={"username": "nonexistent", "password": "wrongpass"}
    )
    assert response.status_code == 401


def test_register_duplicate_user(client: TestClient, test_user):
    """Test registration with duplicate email/username."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "newpass123"
        }
    )
    assert response.status_code == 400