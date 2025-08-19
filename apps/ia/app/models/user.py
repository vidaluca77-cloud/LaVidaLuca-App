from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    
    # Profile information
    skills = Column(JSON, default=list)  # List of skill tags
    availability = Column(JSON, default=list)  # Availability preferences
    location = Column(String, nullable=True)
    preferences = Column(JSON, default=list)  # Activity preferences
    
    # MFR specific
    is_mfr_student = Column(Boolean, default=False)
    mfr_institution = Column(String, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    bookings = relationship("Booking", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")