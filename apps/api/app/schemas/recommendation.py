from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class ProgressBase(BaseModel):
    metric_type: str
    metric_value: float
    metric_unit: Optional[str] = None
    description: Optional[str] = None
    evidence: Optional[dict] = None
    verified_by: Optional[str] = None


class ProgressCreate(ProgressBase):
    participation_id: Optional[int] = None


class ProgressUpdate(BaseModel):
    metric_value: Optional[float] = None
    metric_unit: Optional[str] = None
    description: Optional[str] = None
    evidence: Optional[dict] = None
    verified_by: Optional[str] = None


class Progress(ProgressBase):
    id: int
    user_id: int
    participation_id: Optional[int] = None
    recorded_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# Recommendation schemas
class RecommendationRequest(BaseModel):
    user_skills: Optional[List[str]] = []
    user_preferences: Optional[List[str]] = []
    user_availability: Optional[List[str]] = []
    limit: Optional[int] = 5


class ActivityRecommendation(BaseModel):
    activity: Any  # Activity schema
    score: float
    reasons: List[str]
    confidence: Optional[float] = None


class RecommendationResponse(BaseModel):
    recommendations: List[ActivityRecommendation]
    total_activities: int
    user_profile_completeness: Optional[float] = None