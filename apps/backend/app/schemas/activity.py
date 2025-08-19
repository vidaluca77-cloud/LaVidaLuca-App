from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class ActivityBase(BaseModel):
    """Base activity schema"""
    slug: str
    title: str
    category: str
    summary: str
    description: Optional[str] = None
    duration_min: int
    skill_tags: List[str] = []
    seasonality: List[str] = []
    safety_level: int = 1
    materials: List[str] = []
    location_type: Optional[str] = None
    max_participants: int = 10
    min_age: int = 14
    is_mfr_only: bool = False
    difficulty_level: int = 1
    learning_objectives: List[str] = []
    prerequisites: List[str] = []

class ActivityCreate(ActivityBase):
    """Schema for activity creation"""
    
    @validator('category')
    def validate_category(cls, v):
        allowed_categories = ['agri', 'transfo', 'artisanat', 'nature', 'social']
        if v not in allowed_categories:
            raise ValueError(f'Category must be one of: {", ".join(allowed_categories)}')
        return v
    
    @validator('safety_level')
    def validate_safety_level(cls, v):
        if v < 1 or v > 3:
            raise ValueError('Safety level must be between 1 and 3')
        return v
    
    @validator('difficulty_level')
    def validate_difficulty_level(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Difficulty level must be between 1 and 5')
        return v

class ActivityUpdate(BaseModel):
    """Schema for activity updates"""
    title: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = None
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[List[str]] = None
    safety_level: Optional[int] = None
    materials: Optional[List[str]] = None
    location_type: Optional[str] = None
    max_participants: Optional[int] = None
    min_age: Optional[int] = None
    is_active: Optional[bool] = None
    is_mfr_only: Optional[bool] = None
    difficulty_level: Optional[int] = None
    learning_objectives: Optional[List[str]] = None
    prerequisites: Optional[List[str]] = None

class ActivityResponse(ActivityBase):
    """Schema for activity response"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ActivityRecommendation(BaseModel):
    """Schema for activity recommendations"""
    activity: ActivityResponse
    score: float
    reasons: List[str]
    match_percentage: int