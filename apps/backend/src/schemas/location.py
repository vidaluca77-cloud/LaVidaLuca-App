"""Location schemas."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# Base schemas
class LocationBase(BaseModel):
    """Base location schema."""
    name: str
    address: str
    city: str
    postal_code: str
    country: str = "France"
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    description: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    image_url: Optional[str] = None


class LocationCreate(LocationBase):
    """Schema for creating a location."""
    pass


class LocationUpdate(BaseModel):
    """Schema for updating a location."""
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    description: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    image_url: Optional[str] = None


class Location(LocationBase):
    """Schema for location response."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LocationWithActivities(Location):
    """Location schema with activities."""
    activities: List["ActivitySummary"] = []

    class Config:
        from_attributes = True


class LocationSummary(BaseModel):
    """Summary location schema."""
    id: UUID
    name: str
    city: str
    country: str

    class Config:
        from_attributes = True


# Avoid circular imports
from .activity import ActivitySummary  # noqa: E402
LocationWithActivities.model_rebuild()