from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ActivityBase(BaseModel):
    slug: str
    title: str
    category: str  # 'agri', 'transfo', 'artisanat', 'nature', 'social'
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = None
    skill_tags: List[str] = []
    seasonality: List[str] = []
    safety_level: int = 1
    materials: List[str] = []


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    slug: Optional[str] = None
    title: Optional[str] = None
    category: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = None
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[List[str]] = None
    safety_level: Optional[int] = None
    materials: Optional[List[str]] = None


class Activity(ActivityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserActivityBase(BaseModel):
    user_id: int
    activity_id: int
    status: str = "interested"
    rating: Optional[int] = None
    feedback: Optional[str] = None


class UserActivityCreate(UserActivityBase):
    pass


class UserActivityUpdate(BaseModel):
    status: Optional[str] = None
    rating: Optional[int] = None
    feedback: Optional[str] = None


class UserActivity(UserActivityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True