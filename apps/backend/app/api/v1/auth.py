from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.api.deps import get_db, get_current_active_user
from app.core.config import settings
from app.core.security import create_access_token
from app.services.auth import AuthService
from app.models.user import User

router = APIRouter()


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserProfile(BaseModel):
    id: int
    email: str
    full_name: str = None
    is_active: bool
    skills: list = []
    availability: list = []
    location: str = None
    preferences: list = []
    is_mfr_student: bool = False
    mfr_institution: str = None

    class Config:
        from_attributes = True


@router.post("/register", response_model=UserProfile)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Créer un nouveau compte utilisateur
    """
    auth_service = AuthService(db)
    
    # Vérifier si l'utilisateur existe déjà
    user = auth_service.get_user_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Un utilisateur avec cet email existe déjà"
        )
    
    # Créer l'utilisateur
    user = auth_service.create_user(
        email=user_in.email,
        password=user_in.password,
        full_name=user_in.full_name
    )
    
    return user


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    Connexion utilisateur avec email et mot de passe
    """
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(
        email=form_data.username,  # OAuth2PasswordRequestForm uses 'username' field
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login/json", response_model=Token)
def login_json(
    user_in: UserLogin,
    db: Session = Depends(get_db)
) -> Any:
    """
    Connexion utilisateur avec JSON (alternative à OAuth2)
    """
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(
        email=user_in.email,
        password=user_in.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserProfile)
def read_users_me(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Récupérer le profil de l'utilisateur actuel
    """
    return current_user


@router.get("/test-token", response_model=UserProfile)
def test_token(current_user: User = Depends(get_current_active_user)) -> Any:
    """
    Tester le token d'accès
    """
    return current_user