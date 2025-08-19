from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.booking import BookingStatus


class BookingBase(BaseModel):
    activity_id: int
    scheduled_date: datetime
    participants_count: int = 1
    user_notes: Optional[str] = None


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    scheduled_date: Optional[datetime] = None
    participants_count: Optional[int] = None
    user_notes: Optional[str] = None
    status: Optional[BookingStatus] = None
    admin_notes: Optional[str] = None
    completion_feedback: Optional[str] = None
    rating: Optional[float] = None


class Booking(BookingBase):
    id: int
    user_id: int
    status: BookingStatus
    admin_notes: Optional[str] = None
    completion_feedback: Optional[str] = None
    rating: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class BookingWithDetails(Booking):
    """Booking with user and activity details"""
    user: "User"
    activity: "Activity"


class RecommendationBase(BaseModel):
    activity_id: int
    score: float
    reasons: Optional[str] = None


class RecommendationCreate(RecommendationBase):
    user_id: int
    model_version: Optional[str] = None


class Recommendation(RecommendationBase):
    id: int
    user_id: int
    model_version: Optional[str] = None
    generated_at: datetime
    clicked: bool = False
    clicked_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Avoid circular imports
from app.schemas.user import User
from app.schemas.activity import Activity
BookingWithDetails.model_rebuild()