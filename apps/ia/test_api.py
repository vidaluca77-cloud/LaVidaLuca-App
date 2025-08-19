import pytest
import asyncio
from fastapi.testclient import TestClient
from main import app, SAMPLE_ACTIVITIES

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns correct information"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_get_activities():
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, list)
    assert len(activities) >= len(SAMPLE_ACTIVITIES)
    
    # Check structure of first activity
    if activities:
        activity = activities[0]
        required_fields = ["id", "slug", "title", "category", "summary", 
                          "duration_min", "skill_tags", "seasonality", 
                          "safety_level", "materials"]
        for field in required_fields:
            assert field in activity

def test_activity_suggestions():
    """Test getting activity suggestions based on user profile"""
    test_profile = {
        "skills": ["patience", "observation"],
        "availability": ["weekend"],
        "location": "test-location",
        "preferences": ["agri"]
    }
    
    response = client.post("/activities/suggestions", json=test_profile)
    assert response.status_code == 200
    suggestions = response.json()
    assert isinstance(suggestions, list)
    
    if suggestions:
        suggestion = suggestions[0]
        assert "activity" in suggestion
        assert "score" in suggestion
        assert "reasons" in suggestion
        assert isinstance(suggestion["score"], int)
        assert isinstance(suggestion["reasons"], list)

def test_contact_form():
    """Test submitting a contact form"""
    contact_data = {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "message": "This is a test message",
        "type": "general"
    }
    
    response = client.post("/contact", json=contact_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "message" in data
    assert "id" in data

def test_authentication_token():
    """Test authentication token generation"""
    response = client.post(
        "/auth/token",
        params={"username": "demo", "password": "demo"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_authentication_failure():
    """Test authentication with wrong credentials"""
    response = client.post(
        "/auth/token",
        params={"username": "wrong", "password": "wrong"}
    )
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

def test_protected_route_without_token():
    """Test accessing protected route without token"""
    response = client.get("/protected")
    assert response.status_code == 403

def test_protected_route_with_token():
    """Test accessing protected route with valid token"""
    # First get a token
    token_response = client.post(
        "/auth/token",
        params={"username": "demo", "password": "demo"}
    )
    token_data = token_response.json()
    token = token_data["access_token"]
    
    # Use token to access protected route
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_cors_headers():
    """Test that CORS headers are present"""
    response = client.options("/activities")
    # CORS headers should be added by middleware
    assert response.status_code == 200

def test_invalid_contact_form():
    """Test contact form with missing required fields"""
    invalid_data = {
        "name": "Test User",
        # Missing email, subject, message
    }
    
    response = client.post("/contact", json=invalid_data)
    assert response.status_code == 422  # Validation error

def test_activity_suggestions_invalid_profile():
    """Test suggestions with invalid profile data"""
    invalid_profile = {
        "skills": "not_a_list",  # Should be list
        "availability": [],
        "location": "",
        "preferences": []
    }
    
    response = client.post("/activities/suggestions", json=invalid_profile)
    assert response.status_code == 422  # Validation error