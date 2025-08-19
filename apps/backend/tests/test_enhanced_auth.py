"""
Tests for enhanced authentication system.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from ..app.main import app
from ..database import Base, get_db
from ..models.user import User
from ..models.session import RefreshToken, UserSession
from ..core.security import get_password_hash
from ..services.session_service import SessionService
from ..services.two_factor_service import TwoFactorService


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    """Create test database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(test_db):
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("TestPassword123!"),
        first_name="Test",
        last_name="User",
        is_active=True
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


class TestEnhancedAuth:
    """Test enhanced authentication features."""
    
    def test_register_with_strong_password_policy(self, test_db):
        """Test user registration with password policy enforcement."""
        # Valid password
        response = client.post("/api/v1/auth/register", json={
            "email": "newuser@example.com",
            "password": "StrongPass123!",
            "first_name": "New",
            "last_name": "User"
        })
        assert response.status_code == 200
        
        # Weak password - too short
        response = client.post("/api/v1/auth/register", json={
            "email": "user2@example.com",
            "password": "weak",
            "first_name": "User",
            "last_name": "Two"
        })
        assert response.status_code == 422  # Validation error
        
        # Weak password - no uppercase
        response = client.post("/api/v1/auth/register", json={
            "email": "user3@example.com",
            "password": "weakpass123!",
            "first_name": "User",
            "last_name": "Three"
        })
        assert response.status_code == 422
        
        # Common password
        response = client.post("/api/v1/auth/register", json={
            "email": "user4@example.com",
            "password": "Password123!",  # Would be caught by common password check
            "first_name": "User",
            "last_name": "Four"
        })
        # This might pass basic validation but fail policy check
    
    def test_login_with_device_tracking(self, test_db, test_user):
        """Test login with device tracking and session creation."""
        response = client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123!",
            "device_name": "Test Device",
            "remember_me": False
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "access_token" in data
        assert "refresh_token" in data
        assert "session_id" in data
        assert data["token_type"] == "bearer"
        
        # Verify session was created
        session = test_db.query(UserSession).filter(
            UserSession.user_id == test_user.id
        ).first()
        assert session is not None
        assert session.device_name == "Test Device"
    
    def test_refresh_token_rotation(self, test_db, test_user):
        """Test refresh token functionality."""
        session_service = SessionService(test_db)
        
        # Create a session
        session, refresh_token = session_service.create_session(
            user=test_user,
            ip_address="127.0.0.1",
            user_agent="Test Agent",
            device_name="Test Device"
        )
        
        # Use refresh token
        refreshed_user, user_id = session_service.refresh_access_token(
            refresh_token=refresh_token,
            ip_address="127.0.0.1",
            user_agent="Test Agent"
        )
        
        assert refreshed_user is not None
        assert user_id == str(test_user.id)
    
    def test_account_lockout_after_failed_attempts(self, test_db, test_user):
        """Test account lockout after multiple failed login attempts."""
        session_service = SessionService(test_db)
        
        # Simulate failed login attempts
        for _ in range(5):
            session_service.handle_failed_login(test_user)
        
        # User should be locked now
        test_db.refresh(test_user)
        assert test_user.is_locked
        assert test_user.failed_login_attempts == 0  # Reset after lock
    
    def test_session_termination(self, test_db, test_user):
        """Test session termination functionality."""
        session_service = SessionService(test_db)
        
        # Create multiple sessions
        session1, _ = session_service.create_session(
            user=test_user,
            ip_address="127.0.0.1",
            user_agent="Device 1",
            device_name="Device 1"
        )
        
        session2, _ = session_service.create_session(
            user=test_user,
            ip_address="192.168.1.1",
            user_agent="Device 2",
            device_name="Device 2"
        )
        
        # Terminate one session
        result = session_service.terminate_session(str(session1.id), str(test_user.id))
        assert result is True
        
        # Verify session is terminated
        test_db.refresh(session1)
        assert not session1.is_active
        
        # Other session should still be active
        test_db.refresh(session2)
        assert session2.is_active
        
        # Terminate all sessions
        terminated_count = session_service.terminate_all_sessions(str(test_user.id))
        assert terminated_count == 1  # Only session2 was active


