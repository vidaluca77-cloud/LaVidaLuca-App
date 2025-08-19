"""
Test the OpenAI service integration with enhanced activity models.
"""

import pytest
from unittest.mock import AsyncMock, patch
from app.services.openai_service import get_activity_suggestions, _fallback_suggestions


@pytest.mark.asyncio
async def test_fallback_suggestions():
    """Test the fallback suggestion algorithm."""
    
    # Mock user profile
    user_profile = {
        "skills": ["elevage", "agriculture"],
        "interests": ["agri", "nature"],
        "experience_level": "beginner"
    }
    
    # Mock activities
    activities = [
        {
            "id": 1,
            "title": "Introduction à l'élevage",
            "category": "agri",
            "skill_tags": ["elevage", "soin_animaux"],
            "keywords": ["agriculture", "elevage"],
            "difficulty_level": 1,
            "is_featured": True
        },
        {
            "id": 2,
            "title": "Transformation du lait",
            "category": "transfo",
            "skill_tags": ["transformation", "hygiene"],
            "keywords": ["lait", "transformation"],
            "difficulty_level": 3,
            "is_featured": False
        }
    ]
    
    suggestions = _fallback_suggestions(
        user_profile, 
        "Je veux apprendre l'élevage", 
        activities, 
        5
    )
    
    assert len(suggestions) == 2
    
    # First suggestion should have higher score due to skill match
    first_suggestion = suggestions[0]
    assert first_suggestion["activity"]["id"] == 1
    assert first_suggestion["score"] > 0.5
    assert "elevage" in " ".join(first_suggestion["reasons"]).lower()


@pytest.mark.asyncio
async def test_openai_service_fallback():
    """Test that the service falls back gracefully when OpenAI fails."""
    
    user_profile = {"skills": ["agriculture"], "interests": ["nature"]}
    activities = [
        {
            "id": 1,
            "title": "Agriculture biologique",
            "category": "agri",
            "skill_tags": ["agriculture"],
            "keywords": ["bio", "agriculture"],
            "difficulty_level": 1
        }
    ]
    
    # Mock OpenAI to raise an exception
    with patch('app.services.openai_service.openai.chat.completions.create', side_effect=Exception("API Error")):
        suggestions = await get_activity_suggestions(
            user_profile,
            "Je veux apprendre l'agriculture",
            activities,
            3
        )
    
    # Should still get suggestions from fallback
    assert len(suggestions) >= 1
    assert suggestions[0]["activity"]["id"] == 1


def test_activity_to_dict():
    """Test the Activity model's to_dict method."""
    from app.models.models import Activity
    
    # Create a mock activity
    activity = Activity(
        id=1,
        title="Test Activity",
        category="agri",
        skill_tags=["test", "agriculture"],
        materials=["gants", "outils"],
        season_tags=["printemps"],
        safety_level=2,
        is_published=True
    )
    
    result = activity.to_dict()
    
    assert result["id"] == 1
    assert result["title"] == "Test Activity"
    assert result["category"] == "agri"
    assert result["skill_tags"] == ["test", "agriculture"]
    assert result["materials"] == ["gants", "outils"]
    assert result["season_tags"] == ["printemps"]
    assert result["safety_level"] == 2
    assert result["is_published"] is True


@pytest.mark.asyncio
async def test_enhanced_model_fields():
    """Test that enhanced model fields work properly."""
    from app.models.models import User, Activity, Contact
    
    # Test User profile field
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed",
        profile={
            "skills": ["agriculture", "elevage"],
            "location": "Bretagne",
            "experience": "debutant"
        }
    )
    
    assert user.profile["skills"] == ["agriculture", "elevage"]
    assert user.profile["location"] == "Bretagne"
    
    # Test Activity enhanced fields
    activity = Activity(
        title="Test Enhanced Activity",
        category="agri",
        skill_tags=["test", "enhanced"],
        materials=["material1", "material2"],
        external_resources={"video": "https://example.com/video"},
        creator_id=1
    )
    
    assert activity.skill_tags == ["test", "enhanced"]
    assert activity.materials == ["material1", "material2"]
    assert activity.external_resources["video"] == "https://example.com/video"
    
    # Test Contact model
    contact = Contact(
        name="Test User",
        email="contact@example.com",
        subject="Test Subject",
        message="Test message",
        tags=["urgent", "partnership"],
        extra_data={"source": "website"}
    )
    
    assert contact.tags == ["urgent", "partnership"]
    assert contact.extra_data["source"] == "website"