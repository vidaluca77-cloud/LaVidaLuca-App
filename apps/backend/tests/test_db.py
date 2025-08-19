"""
Comprehensive database tests for LaVidaLuca Backend.
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from app.models.models import User, Activity, ActivitySuggestion
from app.core.security import get_password_hash, verify_password


class TestUserModel:
    """Test User model database operations."""
    
    def test_create_user(self, db_session: Session):
        """Test creating a user in the database."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "hashed_password": get_password_hash("testpassword"),
            "full_name": "Test User",
            "is_active": True,
            "is_superuser": False
        }
        
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        assert user.id is not None
        assert user.email == user_data["email"]
        assert user.username == user_data["username"]
        assert user.full_name == user_data["full_name"]
        assert user.is_active == user_data["is_active"]
        assert user.is_superuser == user_data["is_superuser"]
        assert user.created_at is not None
        assert verify_password("testpassword", user.hashed_password)
    
    def test_user_unique_email_constraint(self, db_session: Session, test_user: User):
        """Test that email must be unique."""
        duplicate_user = User(
            email=test_user.email,  # Same email
            username="differentusername",
            hashed_password=get_password_hash("password"),
            full_name="Different User"
        )
        
        db_session.add(duplicate_user)
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_user_unique_username_constraint(self, db_session: Session, test_user: User):
        """Test that username must be unique."""
        duplicate_user = User(
            email="different@example.com",
            username=test_user.username,  # Same username
            hashed_password=get_password_hash("password"),
            full_name="Different User"
        )
        
        db_session.add(duplicate_user)
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_user_required_fields(self, db_session: Session):
        """Test that required fields cannot be null."""
        # Test missing email
        with pytest.raises(IntegrityError):
            user = User(
                username="testuser",
                hashed_password=get_password_hash("password")
            )
            db_session.add(user)
            db_session.commit()
        
        db_session.rollback()
        
        # Test missing username
        with pytest.raises(IntegrityError):
            user = User(
                email="test@example.com",
                hashed_password=get_password_hash("password")
            )
            db_session.add(user)
            db_session.commit()
        
        db_session.rollback()
        
        # Test missing hashed_password
        with pytest.raises(IntegrityError):
            user = User(
                email="test@example.com",
                username="testuser"
            )
            db_session.add(user)
            db_session.commit()
    
    def test_user_default_values(self, db_session: Session):
        """Test default values for user fields."""
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("password")
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        assert user.is_active is True  # Default value
        assert user.is_superuser is False  # Default value
        assert user.full_name is None  # Nullable field
    
    def test_user_timestamps(self, db_session: Session):
        """Test that timestamps are set correctly."""
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("password")
        )
        
        before_create = datetime.utcnow()
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        after_create = datetime.utcnow()
        
        assert before_create <= user.created_at <= after_create
        assert user.updated_at is None  # Only set on updates
        
        # Test update timestamp
        user.full_name = "Updated Name"
        before_update = datetime.utcnow()
        db_session.commit()
        db_session.refresh(user)
        after_update = datetime.utcnow()
        
        assert before_update <= user.updated_at <= after_update
    
    def test_user_relationships(self, db_session: Session, test_user: User):
        """Test user relationships with activities."""
        # Create an activity for the user
        activity = Activity(
            title="Test Activity",
            description="Test Description",
            category="test",
            difficulty_level="beginner",
            creator_id=test_user.id
        )
        
        db_session.add(activity)
        db_session.commit()
        db_session.refresh(test_user)
        
        assert len(test_user.activities) == 1
        assert test_user.activities[0].title == "Test Activity"
        assert test_user.activities[0].creator_id == test_user.id


