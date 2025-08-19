#!/usr/bin/env python3
"""
Database seeding script for La Vida Luca backend.
Creates sample activities and users for development and testing.
"""

import os
import sys
from sqlalchemy.orm import Session
from auth import get_password_hash
from database import SessionLocal, engine, Base
from models import User, Activity

def create_sample_users(db: Session):
    """Create sample users."""
    sample_users = [
        {
            "email": "marie@example.com",
            "password": "password123",
            "profile": {
                "skills": ["jardinage", "compostage", "maraîchage"],
                "interests": ["agri", "nature"],
                "location": "Lyon",
                "experience_level": "intermediate"
            }
        },
        {
            "email": "pierre@example.com", 
            "password": "password123",
            "profile": {
                "skills": ["menuiserie", "construction", "électricité"],
                "interests": ["artisanat", "transfo"],
                "location": "Grenoble",
                "experience_level": "advanced"
            }
        },
        {
            "email": "sophie@example.com",
            "password": "password123", 
            "profile": {
                "skills": ["cuisine", "conservation", "fermentation"],
                "interests": ["transfo", "social"],
                "location": "Annecy",
                "experience_level": "beginner"
            }
        }
    ]
    
    created_users = []
    for user_data in sample_users:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()
        if existing_user:
            print(f"User {user_data['email']} already exists, skipping...")
            created_users.append(existing_user)
            continue
            
        user = User(
            email=user_data["email"],
            hashed_password=get_password_hash(user_data["password"]),
            profile=user_data["profile"]
        )
        db.add(user)
        created_users.append(user)
        print(f"Created user: {user_data['email']}")
    
    db.commit()
    return created_users

def create_sample_activities(db: Session, users: list):
    """Create sample activities."""
    sample_activities = [
        {
            "title": "Culture de légumes biologiques",
            "category": "agri",
            "summary": "Apprenez les techniques de base pour cultiver vos légumes sans pesticides",
            "description": "Atelier pratique sur la culture biologique de légumes de saison. Nous aborderons la préparation du sol, le semis, l'entretien et la récolte.",
            "duration_min": 180,
            "skill_tags": ["jardinage", "biologie", "compostage"],
            "materials": ["graines bio", "outils de jardinage", "compost", "paillis"],
            "safety_level": 2,
            "difficulty_level": 2,
            "location": "Lyon",
            "engagement_score": 0.85,
            "success_rate": 0.78
        },
        {
            "title": "Fabrication de fromage artisanal",
            "category": "transfo",
            "summary": "Découvrez l'art de la fabrication de fromage maison avec du lait local",
            "description": "Formation complète sur la transformation du lait en fromage. Techniques traditionnelles et modernes, affinage et conservation.",
            "duration_min": 240,
            "skill_tags": ["transformation", "fermentation", "conservation"],
            "materials": ["lait cru", "présure", "ferments", "matériel de fromagerie"],
            "safety_level": 3,
            "difficulty_level": 3,
            "location": "Annecy", 
            "engagement_score": 0.92,
            "success_rate": 0.68
        },
        {
            "title": "Construction d'un poulailler écologique",
            "category": "artisanat",
            "summary": "Construisez un poulailler durable avec des matériaux recyclés",
            "description": "Atelier de construction d'un poulailler utilisant des techniques d'éco-construction et des matériaux de récupération.",
            "duration_min": 360,
            "skill_tags": ["menuiserie", "construction", "éco-construction"],
            "materials": ["bois de récupération", "grillage", "outils", "quincaillerie"],
            "safety_level": 4,
            "difficulty_level": 3,
            "location": "Grenoble",
            "engagement_score": 0.89,
            "success_rate": 0.72
        },
        {
            "title": "Découverte de la permaculture",
            "category": "nature", 
            "summary": "Introduction aux principes de la permaculture pour un jardin durable",
            "description": "Découvrez les principes fondamentaux de la permaculture et apprenez à concevoir un système agricole durable.",
            "duration_min": 120,
            "skill_tags": ["permaculture", "écosystème", "design"],
            "materials": ["carnet", "crayon", "mètre"],
            "safety_level": 1,
            "difficulty_level": 2,
            "location": "Lyon",
            "engagement_score": 0.91,
            "success_rate": 0.85
        },
        {
            "title": "Cuisine collective et zéro déchet",
            "category": "social",
            "summary": "Organisez un repas collectif en valorisant les restes alimentaires",
            "description": "Atelier de cuisine collaborative axé sur la réduction du gaspillage alimentaire et le lien social.",
            "duration_min": 150,
            "skill_tags": ["cuisine", "zéro déchet", "animation sociale"],
            "materials": ["ingrédients", "ustensiles", "contenants réutilisables"],
            "safety_level": 2,
            "difficulty_level": 1,
            "location": "Lyon",
            "engagement_score": 0.88,
            "success_rate": 0.91
        }
    ]
    
    for i, activity_data in enumerate(sample_activities):
        # Check if activity already exists
        existing_activity = db.query(Activity).filter(Activity.title == activity_data["title"]).first()
        if existing_activity:
            print(f"Activity '{activity_data['title']}' already exists, skipping...")
            continue
            
        # Assign creator (cycle through users)
        creator = users[i % len(users)] if users else None
        
        activity = Activity(
            **activity_data,
            creator_id=creator.id if creator else None
        )
        db.add(activity)
        print(f"Created activity: {activity_data['title']}")
    
    db.commit()

def main():
    """Main seeding function."""
    print("🌱 Seeding La Vida Luca database...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Create sample users
        print("\n👥 Creating sample users...")
        users = create_sample_users(db)
        
        # Create sample activities
        print("\n🎯 Creating sample activities...")
        create_sample_activities(db, users)
        
        print("\n✅ Database seeding completed successfully!")
        print("\nSample users created:")
        for user in users:
            print(f"  - {user.email} (password: password123)")
            
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()