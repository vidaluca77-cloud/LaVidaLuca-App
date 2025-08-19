from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.activity import ActivityCategory


class ActivityBase(BaseModel):
    slug: str
    title: str
    category: ActivityCategory
    summary: str
    description: Optional[str] = None
    duration_min: int
    skill_tags: List[str] = []
    seasonality: List[str] = []
    safety_level: int = 1
    materials: List[str] = []
    max_participants: int = 6
    min_age: int = 14
    location: Optional[str] = None


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
    max_participants: Optional[int] = None
    min_age: Optional[int] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None


class Activity(ActivityBase):
    id: int
    is_active: bool
    is_featured: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ActivitySuggestion(BaseModel):
    """Activity suggestion with AI score and reasons"""
    activity: Activity
    score: float
    reasons: List[str]