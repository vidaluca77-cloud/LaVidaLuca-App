from sqlalchemy import Column, String, Integer, DateTime, JSON, Text
from datetime import datetime
import uuid
from app.core.database import Base


class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)  # 'agri', 'transfo', 'artisanat', 'nature', 'social'
    summary = Column(Text, nullable=False)
    description = Column(Text, default="")
    duration_min = Column(Integer, nullable=False)
    skill_tags = Column(JSON, default=list)  # List of required/developed skills
    seasonality = Column(JSON, default=list)  # List of suitable seasons
    safety_level = Column(Integer, default=1)  # 1=low risk, 2=medium, 3=high
    materials = Column(JSON, default=list)  # List of required materials/equipment
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Activity(title='{self.title}', category='{self.category}')>"