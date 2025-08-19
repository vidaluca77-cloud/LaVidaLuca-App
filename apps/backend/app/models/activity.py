"""
Activity model for managing agricultural and educational activities.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func

from ..core.database import Base


class Activity(Base):
    """Activity model for managing agricultural activities."""
    
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    
    # Activity details
    category = Column(String, nullable=False)  # agri, transfo, artisanat, nature, social
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    
    # Activity metadata
    duration_min = Column(Integer, nullable=False)
    safety_level = Column(Integer, default=1)  # 1-3 safety levels
    
    # Skills and requirements (stored as JSON strings for simplicity)
    skill_tags = Column(Text, nullable=True)  # JSON array as string
    seasonality = Column(Text, nullable=True)  # JSON array as string
    materials = Column(Text, nullable=True)  # JSON array as string
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())