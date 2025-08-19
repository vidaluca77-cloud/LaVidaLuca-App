"""
Unit tests for service layer components.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session

from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    verify_token
)
from app.api.deps import get_current_user
from app.services.openai_service import OpenAIService
from app.models.models import User, Activity


class TestSecurityService:
    """Test security service functions."""
    
    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        # Hash should be different from original password
        assert hashed != password
        
        # Should verify correctly
        assert verify_password(password, hashed) is True
        
        # Should not verify with wrong password
        assert verify_password("wrongpassword", hashed) is False
    
    def test_password_hash_uniqueness(self):
        """Test that same password produces different hashes."""
        password = "testpassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Hashes should be different due to salt
        assert hash1 != hash2
        
        # But both should verify the same password
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True
    
    def test_create_access_token(self):
        """Test JWT token creation."""
        user_id = 123
        token = create_access_token(subject=user_id)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_with_expiry(self):
        """Test JWT token creation with custom expiry."""
        from datetime import timedelta
        
        user_id = 123
        custom_expiry = timedelta(minutes=60)
        token = create_access_token(subject=user_id, expires_delta=custom_expiry)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    @patch('app.core.security.jwt.decode')
    def test_verify_token_valid(self, mock_decode):
        """Test token verification with valid token."""
        mock_decode.return_value = {"sub": "123"}
        
        token = "valid_token"
        user_id = verify_token(token)
        
        assert user_id == 123
        mock_decode.assert_called_once()
    
    @patch('app.core.security.jwt.decode')
    def test_verify_token_invalid(self, mock_decode):
        """Test token verification with invalid token."""
        from jose import JWTError
        mock_decode.side_effect = JWTError("Invalid token")
        
        token = "invalid_token"
        user_id = verify_token(token)
        
        assert user_id is None
        mock_decode.assert_called_once()
    
    def test_get_current_user_valid_token(self, db_session: Session, test_user: User):
        """Test getting current user with valid token."""
        from app.api.deps import get_current_user
        from fastapi.security import HTTPAuthorizationCredentials
        
        # Create mock credentials
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=create_access_token(subject=test_user.id)
        )
        
        # Mock the database query
        with patch.object(db_session, 'query') as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = test_user
            
            user = get_current_user(db_session, credentials)
            
            assert user == test_user
    
    def test_get_current_user_invalid_token(self, db_session: Session):
        """Test getting current user with invalid token."""
        from app.api.deps import get_current_user
        from fastapi.security import HTTPAuthorizationCredentials
        from fastapi import HTTPException
        
        # Create mock credentials with invalid token
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="invalid_token"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(db_session, credentials)
        
        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in str(exc_info.value.detail)
    
    def test_get_current_user_malformed_token(self, db_session: Session):
        """Test getting current user with malformed token."""
        from app.api.deps import get_current_user
        from fastapi.security import HTTPAuthorizationCredentials
        from fastapi import HTTPException
        
        # Create mock credentials with malformed token
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="malformed_token"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(db_session, credentials)
        
        assert exc_info.value.status_code == 401


class TestOpenAIService:
    """Test OpenAI service integration."""
    
    def test_openai_service_initialization(self):
        """Test OpenAI service can be initialized."""
        service = OpenAIService()
        assert service is not None
    
    @patch('app.services.openai_service.openai.OpenAI')
    def test_generate_activity_suggestions_success(self, mock_openai_client):
        """Test successful activity suggestion generation."""
        # Mock OpenAI client response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '''
        {
            "suggestions": [
                {
                    "title": "Learn Python Basics",
                    "description": "Introduction to Python programming",
                    "category": "technology",
                    "difficulty_level": "beginner",
                    "duration_minutes": 60
                }
            ]
        }
        '''
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_client.return_value = mock_client
        
        service = OpenAIService()
        user_preferences = {
            "interests": ["programming", "technology"],
            "skill_level": "beginner",
            "available_time": 60
        }
        
        suggestions = service.generate_activity_suggestions(user_preferences)
        
        assert len(suggestions) == 1
        assert suggestions[0]["title"] == "Learn Python Basics"
        assert suggestions[0]["category"] == "technology"
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('app.services.openai_service.openai.OpenAI')
    def test_generate_activity_suggestions_api_error(self, mock_openai_client):
        """Test handling of OpenAI API errors."""
        # Mock API error
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai_client.return_value = mock_client
        
        service = OpenAIService()
        user_preferences = {"interests": ["programming"]}
        
        # Should handle error gracefully
        suggestions = service.generate_activity_suggestions(user_preferences)
        
        assert suggestions == []  # Should return empty list on error
    
    @patch('app.services.openai_service.openai.OpenAI')
    def test_generate_activity_suggestions_invalid_json(self, mock_openai_client):
        """Test handling of invalid JSON response."""
        # Mock response with invalid JSON
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Invalid JSON response"
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_client.return_value = mock_client
        
        service = OpenAIService()
        user_preferences = {"interests": ["programming"]}
        
        # Should handle invalid JSON gracefully
        suggestions = service.generate_activity_suggestions(user_preferences)
        
        assert suggestions == []  # Should return empty list on JSON error
    
    @patch('app.services.openai_service.openai.OpenAI')
    def test_analyze_activity_content_success(self, mock_openai_client):
        """Test successful activity content analysis."""
        # Mock OpenAI client response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '''
        {
            "analysis": {
                "difficulty_assessment": "This activity is suitable for beginners",
                "learning_objectives": ["Learn basic concepts", "Understand fundamentals"],
                "estimated_duration": 45,
                "required_skills": ["Basic computer literacy"]
            }
        }
        '''
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_client.return_value = mock_client
        
        service = OpenAIService()
        activity_content = {
            "title": "Introduction to Programming",
            "description": "Learn the basics of programming",
            "category": "technology"
        }
        
        analysis = service.analyze_activity_content(activity_content)
        
        assert "analysis" in analysis
        assert "difficulty_assessment" in analysis["analysis"]
        assert analysis["analysis"]["estimated_duration"] == 45
        mock_client.chat.completions.create.assert_called_once()
    
    def test_format_user_preferences(self):
        """Test user preferences formatting for OpenAI prompts."""
        service = OpenAIService()
        preferences = {
            "interests": ["technology", "sports"],
            "skill_level": "intermediate",
            "available_time": 120,
            "learning_style": "hands-on"
        }
        
        formatted = service._format_user_preferences(preferences)
        
        assert "interests: technology, sports" in formatted.lower()
        assert "skill_level: intermediate" in formatted.lower()
        assert "available_time: 120" in formatted.lower()
        assert "learning_style: hands-on" in formatted.lower()
    
    def test_validate_suggestion_format(self):
        """Test validation of suggestion format."""
        service = OpenAIService()
        
        # Valid suggestion
        valid_suggestion = {
            "title": "Test Activity",
            "description": "Test description",
            "category": "technology",
            "difficulty_level": "beginner",
            "duration_minutes": 60
        }
        
        assert service._validate_suggestion_format(valid_suggestion) is True
        
        # Invalid suggestion (missing required fields)
        invalid_suggestion = {
            "title": "Test Activity",
            "category": "technology"
            # Missing description, difficulty_level, duration_minutes
        }
        
        assert service._validate_suggestion_format(invalid_suggestion) is False
    
    @patch('app.services.openai_service.settings.OPENAI_API_KEY', None)
    def test_openai_service_without_api_key(self):
        """Test OpenAI service behavior when API key is not configured."""
        service = OpenAIService()
        
        # Should handle missing API key gracefully
        user_preferences = {"interests": ["programming"]}
        suggestions = service.generate_activity_suggestions(user_preferences)
        
        assert suggestions == []  # Should return empty list when no API key


class TestActivityService:
    """Test activity-related service functions."""
    
    def test_filter_activities_by_user_preferences(self, db_session: Session, test_activities: list):
        """Test filtering activities based on user preferences."""
        from app.services.activity_service import ActivityService
        
        service = ActivityService(db_session)
        
        # Test filtering by category
        preferences = {"preferred_categories": ["technology"]}
        tech_activities = service.filter_by_preferences(test_activities, preferences)
        
        for activity in tech_activities:
            assert activity.category == "technology"
    
    def test_calculate_activity_match_score(self):
        """Test activity matching score calculation."""
        from app.services.activity_service import ActivityService
        
        service = ActivityService(None)  # No DB needed for this test
        
        user_preferences = {
            "interests": ["technology", "programming"],
            "skill_level": "beginner",
            "preferred_duration": 60
        }
        
        # Perfect match activity
        perfect_activity = {
            "category": "technology",
            "difficulty_level": "beginner",
            "duration_minutes": 60,
            "title": "Learn Programming Basics",
            "description": "Introduction to programming concepts"
        }
        
        # Calculate match score
        score = service.calculate_match_score(perfect_activity, user_preferences)
        
        assert score > 0.8  # Should be a high match score
        assert score <= 1.0  # Should not exceed 1.0
    
    def test_get_activity_recommendations(self, db_session: Session, test_user: User, test_activities: list):
        """Test getting personalized activity recommendations."""
        from app.services.activity_service import ActivityService
        
        service = ActivityService(db_session)
        
        user_preferences = {
            "interests": ["technology"],
            "skill_level": "beginner"
        }
        
        recommendations = service.get_recommendations(test_user.id, user_preferences)
        
        assert isinstance(recommendations, list)
        # Should return activities sorted by relevance
        if len(recommendations) > 1:
            # Check that activities are sorted by match score (descending)
            for i in range(len(recommendations) - 1):
                curr_score = recommendations[i].get("match_score", 0)
                next_score = recommendations[i + 1].get("match_score", 0)
                assert curr_score >= next_score


class TestUserService:
    """Test user-related service functions."""
    
    def test_create_user_service(self, db_session: Session):
        """Test user creation through service layer."""
        from app.services.user_service import UserService
        
        service = UserService(db_session)
        
        user_data = {
            "email": "servicetest@example.com",
            "username": "serviceuser",
            "password": "testpassword",
            "full_name": "Service Test User"
        }
        
        user = service.create_user(user_data)
        
        assert user.id is not None
        assert user.email == user_data["email"]
        assert user.username == user_data["username"]
        assert user.full_name == user_data["full_name"]
        assert verify_password(user_data["password"], user.hashed_password)
    
    def test_authenticate_user_service(self, db_session: Session, test_user: User):
        """Test user authentication through service layer."""
        from app.services.user_service import UserService
        
        service = UserService(db_session)
        
        # Test successful authentication
        authenticated_user = service.authenticate(test_user.username, "testpassword")
        assert authenticated_user is not None
        assert authenticated_user.id == test_user.id
        
        # Test failed authentication
        failed_auth = service.authenticate(test_user.username, "wrongpassword")
        assert failed_auth is None
        
        # Test non-existent user
        no_user = service.authenticate("nonexistent", "password")
        assert no_user is None
    
    def test_update_user_profile_service(self, db_session: Session, test_user: User):
        """Test updating user profile through service layer."""
        from app.services.user_service import UserService
        
        service = UserService(db_session)
        
        update_data = {
            "full_name": "Updated Full Name",
            "email": "updated@example.com"
        }
        
        updated_user = service.update_profile(test_user.id, update_data)
        
        assert updated_user.full_name == update_data["full_name"]
        assert updated_user.email == update_data["email"]
        assert updated_user.username == test_user.username  # Should remain unchanged
    
    def test_get_user_activity_history(self, db_session: Session, test_user: User, test_activities: list):
        """Test getting user's activity history."""
        from app.services.user_service import UserService
        
        service = UserService(db_session)
        
        # Get user's created activities
        user_activities = service.get_user_activities(test_user.id)
        
        assert isinstance(user_activities, list)
        for activity in user_activities:
            assert activity.creator_id == test_user.id


