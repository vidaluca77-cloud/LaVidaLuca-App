"""
Activity schemas for API serialization.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


# Base schemas
class ActivityBase(BaseModel):
    """Base activity schema."""
    title: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., regex="^(agri|transfo|artisanat|nature|social)$")
    summary: str = Field(..., min_length=1)
    description: Optional[str] = None
    duration_min: int = Field(..., gt=0)
    difficulty_level: int = Field(default=1, ge=1, le=5)
    safety_level: int = Field(default=1, ge=1, le=5)
    min_participants: int = Field(default=1, gt=0)
    max_participants: Optional[int] = Field(None, gt=0)
    skill_tags: Optional[List[str]] = None
    materials: Optional[List[str]] = None
    prerequisites: Optional[List[str]] = None
    location_type: Optional[str] = Field(None, regex="^(indoor|outdoor|both)$")
    season_availability: Optional[List[str]] = None
    instructions: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    assessment_criteria: Optional[str] = None


class ActivityCreate(ActivityBase):
    """Schema for activity creation."""
    pass


class ActivityUpdate(BaseModel):
    """Schema for activity updates."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, regex="^(agri|transfo|artisanat|nature|social)$")
    summary: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    duration_min: Optional[int] = Field(None, gt=0)
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    safety_level: Optional[int] = Field(None, ge=1, le=5)
    min_participants: Optional[int] = Field(None, gt=0)
    max_participants: Optional[int] = Field(None, gt=0)
    skill_tags: Optional[List[str]] = None
    materials: Optional[List[str]] = None
    prerequisites: Optional[List[str]] = None
    location_type: Optional[str] = Field(None, regex="^(indoor|outdoor|both)$")
    season_availability: Optional[List[str]] = None
    instructions: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    assessment_criteria: Optional[str] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None


class ActivityInDBBase(ActivityBase):
    """Base schema for activity in database."""
    id: UUID
    is_active: bool
    is_featured: bool
    created_by: Optional[UUID] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class Activity(ActivityInDBBase):
    """Activity schema for API responses."""
    pass


class ActivityInDB(ActivityInDBBase):
    """Activity schema for internal use."""
    pass


# Activity submission schemas
class ActivitySubmissionBase(BaseModel):
    """Base activity submission schema."""
    submission_text: Optional[str] = None
    submission_files: Optional[List[str]] = None
    submission_data: Optional[Dict[str, Any]] = None


class ActivitySubmissionCreate(ActivitySubmissionBase):
    """Schema for activity submission creation."""
    activity_id: UUID


class ActivitySubmissionUpdate(BaseModel):
    """Schema for activity submission updates."""
    status: Optional[str] = Field(None, regex="^(started|completed|submitted|reviewed)$")
    progress_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    submission_text: Optional[str] = None
    submission_files: Optional[List[str]] = None
    submission_data: Optional[Dict[str, Any]] = None


class ActivitySubmissionReview(BaseModel):
    """Schema for activity submission review."""
    score: Optional[float] = Field(None, ge=0.0, le=100.0)
    feedback: Optional[str] = None


class ActivitySubmissionInDB(ActivitySubmissionBase):
    """Activity submission schema in database."""
    id: UUID
    user_id: UUID
    activity_id: UUID
    status: str
    progress_percentage: float
    score: Optional[float] = None
    feedback: Optional[str] = None
    reviewed_by: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    submitted_at: Optional[datetime] = None
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ActivitySubmission(ActivitySubmissionInDB):
    """Activity submission schema for API responses."""
    activity: Optional[Activity] = None


# Search and filtering schemas
class ActivityFilter(BaseModel):
    """Schema for activity filtering."""
    category: Optional[str] = None
    difficulty_level: Optional[int] = None
    safety_level: Optional[int] = None
    duration_min_min: Optional[int] = None
    duration_min_max: Optional[int] = None
    skill_tags: Optional[List[str]] = None
    location_type: Optional[str] = None
    season: Optional[str] = None
    is_featured: Optional[bool] = None


class ActivitySuggestion(BaseModel):
    """Schema for AI-generated activity suggestions."""
    activity: Activity
    score: float = Field(..., ge=0.0, le=1.0)
    reasons: List[str]
    
    
class ContactForm(BaseModel):
    """Schema for contact form submission."""
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=1, max_length=255)
    subject: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1, max_length=2000)
    activity_interest: Optional[str] = None