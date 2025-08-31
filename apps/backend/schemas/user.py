"""
User schemas for profile management and user operations.
"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, UUID4


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """User creation schema."""

    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """User update schema."""

    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    profile: Optional[Dict[str, Any]] = None


class UserProfile(BaseModel):
    """User profile schema."""

    skills: Optional[list[str]] = Field(default_factory=list)
    availability: Optional[list[str]] = Field(default_factory=list)
    location: Optional[str] = None
    bio: Optional[str] = None
    interests: Optional[list[str]] = Field(default_factory=list)
    experience_level: Optional[str] = None  # beginner, intermediate, advanced
    preferred_categories: Optional[list[str]] = Field(default_factory=list)

    class Config:
        schema_extra = {
            "example": {
                "skills": ["jardinage", "cuisine", "artisanat"],
                "availability": ["weekends", "evenings"],
                "location": "Paris, France",
                "bio": "Passionné par l'agriculture durable et l'artisanat traditionnel",
                "interests": ["permaculture", "apiculture", "céramique"],
                "experience_level": "intermediate",
                "preferred_categories": ["agri", "artisanat"],
            }
        }


class UserResponse(BaseModel):
    """User response schema."""

    id: UUID4
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: str
    profile: Optional[Dict[str, Any]]
    is_active: bool
    is_verified: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    last_login: Optional[datetime]

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "full_name": "John Doe",
                "profile": {
                    "skills": ["jardinage", "cuisine"],
                    "location": "Paris, France",
                },
                "is_active": True,
                "is_verified": True,
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-02T12:00:00Z",
                "last_login": "2024-01-02T10:30:00Z",
            }
        }


class UserListResponse(BaseModel):
    """User list response schema (minimal info for listings)."""

    id: UUID4
    email: EmailStr
    full_name: str
    is_active: bool
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
