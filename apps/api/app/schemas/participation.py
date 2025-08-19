from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class ParticipationBase(BaseModel):
    scheduled_date: Optional[datetime] = None
    status: Optional[str] = "registered"


class ParticipationCreate(ParticipationBase):
    activity_id: int


class ParticipationUpdate(BaseModel):
    status: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    rating: Optional[int] = None
    comment: Optional[str] = None
    feedback: Optional[dict] = None
    skills_acquired: Optional[List[str]] = None
    completion_percentage: Optional[float] = None


class Participation(ParticipationBase):
    id: int
    user_id: int
    activity_id: int
    completion_date: Optional[datetime] = None
    rating: Optional[int] = None
    comment: Optional[str] = None
    feedback: Optional[dict] = None
    skills_acquired: Optional[List[str]] = []
    completion_percentage: Optional[float] = 0.0
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ParticipationWithActivity(Participation):
    # Participation with activity details
    activity: Optional[Any] = None  # Will be Activity schema


class ParticipationWithUser(Participation):
    # Participation with user details
    user: Optional[Any] = None  # Will be User schema