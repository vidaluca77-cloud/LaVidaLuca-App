"""
Authentication schemas for login, registration, and JWT tokens.
"""

from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
import re


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    device_name: Optional[str] = Field(None, max_length=255)
    remember_me: bool = False


class UserRegister(BaseModel):
    """User registration schema."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        from ..core.security import validate_password_policy, PasswordPolicyError
        try:
            validate_password_policy(v)
        except PasswordPolicyError as e:
            raise ValueError(str(e))
        return v


class TokenResponse(BaseModel):
    """JWT token response with refresh token."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    session_id: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request."""
    refresh_token: str


class TokenData(BaseModel):
    """JWT token payload data."""
    user_id: str
    email: str
    exp: int  # expiration timestamp
    
    
class PasswordReset(BaseModel):
    """Password reset request."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation."""
    token: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def validate_password(cls, v):
        """Validate password strength."""
        from ..core.security import validate_password_policy, PasswordPolicyError
        try:
            validate_password_policy(v)
        except PasswordPolicyError as e:
            raise ValueError(str(e))
        return v


class ChangePassword(BaseModel):
    """Change password schema."""
    current_password: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def validate_password(cls, v):
        """Validate password strength."""
        from ..core.security import validate_password_policy, PasswordPolicyError
        try:
            validate_password_policy(v)
        except PasswordPolicyError as e:
            raise ValueError(str(e))
        return v


class TwoFactorSetup(BaseModel):
    """2FA setup response."""
    secret: str
    qr_code: str
    backup_codes: List[str]


class TwoFactorEnable(BaseModel):
    """Enable 2FA with verification."""
    token: str = Field(..., min_length=6, max_length=6)
    
    @validator('token')
    def validate_token(cls, v):
        """Validate 2FA token format."""
        if not v.isdigit():
            raise ValueError('Token must be 6 digits')
        return v


class TwoFactorVerify(BaseModel):
    """2FA verification during login."""
    token: str = Field(..., min_length=6, max_length=8)  # Allow backup codes
    
    @validator('token')
    def validate_token(cls, v):
        """Validate 2FA token format."""
        # Allow 6-digit TOTP tokens or 8-character backup codes
        if len(v) == 6 and v.isdigit():
            return v
        elif len(v) == 8 and v.replace('-', '').replace(' ', '').isalnum():
            return v
        else:
            raise ValueError('Invalid token format')


class SessionInfo(BaseModel):
    """Session information schema."""
    id: str
    device_name: Optional[str]
    device_fingerprint: str
    ip_address: str
    user_agent: Optional[str]
    location: Optional[str]
    is_current: bool
    last_activity: datetime
    created_at: datetime
    expires_at: datetime


class SessionList(BaseModel):
    """List of user sessions."""
    sessions: List[SessionInfo]
    total: int


class LogoutRequest(BaseModel):
    """Logout request schema."""
    logout_all_devices: bool = False


class UserManagement(BaseModel):
    """User management schema for admin operations."""
    user_id: str
    action: str = Field(..., regex="^(activate|deactivate|lock|unlock|reset_password|enable_2fa|disable_2fa)$")
    reason: Optional[str] = Field(None, max_length=500)


class AuditLog(BaseModel):
    """Audit log entry schema."""
    id: str
    user_id: Optional[str]
    action: str
    resource: str
    ip_address: str
    user_agent: Optional[str]
    success: bool
    details: Optional[dict]
    timestamp: datetime