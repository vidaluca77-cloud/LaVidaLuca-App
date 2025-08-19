from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, UserProfile, user_skills, user_preferences
from schemas import UserCreate, UserUpdate, User as UserSchema, UserWithProfile
from auth import get_password_hash, get_current_active_user

router = APIRouter()

@router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Créer un nouvel utilisateur"""
    # Vérifier si l'utilisateur existe déjà
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Créer l'utilisateur
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        is_mfr_student=user.is_mfr_student
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/me", response_model=UserWithProfile)
def read_users_me(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Obtenir les informations de l'utilisateur actuel"""
    # Charger le profil
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    # Charger les compétences et préférences si le profil existe
    if profile:
        skills_result = db.execute(
            user_skills.select().where(user_skills.c.user_id == current_user.id)
        ).fetchall()
        profile.skills = [row.skill_name for row in skills_result]
        
        prefs_result = db.execute(
            user_preferences.select().where(user_preferences.c.user_id == current_user.id)
        ).fetchall()
        profile.preferences = [row.category for row in prefs_result]
    
    current_user.profile = profile
    return current_user

@router.put("/me", response_model=UserSchema)
def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour les informations de l'utilisateur actuel"""
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.is_mfr_student is not None:
        current_user.is_mfr_student = user_update.is_mfr_student
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/me")
def delete_user_me(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Supprimer le compte de l'utilisateur actuel"""
    db.delete(current_user)
    db.commit()
    return {"message": "User deleted successfully"}