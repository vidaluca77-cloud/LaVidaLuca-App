import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "LaVidaLuca API" in response.json()["message"]


def test_health_check(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user(client: TestClient, test_user_data):
    """Test user registration."""
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]
    assert "id" in data
    assert data["is_active"] is True


def test_register_duplicate_user(client: TestClient, test_user_data):
    """Test registering duplicate user fails."""
    # First registration should succeed
    client.post("/api/auth/register", json=test_user_data)
    
    # Second registration should fail
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 400


def test_login_user(client: TestClient, test_user_data):
    """Test user login."""
    # Register user first
    client.post("/api/auth/register", json=test_user_data)
    
    # Login
    login_data = {
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials fails."""
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 401


def test_get_current_user(client: TestClient, test_user_data):
    """Test getting current user information."""
    # Register and login
    client.post("/api/auth/register", json=test_user_data)
    
    login_data = {
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    }
    login_response = client.post("/api/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    
    # Get current user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]


def test_unauthorized_access(client: TestClient):
    """Test accessing protected endpoint without token fails."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401