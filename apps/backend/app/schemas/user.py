from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from app.schemas.activity import Activity


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    skills: List[str] = []
    availability: List[str] = []
    location: Optional[str] = None
    preferences: List[str] = []


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    skills: Optional[List[str]] = None
    availability: Optional[List[str]] = None
    location: Optional[str] = None
    preferences: Optional[List[str]] = None


class UserProfile(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserActivitiesResponse(BaseModel):
    activities: List[Activity]
    total: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None