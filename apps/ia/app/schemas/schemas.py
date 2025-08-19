from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    location: Optional[str] = None
    skills: List[str] = []
    availability: List[str] = []
    preferences: List[str] = []


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[List[str]] = None
    availability: Optional[List[str]] = None
    preferences: Optional[List[str]] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Activity schemas
class ActivityBase(BaseModel):
    title: str
    slug: str
    category: str  # 'agri', 'transfo', 'artisanat', 'nature', 'social'
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: int
    skill_tags: List[str] = []
    seasonality: List[str] = []
    safety_level: int
    materials: List[str] = []


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    category: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = None
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[List[str]] = None
    safety_level: Optional[int] = None
    materials: Optional[List[str]] = None


class ActivityResponse(ActivityBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Recommendation schemas
class RecommendationResponse(BaseModel):
    id: int
    activity: ActivityResponse
    score: float
    reasons: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class RecommendationRequest(BaseModel):
    user_profile: Optional[UserBase] = None
    limit: int = 5


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str