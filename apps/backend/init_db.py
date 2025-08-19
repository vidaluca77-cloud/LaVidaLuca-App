#!/usr/bin/env python3

from app.db.database import Base, engine
from app.models.models import User, Activity
from app.core.auth import get_password_hash

def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def seed_data():
    """Seed the database with initial data."""
    from app.db.database import SessionLocal
    
    db = SessionLocal()
    
    # Create some test activities based on the frontend data
    activities_data = [
        {
            "slug": "nourrir-soigner-moutons",
            "title": "Nourrir et soigner les moutons",
            "category": "agri",
            "summary": "Gestes quotidiens : alimentation, eau, observation.",
            "duration_min": 60,
            "skill_tags": ["elevage", "responsabilite"],
            "seasonality": ["toutes"],
            "safety_level": 1,
            "materials": ["bottes", "gants"]
        },
        {
            "slug": "tonte-entretien-troupeau",
            "title": "Tonte & entretien du troupeau",
            "category": "agri",
            "summary": "Hygiène, tonte (démo), soins courants.",
            "duration_min": 90,
            "skill_tags": ["elevage", "hygiene"],
            "seasonality": ["printemps"],
            "safety_level": 2,
            "materials": ["bottes", "gants"]
        },
        {
            "slug": "pain-four-bois",
            "title": "Pain au four à bois",
            "category": "transfo",
            "summary": "Pétrissage, façonnage, cuisson : respect des temps.",
            "duration_min": 120,
            "skill_tags": ["precision", "rythme"],
            "seasonality": ["toutes"],
            "safety_level": 2,
            "materials": ["tablier"]
        },
        {
            "slug": "abris-bois",
            "title": "Construction d'abris",
            "category": "artisanat",
            "summary": "Petites structures bois : plan, coupe, assemblage.",
            "duration_min": 120,
            "skill_tags": ["bois", "precision", "securite"],
            "seasonality": ["toutes"],
            "safety_level": 2,
            "materials": ["gants"]
        },
        {
            "slug": "plantation-arbres",
            "title": "Plantation d'arbres",
            "category": "nature",
            "summary": "Techniques de plantation et soins des jeunes plants.",
            "duration_min": 90,
            "skill_tags": ["ecologie", "plantes"],
            "seasonality": ["automne", "hiver"],
            "safety_level": 1,
            "materials": ["gants", "bottes"]
        }
    ]
    
    # Add activities to database
    for activity_data in activities_data:
        # Check if activity already exists
        existing = db.query(Activity).filter(Activity.slug == activity_data["slug"]).first()
        if not existing:
            activity = Activity(**activity_data)
            db.add(activity)
    
    # Create a test user
    test_user_data = {
        "email": "demo@lavidaluca.fr",
        "hashed_password": get_password_hash("demo123"),
        "full_name": "Demo User",
        "skills": ["elevage", "sol", "plantes"],
        "availability": ["weekend", "matin"],
        "location": "Calvados",
        "preferences": ["agri", "nature"]
    }
    
    existing_user = db.query(User).filter(User.email == test_user_data["email"]).first()
    if not existing_user:
        user = User(**test_user_data)
        db.add(user)
    
    db.commit()
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    create_tables()
    seed_data()