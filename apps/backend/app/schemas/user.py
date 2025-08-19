from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    skills: Optional[List[str]] = []
    availability: Optional[List[str]] = []
    location: Optional[str] = ""
    preferences: Optional[List[str]] = []


class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v
    
    @validator('skills', 'availability', 'preferences', pre=True)
    def validate_lists(cls, v):
        if v is None:
            return []
        return v


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    skills: Optional[List[str]] = None
    availability: Optional[List[str]] = None
    location: Optional[str] = None
    preferences: Optional[List[str]] = None


class UserResponse(UserBase):
    id: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str