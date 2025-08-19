import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "LaVidaLuca API"
    assert data["version"] == "1.0.0"
    assert "docs" in data


def test_health_check(client: TestClient):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_register_user(client: TestClient, test_user_data):
    """Test user registration"""
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert "token" in data
    assert data["user"]["email"] == test_user_data["email"]
    assert data["user"]["username"] == test_user_data["username"]
    assert "access_token" in data["token"]
    assert "refresh_token" in data["token"]


def test_register_duplicate_user(client: TestClient, test_user_data):
    """Test registering duplicate user"""
    # Register first user
    client.post("/api/auth/register", json=test_user_data)
    
    # Try to register same user again
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_user(client: TestClient, test_user_data):
    """Test user login"""
    # Register user first
    client.post("/api/auth/register", json=test_user_data)
    
    # Login
    login_data = {
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials"""
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_get_current_user(client: TestClient, test_user_data):
    """Test getting current user info"""
    # Register and login
    register_response = client.post("/api/auth/register", json=test_user_data)
    token = register_response.json()["token"]["access_token"]
    
    # Get current user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]


def test_get_current_user_unauthorized(client: TestClient):
    """Test getting current user without token"""
    response = client.get("/api/auth/me")
    assert response.status_code == 403