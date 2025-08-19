"""Progress schemas."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# Base schemas
class ProgressBase(BaseModel):
    """Base progress schema."""
    activity_id: UUID
    completed_at: datetime
    rating: Optional[int] = Field(None, ge=1, le=5)
    feedback: Optional[str] = None
    skills_gained: List[str] = []
    time_spent_minutes: Optional[int] = Field(None, gt=0)
    achievements: List[str] = []


class ProgressCreate(ProgressBase):
    """Schema for creating a progress record."""
    pass


class ProgressUpdate(BaseModel):
    """Schema for updating a progress record."""
    rating: Optional[int] = Field(None, ge=1, le=5)
    feedback: Optional[str] = None
    skills_gained: Optional[List[str]] = None
    instructor_notes: Optional[str] = None
    time_spent_minutes: Optional[int] = Field(None, gt=0)
    achievements: Optional[List[str]] = None


class Progress(ProgressBase):
    """Schema for progress response."""
    id: UUID
    user_id: UUID
    instructor_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProgressWithDetails(Progress):
    """Progress schema with user and activity details."""
    user: "UserSummary"
    activity: "ActivitySummary"

    class Config:
        from_attributes = True


class ProgressSummary(BaseModel):
    """Summary progress schema."""
    id: UUID
    activity_id: UUID
    completed_at: datetime
    rating: Optional[int] = None
    skills_gained: List[str]

    class Config:
        from_attributes = True


class UserProgress(BaseModel):
    """User progress statistics."""
    user_id: UUID
    total_activities: int
    completed_activities: int
    total_time_spent: int
    skills_acquired: List[str]
    recent_activities: List[ProgressSummary]


# Avoid circular imports
from .user import User as UserSummary  # noqa: E402
from .activity import ActivitySummary  # noqa: E402
ProgressWithDetails.model_rebuild()