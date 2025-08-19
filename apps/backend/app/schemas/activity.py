"""
Activity schemas for API input/output validation.
"""

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.models.activity import ActivityCategory


class ActivityBase(BaseModel):
    """Base activity schema with common fields."""
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
    min_participants: int = 1
    max_participants: int = 10
    location_type: Optional[str] = None
    difficulty_level: int = 1
    learning_objectives: List[str] = []
    prerequisites: List[str] = []


class ActivityCreate(ActivityBase):
    """Schema for activity creation."""
    pass


class ActivityUpdate(BaseModel):
    """Schema for activity updates."""
    slug: Optional[str] = None
    title: Optional[str] = None
    category: Optional[ActivityCategory] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = None
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[List[str]] = None
    safety_level: Optional[int] = None
    materials: Optional[List[str]] = None
    min_participants: Optional[int] = None
    max_participants: Optional[int] = None
    location_type: Optional[str] = None
    difficulty_level: Optional[int] = None
    learning_objectives: Optional[List[str]] = None
    prerequisites: Optional[List[str]] = None


class ActivityInDB(ActivityBase):
    """Schema for activity as stored in database."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Activity(ActivityInDB):
    """Schema for activity response (public)."""
    pass


class ActivitySuggestion(BaseModel):
    """Schema for activity suggestions (frontend compatibility)."""
    activity: Activity
    score: int
    reasons: List[str] = []


class ActivityFilter(BaseModel):
    """Schema for filtering activities."""
    category: Optional[ActivityCategory] = None
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[str] = None
    difficulty_level: Optional[int] = None
    safety_level: Optional[int] = None
    duration_min_range: Optional[List[int]] = None  # [min, max]