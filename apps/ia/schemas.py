from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_mfr_student: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_mfr_student: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Profile schemas
class UserProfileBase(BaseModel):
    location: Optional[str] = None
    availability: List[str] = []
    experience_level: str = "debutant"

class UserProfileCreate(UserProfileBase):
    skills: List[str] = []
    preferences: List[str] = []

class UserProfileUpdate(UserProfileBase):
    skills: Optional[List[str]] = None
    preferences: Optional[List[str]] = None

class UserProfile(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    skills: List[str] = []
    preferences: List[str] = []
    
    class Config:
        from_attributes = True

# Activity schemas
class ActivityBase(BaseModel):
    slug: str
    title: str
    category: str
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: int
    skill_tags: List[str] = []
    seasonality: List[str] = []
    safety_level: int = 1
    materials: List[str] = []

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = None
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[List[str]] = None
    safety_level: Optional[int] = None
    materials: Optional[List[str]] = None
    is_active: Optional[bool] = None

class Activity(ActivityBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Recommendation schemas
class RecommendationBase(BaseModel):
    score: float
    reasons: List[str] = []
    ai_explanation: Optional[str] = None

class Recommendation(RecommendationBase):
    id: int
    user_id: int
    activity_id: int
    activity: Activity
    created_at: datetime
    
    class Config:
        from_attributes = True

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Response schemas
class RecommendationResponse(BaseModel):
    recommendations: List[Recommendation]
    total_count: int
    
class UserWithProfile(User):
    profile: Optional[UserProfile] = None