"""
Profile schemas for user profile management.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime


class ProfileCreate(BaseModel):
    """Schema for creating a new profile."""
    skills: Optional[List[str]] = Field(default_factory=list)
    availability: Optional[List[str]] = Field(default_factory=list)
    location: Optional[str] = None
    preferences: Optional[List[str]] = Field(default_factory=list)
    experience_level: str = Field(default="beginner")
    education_background: Optional[List[str]] = Field(default_factory=list)
    certifications: Optional[List[str]] = Field(default_factory=list)
    learning_style: Optional[List[str]] = Field(default_factory=list)
    preferred_activity_types: Optional[List[str]] = Field(default_factory=list)
    preferred_group_size: Optional[str] = None
    time_availability: Optional[Dict[str, Any]] = Field(default_factory=dict)
    seasonal_availability: Optional[List[str]] = Field(default_factory=list)
    interests: Optional[List[str]] = Field(default_factory=list)
    learning_goals: Optional[List[str]] = Field(default_factory=list)
    career_goals: Optional[List[str]] = Field(default_factory=list)
    physical_limitations: Optional[List[str]] = Field(default_factory=list)
    safety_preferences: Optional[Dict[str, Any]] = Field(default_factory=dict)
    accessibility_needs: Optional[List[str]] = Field(default_factory=list)
    mentoring_interest: bool = Field(default=False)
    collaboration_preference: str = Field(default="flexible")
    communication_style: Optional[List[str]] = Field(default_factory=list)
    travel_willingness: str = Field(default="local")
    transportation_access: Optional[List[str]] = Field(default_factory=list)
    custom_fields: Optional[Dict[str, Any]] = Field(default_factory=dict)
    is_public: bool = Field(default=True)
    
    @validator('experience_level')
    def validate_experience_level(cls, v):
        """Validate experience level."""
        allowed_levels = ['beginner', 'intermediate', 'advanced']
        if v not in allowed_levels:
            raise ValueError(f'Experience level must be one of: {", ".join(allowed_levels)}')
        return v
    
    @validator('collaboration_preference')
    def validate_collaboration_preference(cls, v):
        """Validate collaboration preference."""
        allowed_prefs = ['solo', 'team', 'flexible']
        if v not in allowed_prefs:
            raise ValueError(f'Collaboration preference must be one of: {", ".join(allowed_prefs)}')
        return v
    
    @validator('travel_willingness')
    def validate_travel_willingness(cls, v):
        """Validate travel willingness."""
        allowed_options = ['local', 'regional', 'national']
        if v not in allowed_options:
            raise ValueError(f'Travel willingness must be one of: {", ".join(allowed_options)}')
        return v


class ProfileUpdate(BaseModel):
    """Schema for updating an existing profile."""
    skills: Optional[List[str]] = None
    availability: Optional[List[str]] = None
    location: Optional[str] = None
    preferences: Optional[List[str]] = None
    experience_level: Optional[str] = None
    education_background: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    learning_style: Optional[List[str]] = None
    preferred_activity_types: Optional[List[str]] = None
    preferred_group_size: Optional[str] = None
    time_availability: Optional[Dict[str, Any]] = None
    seasonal_availability: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    learning_goals: Optional[List[str]] = None
    career_goals: Optional[List[str]] = None
    physical_limitations: Optional[List[str]] = None
    safety_preferences: Optional[Dict[str, Any]] = None
    accessibility_needs: Optional[List[str]] = None
    mentoring_interest: Optional[bool] = None
    collaboration_preference: Optional[str] = None
    communication_style: Optional[List[str]] = None
    travel_willingness: Optional[str] = None
    transportation_access: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None
    
    @validator('experience_level')
    def validate_experience_level(cls, v):
        """Validate experience level."""
        if v is not None:
            allowed_levels = ['beginner', 'intermediate', 'advanced']
            if v not in allowed_levels:
                raise ValueError(f'Experience level must be one of: {", ".join(allowed_levels)}')
        return v
    
    @validator('collaboration_preference')
    def validate_collaboration_preference(cls, v):
        """Validate collaboration preference."""
        if v is not None:
            allowed_prefs = ['solo', 'team', 'flexible']
            if v not in allowed_prefs:
                raise ValueError(f'Collaboration preference must be one of: {", ".join(allowed_prefs)}')
        return v
    
    @validator('travel_willingness')
    def validate_travel_willingness(cls, v):
        """Validate travel willingness."""
        if v is not None:
            allowed_options = ['local', 'regional', 'national']
            if v not in allowed_options:
                raise ValueError(f'Travel willingness must be one of: {", ".join(allowed_options)}')
        return v


class ProfileResponse(BaseModel):
    """Schema for profile response."""
    id: str
    user_id: str
    skills: List[str]
    availability: List[str]
    location: Optional[str]
    preferences: List[str]
    experience_level: str
    education_background: List[str]
    certifications: List[str]
    learning_style: List[str]
    preferred_activity_types: List[str]
    preferred_group_size: Optional[str]
    time_availability: Dict[str, Any]
    seasonal_availability: List[str]
    interests: List[str]
    learning_goals: List[str]
    career_goals: List[str]
    physical_limitations: List[str]
    safety_preferences: Dict[str, Any]
    accessibility_needs: List[str]
    mentoring_interest: bool
    collaboration_preference: str
    communication_style: List[str]
    travel_willingness: str
    transportation_access: List[str]
    custom_fields: Dict[str, Any]
    is_complete: bool
    is_public: bool
    completion_percentage: float
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_orm(cls, obj):
        """Create ProfileResponse from ORM object."""
        data = obj.to_dict()
        data['completion_percentage'] = obj.completion_percentage
        return cls(**data)


class ProfileListResponse(BaseModel):
    """Schema for profile list response (public info only)."""
    id: str
    user_id: str
    skills: List[str]
    location: Optional[str]
    experience_level: str
    interests: List[str]
    mentoring_interest: bool
    collaboration_preference: str
    travel_willingness: str
    completion_percentage: float
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_orm(cls, obj):
        """Create ProfileListResponse from ORM object."""
        return cls(
            id=str(obj.id),
            user_id=str(obj.user_id),
            skills=obj.skills or [],
            location=obj.location,
            experience_level=obj.experience_level,
            interests=obj.interests or [],
            mentoring_interest=obj.mentoring_interest,
            collaboration_preference=obj.collaboration_preference,
            travel_willingness=obj.travel_willingness,
            completion_percentage=obj.completion_percentage
        )


class ProfileSearchFilters(BaseModel):
    """Schema for profile search filters."""
    skills: Optional[List[str]] = None
    location: Optional[str] = None
    experience_level: Optional[str] = None
    interests: Optional[List[str]] = None
    mentoring_interest: Optional[bool] = None
    collaboration_preference: Optional[str] = None
    travel_willingness: Optional[str] = None
    min_completion: Optional[float] = Field(None, ge=0, le=100)