"""
Database integration tests for LaVidaLuca backend.

Tests CRUD operations, data integrity, constraints, and database performance.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from app.db.database import get_db
from app.models.user import User
from app.models.activity import Activity
from app.schemas.user import UserCreate
from app.services.user_service import UserService
from app.services.activity_service import ActivityService


class TestUserCRUDOperations:
    """Test user database operations."""

    @pytest.mark.asyncio
    async def test_create_user_success(self, db_session):
        """Test successful user creation."""
        user_data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "SecurePassword123"
        }
        
        user_service = UserService(db_session)
        user = await user_service.create_user(UserCreate(**user_data))
        
        assert user.email == user_data["email"]
        assert user.first_name == user_data["first_name"]
        assert user.last_name == user_data["last_name"]
        assert user.is_active is True
        assert user.is_verified is False
        assert user.hashed_password is not None
        assert user.hashed_password != user_data["password"]
        assert user.created_at is not None

    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, db_session):
        """Test user creation with duplicate email fails."""
        email = "duplicate@example.com"
        
        # Create first user
        user1 = User(
            email=email,
            first_name="First",
            last_name="User",
            hashed_password="hashed_password"
        )
        db_session.add(user1)
        await db_session.commit()
        
        # Try to create second user with same email
        user2 = User(
            email=email,
            first_name="Second",
            last_name="User",
            hashed_password="hashed_password"
        )
        db_session.add(user2)
        
        with pytest.raises(IntegrityError):
            await db_session.commit()

    @pytest.mark.asyncio
    async def test_read_user_by_id(self, db_session):
        """Test reading user by ID."""
        # Create test user
        user = User(
            email="read_test@example.com",
            first_name="Read",
            last_name="Test",
            hashed_password="hashed_password"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        # Read user by ID
        result = await db_session.execute(select(User).where(User.id == user.id))
        found_user = result.scalar_one_or_none()
        
        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email == user.email

    @pytest.mark.asyncio
    async def test_read_user_by_email(self, db_session):
        """Test reading user by email."""
        email = "email_search@example.com"
        user = User(
            email=email,
            first_name="Email",
            last_name="Search",
            hashed_password="hashed_password"
        )
        db_session.add(user)
        await db_session.commit()
        
        # Read user by email
        result = await db_session.execute(select(User).where(User.email == email))
        found_user = result.scalar_one_or_none()
        
        assert found_user is not None
        assert found_user.email == email

    @pytest.mark.asyncio
    async def test_update_user(self, db_session):
        """Test updating user information."""
        # Create test user
        user = User(
            email="update_test@example.com",
            first_name="Original",
            last_name="Name",
            hashed_password="hashed_password"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        # Update user
        user.first_name = "Updated"
        user.last_name = "Name"
        user.profile = {"bio": "Updated bio"}
        await db_session.commit()
        
        # Verify update
        result = await db_session.execute(select(User).where(User.id == user.id))
        updated_user = result.scalar_one_or_none()
        
        assert updated_user.first_name == "Updated"
        assert updated_user.profile["bio"] == "Updated bio"

    @pytest.mark.asyncio
    async def test_delete_user(self, db_session):
        """Test user deletion (soft delete)."""
        # Create test user
        user = User(
            email="delete_test@example.com",
            first_name="Delete",
            last_name="Test",
            hashed_password="hashed_password"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        # Soft delete user (set is_active to False)
        user.is_active = False
        await db_session.commit()
        
        # Verify user is inactive
        result = await db_session.execute(select(User).where(User.id == user.id))
        deleted_user = result.scalar_one_or_none()
        
        assert deleted_user is not None
        assert deleted_user.is_active is False


class TestActivityCRUDOperations:
    """Test activity database operations."""

    @pytest.mark.asyncio
    async def test_create_activity(self, db_session):
        """Test activity creation."""
        # Create user first
        user = User(
            email="activity_creator@example.com",
            first_name="Activity",
            last_name="Creator",
            hashed_password="hashed_password"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        # Create activity
        activity = Activity(
            title="Test Activity",
            description="A test activity",
            category="test",
            difficulty_level="beginner",
            estimated_duration=60,
            creator_id=user.id
        )
        db_session.add(activity)
        await db_session.commit()
        await db_session.refresh(activity)
        
        assert activity.title == "Test Activity"
        assert activity.creator_id == user.id
        assert activity.created_at is not None

    @pytest.mark.asyncio
    async def test_activity_user_relationship(self, db_session):
        """Test activity-user relationship."""
        # Create user
        user = User(
            email="relationship_test@example.com",
            first_name="Relationship",
            last_name="Test",
            hashed_password="hashed_password"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        # Create multiple activities for user
        activities = []
        for i in range(3):
            activity = Activity(
                title=f"Activity {i}",
                description=f"Description {i}",
                category="test",
                difficulty_level="beginner",
                estimated_duration=30,
                creator_id=user.id
            )
            activities.append(activity)
            db_session.add(activity)
        
        await db_session.commit()
        
        # Test relationship
        result = await db_session.execute(
            select(Activity).where(Activity.creator_id == user.id)
        )
        user_activities = result.scalars().all()
        
        assert len(user_activities) == 3
        for activity in user_activities:
            assert activity.creator_id == user.id


class TestDatabaseConstraints:
    """Test database constraints and data integrity."""

    @pytest.mark.asyncio
    async def test_user_email_unique_constraint(self, db_session):
        """Test email uniqueness constraint."""
        email = "unique_test@example.com"
        
        user1 = User(email=email, hashed_password="pass1")
        user2 = User(email=email, hashed_password="pass2")
        
        db_session.add(user1)
        await db_session.commit()
        
        db_session.add(user2)
        with pytest.raises(IntegrityError):
            await db_session.commit()

    @pytest.mark.asyncio
    async def test_activity_foreign_key_constraint(self, db_session):
        """Test foreign key constraint for activity creator."""
        # Try to create activity with non-existent user
        activity = Activity(
            title="Invalid Activity",
            description="Should fail",
            category="test",
            difficulty_level="beginner",
            estimated_duration=30,
            creator_id="00000000-0000-0000-0000-000000000000"  # Non-existent UUID
        )
        db_session.add(activity)
        
        with pytest.raises(IntegrityError):
            await db_session.commit()

    @pytest.mark.asyncio
    async def test_user_required_fields(self, db_session):
        """Test required field constraints."""
        # Test missing email
        user_no_email = User(hashed_password="password")
        db_session.add(user_no_email)
        
        with pytest.raises(IntegrityError):
            await db_session.commit()


class TestDatabasePerformance:
    """Test database performance and optimization."""

    @pytest.mark.asyncio
    async def test_bulk_user_creation_performance(self, db_session):
        """Test performance of bulk user creation."""
        start_time = datetime.utcnow()
        
        # Create 100 users
        users = []
        for i in range(100):
            user = User(
                email=f"bulk_user_{i}@example.com",
                first_name=f"User{i}",
                last_name="Test",
                hashed_password="hashed_password"
            )
            users.append(user)
        
        db_session.add_all(users)
        await db_session.commit()
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        # Should complete within 5 seconds
        assert duration < 5.0
        
        # Verify all users were created
        result = await db_session.execute(select(func.count(User.id)))
        count = result.scalar()
        assert count >= 100

    @pytest.mark.asyncio
    async def test_complex_query_performance(self, db_session):
        """Test performance of complex queries."""
        # Create test data
        users = []
        activities = []
        
        for i in range(50):
            user = User(
                email=f"perf_user_{i}@example.com",
                first_name=f"User{i}",
                last_name="Test",
                hashed_password="hashed_password"
            )
            users.append(user)
        
        db_session.add_all(users)
        await db_session.commit()
        
        # Create activities for each user
        for user in users:
            for j in range(5):
                activity = Activity(
                    title=f"Activity {j} by {user.first_name}",
                    description="Performance test activity",
                    category="performance",
                    difficulty_level="intermediate",
                    estimated_duration=45,
                    creator_id=user.id
                )
                activities.append(activity)
        
        db_session.add_all(activities)
        await db_session.commit()
        
        # Test complex query performance
        start_time = datetime.utcnow()
        
        # Query with joins and aggregations
        result = await db_session.execute(
            select(User.first_name, func.count(Activity.id).label('activity_count'))
            .join(Activity, User.id == Activity.creator_id)
            .group_by(User.id, User.first_name)
            .having(func.count(Activity.id) > 3)
        )
        results = result.all()
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        # Complex query should complete within 2 seconds
        assert duration < 2.0
        assert len(results) == 50  # All users should have 5 activities


class TestTransactionHandling:
    """Test database transaction handling."""

    @pytest.mark.asyncio
    async def test_transaction_rollback(self, db_session):
        """Test transaction rollback on error."""
        # Start with clean state
        initial_count_result = await db_session.execute(select(func.count(User.id)))
        initial_count = initial_count_result.scalar()
        
        try:
            # Create valid user
            user1 = User(
                email="rollback_test1@example.com",
                first_name="Valid",
                last_name="User",
                hashed_password="hashed_password"
            )
            db_session.add(user1)
            
            # Create invalid user (duplicate email after flush)
            user2 = User(
                email="rollback_test1@example.com",  # Same email
                first_name="Invalid",
                last_name="User",
                hashed_password="hashed_password"
            )
            db_session.add(user2)
            
            # This should fail and rollback the entire transaction
            await db_session.commit()
            
        except IntegrityError:
            await db_session.rollback()
        
        # Verify no users were created due to rollback
        final_count_result = await db_session.execute(select(func.count(User.id)))
        final_count = final_count_result.scalar()
        
        assert final_count == initial_count

    @pytest.mark.asyncio
    async def test_nested_transaction(self, db_session):
        """Test nested transaction handling."""
        # Create savepoint
        savepoint = await db_session.begin_nested()
        
        try:
            # Create user in nested transaction
            user = User(
                email="nested_test@example.com",
                first_name="Nested",
                last_name="Test",
                hashed_password="hashed_password"
            )
            db_session.add(user)
            await db_session.flush()  # Flush to savepoint
            
            # Verify user exists in current transaction
            result = await db_session.execute(
                select(User).where(User.email == "nested_test@example.com")
            )
            found_user = result.scalar_one_or_none()
            assert found_user is not None
            
            # Rollback to savepoint
            await savepoint.rollback()
            
            # Verify user is gone after rollback
            result = await db_session.execute(
                select(User).where(User.email == "nested_test@example.com")
            )
            found_user = result.scalar_one_or_none()
            assert found_user is None
            
        except Exception:
            await savepoint.rollback()
            raise