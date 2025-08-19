#!/usr/bin/env python3
"""
Script to populate the database with sample activities from the LaVidaLuca project
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.models import Base, User, Activity
from app.schemas.schemas import UserCreate, ActivityCreate
from app.crud.crud import create_user, create_activity, get_user_by_username
from app.core.security import get_password_hash

# Create tables
Base.metadata.create_all(bind=engine)

def create_sample_data():
    db: Session = SessionLocal()
    
    try:
        # Create admin user
        admin_user = get_user_by_username(db, "admin")
        if not admin_user:
            admin_data = UserCreate(
                email="admin@lavidaluca.com",
                username="admin",
                full_name="Administrator",
                password="admin123",
                is_active=True
            )
            admin_user = create_user(db, admin_data)
            # Make them superuser
            admin_user.is_superuser = True
            db.commit()
            print("Created admin user")
        
        # Sample activities based on the frontend data
        activities = [
            {
                "slug": "soin-animaux",
                "title": "Soin aux animaux",
                "category": "agri",
                "summary": "Alimentation, observation, nettoyage des enclos.",
                "description": "Apprendre les gestes de base pour s'occuper des animaux de ferme en toute sécurité.",
                "duration_min": 90,
                "skill_tags": ["animaux", "observation", "responsabilite"],
                "seasonality": ["toutes"],
                "safety_level": 1,
                "materials": ["gants", "bottes"]
            },
            {
                "slug": "plantation-cultures",
                "title": "Plantation de cultures",
                "category": "agri",
                "summary": "Semis, arrosage, paillage, suivi de plants.",
                "description": "Initiation aux techniques de plantation et d'entretien des cultures maraîchères.",
                "duration_min": 90,
                "skill_tags": ["sol", "plantes"],
                "seasonality": ["printemps", "ete"],
                "safety_level": 1,
                "materials": ["gants"]
            },
            {
                "slug": "init-maraichage",
                "title": "Initiation maraîchage",
                "category": "agri",
                "summary": "Plan de culture, entretien, récolte respectueuse.",
                "description": "Découverte des principes du maraîchage biologique et des bonnes pratiques.",
                "duration_min": 120,
                "skill_tags": ["sol", "organisation"],
                "seasonality": ["printemps", "ete", "automne"],
                "safety_level": 1,
                "materials": ["gants", "bottes"]
            },
            {
                "slug": "fromage",
                "title": "Fabrication de fromage",
                "category": "transfo",
                "summary": "Du lait au caillé : hygiène, moulage, affinage (découverte).",
                "description": "Découverte des étapes de fabrication du fromage artisanal.",
                "duration_min": 90,
                "skill_tags": ["hygiene", "precision"],
                "seasonality": ["toutes"],
                "safety_level": 2,
                "materials": ["tablier"]
            },
            {
                "slug": "conserves",
                "title": "Confitures & conserves",
                "category": "transfo",
                "summary": "Préparation, stérilisation, mise en pot, étiquetage.",
                "description": "Apprendre les techniques de conservation traditionnelles.",
                "duration_min": 90,
                "skill_tags": ["organisation", "hygiene"],
                "seasonality": ["ete", "automne"],
                "safety_level": 1,
                "materials": ["tablier"]
            },
            {
                "slug": "menuiserie-simple",
                "title": "Menuiserie simple",
                "category": "artisanat",
                "summary": "Mesurer, scier, poncer, assembler (objets simples).",
                "description": "Initiation aux gestes de base de la menuiserie avec des projets simples.",
                "duration_min": 120,
                "skill_tags": ["precision", "outils"],
                "seasonality": ["toutes"],
                "safety_level": 2,
                "materials": ["gants", "lunettes"]
            },
            {
                "slug": "potager-bio",
                "title": "Création d'un potager bio",
                "category": "nature",
                "summary": "Préparation du sol, choix des plants, companion planting.",
                "description": "Apprendre à créer et gérer un potager en respectant les principes de l'agriculture biologique.",
                "duration_min": 180,
                "skill_tags": ["sol", "plantes", "organisation"],
                "seasonality": ["printemps", "ete"],
                "safety_level": 1,
                "materials": ["gants", "bottes", "outils"]
            },
            {
                "slug": "animation-groupe",
                "title": "Animation d'un groupe de jeunes",
                "category": "social",
                "summary": "Activités ludiques, pédagogiques, gestion de groupe.",
                "description": "Développer ses compétences d'animation et de gestion de groupe dans un contexte éducatif.",
                "duration_min": 120,
                "skill_tags": ["contact", "pedagogie", "equipe"],
                "seasonality": ["toutes"],
                "safety_level": 1,
                "materials": []
            }
        ]
        
        # Create activities
        for activity_data in activities:
            existing = db.query(Activity).filter(Activity.slug == activity_data["slug"]).first()
            if not existing:
                activity = ActivityCreate(**activity_data)
                create_activity(db, activity)
                print(f"Created activity: {activity_data['title']}")
        
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()