import pytest
from app.auth.jwt_handler import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token
)
from datetime import timedelta
from jose import jwt
from app.core.config import settings

class TestPasswordHashing:
    """Test password hashing functions"""
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False
    
    def test_different_passwords_produce_different_hashes(self):
        """Test that different passwords produce different hashes"""
        password1 = "password1"
        password2 = "password2"
        
        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)
        
        assert hash1 != hash2

class TestJWTTokens:
    """Test JWT token functions"""
    
    def test_create_access_token(self):
        """Test access token creation"""
        data = {"sub": "testuser", "username": "testuser"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_token_valid(self):
        """Test token verification with valid token"""
        data = {"sub": "testuser", "username": "testuser"}
        token = create_access_token(data)
        
        payload = verify_token(token)
        
        assert payload["sub"] == "testuser"
        assert payload["username"] == "testuser"
        assert "exp" in payload
    
    def test_verify_token_invalid(self):
        """Test token verification with invalid token"""
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token("invalid_token")
        
        assert exc_info.value.status_code == 401
        assert "Token invalide" in exc_info.value.detail
    
    def test_verify_token_expired(self):
        """Test token verification with expired token"""
        from fastapi import HTTPException
        
        data = {"sub": "testuser", "username": "testuser"}
        # Create expired token
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(token)
        
        assert exc_info.value.status_code == 401
    
    def test_token_without_sub(self):
        """Test token verification without sub claim"""
        from fastapi import HTTPException
        
        # Create token without sub claim
        data = {"username": "testuser"}
        token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(token)
        
        assert exc_info.value.status_code == 401