import pytest

class TestAuthEndpoints:
    def test_register_user(self, client):
        """Test user registration endpoint."""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert "id" in data

    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email."""
        user_data = {
            "email": "test@example.com",  # Same as test_user
            "username": "differentuser",
            "password": "password123"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_login_success(self, client, test_user):
        """Test successful login."""
        login_data = {
            "username_or_email": "testuser",
            "password": "testpassword123"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_with_email(self, client, test_user):
        """Test login with email instead of username."""
        login_data = {
            "username_or_email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_login_invalid_credentials(self, client, test_user):
        """Test login with invalid credentials."""
        login_data = {
            "username_or_email": "testuser",
            "password": "wrongpassword"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "Incorrect username/email or password" in response.json()["detail"]

    def test_refresh_token(self, client, test_user):
        """Test token refresh."""
        # First login to get tokens
        login_data = {
            "username_or_email": "testuser",
            "password": "testpassword123"
        }
        
        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        refresh_token = login_response.json()["refresh_token"]
        
        # Use refresh token to get new tokens
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data