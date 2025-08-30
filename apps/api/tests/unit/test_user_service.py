import pytest
from app.services.user_service import UserService
from app.schemas.schemas import UserCreate, UserUpdate, UserProfileUpdate

class TestUserService:
    def test_create_user(self, db_session):
        """Test user creation."""
        user_service = UserService(db_session)
        user_create = UserCreate(
            email="newuser@example.com",
            username="newuser",
            password="password123",
            first_name="New",
            last_name="User"
        )
        
        user = user_service.create_user(user_create)
        
        assert user.email == "newuser@example.com"
        assert user.username == "newuser"
        assert user.first_name == "New"
        assert user.last_name == "User"
        assert user.is_active is True
        assert user.hashed_password != "password123"  # Should be hashed

    def test_get_user_by_email(self, db_session, test_user):
        """Test getting user by email."""
        user_service = UserService(db_session)
        found_user = user_service.get_user_by_email("test@example.com")
        
        assert found_user is not None
        assert found_user.email == "test@example.com"

    def test_get_user_by_username(self, db_session, test_user):
        """Test getting user by username."""
        user_service = UserService(db_session)
        found_user = user_service.get_user_by_username("testuser")
        
        assert found_user is not None
        assert found_user.username == "testuser"

    def test_authenticate_user(self, db_session, test_user):
        """Test user authentication."""
        user_service = UserService(db_session)
        
        # Valid credentials
        authenticated_user = user_service.authenticate_user("testuser", "testpassword123")
        assert authenticated_user is not None
        assert authenticated_user.username == "testuser"
        
        # Invalid password
        assert user_service.authenticate_user("testuser", "wrongpassword") is None
        
        # Invalid username
        assert user_service.authenticate_user("wronguser", "testpassword123") is None

    def test_update_user(self, db_session, test_user):
        """Test user update."""
        user_service = UserService(db_session)
        user_update = UserUpdate(
            first_name="Updated",
            last_name="Name"
        )
        
        updated_user = user_service.update_user(test_user.id, user_update)
        
        assert updated_user is not None
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"

    def test_user_profile_operations(self, db_session, test_user):
        """Test user profile creation and update."""
        user_service = UserService(db_session)
        
        # Get initial profile (created automatically)
        profile = user_service.get_user_profile(test_user.id)
        assert profile is not None
        
        # Update profile
        profile_update = UserProfileUpdate(
            bio="Test bio",
            skills=["elevage", "hygiene"],
            availability=["weekend", "matin"],
            preferences=["agri", "nature"]
        )
        
        updated_profile = user_service.update_user_profile(test_user.id, profile_update)
        
        assert updated_profile is not None
        assert updated_profile.bio == "Test bio"
        assert "elevage" in updated_profile.skills
        assert "weekend" in updated_profile.availability
        assert "agri" in updated_profile.preferences