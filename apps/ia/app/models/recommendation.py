"""
Recommendation model.
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Recommendation(Base):
    """Recommendation model for AI-powered activity suggestions."""
    
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    
    # AI recommendation data
    confidence_score = Column(Float, nullable=False)  # 0.0 to 1.0
    reasoning = Column(Text, nullable=True)
    recommendation_type = Column(String(50), nullable=False)  # "skill_based", "interest_based", "collaborative"
    
    # User feedback
    user_rating = Column(Integer, nullable=True)  # 1-5 stars
    user_feedback = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships will be defined after all models are imported
    # user = relationship("User", back_populates="recommendations")
    # activity = relationship("Activity", back_populates="recommendations")