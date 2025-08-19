"""User schemas."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from ..models.user import UserRole


# Base schemas
class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.STUDENT
    is_active: bool = True
    phone: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[List[str]] = None
    preferences: Optional[List[str]] = None


class UserUpdatePassword(BaseModel):
    """Schema for updating user password."""
    current_password: str
    new_password: str


class UserInDB(UserBase):
    """Schema for user in database."""
    id: UUID
    hashed_password: str
    skills: Optional[List[str]] = None
    preferences: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserBase):
    """Schema for user response."""
    id: UUID
    skills: Optional[List[str]] = None
    preferences: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """Extended user profile schema."""
    id: UUID
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole
    phone: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[List[str]] = None
    preferences: Optional[List[str]] = None
    total_activities: int = 0
    completed_activities: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True