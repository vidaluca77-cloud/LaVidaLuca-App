from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class CategoryEnum(str, Enum):
    AGRI = "agri"
    TRANSFO = "transfo"
    ARTISANAT = "artisanat"
    NATURE = "nature"
    SOCIAL = "social"

# Base schemas
class SkillBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    model_config = ConfigDict(from_attributes=True)

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    location: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    location: Optional[str] = None
    availability: Optional[List[str]] = None
    preferences: Optional[List[str]] = None
    skills: Optional[List[str]] = None

class UserProfile(BaseModel):
    skills: List[str] = []
    availability: List[str] = []
    location: str = ""
    preferences: List[str] = []

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    availability: Optional[List[str]] = None
    preferences: Optional[List[str]] = None
    skills: List[Skill] = []
    
    model_config = ConfigDict(from_attributes=True)

class UserInDB(User):
    hashed_password: str

# Activity schemas
class ActivityBase(BaseModel):
    slug: str
    title: str
    category: CategoryEnum
    summary: str
    description: Optional[str] = None
    duration_min: int
    safety_level: int = Field(ge=1, le=3, default=1)
    seasonality: Optional[List[str]] = None
    materials: Optional[List[str]] = None

class ActivityCreate(ActivityBase):
    skill_tags: Optional[List[str]] = None

class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = None
    safety_level: Optional[int] = Field(None, ge=1, le=3)
    seasonality: Optional[List[str]] = None
    materials: Optional[List[str]] = None
    skill_tags: Optional[List[str]] = None
    is_active: Optional[bool] = None

class Activity(ActivityBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    skill_tags: List[str] = []
    
    model_config = ConfigDict(from_attributes=True)

# Activity suggestion schemas
class SuggestionReason(BaseModel):
    type: str
    description: str
    score_impact: float

class ActivitySuggestionBase(BaseModel):
    score: float
    reasons: List[str] = []

class ActivitySuggestionCreate(ActivitySuggestionBase):
    user_id: int
    activity_id: int

class ActivitySuggestion(ActivitySuggestionBase):
    id: int
    user_id: int
    activity_id: int
    activity: Activity
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Suggestion(BaseModel):
    activity: Activity
    score: float
    reasons: List[str]

# Authentication schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# Response schemas
class UserResponse(BaseModel):
    user: User
    token: Token

class ActivitiesResponse(BaseModel):
    activities: List[Activity]
    total: int
    page: int
    per_page: int

class SuggestionsResponse(BaseModel):
    suggestions: List[Suggestion]
    user_profile: UserProfile

# Matching and AI schemas
class MatchingRequest(BaseModel):
    user_profile: UserProfile

class MatchingResponse(BaseModel):
    suggestions: List[Suggestion]
    
class SafetyGuide(BaseModel):
    activity_id: int
    rules: List[str]
    checklist: List[str]
    materials: List[str]

# Error schemas
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None