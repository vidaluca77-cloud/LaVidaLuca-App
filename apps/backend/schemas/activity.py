"""
Activity schemas for educational activities and learning experiences.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, UUID4, validator
from enum import Enum


class ActivityCategory(str, Enum):
    """Activity categories."""
    AGRI = "agri"
    TRANSFO = "transfo"
    ARTISANAT = "artisanat"
    NATURE = "nature"
    SOCIAL = "social"


class LocationType(str, Enum):
    """Location types for activities."""
    INDOOR = "indoor"
    OUTDOOR = "outdoor"
    FIELD = "field"
    WORKSHOP = "workshop"
    MIXED = "mixed"


class ActivityBase(BaseModel):
    """Base activity schema."""
    title: str = Field(..., max_length=255)
    category: ActivityCategory
    summary: str = Field(..., max_length=1000)
    description: Optional[str] = None
    duration_min: int = Field(..., gt=0)
    skill_tags: Optional[List[str]] = Field(default_factory=list)
    safety_level: int = Field(1, ge=1, le=5)
    materials: Optional[List[str]] = Field(default_factory=list)


class ActivityCreate(ActivityBase):
    """Activity creation schema."""
    difficulty_level: int = Field(1, ge=1, le=5)
    min_participants: int = Field(1, ge=1)
    max_participants: Optional[int] = Field(None, gt=0)
    age_min: Optional[int] = Field(None, ge=0)
    age_max: Optional[int] = Field(None, ge=0)
    location_type: Optional[LocationType] = None
    location_details: Optional[str] = None
    preparation_time: int = Field(0, ge=0)
    learning_objectives: Optional[List[str]] = Field(default_factory=list)
    assessment_methods: Optional[List[str]] = Field(default_factory=list)
    pedagogical_notes: Optional[str] = None
    keywords: Optional[List[str]] = Field(default_factory=list)
    season_tags: Optional[List[str]] = Field(default_factory=list)
    external_resources: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    @validator('max_participants')
    def validate_max_participants(cls, v, values):
        """Ensure max_participants >= min_participants."""
        if v is not None and 'min_participants' in values:
            if v < values['min_participants']:
                raise ValueError('max_participants must be >= min_participants')
        return v
    
    @validator('age_max')
    def validate_age_max(cls, v, values):
        """Ensure age_max >= age_min."""
        if v is not None and 'age_min' in values and values['age_min'] is not None:
            if v < values['age_min']:
                raise ValueError('age_max must be >= age_min')
        return v


class ActivityUpdate(BaseModel):
    """Activity update schema."""
    title: Optional[str] = Field(None, max_length=255)
    category: Optional[ActivityCategory] = None
    summary: Optional[str] = Field(None, max_length=1000)
    description: Optional[str] = None
    duration_min: Optional[int] = Field(None, gt=0)
    skill_tags: Optional[List[str]] = None
    safety_level: Optional[int] = Field(None, ge=1, le=5)
    materials: Optional[List[str]] = None
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    min_participants: Optional[int] = Field(None, ge=1)
    max_participants: Optional[int] = Field(None, gt=0)
    age_min: Optional[int] = Field(None, ge=0)
    age_max: Optional[int] = Field(None, ge=0)
    location_type: Optional[LocationType] = None
    location_details: Optional[str] = None
    preparation_time: Optional[int] = Field(None, ge=0)
    learning_objectives: Optional[List[str]] = None
    assessment_methods: Optional[List[str]] = None
    pedagogical_notes: Optional[str] = None
    keywords: Optional[List[str]] = None
    season_tags: Optional[List[str]] = None
    external_resources: Optional[Dict[str, Any]] = None
    is_published: Optional[bool] = None
    is_featured: Optional[bool] = None


class ActivityResponse(BaseModel):
    """Activity response schema."""
    id: UUID4
    title: str
    category: str
    summary: str
    description: Optional[str]
    duration_min: int
    skill_tags: List[str]
    safety_level: int
    materials: List[str]
    difficulty_level: int
    min_participants: int
    max_participants: Optional[int]
    age_min: Optional[int]
    age_max: Optional[int]
    location_type: Optional[str]
    location_details: Optional[str]
    preparation_time: int
    learning_objectives: List[str]
    assessment_methods: List[str]
    pedagogical_notes: Optional[str]
    is_published: bool
    is_featured: bool
    keywords: List[str]
    season_tags: List[str]
    external_resources: Dict[str, Any]
    metadata: Dict[str, Any]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ActivityListResponse(BaseModel):
    """Activity list response schema (minimal info for listings)."""
    id: UUID4
    title: str
    category: str
    summary: str
    duration_min: int
    skill_tags: List[str]
    safety_level: int
    difficulty_level: int
    is_featured: bool
    created_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ActivitySearchFilters(BaseModel):
    """Activity search and filter parameters."""
    category: Optional[ActivityCategory] = None
    min_duration: Optional[int] = Field(None, ge=0)
    max_duration: Optional[int] = Field(None, gt=0)
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    safety_level: Optional[int] = Field(None, ge=1, le=5)
    skill_tags: Optional[List[str]] = None
    keywords: Optional[str] = None
    location_type: Optional[LocationType] = None
    season_tags: Optional[List[str]] = None
    is_featured: Optional[bool] = None
    
    @validator('max_duration')
    def validate_max_duration(cls, v, values):
        """Ensure max_duration >= min_duration."""
        if v is not None and 'min_duration' in values and values['min_duration'] is not None:
            if v < values['min_duration']:
                raise ValueError('max_duration must be >= min_duration')
        return v