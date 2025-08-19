"""
Pydantic schemas for request/response validation.
Defines data structures for API endpoints.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr

class UserCreate(UserBase):
    """Schema for user creation."""
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

class UserProfile(BaseModel):
    """User profile information."""
    skills: List[str] = []
    availability: List[str] = []
    location: Optional[str] = None
    interests: List[str] = []
    experience_level: Optional[str] = None  # beginner, intermediate, advanced

class UserUpdate(BaseModel):
    """Schema for user updates."""
    profile: Optional[UserProfile] = None

class User(UserBase):
    """Complete user schema for responses."""
    id: str
    is_active: bool
    created_at: datetime
    profile: Dict[str, Any] = {}
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Token payload data."""
    email: Optional[str] = None

class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str

# Activity schemas
class ActivityBase(BaseModel):
    """Base activity schema."""
    title: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., pattern="^(agri|transfo|artisanat|nature|social)$")
    summary: str = Field(..., min_length=1, max_length=500)
    duration_min: int = Field(..., gt=0, le=1440, description="Duration in minutes (1-1440)")

class ActivityCreate(ActivityBase):
    """Schema for activity creation."""
    description: Optional[str] = None
    skill_tags: List[str] = []
    materials: List[str] = []
    safety_level: int = Field(3, ge=1, le=5, description="Safety level from 1 (very safe) to 5 (risky)")
    difficulty_level: int = Field(3, ge=1, le=5, description="Difficulty level from 1 (easy) to 5 (hard)")
    location: Optional[str] = None

class ActivityUpdate(BaseModel):
    """Schema for activity updates."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[str] = Field(None, pattern="^(agri|transfo|artisanat|nature|social)$")
    summary: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    duration_min: Optional[int] = Field(None, gt=0, le=1440)
    skill_tags: Optional[List[str]] = None
    materials: Optional[List[str]] = None
    safety_level: Optional[int] = Field(None, ge=1, le=5)
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    location: Optional[str] = None
    is_active: Optional[bool] = None

class Activity(ActivityBase):
    """Complete activity schema for responses."""
    id: str
    description: Optional[str] = None
    skill_tags: List[str] = []
    materials: List[str] = []
    safety_level: int
    difficulty_level: int
    location: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    creator_id: Optional[str] = None
    engagement_score: float = 0.0
    success_rate: float = 0.0
    
    class Config:
        from_attributes = True

# AI Suggestion schemas
class SuggestionRequest(BaseModel):
    """Request for AI suggestions."""
    user_id: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = {}
    limit: int = Field(5, ge=1, le=20, description="Number of suggestions to return")

class Suggestion(BaseModel):
    """AI suggestion response."""
    activity: Activity
    score: float = Field(..., ge=0, le=1, description="Relevance score from 0 to 1")
    reasons: List[str] = Field(..., description="Reasons for the suggestion")

class SuggestionResponse(BaseModel):
    """Response containing multiple suggestions."""
    suggestions: List[Suggestion]
    total: int
    generated_at: datetime

# Response schemas
class SuccessResponse(BaseModel):
    """Standard success response."""
    success: bool = True
    data: Optional[Any] = None
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: Dict[str, Any]

class PaginatedResponse(BaseModel):
    """Paginated response for list endpoints."""
    success: bool = True
    data: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int