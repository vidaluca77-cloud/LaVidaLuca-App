from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class UserRole(str, Enum):
    STUDENT = "student"
    MENTOR = "mentor"
    ADMIN = "admin"
    VISITOR = "visitor"

class ActivityCategory(str, Enum):
    AGRI = "agri"
    TRANSFO = "transfo"
    ARTISANAT = "artisanat"
    NATURE = "nature"
    SOCIAL = "social"

class ReservationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class SafetyLevel(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseSchema):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None
    role: UserRole = UserRole.VISITOR
    location: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    availability: List[str] = []
    preferences: List[str] = []

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseSchema):
    full_name: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    availability: Optional[List[str]] = None
    preferences: Optional[List[str]] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class UserProfile(BaseSchema):
    skills: List[str] = []
    availability: List[str] = []
    location: str = ""
    preferences: List[str] = []

# Authentication schemas
class Token(BaseSchema):
    access_token: str
    token_type: str

class TokenData(BaseSchema):
    username: Optional[str] = None

class LoginRequest(BaseSchema):
    username: str
    password: str

# Location schemas
class LocationBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    address: Optional[str] = None
    departement: Optional[str] = None
    coordinates: Optional[Dict[str, float]] = None
    contact_person: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    max_capacity: int = Field(default=10, ge=1)
    facilities: List[str] = []

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    departement: Optional[str] = None
    coordinates: Optional[Dict[str, float]] = None
    contact_person: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    max_capacity: Optional[int] = None
    facilities: Optional[List[str]] = None

class LocationResponse(LocationBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

# Activity schemas
class ActivityBase(BaseSchema):
    slug: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=255)
    category: ActivityCategory
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: int = Field(..., ge=15, le=480)  # 15 min to 8 hours
    seasonality: List[str] = []
    safety_level: SafetyLevel = SafetyLevel.LOW
    min_age: int = Field(default=16, ge=12, le=25)
    max_participants: int = Field(default=8, ge=1, le=20)
    prerequisites: Optional[str] = None
    location_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    skill_tags: List[str] = []
    materials: List[str] = []

class ActivityUpdate(BaseSchema):
    title: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = None
    seasonality: Optional[List[str]] = None
    safety_level: Optional[SafetyLevel] = None
    min_age: Optional[int] = None
    max_participants: Optional[int] = None
    prerequisites: Optional[str] = None
    location_id: Optional[int] = None
    skill_tags: Optional[List[str]] = None
    materials: Optional[List[str]] = None

class ActivityResponse(ActivityBase):
    id: int
    skill_tags: List[str] = []
    materials: List[str] = []
    location: Optional[LocationResponse] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class ActivitySummary(BaseSchema):
    id: int
    slug: str
    title: str
    category: ActivityCategory
    summary: Optional[str] = None
    duration_min: int
    safety_level: SafetyLevel
    location_name: Optional[str] = None

# Reservation schemas
class ReservationBase(BaseSchema):
    activity_id: int
    scheduled_date: Optional[datetime] = None
    notes: Optional[str] = None

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseSchema):
    scheduled_date: Optional[datetime] = None
    status: Optional[ReservationStatus] = None
    notes: Optional[str] = None
    mentor_notes: Optional[str] = None
    duration_actual: Optional[int] = None

class ReservationResponse(BaseSchema):
    id: int
    user_id: int
    activity_id: int
    scheduled_date: Optional[datetime] = None
    duration_actual: Optional[int] = None
    status: ReservationStatus
    notes: Optional[str] = None
    mentor_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    activity: Optional[ActivitySummary] = None
    user: Optional[UserResponse] = None

# Evaluation schemas
class EvaluationBase(BaseSchema):
    skill_demonstration: Optional[float] = Field(None, ge=1, le=5)
    safety_compliance: Optional[float] = Field(None, ge=1, le=5)
    teamwork: Optional[float] = Field(None, ge=1, le=5)
    initiative: Optional[float] = Field(None, ge=1, le=5)
    overall_rating: Optional[float] = Field(None, ge=1, le=5)
    strengths: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    mentor_comments: Optional[str] = None
    student_feedback: Optional[str] = None
    goals_achieved: List[str] = []
    next_recommendations: List[str] = []

class EvaluationCreate(EvaluationBase):
    reservation_id: int

class EvaluationUpdate(EvaluationBase):
    pass

class EvaluationResponse(EvaluationBase):
    id: int
    reservation_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

# AI Suggestion schemas
class ActivitySuggestion(BaseSchema):
    activity: ActivityResponse
    score: float
    reasons: List[str]

class AIRecommendationRequest(BaseSchema):
    user_profile: UserProfile
    context: Optional[str] = None
    limit: int = Field(default=5, ge=1, le=20)

class AIRecommendationResponse(BaseSchema):
    suggestions: List[ActivitySuggestion]
    reasoning: str

# Generic response schemas
class MessageResponse(BaseSchema):
    message: str
    success: bool = True

class PaginatedResponse(BaseSchema):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int