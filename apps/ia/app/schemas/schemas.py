"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class User(UserInDB):
    pass


# User Profile schemas
class UserProfileBase(BaseModel):
    skills: List[str] = Field(default_factory=list)
    preferences: List[str] = Field(default_factory=list)
    availability: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    experience_level: str = Field(default="debutant")
    bio: Optional[str] = None
    phone: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    skills: Optional[List[str]] = None
    preferences: Optional[List[str]] = None
    availability: Optional[List[str]] = None
    experience_level: Optional[str] = None


class UserProfile(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Activity schemas
class ActivityBase(BaseModel):
    slug: str
    title: str
    category: str
    summary: str
    description: Optional[str] = None
    duration_min: int
    skill_tags: List[str] = Field(default_factory=list)
    seasonality: List[str] = Field(default_factory=list)
    safety_level: int = Field(default=1, ge=1, le=3)
    materials: List[str] = Field(default_factory=list)


class ActivityCreate(ActivityBase):
    pass


class Activity(ActivityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Recommendation schemas
class RecommendationRequest(BaseModel):
    user_profile: UserProfileBase
    limit: int = Field(default=5, ge=1, le=20)


class ActivityRecommendation(BaseModel):
    activity: Activity
    score: int = Field(..., ge=0, le=100)
    reasons: List[str]
    ai_explanation: Optional[str] = None

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    recommendations: List[ActivityRecommendation]
    total_activities: int
    profile_completeness: float = Field(..., ge=0, le=1)


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# Generic response schemas
class Message(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None