"""
Activity schemas for La Vida Luca application.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator


class ActivityBase(BaseModel):
    """Base activity schema with common fields."""
    title: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    tags: Optional[List[str]] = None
    difficulty_level: str = "beginner"
    duration_minutes: Optional[int] = None
    max_participants: Optional[int] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    location_type: Optional[str] = None
    location: Optional[str] = None
    equipment_needed: Optional[List[str]] = None
    preparation_time_minutes: Optional[int] = None
    learning_objectives: Optional[List[str]] = None
    competencies_developed: Optional[List[str]] = None
    prerequisites: Optional[str] = None
    assessment_methods: Optional[str] = None
    materials_provided: Optional[List[str]] = None
    additional_resources: Optional[List[str]] = None
    instructions: Optional[str] = None
    language: str = "fr"
    cost_estimate: Optional[float] = None
    sustainability_score: Optional[int] = None

    @validator('difficulty_level')
    def validate_difficulty(cls, v):
        allowed_levels = ['beginner', 'intermediate', 'advanced']
        if v not in allowed_levels:
            raise ValueError(f'Difficulty level must be one of: {", ".join(allowed_levels)}')
        return v

    @validator('sustainability_score')
    def validate_sustainability_score(cls, v):
        if v is not None and (v < 1 or v > 10):
            raise ValueError('Sustainability score must be between 1 and 10')
        return v

    @validator('duration_minutes')
    def validate_duration(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Duration must be positive')
        return v


class ActivityCreate(ActivityBase):
    """Schema for creating a new activity."""
    pass


class ActivityUpdate(BaseModel):
    """Schema for updating activity information."""
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    tags: Optional[List[str]] = None
    difficulty_level: Optional[str] = None
    duration_minutes: Optional[int] = None
    max_participants: Optional[int] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    location_type: Optional[str] = None
    location: Optional[str] = None
    equipment_needed: Optional[List[str]] = None
    preparation_time_minutes: Optional[int] = None
    learning_objectives: Optional[List[str]] = None
    competencies_developed: Optional[List[str]] = None
    prerequisites: Optional[str] = None
    assessment_methods: Optional[str] = None
    materials_provided: Optional[List[str]] = None
    additional_resources: Optional[List[str]] = None
    instructions: Optional[str] = None
    language: Optional[str] = None
    cost_estimate: Optional[float] = None
    sustainability_score: Optional[int] = None
    is_published: Optional[bool] = None

    @validator('difficulty_level')
    def validate_difficulty(cls, v):
        if v is not None:
            allowed_levels = ['beginner', 'intermediate', 'advanced']
            if v not in allowed_levels:
                raise ValueError(f'Difficulty level must be one of: {", ".join(allowed_levels)}')
        return v

    @validator('sustainability_score')
    def validate_sustainability_score(cls, v):
        if v is not None and (v < 1 or v > 10):
            raise ValueError('Sustainability score must be between 1 and 10')
        return v


class Activity(ActivityBase):
    """Complete activity schema for responses."""
    id: str
    creator_id: str
    is_published: bool
    is_featured: bool
    approval_status: str
    view_count: int
    rating_average: float
    rating_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ActivitySummary(BaseModel):
    """Summary activity schema for lists."""
    id: str
    title: str
    short_description: Optional[str] = None
    category: str
    difficulty_level: str
    duration_minutes: Optional[int] = None
    location_type: Optional[str] = None
    sustainability_score: Optional[int] = None
    rating_average: float
    rating_count: int
    is_featured: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ActivitySuggestionBase(BaseModel):
    """Base activity suggestion schema."""
    suggestion_reason: Optional[str] = None
    confidence_score: Optional[float] = None
    ai_generated: bool = True
    suggestion_type: str = "automatic"
    user_context: Optional[dict] = None
    matching_criteria: Optional[dict] = None

    @validator('confidence_score')
    def validate_confidence(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Confidence score must be between 0.0 and 1.0')
        return v

    @validator('suggestion_type')
    def validate_type(cls, v):
        allowed_types = ['automatic', 'manual', 'collaborative']
        if v not in allowed_types:
            raise ValueError(f'Suggestion type must be one of: {", ".join(allowed_types)}')
        return v


class ActivitySuggestionCreate(ActivitySuggestionBase):
    """Schema for creating activity suggestions."""
    activity_id: str
    user_id: str


class ActivitySuggestion(ActivitySuggestionBase):
    """Complete activity suggestion schema."""
    id: str
    user_id: str
    activity_id: str
    is_viewed: bool
    is_bookmarked: bool
    user_feedback: Optional[str] = None
    created_at: datetime
    viewed_at: Optional[datetime] = None
    activity: ActivitySummary

    class Config:
        from_attributes = True


class ActivitySearchFilters(BaseModel):
    """Schema for activity search filters."""
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    duration_min: Optional[int] = None
    duration_max: Optional[int] = None
    location_type: Optional[str] = None
    sustainability_min: Optional[int] = None
    tags: Optional[List[str]] = None
    search_query: Optional[str] = None
    is_featured: Optional[bool] = None
    limit: int = 20
    offset: int = 0

    @validator('limit')
    def validate_limit(cls, v):
        if v < 1 or v > 100:
            raise ValueError('Limit must be between 1 and 100')
        return v