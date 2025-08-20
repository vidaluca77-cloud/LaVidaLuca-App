from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Gamification fields
    total_points = Column(Integer, default=0)
    current_level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    activities = relationship("Activity", back_populates="creator")
    user_skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    activity_completions = relationship("ActivityCompletion", back_populates="user", cascade="all, delete-orphan")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String, nullable=False)
    difficulty_level = Column(String, default="beginner")  # beginner, intermediate, advanced
    duration_minutes = Column(Integer)
    location = Column(String)
    equipment_needed = Column(Text)
    learning_objectives = Column(Text)
    is_published = Column(Boolean, default=False)
    
    # Gamification fields
    points_reward = Column(Integer, default=10)  # Points awarded for completion
    required_skills = Column(JSON)  # List of skill IDs required
    skills_taught = Column(JSON)  # List of skill IDs this activity teaches
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Keys
    creator_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    creator = relationship("User", back_populates="activities")
    completions = relationship("ActivityCompletion", back_populates="activity", cascade="all, delete-orphan")


class ActivitySuggestion(Base):
    __tablename__ = "activity_suggestions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_id = Column(Integer, ForeignKey("activities.id"))
    suggestion_reason = Column(Text)
    ai_generated = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    activity = relationship("Activity")


# Gamification Models

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    category = Column(String, nullable=False)  # e.g., 'agriculture', 'artisanat', 'social'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user_skills = relationship("UserSkill", back_populates="skill", cascade="all, delete-orphan")


class UserSkill(Base):
    __tablename__ = "user_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    level = Column(Integer, default=1)  # 1-5 proficiency level
    experience = Column(Integer, default=0)  # Experience points in this skill
    obtained_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="user_skills")
    skill = relationship("Skill", back_populates="user_skills")


class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    icon = Column(String)  # URL or path to achievement icon
    points_reward = Column(Integer, default=50)
    category = Column(String)  # e.g., 'completion', 'streak', 'social', 'skill'
    criteria = Column(JSON)  # JSON object describing achievement criteria
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement", cascade="all, delete-orphan")


class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")


class ActivityCompletion(Base):
    __tablename__ = "activity_completions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_id = Column(Integer, ForeignKey("activities.id"))
    completion_date = Column(DateTime(timezone=True), server_default=func.now())
    rating = Column(Integer)  # 1-5 rating of the activity
    feedback = Column(Text)  # User feedback
    points_earned = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="activity_completions")
    activity = relationship("Activity", back_populates="completions")


class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime(timezone=True), server_default=func.now())
    activities_completed = Column(Integer, default=0)
    points_earned = Column(Integer, default=0)
    skills_learned = Column(Integer, default=0)
    achievements_unlocked = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User")