import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

def test_get_activity_suggestions(client: TestClient, test_user_profile):
    """Test getting AI activity suggestions."""
    with patch('app.routers.ai.get_supabase_client') as mock_supabase:
        # Mock activities data
        mock_activities = [
            {
                "id": "activity-1",
                "title": "Nourrir et soigner les moutons",
                "slug": "nourrir-soigner-moutons",
                "category": "agri",
                "summary": "Gestes quotidiens : alimentation, eau, observation.",
                "duration_min": 60,
                "skill_tags": ["elevage", "responsabilite"],
                "seasonality": ["toutes"],
                "safety_level": 1,
                "materials": ["bottes", "gants"],
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            },
            {
                "id": "activity-2",
                "title": "Plantation d'arbres",
                "slug": "plantation-arbres",
                "category": "nature",
                "summary": "Choix essences, préparation sol, plantation correcte.",
                "duration_min": 120,
                "skill_tags": ["sol", "ecologie"],
                "seasonality": ["automne", "hiver"],
                "safety_level": 1,
                "materials": ["beche", "gants"],
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        ]
        mock_supabase.return_value.table.return_value.select.return_value.execute.return_value.data = mock_activities
        
        response = client.post("/api/v1/ai/suggestions", json={"profile": test_user_profile})
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert all("activity" in suggestion for suggestion in data)
        assert all("score" in suggestion for suggestion in data)
        assert all("reasons" in suggestion for suggestion in data)
        
        # Verify suggestions are sorted by score (descending)
        scores = [suggestion["score"] for suggestion in data]
        assert scores == sorted(scores, reverse=True)

def test_calculate_matching_score():
    """Test the matching score calculation logic."""
    from app.routers.ai import calculate_matching_score
    from app.models import Activity, UserProfile
    
    # Create test activity
    activity = Activity(
        id="test-id",
        title="Test Activity",
        slug="test-activity",
        category="agri",
        summary="Test summary",
        duration_min=60,
        skill_tags=["elevage", "hygiene"],
        seasonality=["toutes"],
        safety_level=1,
        materials=["gants"],
        created_at="2024-01-01T00:00:00",
        updated_at="2024-01-01T00:00:00"
    )
    
    # Create test profile
    profile = UserProfile(
        skills=["elevage", "hygiene"],
        availability=["weekend"],
        location="France",
        preferences=["agri"]
    )
    
    score, reasons = calculate_matching_score(activity, profile)
    
    # Should have positive score due to matching skills, category, and other factors
    assert score > 0
    assert len(reasons) > 0
    assert any("elevage" in reason and "hygiene" in reason for reason in reasons)

def test_get_activity_categories(client: TestClient):
    """Test getting activity categories with counts."""
    with patch('app.routers.ai.get_supabase_client') as mock_supabase:
        # Mock category data
        mock_categories = [
            {"category": "agri"},
            {"category": "agri"},
            {"category": "nature"},
            {"category": "transfo"}
        ]
        mock_supabase.return_value.table.return_value.select.return_value.execute.return_value.data = mock_categories
        
        response = client.get("/api/v1/ai/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        categories = data["categories"]
        
        # Check structure
        assert len(categories) == 5  # Should have all 5 categories
        for category in categories:
            assert "id" in category
            assert "name" in category
            assert "count" in category
        
        # Check counts
        agri_category = next(cat for cat in categories if cat["id"] == "agri")
        assert agri_category["count"] == 2

def test_get_available_skills(client: TestClient):
    """Test getting available skills from activities."""
    with patch('app.routers.ai.get_supabase_client') as mock_supabase:
        # Mock skill data
        mock_skills = [
            {"skill_tags": ["elevage", "hygiene"]},
            {"skill_tags": ["sol", "ecologie"]},
            {"skill_tags": ["elevage", "precision"]}  # overlapping skills
        ]
        mock_supabase.return_value.table.return_value.select.return_value.execute.return_value.data = mock_skills
        
        response = client.get("/api/v1/ai/skills")
        assert response.status_code == 200
        data = response.json()
        assert "skills" in data
        skills = data["skills"]
        
        # Should be unique and sorted
        expected_skills = ["ecologie", "elevage", "hygiene", "precision", "sol"]
        assert skills == expected_skills

def test_suggestions_with_empty_profile(client: TestClient):
    """Test suggestions with empty user profile."""
    empty_profile = {
        "skills": [],
        "availability": [],
        "location": "",
        "preferences": []
    }
    
    with patch('app.routers.ai.get_supabase_client') as mock_supabase:
        mock_activities = [{
            "id": "activity-1",
            "title": "Test Activity",
            "slug": "test-activity",
            "category": "agri",
            "summary": "Test summary",
            "duration_min": 60,
            "skill_tags": ["test"],
            "seasonality": ["toutes"],
            "safety_level": 1,
            "materials": [],
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }]
        mock_supabase.return_value.table.return_value.select.return_value.execute.return_value.data = mock_activities
        
        response = client.post("/api/v1/ai/suggestions", json={"profile": empty_profile})
        assert response.status_code == 200
        # Even with empty profile, should get some suggestions based on other factors