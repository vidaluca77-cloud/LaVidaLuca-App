"""Activity model."""

import enum
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import ARRAY, Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.session import Base

if TYPE_CHECKING:
    from .location import Location  # noqa: F401
    from .booking import Booking  # noqa: F401
    from .progress import Progress  # noqa: F401


class ActivityCategory(str, enum.Enum):
    """Activity categories."""
    AGRI = "agri"
    TRANSFO = "transfo"
    ARTISANAT = "artisanat"
    NATURE = "nature"
    SOCIAL = "social"


class Activity(Base):
    """Activity model."""
    
    __tablename__ = "activities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    category = Column(String, nullable=False)  # ActivityCategory enum
    duration_min = Column(Integer, nullable=False)
    max_participants = Column(Integer, nullable=False, default=10)
    difficulty_level = Column(Integer, nullable=False)  # 1-5
    materials = Column(ARRAY(String), nullable=False, default=[])
    skill_tags = Column(ARRAY(String), nullable=False, default=[])
    seasonality = Column(ARRAY(String), nullable=False, default=[])
    safety_level = Column(Integer, nullable=False)  # 1-3
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=True)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    location = relationship("Location", back_populates="activities")
    bookings = relationship("Booking", back_populates="activity")
    progress_records = relationship("Progress", back_populates="activity")