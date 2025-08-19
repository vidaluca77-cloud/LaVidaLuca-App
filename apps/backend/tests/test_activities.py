"""
Unit tests for activity management endpoints.
Tests CRUD operations and AI suggestions functionality.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from auth import get_password_hash
from models import User, Activity
import json

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
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

@pytest.fixture
def test_user():
    """Create a test user."""
    db = TestingSessionLocal()
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        profile={
            "skills": ["gardening", "composting"],
            "interests": ["agri", "nature"],
            "location": "Lyon",
            "experience_level": "beginner"
        }
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.delete(user)
    db.commit()
    db.close()

@pytest.fixture
def test_activity():
    """Create a test activity."""
    db = TestingSessionLocal()
    activity = Activity(
        title="Organic Vegetable Growing",
        category="agri",
        summary="Learn to grow organic vegetables using sustainable methods",
        description="A comprehensive introduction to organic vegetable cultivation",
        duration_min=120,
        skill_tags=["gardening", "organic farming", "soil management"],
        materials=["seeds", "compost", "gardening tools"],
        safety_level=2,
        difficulty_level=2,
        location="Lyon",
        engagement_score=0.8,
        success_rate=0.75
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    yield activity
    db.delete(activity)
    db.commit()
    db.close()

@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for test user."""
    login_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = client.post("/api/auth/login", json=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

class TestActivityCRUD:
    """Test activity CRUD operations."""
    
    def test_list_activities(self, client, test_activity):
        """Test listing activities."""
        response = client.get("/api/activities/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) >= 1
        assert data["total"] >= 1
    
    def test_get_activity(self, client, test_activity):
        """Test getting a specific activity."""
        response = client.get(f"/api/activities/{test_activity.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_activity.id
        assert data["title"] == test_activity.title
    
    def test_get_nonexistent_activity(self, client):
        """Test getting a non-existent activity."""
        response = client.get("/api/activities/nonexistent")
        assert response.status_code == 404
    
    def test_create_activity(self, client, auth_headers):
        """Test creating a new activity."""
        activity_data = {
            "title": "Composting Workshop",
            "category": "agri",
            "summary": "Learn how to make compost for your garden",
            "description": "Hands-on workshop on composting techniques",
            "duration_min": 90,
            "skill_tags": ["composting", "recycling"],
            "materials": ["organic waste", "compost bin"],
            "safety_level": 1,
            "difficulty_level": 1,
            "location": "Paris"
        }
        
        response = client.post("/api/activities/", json=activity_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "activity_id" in data["data"]
    
    def test_create_activity_unauthorized(self, client):
        """Test creating activity without authentication."""
        activity_data = {
            "title": "Test Activity",
            "category": "agri",
            "summary": "Test summary",
            "duration_min": 60
        }
        
        response = client.post("/api/activities/", json=activity_data)
        assert response.status_code == 403
    
    def test_update_activity(self, client, test_user, test_activity, auth_headers):
        """Test updating an activity."""
        # Set the test user as creator
        db = TestingSessionLocal()
        test_activity.creator_id = test_user.id
        db.commit()
        
        update_data = {
            "title": "Updated Organic Vegetable Growing",
            "duration_min": 150
        }
        
        response = client.put(f"/api/activities/{test_activity.id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        db.close()
    
    def test_update_activity_unauthorized(self, client, test_activity, auth_headers):
        """Test updating activity without permission."""
        update_data = {"title": "Unauthorized Update"}
        
        response = client.put(f"/api/activities/{test_activity.id}", json=update_data, headers=auth_headers)
        assert response.status_code == 403
    
    def test_delete_activity(self, client, test_user, test_activity, auth_headers):
        """Test deleting an activity."""
        # Set the test user as creator
        db = TestingSessionLocal()
        test_activity.creator_id = test_user.id
        db.commit()
        
        response = client.delete(f"/api/activities/{test_activity.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # Verify activity is deactivated
        response = client.get(f"/api/activities/{test_activity.id}")
        assert response.status_code == 404
        
        db.close()

class TestActivityFiltering:
    """Test activity filtering and search."""
    
    def test_filter_by_category(self, client, test_activity):
        """Test filtering activities by category."""
        response = client.get("/api/activities/?category=agri")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        for activity in data["data"]:
            assert activity["category"] == "agri"
    
    def test_search_activities(self, client, test_activity):
        """Test searching activities by text."""
        response = client.get("/api/activities/?search=organic")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        # Should find the test activity
        assert len(data["data"]) >= 1
    
    def test_filter_by_skill_tags(self, client, test_activity):
        """Test filtering by skill tags."""
        response = client.get("/api/activities/?skill_tags=gardening")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

class TestActivitySuggestions:
    """Test AI-powered activity suggestions."""
    
    def test_get_suggestions(self, client, test_user, test_activity, auth_headers):
        """Test getting activity suggestions."""
        suggestion_request = {
            "limit": 5,
            "preferences": {}
        }
        
        response = client.post("/api/activities/suggestions", json=suggestion_request, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "suggestions" in data
        assert "total" in data
        assert "generated_at" in data
        assert len(data["suggestions"]) <= 5
        
        # Check suggestion structure
        if data["suggestions"]:
            suggestion = data["suggestions"][0]
            assert "activity" in suggestion
            assert "score" in suggestion
            assert "reasons" in suggestion
            assert 0 <= suggestion["score"] <= 1

class TestActivityCategories:
    """Test activity categories endpoint."""
    
    def test_list_categories(self, client):
        """Test getting list of categories."""
        response = client.get("/api/activities/categories/list")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 5  # 5 predefined categories
        
        # Check category structure
        category = data["data"][0]
        assert "id" in category
        assert "name" in category
        assert "description" in category