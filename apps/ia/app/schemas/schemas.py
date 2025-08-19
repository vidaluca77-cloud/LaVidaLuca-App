from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Activity schemas
class ActivityBase(BaseModel):
    slug: str
    title: str
    category: str
    summary: str
    description: Optional[str] = None
    duration_min: int
    skill_tags: List[str] = []
    seasonality: List[str] = []
    safety_level: int = 1
    materials: List[str] = []
    is_active: bool = True

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    slug: Optional[str] = None
    title: Optional[str] = None
    category: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = None
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[List[str]] = None
    safety_level: Optional[int] = None
    materials: Optional[List[str]] = None
    is_active: Optional[bool] = None

class Activity(ActivityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Application schemas
class ApplicationBase(BaseModel):
    message: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    activity_id: int

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    message: Optional[str] = None

class Application(ApplicationBase):
    id: int
    user_id: int
    activity_id: int
    status: str
    applied_at: datetime
    updated_at: Optional[datetime] = None
    user: Optional[User] = None
    activity: Optional[Activity] = None

    class Config:
        from_attributes = True

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str