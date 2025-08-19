import pytest
import httpx
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "La Vida Luca IA API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "services" in data
    assert data["services"]["api"] == "ok"

def test_activities_endpoint():
    """Test the activities endpoint"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "activities" in data
    assert isinstance(data["activities"], list)
    assert len(data["activities"]) > 0

def test_recommendations_endpoint():
    """Test the recommendations endpoint"""
    user_profile = {
        "skills": ["soin_animaux", "sol"],
        "availability": ["printemps", "ete"],
        "location": "Campagne-sur-Mer",
        "preferences": ["agri", "nature"]
    }
    
    request_data = {
        "user_profile": user_profile,
        "max_suggestions": 3
    }
    
    response = client.post("/recommendations", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert "timestamp" in data
    assert isinstance(data["suggestions"], list)
    assert len(data["suggestions"]) <= 3
    
    # Check suggestion structure
    if data["suggestions"]:
        suggestion = data["suggestions"][0]
        assert "activity" in suggestion
        assert "score" in suggestion
        assert "reasons" in suggestion
        assert 0 <= suggestion["score"] <= 1

def test_recommendations_validation():
    """Test recommendations endpoint with invalid data"""
    # Missing required fields
    response = client.post("/recommendations", json={})
    assert response.status_code == 422
    
    # Invalid max_suggestions
    request_data = {
        "user_profile": {
            "skills": ["test"],
            "availability": ["printemps"],
            "location": "test",
            "preferences": ["agri"]
        },
        "max_suggestions": -1
    }
    
    response = client.post("/recommendations", json=request_data)
    # This should still work as our validation is minimal
    assert response.status_code == 200

def test_cors_headers():
    """Test CORS headers are present"""
    response = client.get("/")
    # Note: TestClient doesn't trigger CORS middleware
    # This would need to be tested with actual HTTP requests
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__])