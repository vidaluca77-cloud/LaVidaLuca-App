from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # User profile data for recommendations (using JSON for SQLite compatibility)
    skills = Column(JSON, default=list)
    availability = Column(JSON, default=list)
    location = Column(String)
    preferences = Column(JSON, default=list)

    # Relationships
    user_activities = relationship("UserActivity", back_populates="user")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # 'agri', 'transfo', 'artisanat', 'nature', 'social'
    summary = Column(Text)
    description = Column(Text)
    duration_min = Column(Integer)
    skill_tags = Column(JSON, default=list)
    seasonality = Column(JSON, default=list)
    safety_level = Column(Integer, default=1)
    materials = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user_activities = relationship("UserActivity", back_populates="activity")


class UserActivity(Base):
    __tablename__ = "user_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    status = Column(String, default="interested")  # interested, in_progress, completed
    rating = Column(Integer)  # 1-5 stars
    feedback = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="user_activities")
    activity = relationship("Activity", back_populates="user_activities")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    score = Column(Float, nullable=False)
    reasons = Column(JSON, default=list)
    ai_generated = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
    activity = relationship("Activity")