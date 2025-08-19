"""
Tests for activity and recommendation endpoints
"""
import pytest
from fastapi.testclient import TestClient


def test_get_activities(client: TestClient, test_activities):
    """Test getting all activities."""
    response = client.get("/api/v1/activities/activities")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Test Activity 1"
    assert data[1]["title"] == "Test Activity 2"


def test_get_activities_filter_by_category(client: TestClient, test_activities):
    """Test filtering activities by category."""
    response = client.get("/api/v1/activities/activities?category=agri")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "agri"
    assert data[0]["title"] == "Test Activity 1"


def test_get_activities_filter_by_skill(client: TestClient, test_activities):
    """Test filtering activities by skill tag."""
    response = client.get("/api/v1/activities/activities?skill_tag=hygiene")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Activity 2"
    assert "hygiene" in data[0]["skill_tags"]


def test_get_activities_filter_by_safety_level(client: TestClient, test_activities):
    """Test filtering activities by safety level."""
    response = client.get("/api/v1/activities/activities?safety_level=1")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["safety_level"] == 1


def test_get_activity_by_id(client: TestClient, test_activities):
    """Test getting a specific activity by ID."""
    activity_id = test_activities[0].id
    response = client.get(f"/api/v1/activities/activities/{activity_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == activity_id
    assert data["title"] == "Test Activity 1"


def test_get_activity_not_found(client: TestClient):
    """Test getting non-existent activity."""
    response = client.get("/api/v1/activities/activities/999")
    
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_get_recommendations_anonymous(client: TestClient, test_activities):
    """Test getting recommendations without authentication."""
    request_data = {
        "user_profile": {
            "skills": ["elevage", "hygiene"],
            "preferences": ["agri"],
            "availability": ["weekend"],
            "location": "Test Location",
            "experience_level": "debutant"
        },
        "limit": 5
    }
    
    response = client.post("/api/v1/activities/recommendations", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert "total_activities" in data
    assert "profile_completeness" in data
    assert len(data["recommendations"]) <= 2  # We only have 2 test activities


def test_get_my_recommendations_with_profile(client: TestClient, test_user_profile, test_activities, auth_headers):
    """Test getting recommendations for authenticated user with profile."""
    response = client.post("/api/v1/activities/recommendations/me?limit=5", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) <= 2
    
    # Check recommendation structure
    if data["recommendations"]:
        rec = data["recommendations"][0]
        assert "activity" in rec
        assert "score" in rec
        assert "reasons" in rec
        assert rec["score"] >= 0
        assert rec["score"] <= 100


def test_get_my_recommendations_no_profile(client: TestClient, test_user, test_activities, auth_headers):
    """Test getting recommendations when user has no profile."""
    response = client.post("/api/v1/activities/recommendations/me", headers=auth_headers)
    
    assert response.status_code == 404
    assert "Profile not found" in response.json()["detail"]


def test_recommendation_scoring(client: TestClient, test_activities):
    """Test that recommendation scoring works correctly."""
    # Profile that should match first activity well
    request_data = {
        "user_profile": {
            "skills": ["elevage", "responsabilite"],  # Matches test-activity-1
            "preferences": ["agri"],  # Matches test-activity-1
            "availability": ["weekend"],
            "experience_level": "debutant"
        },
        "limit": 2
    }
    
    response = client.post("/api/v1/activities/recommendations", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    recommendations = data["recommendations"]
    
    # First recommendation should be the agriculture activity with higher score
    assert len(recommendations) >= 1
    first_rec = recommendations[0]
    assert first_rec["activity"]["category"] == "agri"
    assert first_rec["score"] > 0
    assert len(first_rec["reasons"]) > 0


def test_profile_completeness_calculation(client: TestClient, test_activities):
    """Test profile completeness calculation."""
    # Complete profile
    complete_profile = {
        "skills": ["elevage"],
        "preferences": ["agri"],
        "availability": ["weekend"],
        "location": "Test Location",
        "experience_level": "intermediaire",  # Non-default
        "bio": "Test bio"
    }
    
    request_data = {
        "user_profile": complete_profile,
        "limit": 1
    }
    
    response = client.post("/api/v1/activities/recommendations", json=request_data)
    data = response.json()
    
    # Should have high completeness
    assert data["profile_completeness"] == 1.0
    
    # Incomplete profile
    incomplete_profile = {
        "skills": ["elevage"],
        "preferences": [],
        "availability": [],
        "experience_level": "debutant"  # Default value
    }
    
    request_data["user_profile"] = incomplete_profile
    response = client.post("/api/v1/activities/recommendations", json=request_data)
    data = response.json()
    
    # Should have lower completeness
    assert data["profile_completeness"] < 0.5