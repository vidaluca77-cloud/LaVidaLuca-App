"""
Test the gamification API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import get_db, Base
from app.models.models import User, Activity, Skill, Achievement
from app.core.security import get_password_hash, create_access_token
from app.services.gamification_service import create_default_skills, create_default_achievements


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_gamification_api.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def setup_test_data():
    """Set up test data for gamification endpoints."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    try:
        # Create default skills and achievements
        create_default_skills(db)
        create_default_achievements(db)
        
        # Create test user
        test_user = User(
            email="gamification@test.com",
            username="gameuser",
            hashed_password=get_password_hash("testpass123"),
            full_name="Game User",
            total_points=50,
            current_level=2,
            experience_points=150
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        # Create test activities
        activities = [
            Activity(
                title="Test Activity 1",
                description="A test activity for gamification",
                category="agriculture",
                difficulty_level="beginner",
                points_reward=20,
                skills_taught=[1, 2],
                is_published=True,
                creator_id=test_user.id
            ),
            Activity(
                title="Test Activity 2",
                description="Another test activity",
                category="artisanat",
                difficulty_level="intermediate",
                points_reward=30,
                skills_taught=[2, 3],
                is_published=True,
                creator_id=test_user.id
            )
        ]
        
        for activity in activities:
            db.add(activity)
        
        db.commit()
        return test_user.id
        
    finally:
        db.close()


def test_get_skills():
    """Test getting all skills."""
    user_id = setup_test_data()
    client = TestClient(app)
    
    response = client.get("/api/v1/gamification/skills/")
    assert response.status_code == 200
    
    skills = response.json()
    assert len(skills) > 0
    assert "name" in skills[0]
    assert "category" in skills[0]


def test_get_skill_categories():
    """Test getting skill categories."""
    client = TestClient(app)
    
    response = client.get("/api/v1/gamification/skills/categories/")
    assert response.status_code == 200
    
    categories = response.json()
    assert len(categories) > 0
    assert "agriculture" in categories


def test_get_achievements():
    """Test getting all achievements."""
    client = TestClient(app)
    
    response = client.get("/api/v1/gamification/achievements/")
    assert response.status_code == 200
    
    achievements = response.json()
    assert len(achievements) > 0
    assert "name" in achievements[0]
    assert "points_reward" in achievements[0]


def test_get_user_stats_unauthorized():
    """Test getting user stats without authentication."""
    client = TestClient(app)
    
    response = client.get("/api/v1/gamification/users/me/stats")
    assert response.status_code == 401


def test_get_user_stats_authorized():
    """Test getting user stats with authentication."""
    user_id = setup_test_data()
    client = TestClient(app)
    
    # Create access token
    access_token = create_access_token(subject="gameuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = client.get("/api/v1/gamification/users/me/stats", headers=headers)
    assert response.status_code == 200
    
    stats = response.json()
    assert "total_points" in stats
    assert "current_level" in stats
    assert "experience_points" in stats
    assert stats["total_points"] == 50
    assert stats["current_level"] == 2


def test_get_user_skills():
    """Test getting user's skills."""
    user_id = setup_test_data()
    client = TestClient(app)
    
    access_token = create_access_token(subject="gameuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = client.get("/api/v1/gamification/users/me/skills", headers=headers)
    assert response.status_code == 200
    
    skills = response.json()
    assert isinstance(skills, list)


def test_get_user_achievements():
    """Test getting user's achievements."""
    user_id = setup_test_data()
    client = TestClient(app)
    
    access_token = create_access_token(subject="gameuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = client.get("/api/v1/gamification/users/me/achievements", headers=headers)
    assert response.status_code == 200
    
    achievements = response.json()
    assert isinstance(achievements, list)


def test_complete_activity():
    """Test completing an activity."""
    user_id = setup_test_data()
    client = TestClient(app)
    
    access_token = create_access_token(subject="gameuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    completion_data = {
        "activity_id": 1,
        "rating": 5,
        "feedback": "Great activity!"
    }
    
    response = client.post(
        "/api/v1/gamification/activities/1/complete",
        json=completion_data,
        headers=headers
    )
    assert response.status_code == 200
    
    result = response.json()
    assert "points_earned" in result
    assert "total_points" in result
    assert result["points_earned"] > 0


def test_complete_activity_twice():
    """Test completing the same activity twice (should fail)."""
    user_id = setup_test_data()
    client = TestClient(app)
    
    access_token = create_access_token(subject="gameuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    completion_data = {
        "activity_id": 1,
        "rating": 5,
        "feedback": "Great activity!"
    }
    
    # First completion should succeed
    response1 = client.post(
        "/api/v1/gamification/activities/1/complete",
        json=completion_data,
        headers=headers
    )
    assert response1.status_code == 200
    
    # Second completion should fail
    response2 = client.post(
        "/api/v1/gamification/activities/1/complete",
        json=completion_data,
        headers=headers
    )
    assert response2.status_code == 400


def test_get_leaderboard():
    """Test getting the leaderboard."""
    user_id = setup_test_data()
    client = TestClient(app)
    
    response = client.get("/api/v1/gamification/leaderboard")
    assert response.status_code == 200
    
    data = response.json()
    assert "leaderboard" in data
    assert "limit" in data
    assert len(data["leaderboard"]) > 0
    
    # Check leaderboard entry structure
    entry = data["leaderboard"][0]
    assert "username" in entry
    assert "total_points" in entry
    assert "current_level" in entry


def test_get_recommendations():
    """Test getting activity recommendations."""
    user_id = setup_test_data()
    client = TestClient(app)
    
    access_token = create_access_token(subject="gameuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = client.get("/api/v1/gamification/recommendations", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "recommendations" in data
    assert "user_id" in data
    assert len(data["recommendations"]) > 0
    
    # Check recommendation structure
    rec = data["recommendations"][0]
    assert "title" in rec
    assert "category" in rec
    assert "points_reward" in rec


def test_create_skill_unauthorized():
    """Test creating a skill without admin permissions."""
    user_id = setup_test_data()
    client = TestClient(app)
    
    access_token = create_access_token(subject="gameuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    skill_data = {
        "name": "New Test Skill",
        "description": "A new skill for testing",
        "category": "test"
    }
    
    response = client.post(
        "/api/v1/gamification/skills/",
        json=skill_data,
        headers=headers
    )
    assert response.status_code == 403


def test_create_achievement_unauthorized():
    """Test creating an achievement without admin permissions."""
    user_id = setup_test_data()
    client = TestClient(app)
    
    access_token = create_access_token(subject="gameuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    achievement_data = {
        "name": "New Test Achievement",
        "description": "A new achievement for testing",
        "category": "test",
        "points_reward": 100
    }
    
    response = client.post(
        "/api/v1/gamification/achievements/",
        json=achievement_data,
        headers=headers
    )
    assert response.status_code == 403


if __name__ == "__main__":
    # Run individual tests
    print("🧪 Testing Gamification API Endpoints")
    print("=" * 50)
    
    try:
        test_get_skills()
        print("✅ test_get_skills passed")
        
        test_get_skill_categories()
        print("✅ test_get_skill_categories passed")
        
        test_get_achievements()
        print("✅ test_get_achievements passed")
        
        test_get_user_stats_unauthorized()
        print("✅ test_get_user_stats_unauthorized passed")
        
        test_get_user_stats_authorized()
        print("✅ test_get_user_stats_authorized passed")
        
        test_get_user_skills()
        print("✅ test_get_user_skills passed")
        
        test_get_user_achievements()
        print("✅ test_get_user_achievements passed")
        
        test_complete_activity()
        print("✅ test_complete_activity passed")
        
        test_get_leaderboard()
        print("✅ test_get_leaderboard passed")
        
        test_get_recommendations()
        print("✅ test_get_recommendations passed")
        
        test_create_skill_unauthorized()
        print("✅ test_create_skill_unauthorized passed")
        
        test_create_achievement_unauthorized()
        print("✅ test_create_achievement_unauthorized passed")
        
        print("\n🎉 All gamification API tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        raise