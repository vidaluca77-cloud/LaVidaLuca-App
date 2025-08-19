from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    
    # Booking details
    scheduled_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default=BookingStatus.PENDING)
    participants_count = Column(Integer, default=1)
    
    # Notes and feedback
    user_notes = Column(Text, nullable=True)
    admin_notes = Column(Text, nullable=True)
    completion_feedback = Column(Text, nullable=True)
    rating = Column(Float, nullable=True)  # 1-5 rating after completion
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="bookings")
    activity = relationship("Activity", back_populates="bookings")


class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    
    # Recommendation details
    score = Column(Float, nullable=False)  # Matching score 0-1
    reasons = Column(Text, nullable=True)  # JSON string of reasons
    
    # AI metadata
    model_version = Column(String, nullable=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # User interaction
    clicked = Column(Boolean, default=False)
    clicked_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
    activity = relationship("Activity", back_populates="recommendations")