class TestActivityModel:
    """Test Activity model database operations."""
    
    def test_create_activity(self, db_session: Session, test_user: User):
        """Test creating an activity in the database."""
        activity_data = {
            "title": "Test Activity",
            "description": "A test activity for learning",
            "category": "technology",
            "difficulty_level": "intermediate",
            "duration_minutes": 90,
            "location": "Online",
            "equipment_needed": "Computer, Internet",
            "learning_objectives": "Learn testing concepts",
            "is_published": True,
            "creator_id": test_user.id
        }
        
        activity = Activity(**activity_data)
        db_session.add(activity)
        db_session.commit()
        db_session.refresh(activity)
        
        assert activity.id is not None
        assert activity.title == activity_data["title"]
        assert activity.description == activity_data["description"]
        assert activity.category == activity_data["category"]
        assert activity.difficulty_level == activity_data["difficulty_level"]
        assert activity.duration_minutes == activity_data["duration_minutes"]
        assert activity.location == activity_data["location"]
        assert activity.equipment_needed == activity_data["equipment_needed"]
        assert activity.learning_objectives == activity_data["learning_objectives"]
        assert activity.is_published == activity_data["is_published"]
        assert activity.creator_id == activity_data["creator_id"]
        assert activity.created_at is not None
    
    def test_activity_required_fields(self, db_session: Session, test_user: User):
        """Test that required fields cannot be null."""
        # Test missing title
        with pytest.raises(IntegrityError):
            activity = Activity(
                category="test",
                creator_id=test_user.id
            )
            db_session.add(activity)
            db_session.commit()
        
        db_session.rollback()
        
        # Test missing category
        with pytest.raises(IntegrityError):
            activity = Activity(
                title="Test Activity",
                creator_id=test_user.id
            )
            db_session.add(activity)
            db_session.commit()
    
    def test_activity_foreign_key_constraint(self, db_session: Session):
        """Test that creator_id must reference a valid user."""
        activity = Activity(
            title="Test Activity",
            category="test",
            creator_id=999999  # Non-existent user ID
        )
        
        db_session.add(activity)
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_activity_default_values(self, db_session: Session, test_user: User):
        """Test default values for activity fields."""
        activity = Activity(
            title="Minimal Activity",
            category="test",
            creator_id=test_user.id
        )
        
        db_session.add(activity)
        db_session.commit()
        db_session.refresh(activity)
        
        assert activity.difficulty_level == "beginner"  # Default value
        assert activity.is_published is False  # Default value
        assert activity.description is None  # Nullable field
        assert activity.duration_minutes is None  # Nullable field
    
    def test_activity_relationships(self, db_session: Session, test_user: User):
        """Test activity relationships."""
        activity = Activity(
            title="Test Activity",
            category="test",
            creator_id=test_user.id
        )
        
        db_session.add(activity)
        db_session.commit()
        db_session.refresh(activity)
        
        assert activity.creator is not None
        assert activity.creator.id == test_user.id
        assert activity.creator.username == test_user.username
    
    def test_activity_timestamps(self, db_session: Session, test_user: User):
        """Test that timestamps are set correctly."""
        activity = Activity(
            title="Test Activity",
            category="test",
            creator_id=test_user.id
        )
        
        before_create = datetime.utcnow()
        db_session.add(activity)
        db_session.commit()
        db_session.refresh(activity)
        after_create = datetime.utcnow()
        
        assert before_create <= activity.created_at <= after_create
        assert activity.updated_at is None  # Only set on updates
        
        # Test update timestamp
        activity.title = "Updated Activity"
        before_update = datetime.utcnow()
        db_session.commit()
        db_session.refresh(activity)
        after_update = datetime.utcnow()
        
        assert before_update <= activity.updated_at <= after_update


class TestActivitySuggestionModel:
    """Test ActivitySuggestion model database operations."""
    
    def test_create_activity_suggestion(self, db_session: Session, test_user: User, test_activity: Activity):
        """Test creating an activity suggestion."""
        suggestion = ActivitySuggestion(
            user_id=test_user.id,
            activity_id=test_activity.id,
            suggestion_reason="Based on your interests in technology",
            ai_generated=True
        )
        
        db_session.add(suggestion)
        db_session.commit()
        db_session.refresh(suggestion)
        
        assert suggestion.id is not None
        assert suggestion.user_id == test_user.id
        assert suggestion.activity_id == test_activity.id
        assert suggestion.suggestion_reason == "Based on your interests in technology"
        assert suggestion.ai_generated is True
        assert suggestion.created_at is not None
    
    def test_activity_suggestion_foreign_keys(self, db_session: Session):
        """Test foreign key constraints for activity suggestions."""
        # Test invalid user_id
        with pytest.raises(IntegrityError):
            suggestion = ActivitySuggestion(
                user_id=999999,  # Non-existent user
                activity_id=1,
                suggestion_reason="Test"
            )
            db_session.add(suggestion)
            db_session.commit()
        
        db_session.rollback()
        
        # Test invalid activity_id
        with pytest.raises(IntegrityError):
            suggestion = ActivitySuggestion(
                user_id=1,
                activity_id=999999,  # Non-existent activity
                suggestion_reason="Test"
            )
            db_session.add(suggestion)
            db_session.commit()
    
    def test_activity_suggestion_relationships(self, db_session: Session, test_user: User, test_activity: Activity):
        """Test activity suggestion relationships."""
        suggestion = ActivitySuggestion(
            user_id=test_user.id,
            activity_id=test_activity.id,
            suggestion_reason="Test suggestion"
        )
        
        db_session.add(suggestion)
        db_session.commit()
        db_session.refresh(suggestion)
        
        assert suggestion.user is not None
        assert suggestion.user.id == test_user.id
        assert suggestion.activity is not None
        assert suggestion.activity.id == test_activity.id


