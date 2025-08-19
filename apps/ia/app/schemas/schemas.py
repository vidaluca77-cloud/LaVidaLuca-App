"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class ActivityCategory(str, Enum):
    agri = "agri"
    transfo = "transfo"
    artisanat = "artisanat"
    nature = "nature"
    social = "social"


class DifficultyLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class SessionStatus(str, Enum):
    started = "started"
    completed = "completed"
    abandoned = "abandoned"


# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


# User schemas
class UserBase(BaseSchema):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseSchema):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    id: int
    is_superuser: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None


class User(UserInDB):
    profile: Optional["UserProfile"] = None


# User Profile schemas
class UserProfileBase(BaseSchema):
    skills: List[str] = []
    availability: List[str] = []
    location: Optional[str] = None
    preferences: List[str] = []
    bio: Optional[str] = None
    mfr_level: Optional[DifficultyLevel] = None
    age_range: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfile(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


# Activity schemas
class ActivityBase(BaseSchema):
    slug: str
    title: str
    category: ActivityCategory
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = None
    skill_tags: List[str] = []
    seasonality: List[str] = []
    safety_level: int = Field(default=1, ge=1, le=5)
    materials: List[str] = []
    difficulty_level: DifficultyLevel = DifficultyLevel.beginner
    max_participants: Optional[int] = None
    location_type: Optional[str] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseSchema):
    slug: Optional[str] = None
    title: Optional[str] = None
    category: Optional[ActivityCategory] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = None
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[List[str]] = None
    safety_level: Optional[int] = Field(None, ge=1, le=5)
    materials: Optional[List[str]] = None
    difficulty_level: Optional[DifficultyLevel] = None
    max_participants: Optional[int] = None
    location_type: Optional[str] = None
    is_active: Optional[bool] = None


class Activity(ActivityBase):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None


# Recommendation schemas
class RecommendationBase(BaseSchema):
    score: float = Field(ge=0.0, le=1.0)
    reasons: List[str] = []
    ai_explanation: Optional[str] = None


class RecommendationCreate(RecommendationBase):
    user_id: int
    activity_id: int


class Recommendation(RecommendationBase):
    id: int
    user_id: int
    activity_id: int
    activity: Activity
    created_at: datetime


# Activity Session schemas
class ActivitySessionBase(BaseSchema):
    duration_minutes: Optional[int] = None
    satisfaction_rating: Optional[int] = Field(None, ge=1, le=5)
    feedback: Optional[str] = None
    status: SessionStatus = SessionStatus.started


class ActivitySessionCreate(BaseSchema):
    activity_id: int


class ActivitySessionUpdate(ActivitySessionBase):
    completed_at: Optional[datetime] = None


class ActivitySession(ActivitySessionBase):
    id: int
    user_id: int
    activity_id: int
    activity: Activity
    started_at: datetime
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


# Authentication schemas
class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenData(BaseSchema):
    username: Optional[str] = None


class LoginRequest(BaseSchema):
    username: str
    password: str


# AI Recommendation Request
class RecommendationRequest(BaseSchema):
    user_profile: UserProfileBase
    max_recommendations: int = Field(default=5, ge=1, le=20)
    category_filter: Optional[List[ActivityCategory]] = None
    difficulty_filter: Optional[List[DifficultyLevel]] = None


# Response schemas
class RecommendationResponse(BaseSchema):
    recommendations: List[Recommendation]
    total_count: int
    generated_at: datetime


class HealthResponse(BaseSchema):
    status: str
    timestamp: datetime
    version: str = "1.0.0"


# Update forward references
User.model_rebuild()