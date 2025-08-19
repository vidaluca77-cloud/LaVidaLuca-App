"""
User schemas for API serialization.
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


# Base schemas
class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str
    role: str = "student"


class UserUpdate(BaseModel):
    """Schema for user updates."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    profile_data: Optional[Dict[str, Any]] = None


class UserProfileUpdate(BaseModel):
    """Schema for profile-specific updates."""
    skills: Optional[List[str]] = None
    availability: Optional[List[str]] = None
    preferences: Optional[Dict[str, Any]] = None
    location: Optional[str] = None


class UserInDBBase(UserBase):
    """Base schema for user in database."""
    id: UUID
    role: str
    is_active: bool
    is_verified: bool
    profile_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class User(UserInDBBase):
    """User schema for API responses."""
    full_name: str
    is_instructor_or_above: bool
    is_moderator_or_above: bool
    is_admin: bool


class UserInDB(UserInDBBase):
    """User schema with password hash (internal use)."""
    hashed_password: str


# Authentication schemas
class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"
    user: User


class TokenData(BaseModel):
    """Token payload schema."""
    user_id: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str


class RegisterRequest(UserCreate):
    """Registration request schema."""
    confirm_password: str


class PasswordReset(BaseModel):
    """Password reset schema."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema."""
    token: str
    new_password: str
    confirm_password: str


class ChangePassword(BaseModel):
    """Change password schema."""
    current_password: str
    new_password: str
    confirm_password: str