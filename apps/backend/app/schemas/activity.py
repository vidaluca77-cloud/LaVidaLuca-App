"""
Pydantic schemas for activity-related API endpoints.
"""
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class ActivityBase(BaseModel):
    """Base activity schema."""
    slug: str
    title: str
    category: str
    summary: str
    description: Optional[str] = None
    duration_min: int
    safety_level: int = 1


class ActivityCreate(ActivityBase):
    """Schema for creating a new activity."""
    skill_tags: Optional[List[str]] = []
    seasonality: Optional[List[str]] = []
    materials: Optional[List[str]] = []


class ActivityUpdate(BaseModel):
    """Schema for updating activity information."""
    title: Optional[str] = None
    category: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = None
    safety_level: Optional[int] = None
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[List[str]] = None
    materials: Optional[List[str]] = None
    is_active: Optional[bool] = None


class Activity(ActivityBase):
    """Full activity schema with all fields."""
    id: int
    skill_tags: Optional[List[str]] = []
    seasonality: Optional[List[str]] = []
    materials: Optional[List[str]] = []
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ActivitySummary(BaseModel):
    """Simplified activity schema for listings."""
    id: int
    slug: str
    title: str
    category: str
    summary: str
    duration_min: int
    safety_level: int
    skill_tags: Optional[List[str]] = []
    
    class Config:
        from_attributes = True