import pytest
from fastapi import status

class TestAuthEndpoints:
    """Integration tests for authentication endpoints"""
    
    def test_register_user_success(self, client, test_user_data):
        """Test successful user registration"""
        response = client.post("/api/v1/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == test_user_data["username"]
        assert data["email"] == test_user_data["email"]
        assert data["full_name"] == test_user_data["full_name"]
        assert "id" in data
        assert "created_at" in data
        assert "password" not in data  # Password should not be returned
    
    def test_register_user_duplicate_username(self, client, test_user_data):
        """Test registration with duplicate username"""
        # Register first user
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Try to register with same username
        duplicate_data = test_user_data.copy()
        duplicate_data["email"] = "different@example.com"
        
        response = client.post("/api/v1/auth/register", json=duplicate_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "existe déjà" in response.json()["detail"]
    
    def test_register_user_duplicate_email(self, client, test_user_data):
        """Test registration with duplicate email"""
        # Register first user
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Try to register with same email
        duplicate_data = test_user_data.copy()
        duplicate_data["username"] = "differentuser"
        
        response = client.post("/api/v1/auth/register", json=duplicate_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "existe déjà" in response.json()["detail"]
    
    def test_login_success(self, client, test_user_data):
        """Test successful login"""
        # Register user first
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Login
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
    
    def test_login_invalid_username(self, client, test_user_data):
        """Test login with invalid username"""
        login_data = {
            "username": "nonexistent",
            "password": test_user_data["password"]
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "incorrect" in response.json()["detail"]
    
    def test_login_invalid_password(self, client, test_user_data):
        """Test login with invalid password"""
        # Register user first
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Login with wrong password
        login_data = {
            "username": test_user_data["username"],
            "password": "wrongpassword"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "incorrect" in response.json()["detail"]
    
    def test_get_current_user(self, authenticated_client, test_user_data):
        """Test getting current user information"""
        response = authenticated_client.get("/api/v1/auth/me")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == test_user_data["username"]
        assert data["email"] == test_user_data["email"]
    
    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without authentication"""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_refresh_token(self, authenticated_client):
        """Test token refresh"""
        response = authenticated_client.post("/api/v1/auth/refresh")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data

class TestActivitiesEndpoints:
    """Integration tests for activities endpoints"""
    
    def test_get_activities_empty(self, client):
        """Test getting activities when none exist"""
        response = client.get("/api/v1/activities/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_get_activity_not_found(self, client):
        """Test getting non-existent activity"""
        response = client.get("/api/v1/activities/nonexistent")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "non trouvée" in response.json()["detail"]
    
    def test_create_activity_unauthorized(self, client):
        """Test creating activity without authentication"""
        activity_data = {
            "slug": "test-activity",
            "title": "Test Activity",
            "category": "agri",
            "summary": "Test summary",
            "duration_min": 60,
            "skill_tags": ["test"],
            "seasonality": ["toutes"],
            "safety_level": 1,
            "materials": []
        }
        
        response = client.post("/api/v1/activities/", json=activity_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_activity_success(self, authenticated_client):
        """Test successful activity creation"""
        activity_data = {
            "slug": "test-activity",
            "title": "Test Activity",
            "category": "agri",
            "summary": "Test summary",
            "duration_min": 60,
            "skill_tags": ["test"],
            "seasonality": ["toutes"],
            "safety_level": 1,
            "materials": []
        }
        
        response = authenticated_client.post("/api/v1/activities/", json=activity_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["slug"] == activity_data["slug"]
        assert data["title"] == activity_data["title"]
        assert data["category"] == activity_data["category"]
        assert "id" in data