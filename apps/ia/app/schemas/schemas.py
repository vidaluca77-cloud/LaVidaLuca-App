"""
Pydantic schemas for API requests and responses
"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class ActivityCategory(str, Enum):
    AGRI = "agri"
    TRANSFO = "transfo"
    ARTISANAT = "artisanat"
    NATURE = "nature"
    SOCIAL = "social"

class SeasonEnum(str, Enum):
    PRINTEMPS = "printemps"
    ETE = "ete"
    AUTOMNE = "automne"
    HIVER = "hiver"
    TOUTES = "toutes"

class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    location: Optional[str] = None
    is_mfr_student: bool = False

class UserCreate(UserBase):
    password: str
    skills: List[str] = []
    availability: List[str] = []
    preferences: List[str] = []

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[List[str]] = None
    availability: Optional[List[str]] = None
    preferences: Optional[List[str]] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    skills: List[str] = []
    availability: List[str] = []
    preferences: List[str] = []
    
    class Config:
        from_attributes = True

class User(UserInDB):
    pass

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# Activity schemas
class ActivityBase(BaseModel):
    slug: str
    title: str
    category: ActivityCategory
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: int
    skill_tags: List[str] = []
    seasonality: List[SeasonEnum] = []
    safety_level: int = 1
    materials: List[str] = []
    max_participants: int = 10
    min_age: int = 16

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[ActivityCategory] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = None
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[List[SeasonEnum]] = None
    safety_level: Optional[int] = None
    materials: Optional[List[str]] = None
    max_participants: Optional[int] = None
    min_age: Optional[int] = None
    is_active: Optional[bool] = None

class ActivityInDB(ActivityBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Activity(ActivityInDB):
    pass

# Booking schemas
class BookingBase(BaseModel):
    activity_id: int
    scheduled_date: datetime
    notes: Optional[str] = None

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    scheduled_date: Optional[datetime] = None
    status: Optional[BookingStatus] = None
    notes: Optional[str] = None

class BookingInDB(BookingBase):
    id: int
    user_id: int
    status: BookingStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Booking(BookingInDB):
    activity: Optional[Activity] = None
    user: Optional[User] = None

# Suggestion schemas
class ActivitySuggestion(BaseModel):
    activity: Activity
    score: float
    reasons: List[str]

class SuggestionRequest(BaseModel):
    user_id: Optional[int] = None
    skills: Optional[List[str]] = None
    availability: Optional[List[str]] = None
    preferences: Optional[List[str]] = None
    limit: int = 10

# Analytics schemas
class AnalyticsEventCreate(BaseModel):
    event_type: str
    event_data: Optional[Dict[str, Any]] = None

class AnalyticsEvent(BaseModel):
    id: int
    user_id: Optional[int]
    event_type: str
    event_data: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# API Response schemas
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int