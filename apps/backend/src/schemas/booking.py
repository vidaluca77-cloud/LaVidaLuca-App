"""Booking schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator

from ..models.booking import BookingStatus


# Base schemas
class BookingBase(BaseModel):
    """Base booking schema."""
    activity_id: UUID
    start_date: datetime
    end_date: datetime
    participants_count: int = Field(ge=1, default=1)
    notes: Optional[str] = None

    @validator('end_date')
    def end_date_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v


class BookingCreate(BookingBase):
    """Schema for creating a booking."""
    pass


class BookingUpdate(BaseModel):
    """Schema for updating a booking."""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    participants_count: Optional[int] = Field(None, ge=1)
    notes: Optional[str] = None
    status: Optional[BookingStatus] = None
    cancellation_reason: Optional[str] = None

    @validator('end_date')
    def end_date_after_start_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v <= values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v


class Booking(BookingBase):
    """Schema for booking response."""
    id: UUID
    user_id: UUID
    status: BookingStatus
    cancellation_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookingWithDetails(Booking):
    """Booking schema with user and activity details."""
    user: "UserSummary"
    activity: "ActivitySummary"

    class Config:
        from_attributes = True


class BookingSummary(BaseModel):
    """Summary booking schema."""
    id: UUID
    activity_id: UUID
    start_date: datetime
    end_date: datetime
    status: BookingStatus
    participants_count: int

    class Config:
        from_attributes = True


# Avoid circular imports
from .user import User as UserSummary  # noqa: E402
from .activity import ActivitySummary  # noqa: E402
BookingWithDetails.model_rebuild()