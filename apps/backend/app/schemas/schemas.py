from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    profile: Optional[Dict[str, Any]] = None


class User(UserBase):
    id: int
    profile: Optional[Dict[str, Any]] = None
    is_verified: bool = False
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Activity Schemas
class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    difficulty_level: str = "beginner"
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    equipment_needed: Optional[str] = None
    learning_objectives: Optional[str] = None
    is_published: bool = False


class ActivityCreate(ActivityBase):
    # Enhanced fields for creation
    skill_tags: Optional[List[str]] = []
    materials: Optional[List[str]] = []
    safety_level: Optional[int] = 1
    min_participants: Optional[int] = 1
    max_participants: Optional[int] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    season_tags: Optional[List[str]] = []
    location_type: Optional[str] = None
    preparation_time: Optional[int] = 0
    assessment_methods: Optional[List[str]] = []
    pedagogical_notes: Optional[str] = None
    keywords: Optional[List[str]] = []
    external_resources: Optional[Dict[str, Any]] = {}
    is_featured: bool = False


class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    equipment_needed: Optional[str] = None
    learning_objectives: Optional[str] = None
    is_published: Optional[bool] = None
    skill_tags: Optional[List[str]] = None
    materials: Optional[List[str]] = None
    safety_level: Optional[int] = None
    min_participants: Optional[int] = None
    max_participants: Optional[int] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    season_tags: Optional[List[str]] = None
    location_type: Optional[str] = None
    preparation_time: Optional[int] = None
    assessment_methods: Optional[List[str]] = None
    pedagogical_notes: Optional[str] = None
    keywords: Optional[List[str]] = None
    external_resources: Optional[Dict[str, Any]] = None
    is_featured: Optional[bool] = None


class Activity(ActivityCreate):
    id: int
    creator_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


# Activity Suggestion Schemas
class ActivitySuggestionBase(BaseModel):
    suggestion_reason: str
    score: Optional[int] = 50
    ai_generated: bool = True


class ActivitySuggestionCreate(ActivitySuggestionBase):
    user_query: Optional[str] = None
    matching_criteria: Optional[Dict[str, Any]] = {}


class ActivitySuggestion(ActivitySuggestionBase):
    id: int
    user_id: int
    activity_id: int
    user_query: Optional[str] = None
    matching_criteria: Optional[Dict[str, Any]] = {}
    created_at: datetime
    activity: Activity

    class Config:
        from_attributes = True


# Contact Schemas
class ContactBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    organization: Optional[str] = None
    subject: str
    message: str
    contact_type: str = "general"


class ContactCreate(ContactBase):
    consent_privacy: bool = True
    consent_marketing: bool = False


class ContactUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[int] = None
    is_responded: Optional[bool] = None
    tags: Optional[List[str]] = None


class Contact(ContactBase):
    id: int
    status: str = "new"
    priority: str = "normal"
    assigned_to: Optional[int] = None
    is_responded: bool = False
    response_count: int = 0
    last_response_at: Optional[datetime] = None
    tags: Optional[List[str]] = []
    consent_privacy: bool = True
    consent_marketing: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# OpenAI Integration Schemas
class SuggestionRequest(BaseModel):
    query: str
    preferences: Optional[Dict[str, Any]] = {}
    max_suggestions: int = 5
    filters: Optional[Dict[str, Any]] = {}


class SuggestionResponse(BaseModel):
    suggestions: List[ActivitySuggestion]
    total_count: int
    ai_generated: bool = True
    processing_time: Optional[float] = None

    class Config:
        from_attributes = True