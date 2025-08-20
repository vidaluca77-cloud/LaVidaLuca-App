"""
Test script for gamification functionality.
This script creates test data and demonstrates the gamification system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.models.models import User, Activity, Skill, Achievement
from app.services.gamification_service import (
    GamificationService, create_default_skills, create_default_achievements
)
from app.core.security import get_password_hash


def test_gamification():
    """Test the gamification system with sample data."""
    
    # Create SQLite engine for testing
    engine = create_engine("sqlite:///./test_gamification.db", echo=True)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        print("🎮 Testing LaVidaLuca Gamification System")
        print("=" * 50)
        
        # Create default skills and achievements
        create_default_skills(db)
        create_default_achievements(db)
        print("✅ Created default skills and achievements")
        
        # Create test user
        test_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("testpass"),
            full_name="Test User"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"✅ Created test user: {test_user.username}")
        
        # Create test activities
        activities_data = [
            {
                "title": "Initiation au Jardinage Bio",
                "description": "Découverte des techniques de base du jardinage biologique",
                "category": "agriculture",
                "difficulty_level": "beginner",
                "duration_minutes": 120,
                "points_reward": 15,
                "skills_taught": [1, 2],  # Jardinage Bio, Compostage
                "is_published": True,
                "creator_id": test_user.id
            },
            {
                "title": "Construction d'un Composteur",
                "description": "Apprendre à construire et gérer un composteur",
                "category": "artisanat",
                "difficulty_level": "intermediate",
                "duration_minutes": 180,
                "points_reward": 25,
                "skills_taught": [2, 5],  # Compostage, Menuiserie
                "is_published": True,
                "creator_id": test_user.id
            },
            {
                "title": "Animation d'un Atelier",
                "description": "Développer ses compétences d'animation et de transmission",
                "category": "social",
                "difficulty_level": "advanced",
                "duration_minutes": 240,
                "points_reward": 35,
                "skills_taught": [9, 12],  # Communication, Enseignement
                "is_published": True,
                "creator_id": test_user.id
            }
        ]
        
        for activity_data in activities_data:
            activity = Activity(**activity_data)
            db.add(activity)
        
        db.commit()
        print("✅ Created test activities")
        
        # Initialize gamification service
        gamification_service = GamificationService(db)
        
        # Test initial user stats
        print("\n📊 Initial User Stats:")
        initial_stats = gamification_service.get_user_stats(test_user.id)
        for key, value in initial_stats.items():
            print(f"  {key}: {value}")
        
        # Test activity completion
        print("\n🎯 Testing Activity Completion:")
        
        # Complete first activity
        result1 = gamification_service.complete_activity(
            user_id=test_user.id,
            activity_id=1,  # Jardinage Bio
            rating=5,
            feedback="Excellente activité!"
        )
        print(f"  Activity 1 completed: {result1}")
        
        # Complete second activity
        result2 = gamification_service.complete_activity(
            user_id=test_user.id,
            activity_id=2,  # Composteur
            rating=4,
            feedback="Très instructif"
        )
        print(f"  Activity 2 completed: {result2}")
        
        # Complete third activity
        result3 = gamification_service.complete_activity(
            user_id=test_user.id,
            activity_id=3,  # Animation
            rating=5,
            feedback="Challenge relevé!"
        )
        print(f"  Activity 3 completed: {result3}")
        
        # Test final user stats
        print("\n📈 Final User Stats:")
        final_stats = gamification_service.get_user_stats(test_user.id)
        for key, value in final_stats.items():
            print(f"  {key}: {value}")
        
        # Test leaderboard
        print("\n🏆 Leaderboard:")
        leaderboard = gamification_service.get_leaderboard(5)
        for i, user_data in enumerate(leaderboard, 1):
            print(f"  {i}. {user_data['username']} - {user_data['total_points']} points (Level {user_data['current_level']})")
        
        # Test recommendations
        print("\n💡 Activity Recommendations:")
        recommendations = gamification_service.recommend_activities_by_skills(test_user.id, 3)
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec['title']} ({rec['points_reward']} points)")
        
        # Test skills count
        skills_count = db.query(Skill).count()
        achievements_count = db.query(Achievement).count()
        print(f"\n📚 Content Summary:")
        print(f"  Total skills: {skills_count}")
        print(f"  Total achievements: {achievements_count}")
        
        print("\n🎉 Gamification system test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    test_gamification()