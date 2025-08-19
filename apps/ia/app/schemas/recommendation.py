"""
Recommendation schemas for API request/response models.
"""
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from .activity import Activity


class RecommendationBase(BaseModel):
    """Base recommendation schema."""
    confidence_score: float
    reasoning: Optional[str] = None
    recommendation_type: str


class RecommendationCreate(RecommendationBase):
    """Schema for recommendation creation."""
    user_id: int
    activity_id: int


class RecommendationUpdate(BaseModel):
    """Schema for recommendation updates."""
    user_rating: Optional[int] = None
    user_feedback: Optional[str] = None


class RecommendationInDB(RecommendationBase):
    """Schema for recommendation in database."""
    id: int
    user_id: int
    activity_id: int
    user_rating: Optional[int] = None
    user_feedback: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Recommendation(RecommendationInDB):
    """Schema for recommendation response."""
    activity: Optional[Activity] = None


class RecommendationList(BaseModel):
    """Schema for recommendation list response."""
    recommendations: List[Recommendation]
    total: int
    page: int
    size: int


class RecommendationRequest(BaseModel):
    """Schema for requesting recommendations."""
    user_interests: Optional[List[str]] = None
    preferred_difficulty: Optional[int] = None
    max_duration: Optional[float] = None
    location_preference: Optional[str] = None