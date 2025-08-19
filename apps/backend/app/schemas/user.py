"""
User schemas for API input/output validation.
"""

from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    full_name: str
    skills: List[str] = []
    availability: List[str] = []
    location: Optional[str] = None
    preferences: List[str] = []
    bio: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str


class UserUpdate(BaseModel):
    """Schema for user updates."""
    full_name: Optional[str] = None
    skills: Optional[List[str]] = None
    availability: Optional[List[str]] = None
    location: Optional[str] = None
    preferences: Optional[List[str]] = None
    bio: Optional[str] = None
    phone: Optional[str] = None


class UserProfile(BaseModel):
    """Schema for user profile matching (frontend compatibility)."""
    skills: List[str] = []
    availability: List[str] = []
    location: str = ""
    preferences: List[str] = []


class UserInDB(UserBase):
    """Schema for user as stored in database."""
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class User(UserInDB):
    """Schema for user response (public)."""
    pass


class UserAuth(BaseModel):
    """Schema for user authentication."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data."""
    email: Optional[str] = None