from sqlalchemy import Column, Integer, String, Text, JSON, Enum, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class ActivityCategory(str, enum.Enum):
    AGRI = "agri"
    TRANSFO = "transfo"
    ARTISANAT = "artisanat"
    NATURE = "nature"
    SOCIAL = "social"


class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(Enum(ActivityCategory), nullable=False)
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=True)  # Extended description
    
    # Activity details
    duration_min = Column(Integer, nullable=False)
    skill_tags = Column(JSON, default=list)  # Required/taught skills
    seasonality = Column(JSON, default=list)  # When activity is available
    safety_level = Column(Integer, default=1)  # 1-3 safety complexity
    materials = Column(JSON, default=list)  # Required materials
    
    # Capacity and logistics
    max_participants = Column(Integer, default=6)
    min_age = Column(Integer, default=14)
    location = Column(String, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    bookings = relationship("Booking", back_populates="activity")
    recommendations = relationship("Recommendation", back_populates="activity")