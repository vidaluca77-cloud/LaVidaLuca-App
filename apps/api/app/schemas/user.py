from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[List[str]] = []
    preferences: Optional[List[str]] = []
    availability: Optional[List[str]] = []


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[List[str]] = None
    preferences: Optional[List[str]] = None
    availability: Optional[List[str]] = None


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserProfile(User):
    # Extended user info for profile pages
    participation_count: Optional[int] = 0
    completed_activities: Optional[int] = 0
    skill_level: Optional[str] = "beginner"


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str