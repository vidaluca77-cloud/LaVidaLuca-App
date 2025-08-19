"""
Pydantic schemas for user-related API endpoints.
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str
    skills: Optional[List[str]] = []
    availability: Optional[List[str]] = []
    preferences: Optional[List[str]] = []


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[List[str]] = None
    availability: Optional[List[str]] = None
    preferences: Optional[List[str]] = None


class UserProfile(BaseModel):
    """Schema for user profile (public information)."""
    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[List[str]] = []
    availability: Optional[List[str]] = []
    created_at: datetime
    
    class Config:
        from_attributes = True


class User(UserBase):
    """Full user schema with all fields."""
    id: int
    is_active: bool
    is_verified: bool
    skills: Optional[List[str]] = []
    availability: Optional[List[str]] = []
    preferences: Optional[List[str]] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Authentication schemas
class Token(BaseModel):
    """JWT token response schema."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""
    username: Optional[str] = None


class LoginData(BaseModel):
    """Login request schema."""
    username: str
    password: str