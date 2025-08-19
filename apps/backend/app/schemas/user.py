from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    """Schema de base pour les utilisateurs"""
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    skills: List[str] = []
    availability: List[str] = []
    location: Optional[str] = None
    preferences: List[str] = []


class UserCreate(UserBase):
    """Schema pour la création d'utilisateur"""
    password: str


class UserUpdate(BaseModel):
    """Schema pour la mise à jour d'utilisateur"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    skills: Optional[List[str]] = None
    availability: Optional[List[str]] = None
    location: Optional[str] = None
    preferences: Optional[List[str]] = None


class UserInDBBase(UserBase):
    """Schema de base pour les utilisateurs en base de données"""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class User(UserInDBBase):
    """Schema pour les réponses API utilisateur"""
    pass


class UserInDB(UserInDBBase):
    """Schema pour les utilisateurs stockés en base"""
    hashed_password: str


class UserProfile(BaseModel):
    """Schema pour le profil utilisateur (compatible avec le frontend)"""
    skills: List[str]
    availability: List[str]
    location: str
    preferences: List[str]


class Token(BaseModel):
    """Schema pour les tokens d'authentification"""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Schema pour le payload des tokens"""
    sub: Optional[str] = None