import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "La Vida Luca IA API - Opérationnelle"}

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "la-vida-luca-ia"

def test_get_activities():
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, list)
    assert len(activities) >= 2  # We have at least 2 activities in our test data

def test_get_activity_by_id():
    """Test getting a specific activity"""
    response = client.get("/activities/1")
    assert response.status_code == 200
    activity = response.json()
    assert activity["id"] == "1"
    assert activity["title"] == "Nourrir les animaux"

def test_get_activity_not_found():
    """Test getting a non-existent activity"""
    response = client.get("/activities/999")
    assert response.status_code == 404

def test_matching_endpoint():
    """Test the activity matching endpoint"""
    profile_data = {
        "profile": {
            "skills": ["observation", "douceur"],
            "availability": ["toutes"],
            "location": "Calvados",
            "preferences": ["agri"]
        }
    }
    
    response = client.post("/matching", json=profile_data)
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)
    
    # Check that suggestions have the right structure
    if data["suggestions"]:
        suggestion = data["suggestions"][0]
        assert "activity" in suggestion
        assert "score" in suggestion
        assert "reasons" in suggestion
        assert suggestion["score"] > 0

def test_matching_no_skills():
    """Test matching with profile that has no matching skills"""
    profile_data = {
        "profile": {
            "skills": ["unknown_skill"],
            "availability": ["never"],
            "location": "Unknown",
            "preferences": ["unknown_category"]
        }
    }
    
    response = client.post("/matching", json=profile_data)
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    # Should return empty suggestions or low-scored ones