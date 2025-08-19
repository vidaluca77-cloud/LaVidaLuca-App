from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime


class ActivityBase(BaseModel):
    slug: str
    title: str
    category: str
    summary: str
    description: Optional[str] = ""
    duration_min: int
    skill_tags: Optional[List[str]] = []
    seasonality: Optional[List[str]] = []
    safety_level: int = 1
    materials: Optional[List[str]] = []
    
    @validator('category')
    def validate_category(cls, v):
        valid_categories = ['agri', 'transfo', 'artisanat', 'nature', 'social']
        if v not in valid_categories:
            raise ValueError(f'Category must be one of: {", ".join(valid_categories)}')
        return v
    
    @validator('safety_level')
    def validate_safety_level(cls, v):
        if v not in [1, 2, 3]:
            raise ValueError('Safety level must be 1, 2, or 3')
        return v
    
    @validator('duration_min')
    def validate_duration(cls, v):
        if v <= 0:
            raise ValueError('Duration must be positive')
        return v


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
    
    @validator('category')
    def validate_category(cls, v):
        if v is not None:
            valid_categories = ['agri', 'transfo', 'artisanat', 'nature', 'social']
            if v not in valid_categories:
                raise ValueError(f'Category must be one of: {", ".join(valid_categories)}')
        return v
    
    @validator('safety_level')
    def validate_safety_level(cls, v):
        if v is not None and v not in [1, 2, 3]:
            raise ValueError('Safety level must be 1, 2, or 3')
        return v
    
    @validator('duration_min')
    def validate_duration(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Duration must be positive')
        return v


class ActivityResponse(ActivityBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True