"""
Authentication schemas for La Vida Luca application.
"""

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Schema for token data."""
    user_id: Optional[str] = None


class RefreshToken(BaseModel):
    """Schema for refreshing tokens."""
    refresh_token: str


class PasswordReset(BaseModel):
    """Schema for password reset request."""
    email: str


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation."""
    token: str
    new_password: str