class TestDatabaseQueries:
    """Test complex database queries and operations."""
    
    def test_filter_published_activities(self, db_session: Session, test_user: User):
        """Test filtering activities by published status."""
        # Create published and unpublished activities
        published_activity = Activity(
            title="Published Activity",
            category="test",
            is_published=True,
            creator_id=test_user.id
        )
        unpublished_activity = Activity(
            title="Unpublished Activity",
            category="test",
            is_published=False,
            creator_id=test_user.id
        )
        
        db_session.add_all([published_activity, unpublished_activity])
        db_session.commit()
        
        # Query only published activities
        published_activities = db_session.query(Activity).filter(
            Activity.is_published == True
        ).all()
        
        assert len(published_activities) == 1
        assert published_activities[0].title == "Published Activity"
    
    def test_filter_activities_by_category(self, db_session: Session, test_user: User):
        """Test filtering activities by category."""
        # Create activities with different categories
        tech_activity = Activity(
            title="Tech Activity",
            category="technology",
            creator_id=test_user.id
        )
        sports_activity = Activity(
            title="Sports Activity",
            category="sports",
            creator_id=test_user.id
        )
        
        db_session.add_all([tech_activity, sports_activity])
        db_session.commit()
        
        # Query activities by category
        tech_activities = db_session.query(Activity).filter(
            Activity.category == "technology"
        ).all()
        
        assert len(tech_activities) == 1
        assert tech_activities[0].title == "Tech Activity"
    
    def test_filter_activities_by_difficulty(self, db_session: Session, test_user: User):
        """Test filtering activities by difficulty level."""
        # Create activities with different difficulty levels
        beginner_activity = Activity(
            title="Beginner Activity",
            category="test",
            difficulty_level="beginner",
            creator_id=test_user.id
        )
        advanced_activity = Activity(
            title="Advanced Activity",
            category="test",
            difficulty_level="advanced",
            creator_id=test_user.id
        )
        
        db_session.add_all([beginner_activity, advanced_activity])
        db_session.commit()
        
        # Query activities by difficulty
        beginner_activities = db_session.query(Activity).filter(
            Activity.difficulty_level == "beginner"
        ).all()
        
        assert len(beginner_activities) == 1
        assert beginner_activities[0].title == "Beginner Activity"
    
    def test_pagination_queries(self, db_session: Session, test_user: User):
        """Test pagination with offset and limit."""
        # Create multiple activities
        activities = []
        for i in range(10):
            activity = Activity(
                title=f"Activity {i}",
                category="test",
                creator_id=test_user.id
            )
            activities.append(activity)
        
        db_session.add_all(activities)
        db_session.commit()
        
        # Test pagination
        page_1 = db_session.query(Activity).offset(0).limit(5).all()
        page_2 = db_session.query(Activity).offset(5).limit(5).all()
        
        assert len(page_1) == 5
        assert len(page_2) == 5
        
        # Ensure no overlap
        page_1_ids = [activity.id for activity in page_1]
        page_2_ids = [activity.id for activity in page_2]
        assert not set(page_1_ids).intersection(set(page_2_ids))
    
    def test_count_queries(self, db_session: Session, test_user: User):
        """Test counting records."""
        # Create some activities
        for i in range(5):
            activity = Activity(
                title=f"Activity {i}",
                category="test",
                creator_id=test_user.id
            )
            db_session.add(activity)
        
        db_session.commit()
        
        # Count total activities
        total_count = db_session.query(Activity).count()
        assert total_count == 5
        
        # Count published activities
        published_count = db_session.query(Activity).filter(
            Activity.is_published == True
        ).count()
        assert published_count == 0  # All are unpublished by default
    
    def test_aggregate_queries(self, db_session: Session, test_user: User):
        """Test aggregate functions."""
        # Create activities with different durations
        durations = [30, 60, 90, 120, 150]
        for i, duration in enumerate(durations):
            activity = Activity(
                title=f"Activity {i}",
                category="test",
                duration_minutes=duration,
                creator_id=test_user.id
            )
            db_session.add(activity)
        
        db_session.commit()
        
        # Test aggregate functions
        avg_duration = db_session.query(func.avg(Activity.duration_minutes)).scalar()
        max_duration = db_session.query(func.max(Activity.duration_minutes)).scalar()
        min_duration = db_session.query(func.min(Activity.duration_minutes)).scalar()
        
        assert avg_duration == 90.0  # Average of [30, 60, 90, 120, 150]
        assert max_duration == 150
        assert min_duration == 30
    
    def test_join_queries(self, db_session: Session, test_user: User):
        """Test queries with joins."""
        # Create an activity
        activity = Activity(
            title="Test Activity",
            category="test",
            creator_id=test_user.id
        )
        db_session.add(activity)
        db_session.commit()
        
        # Query activities with creator information
        result = db_session.query(Activity, User).join(User).filter(
            Activity.creator_id == test_user.id
        ).first()
        
        assert result is not None
        activity_obj, user_obj = result
        assert activity_obj.title == "Test Activity"
        assert user_obj.id == test_user.id


