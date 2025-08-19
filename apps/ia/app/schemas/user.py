from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    skills: List[str] = []
    availability: List[str] = []
    location: Optional[str] = None
    preferences: List[str] = []
    is_mfr_student: bool = False
    mfr_institution: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    skills: Optional[List[str]] = None
    availability: Optional[List[str]] = None
    location: Optional[str] = None
    preferences: Optional[List[str]] = None
    is_mfr_student: Optional[bool] = None
    mfr_institution: Optional[str] = None


class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """User profile for AI recommendations"""
    skills: List[str]
    availability: List[str]
    location: str
    preferences: List[str]


class UserInDB(User):
    hashed_password: str