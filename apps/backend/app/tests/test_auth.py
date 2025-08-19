import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.models import User
from app.core.security import get_password_hash, verify_password, create_access_token


def test_register_user(client: TestClient):
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword",
        "full_name": "Test User"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data


def test_register_duplicate_user(client: TestClient):
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword"
    }
    # Register first user
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    
    # Try to register same user again
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_user(client: TestClient, db_session: Session):
    # Create a user first
    password = "testpassword"
    hashed_password = get_password_hash(password)
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=hashed_password,
        full_name="Test User"
    )
    db_session.add(user)
    db_session.commit()
    
    # Test login
    login_data = {
        "username": "testuser",
        "password": password
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_password_hashing():
    password = "testpassword"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_create_access_token():
    user_id = 1
    token = create_access_token(subject=user_id)
    assert token is not None
    assert len(token) > 0