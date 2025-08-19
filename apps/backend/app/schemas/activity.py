from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ActivityBase(BaseModel):
    title: str
    slug: str
    category: str = Field(..., regex="^(agri|transfo|artisanat|nature|social)$")
    summary: Optional[str] = None
    duration_min: int = Field(..., gt=0)
    skill_tags: List[str] = []
    seasonality: List[str] = []
    safety_level: int = Field(default=1, ge=1, le=5)
    materials: List[str] = []


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = Field(None, regex="^(agri|transfo|artisanat|nature|social)$")
    summary: Optional[str] = None
    duration_min: Optional[int] = Field(None, gt=0)
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[List[str]] = None
    safety_level: Optional[int] = Field(None, ge=1, le=5)
    materials: Optional[List[str]] = None


class Activity(ActivityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ActivityListResponse(BaseModel):
    activities: List[Activity]
    total: int


class ActivityRegistrationResponse(BaseModel):
    message: str
    activity_id: int
    user_id: int
    registered_at: datetime