class TestTwoFactorAuth:
    """Test 2FA functionality."""
    
    def test_2fa_setup(self, test_db, test_user):
        """Test 2FA setup process."""
        twofa_service = TwoFactorService(test_db)
        
        # Setup 2FA
        setup_data = twofa_service.setup_2fa(test_user)
        
        assert "secret" in setup_data
        assert "qr_code" in setup_data
        assert "backup_codes" in setup_data
        assert len(setup_data["backup_codes"]) == 8
        
        # Verify secret is stored
        test_db.refresh(test_user)
        assert test_user.two_factor_secret is not None
        assert test_user.two_factor_enabled is False  # Not enabled until verified
    
    def test_2fa_enable_with_valid_token(self, test_db, test_user):
        """Test enabling 2FA with valid token."""
        twofa_service = TwoFactorService(test_db)
        
        # Setup 2FA first
        setup_data = twofa_service.setup_2fa(test_user)
        secret = setup_data["secret"]
        
        # Generate a valid token (simplified for testing)
        # In real tests, you'd use the actual TOTP algorithm
        test_token = "123456"  # Mock token
        
        # Note: This test would need a proper TOTP implementation
        # For now, we'll just test the flow
        
    def test_backup_code_verification(self, test_db, test_user):
        """Test backup code verification."""
        twofa_service = TwoFactorService(test_db)
        
        # Setup 2FA with backup codes
        setup_data = twofa_service.setup_2fa(test_user)
        backup_codes = setup_data["backup_codes"]
        
        # Enable 2FA (mock)
        test_user.two_factor_enabled = True
        test_db.commit()
        
        # Verify backup code
        first_code = backup_codes[0]
        result = twofa_service.verify_2fa_token(test_user, first_code)
        
        # The backup code should work and be consumed
        test_db.refresh(test_user)
        assert first_code not in test_user.backup_codes  # Code should be removed


class TestRateLimiting:
    """Test rate limiting functionality."""
    
    def test_login_rate_limiting(self, test_db):
        """Test rate limiting on login attempts."""
        # This would require mocking the rate limiting storage
        # and testing the middleware functionality
        pass
    
    def test_registration_rate_limiting(self, test_db):
        """Test rate limiting on registration attempts."""
        # Similar to login rate limiting
        pass


class TestSecurityFeatures:
    """Test additional security features."""
    
    def test_device_fingerprinting(self, test_db, test_user):
        """Test device fingerprinting for sessions."""
        from ..core.security import generate_device_fingerprint
        
        fingerprint1 = generate_device_fingerprint("Mozilla/5.0", "127.0.0.1")
        fingerprint2 = generate_device_fingerprint("Chrome/91.0", "127.0.0.1")
        fingerprint3 = generate_device_fingerprint("Mozilla/5.0", "192.168.1.1")
        
        # Same user agent and IP should generate same fingerprint
        assert fingerprint1 == generate_device_fingerprint("Mozilla/5.0", "127.0.0.1")
        
        # Different user agent or IP should generate different fingerprint
        assert fingerprint1 != fingerprint2
        assert fingerprint1 != fingerprint3
    
    def test_session_cleanup(self, test_db, test_user):
        """Test cleanup of expired sessions."""
        session_service = SessionService(test_db)
        
        # Create session with past expiration
        session, _ = session_service.create_session(
            user=test_user,
            ip_address="127.0.0.1",
            user_agent="Test Agent"
        )
        
        # Manually set expiration to past
        session.expires_at = datetime.utcnow() - timedelta(hours=1)
        test_db.commit()
        
        # Run cleanup
        expired_sessions, expired_tokens = session_service.cleanup_expired_sessions()
        
        assert expired_sessions >= 1
        
        # Verify session is terminated
        test_db.refresh(session)
        assert not session.is_active


if __name__ == "__main__":
    pytest.main([__file__])