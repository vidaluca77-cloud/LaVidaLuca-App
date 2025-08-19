import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)

@pytest.fixture
def test_activity_data():
    """Sample activity data for tests."""
    return {
        "title": "Test Activity",
        "slug": "test-activity",
        "category": "agri",
        "summary": "This is a test activity",
        "duration_min": 60,
        "skill_tags": ["test", "demo"],
        "seasonality": ["printemps"],
        "safety_level": 1,
        "materials": ["gants"]
    }

@pytest.fixture
def test_user_data():
    """Sample user data for tests."""
    return {
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "testpassword123",
        "profile": {
            "skills": ["test", "demo"],
            "availability": ["weekend"],
            "location": "Test Location",
            "preferences": ["agri"]
        }
    }

@pytest.fixture
def test_user_profile():
    """Sample user profile for AI suggestions."""
    return {
        "skills": ["elevage", "hygiene", "sol"],
        "availability": ["weekend", "matin"],
        "location": "France",
        "preferences": ["agri", "nature"]
    }