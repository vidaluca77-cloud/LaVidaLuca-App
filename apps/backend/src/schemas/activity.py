"""Activity schemas."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from ..models.activity import ActivityCategory


# Base schemas
class ActivityBase(BaseModel):
    """Base activity schema."""
    title: str
    slug: str
    description: str
    summary: Optional[str] = None
    category: ActivityCategory
    duration_min: int = Field(gt=0)
    max_participants: int = Field(gt=0, default=10)
    difficulty_level: int = Field(ge=1, le=5)
    materials: List[str] = []
    skill_tags: List[str] = []
    seasonality: List[str] = []
    safety_level: int = Field(ge=1, le=3)
    location_id: Optional[UUID] = None
    image_url: Optional[str] = None
    is_active: bool = True


class ActivityCreate(ActivityBase):
    """Schema for creating an activity."""
    pass


class ActivityUpdate(BaseModel):
    """Schema for updating an activity."""
    title: Optional[str] = None
    description: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[ActivityCategory] = None
    duration_min: Optional[int] = Field(None, gt=0)
    max_participants: Optional[int] = Field(None, gt=0)
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    materials: Optional[List[str]] = None
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[List[str]] = None
    safety_level: Optional[int] = Field(None, ge=1, le=3)
    location_id: Optional[UUID] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class Activity(ActivityBase):
    """Schema for activity response."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActivityWithLocation(Activity):
    """Activity schema with location details."""
    location: Optional["LocationSummary"] = None

    class Config:
        from_attributes = True


class ActivitySummary(BaseModel):
    """Summary activity schema."""
    id: UUID
    title: str
    slug: str
    summary: Optional[str] = None
    category: ActivityCategory
    duration_min: int
    difficulty_level: int
    safety_level: int
    skill_tags: List[str]
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


# Avoid circular imports
from .location import LocationSummary  # noqa: E402
ActivityWithLocation.model_rebuild()