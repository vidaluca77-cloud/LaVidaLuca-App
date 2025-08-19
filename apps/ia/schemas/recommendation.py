from pydantic import BaseModel
from typing import List
from datetime import datetime
from schemas.activity import Activity


class RecommendationBase(BaseModel):
    user_id: int
    activity_id: int
    score: float
    reasons: List[str] = []
    ai_generated: bool = True


class RecommendationCreate(RecommendationBase):
    pass


class Recommendation(RecommendationBase):
    id: int
    created_at: datetime
    activity: Activity

    class Config:
        from_attributes = True


class Suggestion(BaseModel):
    activity: Activity
    score: float
    reasons: List[str]


class RecommendationRequest(BaseModel):
    user_profile: dict
    limit: int = 5