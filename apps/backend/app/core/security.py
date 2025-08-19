"""
Enhanced security utilities for authentication system.
"""

from datetime import datetime, timedelta
from typing import Any, Union, Optional, Dict, Tuple
from jose import jwt, JWTError
from passlib.context import CryptContext
import secrets
import hashlib
import re

from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Rate limiting storage (in production, use Redis)
_rate_limit_storage = {}


class SecurityError(Exception):
    """Base security exception."""
    pass


class TokenError(SecurityError):
    """Token-related errors."""
    pass


class RateLimitError(SecurityError):
    """Rate limiting errors."""
    pass


class PasswordPolicyError(SecurityError):
    """Password policy violations."""
    pass


def create_access_token(
    subject: Union[str, Any], 
    expires_delta: Optional[timedelta] = None,
    additional_claims: Optional[Dict] = None
) -> str:
    """Create JWT access token with enhanced claims."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire, 
        "sub": str(subject),
        "iat": datetime.utcnow(),
        "type": "access"
    }
    
    if additional_claims:
        to_encode.update(additional_claims)
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(user_id: str) -> Tuple[str, str]:
    """Create refresh token and return token + hash for storage."""
    # Generate cryptographically secure random token
    token = secrets.token_urlsafe(64)
    
    # Create hash for storage (never store plain token)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    
    return token, token_hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)


def verify_token(token: str, token_type: str = "access") -> Optional[Dict]:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        
        # Verify token type
        if payload.get("type") != token_type:
            return None
            
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
            
        return payload
    except JWTError:
        return None


def verify_refresh_token_hash(token: str, stored_hash: str) -> bool:
    """Verify refresh token against stored hash."""
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    return secrets.compare_digest(token_hash, stored_hash)


def generate_device_fingerprint(user_agent: str, ip_address: str) -> str:
    """Generate device fingerprint for session tracking."""
    fingerprint_data = f"{user_agent}:{ip_address}"
    return hashlib.sha256(fingerprint_data.encode()).hexdigest()[:32]


def validate_password_policy(password: str) -> bool:
    """Validate password against security policy."""
    errors = []
    
    # Length check
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if len(password) > 128:
        errors.append("Password must not exceed 128 characters")
    
    # Character requirements
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one digit")
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\?]', password):
        errors.append("Password must contain at least one special character")
    
    # Common password checks
    common_passwords = {
        "password", "123456", "password123", "admin", "qwerty", 
        "letmein", "welcome", "monkey", "dragon", "master"
    }
    if password.lower() in common_passwords:
        errors.append("Password is too common")
    
    # Sequential characters
    if has_sequential_chars(password):
        errors.append("Password cannot contain sequential characters (abc, 123)")
    
    if errors:
        raise PasswordPolicyError("; ".join(errors))
    
    return True


def has_sequential_chars(password: str, min_length: int = 3) -> bool:
    """Check for sequential characters in password."""
    password = password.lower()
    
    for i in range(len(password) - min_length + 1):
        # Check for sequential numbers
        if password[i:i+min_length].isdigit():
            chars = [int(c) for c in password[i:i+min_length]]
            if all(chars[j] == chars[j-1] + 1 for j in range(1, len(chars))):
                return True
        
        # Check for sequential letters
        if password[i:i+min_length].isalpha():
            chars = [ord(c) for c in password[i:i+min_length]]
            if all(chars[j] == chars[j-1] + 1 for j in range(1, len(chars))):
                return True
    
    return False


# Rate limiting functions
def check_rate_limit(key: str, max_attempts: int, window_minutes: int) -> bool:
    """Check if rate limit is exceeded."""
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=window_minutes)
    
    if key not in _rate_limit_storage:
        _rate_limit_storage[key] = []
    
    # Clean old attempts
    _rate_limit_storage[key] = [
        attempt for attempt in _rate_limit_storage[key] 
        if attempt > window_start
    ]
    
    # Check if limit exceeded
    if len(_rate_limit_storage[key]) >= max_attempts:
        return False
    
    # Record this attempt
    _rate_limit_storage[key].append(now)
    return True


def get_rate_limit_reset_time(key: str, window_minutes: int) -> Optional[datetime]:
    """Get when rate limit will reset."""
    if key not in _rate_limit_storage or not _rate_limit_storage[key]:
        return None
    
    oldest_attempt = min(_rate_limit_storage[key])
    return oldest_attempt + timedelta(minutes=window_minutes)