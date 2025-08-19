from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    location: Optional[str] = None
    availability: Optional[List[str]] = []
    preferences: Optional[List[str]] = []
    is_student: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    location: Optional[str] = None
    availability: Optional[List[str]] = None
    preferences: Optional[List[str]] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Activity schemas
class ActivityBase(BaseModel):
    title: str
    category: str
    summary: str
    description: Optional[str] = None
    duration_min: int
    seasonality: List[str] = []
    safety_level: int = 1
    materials: List[str] = []
    location_requirements: Optional[str] = None
    max_participants: int = 10
    is_student_only: bool = False

class ActivityCreate(ActivityBase):
    slug: str

class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = None
    seasonality: Optional[List[str]] = None
    safety_level: Optional[int] = None
    materials: Optional[List[str]] = None
    location_requirements: Optional[str] = None
    max_participants: Optional[int] = None
    is_active: Optional[bool] = None
    is_student_only: Optional[bool] = None

class Activity(ActivityBase):
    id: int
    slug: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Skill schemas
class SkillBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Activity recommendation schemas
class ActivityRecommendation(BaseModel):
    activity: Activity
    score: float
    reasons: List[str]

class RecommendationRequest(BaseModel):
    user_id: int
    category_filter: Optional[str] = None
    limit: int = 10