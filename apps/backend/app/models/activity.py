from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class ActivityCategory(str, enum.Enum):
    """Catégories d'activités basées sur le frontend"""
    AGRI = "agri"
    TRANSFO = "transfo"
    ARTISANAT = "artisanat"
    NATURE = "nature"
    SOCIAL = "social"


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(SQLEnum(ActivityCategory), nullable=False)
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    
    # Détails de l'activité basés sur l'interface Activity du frontend
    duration_min = Column(Integer, nullable=False)
    skill_tags = Column(ARRAY(String), default=[])
    seasonality = Column(ARRAY(String), default=[])
    safety_level = Column(Integer, default=1)  # 1=Facile, 2=Attention, 3=Expert
    materials = Column(ARRAY(String), default=[])
    
    # Informations supplémentaires
    location = Column(String, nullable=True)
    max_participants = Column(Integer, nullable=True)
    min_age = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Métadonnées
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())