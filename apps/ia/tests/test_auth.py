import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

def test_register_user_success(client: TestClient, test_user_data):
    """Test successful user registration."""
    with patch('app.routers.auth.get_supabase_admin_client') as mock_supabase:
        # Mock no existing user
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
        
        # Mock successful insert
        mock_insert_response = MagicMock()
        mock_insert_response.data = [{
            "id": "test-user-id",
            "email": test_user_data["email"],
            "full_name": test_user_data["full_name"],
            "profile": test_user_data["profile"],
            "is_active": True,
            "created_at": "2024-01-01T00:00:00"
        }]
        mock_supabase.return_value.table.return_value.insert.return_value.execute.return_value = mock_insert_response
        
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["full_name"] == test_user_data["full_name"]

def test_register_user_duplicate_email(client: TestClient, test_user_data):
    """Test registration with duplicate email."""
    with patch('app.routers.auth.get_supabase_admin_client') as mock_supabase:
        # Mock existing user
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{"id": "existing-id"}]
        
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

def test_login_success(client: TestClient):
    """Test successful login."""
    login_data = {"email": "test@example.com", "password": "testpass"}
    
    with patch('app.routers.auth.authenticate_user') as mock_auth:
        # Mock successful authentication
        mock_user = MagicMock()
        mock_user.id = "test-user-id"
        mock_auth.return_value = mock_user
        
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    login_data = {"email": "test@example.com", "password": "wrongpass"}
    
    with patch('app.routers.auth.authenticate_user') as mock_auth:
        # Mock failed authentication
        mock_auth.return_value = None
        
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

def test_get_current_user(client: TestClient):
    """Test getting current user information."""
    with patch('app.routers.auth.get_current_active_user') as mock_get_user:
        # Mock current user
        mock_user = MagicMock()
        mock_user.id = "test-user-id"
        mock_user.email = "test@example.com"
        mock_user.full_name = "Test User"
        mock_user.dict.return_value = {
            "id": "test-user-id",
            "email": "test@example.com",
            "full_name": "Test User",
            "is_active": True
        }
        mock_get_user.return_value = mock_user
        
        headers = {"Authorization": "Bearer test-token"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 200

def test_logout(client: TestClient):
    """Test logout endpoint."""
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    assert "Successfully logged out" in response.json()["message"]