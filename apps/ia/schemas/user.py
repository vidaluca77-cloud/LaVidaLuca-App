from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    skills: List[str] = []
    availability: List[str] = []
    location: Optional[str] = None
    preferences: List[str] = []


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    skills: Optional[List[str]] = None
    availability: Optional[List[str]] = None
    location: Optional[str] = None
    preferences: Optional[List[str]] = None


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    skills: List[str] = []
    availability: List[str] = []
    location: str = ""
    preferences: List[str] = []