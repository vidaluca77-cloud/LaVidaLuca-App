"""
JWT token handling for authentication with refresh token support.
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple
import jwt
import secrets
from fastapi import HTTPException, status
from ..config import settings
from ..schemas.auth import TokenData


# In-memory storage for refresh tokens (in production, use Redis or database)
REFRESH_TOKEN_STORE = {}


def create_tokens(data: dict, expires_delta: Optional[timedelta] = None) -> Tuple[str, str]:
    """
    Create both access and refresh tokens.
    
    Args:
        data: Data to encode in the token
        expires_delta: Access token expiration time
        
    Returns:
        Tuple of (access_token, refresh_token)
    """
    access_token = create_access_token(data, expires_delta)
    refresh_token = create_refresh_token(data)
    
    return access_token, refresh_token


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    
    to_encode.update({
        "exp": expire,
        "type": "access"
    })
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create a refresh token with longer expiration.
    
    Args:
        data: Data to encode in the token
        
    Returns:
        Refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=30)  # 30 days expiration
    
    # Generate a unique token ID for invalidation
    token_id = secrets.token_urlsafe(32)
    
    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "jti": token_id  # JWT ID for token tracking
    })
    
    refresh_token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    # Store refresh token (in production, use Redis or database)
    user_id = data.get("sub")
    if user_id:
        REFRESH_TOKEN_STORE[token_id] = {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "expires_at": expire
        }
    
    return refresh_token


def verify_token(token: str, token_type: str = "access") -> TokenData:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token to verify
        token_type: Type of token ("access" or "refresh")
        
    Returns:
        Token data
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email") 
        exp: int = payload.get("exp")
        token_type_in_payload: str = payload.get("type")
        jti: str = payload.get("jti")  # JWT ID for refresh tokens
        
        if user_id is None or email is None:
            raise credentials_exception
            
        # Verify token type matches expected
        if token_type_in_payload != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type. Expected {token_type}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # For refresh tokens, check if token is still valid in store
        if token_type == "refresh" and jti:
            if jti not in REFRESH_TOKEN_STORE:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh token has been revoked",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
        token_data = TokenData(user_id=user_id, email=email, exp=exp, jti=jti)
        return token_data
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise credentials_exception


def refresh_access_token(refresh_token: str) -> str:
    """
    Generate a new access token using a refresh token.
    
    Args:
        refresh_token: Valid refresh token
        
    Returns:
        New access token
        
    Raises:
        HTTPException: If refresh token is invalid
    """
    token_data = verify_token(refresh_token, "refresh")
    
    # Create new access token with same user data
    new_access_token = create_access_token({
        "sub": token_data.user_id,
        "email": token_data.email
    })
    
    return new_access_token


def revoke_refresh_token(refresh_token: str) -> bool:
    """
    Revoke a refresh token.
    
    Args:
        refresh_token: Refresh token to revoke
        
    Returns:
        True if revoked successfully
    """
    try:
        token_data = verify_token(refresh_token, "refresh")
        if token_data.jti and token_data.jti in REFRESH_TOKEN_STORE:
            del REFRESH_TOKEN_STORE[token_data.jti]
            return True
    except:
        pass
    return False


def revoke_all_user_tokens(user_id: str) -> int:
    """
    Revoke all refresh tokens for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        Number of tokens revoked
    """
    tokens_to_remove = []
    for jti, token_info in REFRESH_TOKEN_STORE.items():
        if token_info["user_id"] == user_id:
            tokens_to_remove.append(jti)
    
    for jti in tokens_to_remove:
        del REFRESH_TOKEN_STORE[jti]
    
    return len(tokens_to_remove)


def cleanup_expired_tokens():
    """
    Clean up expired refresh tokens from storage.
    This should be called periodically.
    """
    now = datetime.utcnow()
    expired_tokens = []
    
    for jti, token_info in REFRESH_TOKEN_STORE.items():
        if token_info["expires_at"] < now:
            expired_tokens.append(jti)
    
    for jti in expired_tokens:
        del REFRESH_TOKEN_STORE[jti]
    
    return len(expired_tokens)


async def get_current_user(token: str):
    """
    Get current user from JWT token.
    This function would typically fetch the user from database.
    For now, it returns the token data.
    
    Args:
        token: JWT token
        
    Returns:
        User data from token
    """
    return verify_token(token)