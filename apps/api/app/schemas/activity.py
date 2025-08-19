from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class ActivityBase(BaseModel):
    title: str
    category: str
    summary: str
    description: Optional[str] = None
    duration_min: int
    skill_tags: Optional[List[str]] = []
    seasonality: Optional[List[str]] = []
    safety_level: Optional[int] = 1
    materials: Optional[List[str]] = []
    max_participants: Optional[int] = 10
    min_age: Optional[int] = 16
    location: Optional[str] = None
    difficulty_level: Optional[int] = 1


class ActivityCreate(ActivityBase):
    slug: str


class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
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
    difficulty_level: Optional[int] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None


class Activity(ActivityBase):
    id: int
    slug: str
    is_active: bool
    is_featured: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ActivityWithStats(Activity):
    # Activity with participation statistics
    participant_count: Optional[int] = 0
    average_rating: Optional[float] = 0.0
    completion_rate: Optional[float] = 0.0