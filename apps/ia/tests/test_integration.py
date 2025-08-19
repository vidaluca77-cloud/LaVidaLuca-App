"""
Integration tests for the LaVidaLuca API.
"""
import pytest
from fastapi.testclient import TestClient


def test_complete_user_journey(test_client: TestClient):
    """Test a complete user journey from registration to recommendations."""
    
    # 1. Register a new user
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "password123"
    }
    
    response = test_client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == user_data["email"]
    assert user["username"] == user_data["username"]
    
    # 2. Login with the new user
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    response = test_client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    
    # 3. Get current user info
    response = test_client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    current_user = response.json()
    assert current_user["email"] == user_data["email"]
    
    # 4. Create a new activity
    activity_data = {
        "title": "Test Activity",
        "description": "A test agricultural activity",
        "category": "Test",
        "difficulty_level": 2,
        "duration_hours": 3.0
    }
    
    response = test_client.post("/api/v1/activities/", json=activity_data, headers=headers)
    assert response.status_code == 200
    activity = response.json()
    assert activity["title"] == activity_data["title"]
    
    # 5. Get activities list
    response = test_client.get("/api/v1/activities/")
    assert response.status_code == 200
    activities_list = response.json()
    assert "activities" in activities_list
    assert activities_list["total"] >= 1
    
    # 6. Generate recommendations
    recommendation_request = {
        "preferred_difficulty": 2,
        "max_duration": 5.0
    }
    
    response = test_client.post(
        "/api/v1/recommendations/generate", 
        json=recommendation_request, 
        headers=headers
    )
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)
    
    # 7. Get user recommendations
    response = test_client.get("/api/v1/recommendations/", headers=headers)
    assert response.status_code == 200
    user_recommendations = response.json()
    assert "recommendations" in user_recommendations


def test_activity_filtering(test_client: TestClient):
    """Test activity filtering functionality."""
    
    # Test category filtering
    response = test_client.get("/api/v1/activities/?category=Agriculture")
    assert response.status_code == 200
    
    # Test difficulty filtering
    response = test_client.get("/api/v1/activities/?difficulty_level=2")
    assert response.status_code == 200
    
    # Test pagination
    response = test_client.get("/api/v1/activities/?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["activities"]) <= 2


def test_unauthorized_access(test_client: TestClient):
    """Test that protected endpoints require authentication."""
    
    # Try to access protected endpoint without token
    response = test_client.get("/api/v1/auth/me")
    assert response.status_code == 401
    
    # Try to create activity without token
    activity_data = {
        "title": "Test Activity",
        "description": "Test description",
        "category": "Test"
    }
    response = test_client.post("/api/v1/activities/", json=activity_data)
    assert response.status_code == 401
    
    # Try to generate recommendations without token
    response = test_client.post("/api/v1/recommendations/generate", json={})
    assert response.status_code == 401


def test_activity_categories(test_client: TestClient):
    """Test activity categories endpoint."""
    response = test_client.get("/api/v1/activities/categories/")
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)