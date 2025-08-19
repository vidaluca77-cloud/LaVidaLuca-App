import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.models import User


class TestAuth:
    """Test authentication endpoints."""

    def test_register_user_success(self, client: TestClient, test_user_data):
        """Test successful user registration."""
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert "id" in data
        assert data["email"] == test_user_data["email"]
        assert data["first_name"] == test_user_data["first_name"]
        assert data["last_name"] == test_user_data["last_name"]
        assert data["role"] == test_user_data["role"]
        assert data["is_active"] is True
        assert data["is_verified"] is False
        # Password should not be returned
        assert "password" not in data
        assert "hashed_password" not in data

    def test_register_user_duplicate_email(self, client: TestClient, test_user_data):
        """Test registration with duplicate email."""
        # Register first user
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Try to register again with same email
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_register_user_invalid_email(self, client: TestClient, test_user_data):
        """Test registration with invalid email."""
        test_user_data["email"] = "invalid-email"
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 422

    def test_register_user_weak_password(self, client: TestClient, test_user_data):
        """Test registration with weak password."""
        test_user_data["password"] = "weak"
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 422

    def test_login_success(self, client: TestClient, test_user_data):
        """Test successful login."""
        # Register user first
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Login
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client: TestClient, test_user_data):
        """Test login with invalid credentials."""
        # Register user first
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Login with wrong password
        login_data = {
            "email": test_user_data["email"],
            "password": "wrongpassword"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with non-existent user."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "password123"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_form_success(self, client: TestClient, test_user_data):
        """Test successful login with form data."""
        # Register user first
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Login with form data
        form_data = {
            "username": test_user_data["email"],  # OAuth2 uses 'username' field
            "password": test_user_data["password"]
        }
        response = client.post("/api/v1/auth/login/form", data=form_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"


def get_auth_headers(client: TestClient, test_user_data) -> dict:
    """Helper function to get authentication headers."""
    # Register user
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Login
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}