class TestValidationService:
    """Test validation service functions."""
    
    def test_validate_email_format(self):
        """Test email validation."""
        from app.services.validation_service import ValidationService
        
        service = ValidationService()
        
        # Valid emails
        assert service.validate_email("test@example.com") is True
        assert service.validate_email("user.name+tag@domain.co.uk") is True
        
        # Invalid emails
        assert service.validate_email("invalid-email") is False
        assert service.validate_email("@domain.com") is False
        assert service.validate_email("user@") is False
        assert service.validate_email("") is False
    
    def test_validate_password_strength(self):
        """Test password strength validation."""
        from app.services.validation_service import ValidationService
        
        service = ValidationService()
        
        # Strong passwords
        assert service.validate_password_strength("StrongPassword123!") is True
        assert service.validate_password_strength("AnotherGood1@") is True
        
        # Weak passwords
        assert service.validate_password_strength("weak") is False
        assert service.validate_password_strength("12345678") is False
        assert service.validate_password_strength("password") is False
        assert service.validate_password_strength("") is False
    
    def test_validate_activity_data(self):
        """Test activity data validation."""
        from app.services.validation_service import ValidationService
        
        service = ValidationService()
        
        # Valid activity data
        valid_data = {
            "title": "Valid Activity",
            "description": "A valid activity description",
            "category": "technology",
            "difficulty_level": "beginner",
            "duration_minutes": 60
        }
        
        validation_result = service.validate_activity_data(valid_data)
        assert validation_result["valid"] is True
        assert len(validation_result["errors"]) == 0
        
        # Invalid activity data
        invalid_data = {
            "title": "",  # Empty title
            "category": "invalid_category",
            "difficulty_level": "invalid_level",
            "duration_minutes": -10  # Negative duration
        }
        
        validation_result = service.validate_activity_data(invalid_data)
        assert validation_result["valid"] is False
        assert len(validation_result["errors"]) > 0
    
    def test_sanitize_user_input(self):
        """Test user input sanitization."""
        from app.services.validation_service import ValidationService
        
        service = ValidationService()
        
        # Test HTML tag removal
        dirty_input = "<script>alert('xss')</script>Clean text"
        clean_input = service.sanitize_input(dirty_input)
        assert "<script>" not in clean_input
        assert "Clean text" in clean_input
        
        # Test SQL injection prevention
        sql_injection = "'; DROP TABLE users; --"
        sanitized = service.sanitize_input(sql_injection)
        assert "DROP TABLE" not in sanitized.upper()


