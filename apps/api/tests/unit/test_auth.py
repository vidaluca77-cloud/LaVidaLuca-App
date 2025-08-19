import pytest
from app.auth.security import create_access_token, verify_password, get_password_hash, verify_token

class TestSecurity:
    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        # Hash should not equal original password
        assert hashed != password
        
        # Verification should work
        assert verify_password(password, hashed) is True
        
        # Wrong password should fail
        assert verify_password("wrongpassword", hashed) is False

    def test_jwt_token_creation_and_verification(self):
        """Test JWT token creation and verification."""
        username = "testuser"
        
        # Create access token
        access_token = create_access_token(subject=username)
        assert access_token is not None
        
        # Verify token
        decoded_username = verify_token(access_token, "access")
        assert decoded_username == username
        
        # Invalid token should fail
        assert verify_token("invalid_token", "access") is None
        
        # Wrong token type should fail
        assert verify_token(access_token, "refresh") is None