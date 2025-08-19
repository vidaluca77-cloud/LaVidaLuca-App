from sqlalchemy import Column, Integer, String, Text, JSON, Float, Boolean
from app.models.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # 'agri', 'transfo', 'artisanat', 'nature', 'social'
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=True)  # Detailed description
    
    # Activity properties from frontend data
    duration_min = Column(Integer, nullable=False)  # Duration in minutes
    skill_tags = Column(JSON, default=list)  # List of required skills
    seasonality = Column(JSON, default=list)  # List of seasons ['printemps', 'ete', 'automne', 'hiver', 'toutes']
    safety_level = Column(Integer, default=1)  # 1=low risk, 2=medium, 3=high
    materials = Column(JSON, default=list)  # List of required materials
    
    # Location and availability
    location = Column(String, nullable=True)  # Where the activity takes place
    max_participants = Column(Integer, default=10)
    min_age = Column(Integer, default=14)
    
    # MFR specific
    is_mfr_only = Column(Boolean, default=False)  # Reserved for MFR students
    pedagogical_objectives = Column(JSON, default=list)  # Learning objectives
    
    # Metadata
    difficulty_level = Column(Integer, default=1)  # 1=beginner, 2=intermediate, 3=advanced
    is_active = Column(Boolean, default=True)