class TestDatabaseTransactions:
    """Test database transaction handling."""
    
    def test_rollback_on_error(self, db_session: Session, test_user: User):
        """Test that transactions are rolled back on errors."""
        # Start with a count of activities
        initial_count = db_session.query(Activity).count()
        
        try:
            # Create a valid activity
            activity1 = Activity(
                title="Valid Activity",
                category="test",
                creator_id=test_user.id
            )
            db_session.add(activity1)
            
            # Create an invalid activity (missing required field)
            activity2 = Activity(
                # Missing title and category - should cause error
                creator_id=test_user.id
            )
            db_session.add(activity2)
            
            # This should fail
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
        
        # Count should be unchanged due to rollback
        final_count = db_session.query(Activity).count()
        assert final_count == initial_count
    
    def test_nested_transactions(self, db_session: Session, test_user: User):
        """Test nested transaction behavior."""
        initial_count = db_session.query(Activity).count()
        
        # Create first activity
        activity1 = Activity(
            title="Activity 1",
            category="test",
            creator_id=test_user.id
        )
        db_session.add(activity1)
        db_session.flush()  # Flush but don't commit
        
        # Create second activity
        activity2 = Activity(
            title="Activity 2",
            category="test",
            creator_id=test_user.id
        )
        db_session.add(activity2)
        
        # Commit both
        db_session.commit()
        
        final_count = db_session.query(Activity).count()
        assert final_count == initial_count + 2


class TestDatabasePerformance:
    """Test database performance and optimization."""
    
    def test_bulk_insert_performance(self, db_session: Session, test_user: User):
        """Test bulk insert operations."""
        import time
        
        # Create a large number of activities
        activities = []
        for i in range(100):
            activity = Activity(
                title=f"Bulk Activity {i}",
                category="test",
                creator_id=test_user.id
            )
            activities.append(activity)
        
        # Measure bulk insert time
        start_time = time.time()
        db_session.add_all(activities)
        db_session.commit()
        end_time = time.time()
        
        # Should complete reasonably quickly (less than 5 seconds)
        assert (end_time - start_time) < 5.0
        
        # Verify all activities were created
        count = db_session.query(Activity).filter(
            Activity.title.like("Bulk Activity%")
        ).count()
        assert count == 100
    
    def test_query_performance_with_indexes(self, db_session: Session, test_user: User):
        """Test that indexed columns perform well."""
        import time
        
        # Create many activities
        for i in range(500):
            activity = Activity(
                title=f"Performance Test Activity {i}",
                category=f"category_{i % 10}",  # 10 different categories
                creator_id=test_user.id
            )
            db_session.add(activity)
        
        db_session.commit()
        
        # Test query performance on indexed column (category)
        start_time = time.time()
        results = db_session.query(Activity).filter(
            Activity.category == "category_5"
        ).all()
        end_time = time.time()
        
        # Should be fast (less than 1 second)
        assert (end_time - start_time) < 1.0
        assert len(results) == 50  # Should find 50 activities
    
    def test_connection_handling(self, db_session: Session):
        """Test that database connections are handled properly."""
        # This test ensures that the session is working correctly
        # and can execute multiple queries without issues
        
        # Execute multiple queries to test connection stability
        for i in range(10):
            result = db_session.execute("SELECT 1").scalar()
            assert result == 1
        
        # Test that the session is still valid after multiple operations
        count = db_session.query(User).count()
        assert count >= 0  # Should not raise an exception