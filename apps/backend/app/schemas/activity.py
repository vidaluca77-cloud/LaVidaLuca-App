from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from ..models.activity import ActivityCategory, ActivityDifficulty


class ActivityBase(BaseModel):
    """Base activity schema with common fields"""
    title: str
    description: str
    category: ActivityCategory
    difficulty: ActivityDifficulty
    duration_hours: Optional[int] = None
    materials_needed: Optional[str] = None
    prerequisites: Optional[str] = None
    learning_objectives: Optional[str] = None
    location_type: Optional[str] = None
    max_participants: Optional[int] = None
    is_featured: bool = False


class ActivityCreate(ActivityBase):
    """Schema for activity creation"""
    pass


class ActivityUpdate(BaseModel):
    """Schema for activity updates"""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[ActivityCategory] = None
    difficulty: Optional[ActivityDifficulty] = None
    duration_hours: Optional[int] = None
    materials_needed: Optional[str] = None
    prerequisites: Optional[str] = None
    learning_objectives: Optional[str] = None
    location_type: Optional[str] = None
    max_participants: Optional[int] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None


class ActivityInDB(ActivityBase):
    """Schema for activity as stored in database"""
    id: int
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class Activity(ActivityInDB):
    """Schema for activity response"""
    pass


class ActivityWithCreator(Activity):
    """Schema for activity with creator information"""
    creator: Optional[dict] = None  # Will contain basic user info


class ActivityRecommendation(BaseModel):
    """Schema for AI-generated activity recommendations"""
    activity_id: int
    activity_title: str
    reason: str
    confidence_score: float
    recommended_next_steps: Optional[str] = None