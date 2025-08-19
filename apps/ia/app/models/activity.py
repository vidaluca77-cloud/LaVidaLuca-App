"""
Activity model.
"""
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Activity(Base):
    """Activity model for agricultural and educational activities."""
    
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    difficulty_level = Column(Integer, default=1)  # 1-5 scale
    duration_hours = Column(Float, nullable=True)
    max_participants = Column(Integer, nullable=True)
    location = Column(String(255), nullable=True)
    equipment_needed = Column(Text, nullable=True)
    learning_objectives = Column(Text, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Creator
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships will be defined after all models are imported
    # creator = relationship("User", back_populates="activities")
    # recommendations = relationship("Recommendation", back_populates="activity")