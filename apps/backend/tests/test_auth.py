"""
Unit tests for authentication endpoints.
Tests user registration, login, and profile management.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from models import User
import json

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    """Create test client."""
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)

class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_register_user(self, client):
        """Test user registration."""
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == "test@example.com"
        assert "user_id" in data["data"]
    
    def test_register_duplicate_email(self, client):
        """Test registering with duplicate email."""
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        # First registration should succeed
        response1 = client.post("/api/auth/register", json=user_data)
        assert response1.status_code == 200
        
        # Second registration with same email should fail
        response2 = client.post("/api/auth/register", json=user_data)
        assert response2.status_code == 400
        assert "already registered" in response2.json()["detail"].lower()
    
    def test_login_user(self, client):
        """Test user login."""
        # First register a user
        user_data = {
            "email": "login@example.com",
            "password": "testpassword123"
        }
        client.post("/api/auth/register", json=user_data)
        
        # Now login
        login_data = {
            "email": "login@example.com",
            "password": "testpassword123"
        }
        
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401
    
    def test_get_current_user(self, client):
        """Test getting current user info."""
        # Register and login
        user_data = {
            "email": "profile@example.com",
            "password": "testpassword123"
        }
        client.post("/api/auth/register", json=user_data)
        
        login_response = client.post("/api/auth/login", json=user_data)
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get user profile
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "profile@example.com"
        assert "id" in data
    
    def test_unauthorized_access(self, client):
        """Test accessing protected endpoint without auth."""
        response = client.get("/api/auth/me")
        assert response.status_code == 403