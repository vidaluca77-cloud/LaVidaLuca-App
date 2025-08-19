"""
User schemas for La Vida Luca application.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    institution: Optional[str] = None
    role: str = "student"
    expertise_areas: Optional[List[str]] = None
    interests: Optional[List[str]] = None

    @validator('role')
    def validate_role(cls, v):
        allowed_roles = ['student', 'teacher', 'coordinator', 'admin']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    institution: Optional[str] = None
    role: Optional[str] = None
    expertise_areas: Optional[List[str]] = None
    interests: Optional[List[str]] = None

    @validator('role')
    def validate_role(cls, v):
        if v is not None:
            allowed_roles = ['student', 'teacher', 'coordinator', 'admin']
            if v not in allowed_roles:
                raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v


class UserChangePassword(BaseModel):
    """Schema for changing user password."""
    current_password: str
    new_password: str

    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class User(UserBase):
    """Complete user schema for responses."""
    id: str
    is_active: bool
    is_verified: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """Public user profile schema."""
    id: str
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    institution: Optional[str] = None
    role: str
    expertise_areas: Optional[List[str]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class UserRegistration(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
    institution: Optional[str] = None
    role: str = "student"

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

    @validator('role')
    def validate_role(cls, v):
        allowed_roles = ['student', 'teacher', 'coordinator']  # admin can only be set manually
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v