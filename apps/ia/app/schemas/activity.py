"""
Activity schemas for API request/response models.
"""
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class ActivityBase(BaseModel):
    """Base activity schema."""
    title: str
    description: str
    category: str
    difficulty_level: Optional[int] = 1
    duration_hours: Optional[float] = None
    max_participants: Optional[int] = None
    location: Optional[str] = None
    equipment_needed: Optional[str] = None
    learning_objectives: Optional[str] = None


class ActivityCreate(ActivityBase):
    """Schema for activity creation."""
    pass


class ActivityUpdate(BaseModel):
    """Schema for activity updates."""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[int] = None
    duration_hours: Optional[float] = None
    max_participants: Optional[int] = None
    location: Optional[str] = None
    equipment_needed: Optional[str] = None
    learning_objectives: Optional[str] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None


class ActivityInDB(ActivityBase):
    """Schema for activity in database."""
    id: int
    creator_id: int
    is_active: bool
    is_featured: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Activity(ActivityInDB):
    """Schema for activity response."""
    pass


class ActivityList(BaseModel):
    """Schema for activity list response."""
    activities: List[Activity]
    total: int
    page: int
    size: int