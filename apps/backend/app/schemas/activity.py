from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.activity import ActivityCategory


class ActivityBase(BaseModel):
    """Schema de base pour les activités"""
    slug: str
    title: str
    category: ActivityCategory
    summary: str
    description: Optional[str] = None
    duration_min: int
    skill_tags: List[str] = []
    seasonality: List[str] = []
    safety_level: int = 1
    materials: List[str] = []
    location: Optional[str] = None
    max_participants: Optional[int] = None
    min_age: Optional[int] = None


class ActivityCreate(ActivityBase):
    """Schema pour la création d'activité"""
    pass


class ActivityUpdate(BaseModel):
    """Schema pour la mise à jour d'activité"""
    slug: Optional[str] = None
    title: Optional[str] = None
    category: Optional[ActivityCategory] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = None
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[List[str]] = None
    safety_level: Optional[int] = None
    materials: Optional[List[str]] = None
    location: Optional[str] = None
    max_participants: Optional[int] = None
    min_age: Optional[int] = None
    is_active: Optional[bool] = None


class ActivityInDBBase(ActivityBase):
    """Schema de base pour les activités en base de données"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Activity(ActivityInDBBase):
    """Schema pour les réponses API activité"""
    pass


class ActivitySummary(BaseModel):
    """Schema résumé pour les listes d'activités"""
    id: int
    slug: str
    title: str
    category: ActivityCategory
    summary: str
    duration_min: int
    safety_level: int

    class Config:
        from_attributes = True


class ActivityMatch(BaseModel):
    """Schema pour le matching d'activités (compatible avec le frontend)"""
    activity: Activity
    score: int
    reasons: List[str]