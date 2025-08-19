from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from datetime import datetime
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Profile fields from frontend
    skills = Column(JSON, default=list)  # List of skill strings
    availability = Column(JSON, default=list)  # List of availability strings
    location = Column(String, nullable=True)
    preferences = Column(JSON, default=list)  # List of category preferences
    
    # MFR specific fields
    is_mfr_student = Column(Boolean, default=False)
    mfr_institution = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())