class TestCacheService:
    """Test caching service functionality."""
    
    @patch('app.services.cache_service.redis')
    def test_cache_set_and_get(self, mock_redis):
        """Test setting and getting cache values."""
        from app.services.cache_service import CacheService
        
        # Mock Redis client
        mock_redis_client = Mock()
        mock_redis.Redis.return_value = mock_redis_client
        mock_redis_client.get.return_value = b'{"cached": "data"}'
        
        service = CacheService()
        
        # Test setting cache
        service.set("test_key", {"test": "data"}, expiry=300)
        mock_redis_client.setex.assert_called_once()
        
        # Test getting cache
        result = service.get("test_key")
        mock_redis_client.get.assert_called_with("test_key")
        assert result == {"cached": "data"}
    
    @patch('app.services.cache_service.redis')
    def test_cache_delete(self, mock_redis):
        """Test deleting cache values."""
        from app.services.cache_service import CacheService
        
        mock_redis_client = Mock()
        mock_redis.Redis.return_value = mock_redis_client
        
        service = CacheService()
        service.delete("test_key")
        
        mock_redis_client.delete.assert_called_with("test_key")
    
    def test_cache_key_generation(self):
        """Test cache key generation."""
        from app.services.cache_service import CacheService
        
        service = CacheService()
        
        # Test simple key
        key1 = service.generate_key("user", 123)
        assert "user:123" in key1
        
        # Test complex key
        key2 = service.generate_key("activity", "search", category="tech", difficulty="beginner")
        assert "activity:search" in key2
        assert "category" in key2
        assert "difficulty" in key2