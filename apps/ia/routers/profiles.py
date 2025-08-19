from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, UserProfile, user_skills, user_preferences
from schemas import UserProfileCreate, UserProfileUpdate, UserProfile as UserProfileSchema
from auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=UserProfileSchema)
def create_profile(
    profile: UserProfileCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Créer ou mettre à jour le profil utilisateur"""
    # Vérifier si un profil existe déjà
    db_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if db_profile:
        # Mettre à jour le profil existant
        db_profile.location = profile.location
        db_profile.availability = profile.availability
        db_profile.experience_level = profile.experience_level
    else:
        # Créer un nouveau profil
        db_profile = UserProfile(
            user_id=current_user.id,
            location=profile.location,
            availability=profile.availability,
            experience_level=profile.experience_level
        )
        db.add(db_profile)
    
    db.commit()
    db.refresh(db_profile)
    
    # Gérer les compétences
    if profile.skills:
        # Supprimer les anciennes compétences
        db.execute(user_skills.delete().where(user_skills.c.user_id == current_user.id))
        
        # Ajouter les nouvelles compétences
        for skill in profile.skills:
            db.execute(user_skills.insert().values(user_id=current_user.id, skill_name=skill))
    
    # Gérer les préférences
    if profile.preferences:
        # Supprimer les anciennes préférences
        db.execute(user_preferences.delete().where(user_preferences.c.user_id == current_user.id))
        
        # Ajouter les nouvelles préférences
        for pref in profile.preferences:
            db.execute(user_preferences.insert().values(user_id=current_user.id, category=pref))
    
    db.commit()
    
    # Charger les compétences et préférences pour la réponse
    skills_result = db.execute(
        user_skills.select().where(user_skills.c.user_id == current_user.id)
    ).fetchall()
    db_profile.skills = [row.skill_name for row in skills_result]
    
    prefs_result = db.execute(
        user_preferences.select().where(user_preferences.c.user_id == current_user.id)
    ).fetchall()
    db_profile.preferences = [row.category for row in prefs_result]
    
    return db_profile

@router.get("/", response_model=UserProfileSchema)
def get_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtenir le profil de l'utilisateur actuel"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Charger les compétences et préférences
    skills_result = db.execute(
        user_skills.select().where(user_skills.c.user_id == current_user.id)
    ).fetchall()
    profile.skills = [row.skill_name for row in skills_result]
    
    prefs_result = db.execute(
        user_preferences.select().where(user_preferences.c.user_id == current_user.id)
    ).fetchall()
    profile.preferences = [row.category for row in prefs_result]
    
    return profile

@router.put("/", response_model=UserProfileSchema)
def update_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour le profil utilisateur"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Mettre à jour les champs
    if profile_update.location is not None:
        profile.location = profile_update.location
    if profile_update.availability is not None:
        profile.availability = profile_update.availability
    if profile_update.experience_level is not None:
        profile.experience_level = profile_update.experience_level
    
    # Gérer les compétences si fournies
    if profile_update.skills is not None:
        db.execute(user_skills.delete().where(user_skills.c.user_id == current_user.id))
        for skill in profile_update.skills:
            db.execute(user_skills.insert().values(user_id=current_user.id, skill_name=skill))
    
    # Gérer les préférences si fournies
    if profile_update.preferences is not None:
        db.execute(user_preferences.delete().where(user_preferences.c.user_id == current_user.id))
        for pref in profile_update.preferences:
            db.execute(user_preferences.insert().values(user_id=current_user.id, category=pref))
    
    db.commit()
    db.refresh(profile)
    
    # Charger les compétences et préférences pour la réponse
    skills_result = db.execute(
        user_skills.select().where(user_skills.c.user_id == current_user.id)
    ).fetchall()
    profile.skills = [row.skill_name for row in skills_result]
    
    prefs_result = db.execute(
        user_preferences.select().where(user_preferences.c.user_id == current_user.id)
    ).fetchall()
    profile.preferences = [row.category for row in prefs_result]
    
    return profile