import pytest
from app.services.activity_service import ActivityService, ActivityRegistrationService
from app.schemas.schemas import ActivityCreate, ActivityRegistrationCreate

class TestActivityService:
    def test_create_activity(self, db_session):
        """Test activity creation."""
        activity_service = ActivityService(db_session)
        activity_create = ActivityCreate(
            slug="new-activity",
            title="New Activity",
            category="transfo",
            summary="A new transformation activity",
            duration_min=90,
            safety_level=2,
            skill_tags=["precision", "hygiene"],
            seasonality=["printemps", "ete"],
            materials=["tablier"]
        )
        
        activity = activity_service.create_activity(activity_create)
        
        assert activity.slug == "new-activity"
        assert activity.title == "New Activity"
        assert activity.category == "transfo"
        assert activity.duration_min == 90
        assert activity.safety_level == 2
        assert "precision" in activity.skill_tags

    def test_get_activities_with_filters(self, db_session, test_activity):
        """Test getting activities with filters."""
        activity_service = ActivityService(db_session)
        
        # Get all activities
        activities = activity_service.get_activities()
        assert len(activities) == 1
        
        # Filter by category
        activities = activity_service.get_activities(category="agri")
        assert len(activities) == 1
        
        # Filter by non-existent category
        activities = activity_service.get_activities(category="nonexistent")
        assert len(activities) == 0

    def test_get_recommended_activities(self, db_session, test_user, test_activity):
        """Test activity recommendations."""
        activity_service = ActivityService(db_session)
        
        # Update user profile to have matching skills
        from app.services.user_service import UserService
        from app.schemas.schemas import UserProfileUpdate
        
        user_service = UserService(db_session)
        profile_update = UserProfileUpdate(
            skills=["elevage", "responsabilite"],
            preferences=["agri"]
        )
        user_service.update_user_profile(test_user.id, profile_update)
        
        recommendations = activity_service.get_recommended_activities(test_user, limit=5)
        
        assert len(recommendations) > 0
        assert recommendations[0]["activity"].id == test_activity.id
        assert recommendations[0]["score"] > 0
        assert len(recommendations[0]["reasons"]) > 0

class TestActivityRegistrationService:
    def test_create_registration(self, db_session, test_user, test_activity):
        """Test activity registration."""
        registration_service = ActivityRegistrationService(db_session)
        registration_create = ActivityRegistrationCreate(
            activity_id=test_activity.id,
            notes="Looking forward to this activity"
        )
        
        registration = registration_service.create_registration(
            test_user.id, 
            registration_create
        )
        
        assert registration.user_id == test_user.id
        assert registration.activity_id == test_activity.id
        assert registration.notes == "Looking forward to this activity"
        assert registration.status == "pending"

    def test_get_user_registrations(self, db_session, test_user, test_activity):
        """Test getting user registrations."""
        registration_service = ActivityRegistrationService(db_session)
        
        # Create a registration
        registration_create = ActivityRegistrationCreate(activity_id=test_activity.id)
        registration_service.create_registration(test_user.id, registration_create)
        
        # Get user registrations
        registrations = registration_service.get_user_registrations(test_user.id)
        
        assert len(registrations) == 1
        assert registrations[0].user_id == test_user.id
        assert registrations[0].activity_id == test_activity.id

    def test_duplicate_registration_prevention(self, db_session, test_user, test_activity):
        """Test that duplicate registrations are prevented."""
        registration_service = ActivityRegistrationService(db_session)
        registration_create = ActivityRegistrationCreate(activity_id=test_activity.id)
        
        # First registration should succeed
        registration = registration_service.create_registration(
            test_user.id, 
            registration_create
        )
        assert registration is not None
        
        # Second registration should fail
        with pytest.raises(Exception):  # Should raise HTTPException
            registration_service.create_registration(
                test_user.id, 
                registration_create
            )