from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field

# Activity Categories
class ActivityCategory(str, Enum):
    AGRI = "agri"
    TRANSFO = "transfo"
    ARTISANAT = "artisanat"
    NATURE = "nature"
    SOCIAL = "social"

class Seasonality(str, Enum):
    PRINTEMPS = "printemps"
    ETE = "ete"
    AUTOMNE = "automne"
    HIVER = "hiver"
    TOUTES = "toutes"

# Activity Models
class ActivityBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=100)
    category: ActivityCategory
    summary: str = Field(..., min_length=1, max_length=500)
    duration_min: int = Field(..., gt=0)
    skill_tags: List[str] = Field(default_factory=list)
    seasonality: List[Seasonality] = Field(default_factory=list)
    safety_level: int = Field(..., ge=1, le=5)
    materials: List[str] = Field(default_factory=list)

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[ActivityCategory] = None
    summary: Optional[str] = None
    duration_min: Optional[int] = None
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[List[Seasonality]] = None
    safety_level: Optional[int] = None
    materials: Optional[List[str]] = None

class Activity(ActivityBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# User Models
class UserProfile(BaseModel):
    skills: List[str] = Field(default_factory=list)
    availability: List[str] = Field(default_factory=list)
    location: str = ""
    preferences: List[str] = Field(default_factory=list)

class UserBase(BaseModel):
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    full_name: str = Field(..., min_length=1, max_length=100)
    profile: Optional[UserProfile] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    profile: Optional[UserProfile] = None

class User(UserBase):
    id: str
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True

# Registration Models
class RegistrationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class RegistrationBase(BaseModel):
    activity_id: str
    notes: Optional[str] = None

class RegistrationCreate(RegistrationBase):
    pass

class RegistrationUpdate(BaseModel):
    status: Optional[RegistrationStatus] = None
    notes: Optional[str] = None

class Registration(RegistrationBase):
    id: str
    user_id: str
    status: RegistrationStatus = RegistrationStatus.PENDING
    created_at: datetime
    updated_at: datetime
    activity: Optional[Activity] = None

    class Config:
        from_attributes = True

# Authentication Models
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

# AI Suggestion Models
class Suggestion(BaseModel):
    activity: Activity
    score: float
    reasons: List[str]

class SuggestionRequest(BaseModel):
    profile: UserProfile