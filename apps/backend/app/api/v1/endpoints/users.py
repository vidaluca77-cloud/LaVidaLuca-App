"""
User API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate, UserUpdate, UserAuth, Token

router = APIRouter()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Créer un nouveau utilisateur.
    """
    # Check if user already exists
    existing_user = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un utilisateur avec cet email existe déjà"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_in.password)
    db_user = UserModel(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_password,
        skills=user_in.skills,
        availability=user_in.availability,
        location=user_in.location,
        preferences=user_in.preferences,
        bio=user_in.bio,
        phone=user_in.phone
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.post("/auth/login", response_model=Token)
def login(user_auth: UserAuth, db: Session = Depends(get_db)):
    """
    Authentifier un utilisateur et retourner un token JWT.
    """
    user = db.query(UserModel).filter(UserModel.email == user_auth.email).first()
    
    if not user or not verify_password(user_auth.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Compte utilisateur inactif"
        )
    
    access_token = create_access_token(subject=user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/", response_model=List[User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupérer la liste des utilisateurs.
    """
    users = db.query(UserModel).filter(UserModel.is_active == 1).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Récupérer un utilisateur par son ID.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id, UserModel.is_active == 1).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    return user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Mettre à jour un utilisateur.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id, UserModel.is_active == 1).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    # Update user fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un utilisateur (soft delete).
    """
    user = db.query(UserModel).filter(UserModel.id == user_id, UserModel.is_active == 1).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    user.is_active = 0
    db.commit()
    
    return None