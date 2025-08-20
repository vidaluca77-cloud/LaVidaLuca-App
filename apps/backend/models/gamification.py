"""
Gamification models for La Vida Luca.
Handles achievements, badges, points, and user progress tracking.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from ..database import Base

class Achievement(Base):
    """Achievement model for gamification system."""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False)  # e.g., 'agriculture', 'engagement', 'learning'
    points = Column(Integer, default=0)
    icon = Column(String(100))  # Icon identifier or URL
    criteria = Column(JSON)  # Criteria for earning the achievement
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement")

class UserAchievement(Base):
    """User achievement progress and completion."""
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    progress = Column(Integer, default=0)  # Current progress towards achievement
    max_progress = Column(Integer, default=1)  # Target progress for completion
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")

class Badge(Base):
    """Badge model for special recognitions."""
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon = Column(String(100))  # Badge icon identifier or URL
    rarity = Column(String(20), default="common")  # common, rare, epic, legendary
    requirements = Column(JSON)  # Requirements for earning the badge
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge")

class UserBadge(Base):
    """User badge ownership."""
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="user_badges")

class UserPoints(Base):
    """User points transaction history."""
    __tablename__ = "user_points"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    points = Column(Integer, nullable=False)  # Can be positive (earned) or negative (spent)
    reason = Column(String(200), nullable=False)
    activity_type = Column(String(50))  # Type of activity that earned/spent points
    activity_id = Column(Integer)  # ID of related activity (e.g., activity completion)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="point_transactions")

class UserLevel(Base):
    """User level and experience tracking."""
    __tablename__ = "user_levels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    total_points = Column(Integer, default=0)  # Total points ever earned
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="level_info", uselist=False)

class ActivityCompletion(Base):
    """Track completion of activities for gamification."""
    __tablename__ = "activity_completions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    rating = Column(Integer)  # User rating of the activity (1-5)
    feedback = Column(Text)  # Optional user feedback

    # Relationships
    user = relationship("User", back_populates="completed_activities")
    activity = relationship("Activity", back_populates="completions")