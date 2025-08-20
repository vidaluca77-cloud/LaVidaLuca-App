from datetime import datetime
from typing import Optional, Dict, Any
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


class User(UserBase):
    id: int
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
    pass


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


class Activity(ActivityBase):
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
    ai_generated: bool = True


class ActivitySuggestion(ActivitySuggestionBase):
    id: int
    user_id: int
    activity_id: int
    created_at: datetime
    activity: Activity

    class Config:
        from_attributes = True


# Consultation Schemas
class ConsultationRequest(BaseModel):
    question: str
    context: Optional[Dict[str, Any]] = None


class ConsultationResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    question: str
    response: str
    context: Optional[Dict[str, Any]] = None
    model_used: str
    tokens_used: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True