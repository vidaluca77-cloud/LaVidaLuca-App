"""
Pydantic schemas for API request/response models.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional, Any
from datetime import datetime
from enum import Enum


class ActivityCategory(str, Enum):
    """Activity categories."""
    AGRI = "agri"
    TRANSFO = "transfo"
    ARTISANAT = "artisanat"
    NATURE = "nature"
    SOCIAL = "social"


class InteractionType(str, Enum):
    """User-Activity interaction types."""
    COMPLETED = "completed"
    FAVORITED = "favorited"
    INTERESTED = "interested"


class ContactStatus(str, Enum):
    """Contact message status."""
    NEW = "new"
    READ = "read"
    RESPONDED = "responded"


# Base schemas
class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    model_config = ConfigDict(from_attributes=True)


# User schemas
class UserBase(BaseSchema):
    """Base user schema."""
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    availability: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    bio: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""
    password: Optional[str] = None  # Optional for Supabase users


class UserUpdate(BaseSchema):
    """User update schema."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    skills: Optional[List[str]] = None
    availability: Optional[List[str]] = None
    location: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(UserBase):
    """User response schema."""
    id: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


# Activity schemas
class ActivityBase(BaseSchema):
    """Base activity schema."""
    title: str
    category: ActivityCategory
    summary: str
    description: Optional[str] = None
    duration_min: int = Field(gt=0)
    skill_tags: List[str] = Field(default_factory=list)
    safety_level: int = Field(ge=1, le=5, default=1)
    materials: List[str] = Field(default_factory=list)
    location_type: Optional[str] = None
    season: List[str] = Field(default_factory=list)


class ActivityCreate(ActivityBase):
    """Activity creation schema."""
    pass


class ActivityUpdate(BaseSchema):
    """Activity update schema."""
    title: Optional[str] = None
    category: Optional[ActivityCategory] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = Field(None, gt=0)
    skill_tags: Optional[List[str]] = None
    safety_level: Optional[int] = Field(None, ge=1, le=5)
    materials: Optional[List[str]] = None
    location_type: Optional[str] = None
    season: Optional[List[str]] = None


class ActivityResponse(ActivityBase):
    """Activity response schema."""
    id: str
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None


# User-Activity schemas
class UserActivityBase(BaseSchema):
    """Base user-activity schema."""
    interaction_type: InteractionType
    rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None


class UserActivityCreate(UserActivityBase):
    """User-activity creation schema."""
    activity_id: str


class UserActivityResponse(UserActivityBase):
    """User-activity response schema."""
    id: str
    user_id: str
    activity_id: str
    completed_at: Optional[datetime] = None
    created_at: datetime


# Suggestion schemas
class SuggestionResponse(BaseSchema):
    """Suggestion response schema."""
    id: str
    activity: ActivityResponse
    score: float = Field(ge=0.0, le=1.0)
    reasons: List[str]
    viewed: bool
    clicked: bool
    dismissed: bool
    created_at: datetime
    expires_at: Optional[datetime] = None


class SuggestionUpdate(BaseSchema):
    """Suggestion update schema."""
    viewed: Optional[bool] = None
    clicked: Optional[bool] = None
    dismissed: Optional[bool] = None


# Contact schemas
class ContactMessageBase(BaseSchema):
    """Base contact message schema."""
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str


class ContactMessageCreate(ContactMessageBase):
    """Contact message creation schema."""
    pass


class ContactMessageResponse(ContactMessageBase):
    """Contact message response schema."""
    id: str
    status: ContactStatus
    created_at: datetime


# Authentication schemas
class Token(BaseSchema):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseSchema):
    """Token data schema."""
    user_id: Optional[str] = None
    email: Optional[str] = None


class LoginRequest(BaseSchema):
    """Login request schema."""
    email: EmailStr
    password: str


# API Response schemas
class ApiResponse(BaseSchema):
    """Standard API response schema."""
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None


class ErrorResponse(BaseSchema):
    """Error response schema."""
    success: bool = False
    error: dict


# Search and filter schemas
class ActivityFilter(BaseSchema):
    """Activity filter schema."""
    category: Optional[ActivityCategory] = None
    skill_tags: Optional[List[str]] = None
    duration_min_min: Optional[int] = None
    duration_min_max: Optional[int] = None
    safety_level_max: Optional[int] = None
    location_type: Optional[str] = None
    season: Optional[List[str]] = None


class PaginationParams(BaseSchema):
    """Pagination parameters schema."""
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1, le=100)


class PaginatedResponse(BaseSchema):
    """Paginated response schema."""
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int