"""Test authentication endpoints."""

from fastapi.testclient import TestClient

from src.core.security import get_password_hash
from src.models.user import User, UserRole


def test_register_user(client: TestClient):
    """Test user registration."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User",
            "role": "student"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert data["role"] == "student"


def test_login_user(client: TestClient, db):
    """Test user login."""
    # Create a test user
    hashed_password = get_password_hash("testpassword")
    user = User(
        email="test@example.com",
        hashed_password=hashed_password,
        full_name="Test User",
        role=UserRole.STUDENT
    )
    db.add(user)
    db.commit()
    
    # Test login
    response = client.post(
        "/api/v1/auth/login/json",
        json={
            "email": "test@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    response = client.post(
        "/api/v1/auth/login/json",
        json={
            "email": "invalid@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401