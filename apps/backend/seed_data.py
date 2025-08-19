"""Seed script to populate the database with initial data."""

import asyncio
import json
from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from src.core.security import get_password_hash
from src.db.session import SessionLocal
from src.models.user import User, UserRole
from src.models.location import Location
from src.models.activity import Activity


# Sample activities from the frontend
ACTIVITIES_DATA = [
    # Agriculture
    {"id": "1", "slug": "nourrir-soigner-moutons", "title": "Nourrir et soigner les moutons", "category": "agri", "summary": "Gestes quotidiens : alimentation, eau, observation.", "duration_min": 60, "skill_tags": ["elevage", "responsabilite"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["bottes", "gants"]},
    {"id": "2", "slug": "tonte-entretien-troupeau", "title": "Tonte & entretien du troupeau", "category": "agri", "summary": "Hygiène, tonte (démo), soins courants.", "duration_min": 90, "skill_tags": ["elevage", "hygiene"], "seasonality": ["printemps"], "safety_level": 2, "materials": ["bottes", "gants"]},
    {"id": "3", "slug": "basse-cour-soins", "title": "Soins basse-cour", "category": "agri", "summary": "Poules/canards/lapins : alimentation, abris, propreté.", "duration_min": 60, "skill_tags": ["soins_animaux"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["bottes", "gants"]},
    {"id": "4", "slug": "potager-saison", "title": "Potager de saison", "category": "agri", "summary": "Plantation, arrosage, récolte selon calendrier.", "duration_min": 90, "skill_tags": ["jardinage", "patience"], "seasonality": ["printemps", "ete"], "safety_level": 1, "materials": ["gants", "bottes"]},
    {"id": "5", "slug": "verger-entretien", "title": "Entretien du verger", "category": "agri", "summary": "Taille, traitement bio, ramassage des fruits.", "duration_min": 120, "skill_tags": ["arboriculture", "precision"], "seasonality": ["automne", "hiver"], "safety_level": 2, "materials": ["secateur", "gants"]},
    {"id": "6", "slug": "cereales-recolte", "title": "Céréales & récolte", "category": "agri", "summary": "Moisson, battage, stockage selon méthode locale.", "duration_min": 180, "skill_tags": ["endurance", "coordination"], "seasonality": ["ete"], "safety_level": 2, "materials": ["chapeau", "gants"]},
    
    # Transformation
    {"id": "7", "slug": "produits-laitiers", "title": "Produits laitiers fermiers", "category": "transfo", "summary": "Fromages frais, yaourts : bases de la transformation.", "duration_min": 120, "skill_tags": ["hygiene", "precision", "patience"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["tablier", "gants"]},
    {"id": "8", "slug": "conserves", "title": "Confitures & conserves", "category": "transfo", "summary": "Préparation, stérilisation, mise en pot, étiquetage.", "duration_min": 90, "skill_tags": ["organisation", "hygiene"], "seasonality": ["ete", "automne"], "safety_level": 1, "materials": ["tablier"]},
    {"id": "9", "slug": "laine", "title": "Transformation de la laine", "category": "transfo", "summary": "Lavage, cardage, petite création textile.", "duration_min": 90, "skill_tags": ["patience", "creativite"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier", "gants"]},
    {"id": "10", "slug": "miel-cire", "title": "Miel & produits de la ruche", "category": "transfo", "summary": "Extraction, filtrage, conditionnement, cire.", "duration_min": 90, "skill_tags": ["delicatesse", "hygiene"], "seasonality": ["ete"], "safety_level": 3, "materials": ["combinaison", "gants"]},
    {"id": "11", "slug": "huiles-essentielles", "title": "Huiles essentielles & tisanes", "category": "transfo", "summary": "Cueillette, séchage, distillation simple.", "duration_min": 120, "skill_tags": ["connaissance_plantes", "precision"], "seasonality": ["ete"], "safety_level": 2, "materials": ["gants"]},
    {"id": "12", "slug": "pain-four-bois", "title": "Pain au four à bois", "category": "transfo", "summary": "Pétrissage, façonnage, cuisson : respect des temps.", "duration_min": 120, "skill_tags": ["precision", "rythme"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["tablier"]},
    
    # Artisanat
    {"id": "13", "slug": "abris-bois", "title": "Construction d'abris", "category": "artisanat", "summary": "Petites structures bois : plan, coupe, assemblage.", "duration_min": 120, "skill_tags": ["bois", "precision", "securite"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    {"id": "14", "slug": "clotures-portails", "title": "Clôtures & portails", "category": "artisanat", "summary": "Pose, réparation, entretien des séparations.", "duration_min": 90, "skill_tags": ["bricolage", "endurance"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants", "bottes"]},
    {"id": "15", "slug": "outils-maintenance", "title": "Maintenance des outils", "category": "artisanat", "summary": "Affûtage, graissage, réparations simples.", "duration_min": 60, "skill_tags": ["mecanique", "soin"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    {"id": "16", "slug": "peinture-deco", "title": "Peinture & décoration d'espaces", "category": "artisanat", "summary": "Préparer, protéger, peindre proprement.", "duration_min": 90, "skill_tags": ["proprete", "finitions"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier", "gants"]},
    {"id": "17", "slug": "amenagement-verts", "title": "Aménagement d'espaces verts", "category": "artisanat", "summary": "Désherbage doux, paillage, plantations.", "duration_min": 90, "skill_tags": ["endurance", "esthetique"], "seasonality": ["printemps", "ete"], "safety_level": 1, "materials": ["gants", "bottes"]},
    {"id": "18", "slug": "vannerie-simple", "title": "Vannerie simple", "category": "artisanat", "summary": "Paniers, corbeilles avec matériaux locaux.", "duration_min": 120, "skill_tags": ["patience", "creativite"], "seasonality": ["automne", "hiver"], "safety_level": 1, "materials": []},
    
    # Nature
    {"id": "19", "slug": "mare-ecosystem", "title": "Entretien de la mare", "category": "nature", "summary": "Nettoyage, plantations aquatiques, observation.", "duration_min": 90, "skill_tags": ["patience", "respect"], "seasonality": ["printemps", "ete"], "safety_level": 2, "materials": ["bottes"]},
    {"id": "20", "slug": "haies-bocage", "title": "Entretien des haies bocagères", "category": "nature", "summary": "Taille, plantation, protection de la biodiversité.", "duration_min": 120, "skill_tags": ["endurance", "ecologie"], "seasonality": ["automne", "hiver"], "safety_level": 2, "materials": ["gants", "secateur"]},
    {"id": "21", "slug": "sentiers-nature", "title": "Création de sentiers nature", "category": "nature", "summary": "Débroussaillage, balisage, panneaux pédagogiques.", "duration_min": 120, "skill_tags": ["orientation", "creativite"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants", "bottes"]},
    {"id": "22", "slug": "compostage", "title": "Compostage", "category": "nature", "summary": "Tri, compost, valorisation des déchets verts.", "duration_min": 60, "skill_tags": ["geste_utile", "hygiene"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["gants"]},
    {"id": "23", "slug": "faune-locale", "title": "Observation de la faune locale", "category": "nature", "summary": "Discrétion, repérage, traces/indices.", "duration_min": 60, "skill_tags": ["patience", "respect"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"id": "24", "slug": "graines-plants", "title": "Préparation de graines & plants", "category": "nature", "summary": "Semis, repiquage, bouturage, élevage de plants.", "duration_min": 90, "skill_tags": ["delicatesse", "patience"], "seasonality": ["printemps"], "safety_level": 1, "materials": ["gants"]},
    
    # Social
    {"id": "25", "slug": "accueil-visiteurs", "title": "Accueil des visiteurs", "category": "social", "summary": "Présentation, tour guidé, sensibilisation.", "duration_min": 90, "skill_tags": ["communication", "pedagogie"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"id": "26", "slug": "marche-local", "title": "Marché local & vente", "category": "social", "summary": "Préparation des produits, étal, contact client.", "duration_min": 180, "skill_tags": ["organisation", "relationnel"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"id": "27", "slug": "animation-enfants", "title": "Animation pour enfants", "category": "social", "summary": "Ateliers ludiques, découverte, sécurité.", "duration_min": 120, "skill_tags": ["pedagogie", "patience", "securite"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"id": "28", "slug": "cuisine-collective", "title": "Cuisine collective (équipe)", "category": "social", "summary": "Préparer un repas simple et bon.", "duration_min": 90, "skill_tags": ["hygiene", "equipe", "temps"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier"]},
    {"id": "29", "slug": "gouter-fermier", "title": "Goûter fermier", "category": "social", "summary": "Organisation, service, convivialité, propreté.", "duration_min": 60, "skill_tags": ["rigueur", "relationnel"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier"]},
    {"id": "30", "slug": "fetes-traditions", "title": "Fêtes & traditions locales", "category": "social", "summary": "Participation, organisation, transmission.", "duration_min": 240, "skill_tags": ["culture", "organisation"], "seasonality": ["toutes"], "safety_level": 1, "materials": []}
]


def create_default_location(db: Session) -> Location:
    """Create a default location."""
    location = Location(
        name="Ferme Pédagogique de la Vallée",
        address="123 Chemin de la Vallée",
        city="Caen",
        postal_code="14000",
        country="France",
        latitude=49.1829,
        longitude=-0.3707,
        description="Ferme pédagogique dédiée à l'agriculture durable et à l'insertion sociale des jeunes.",
        contact_email="contact@fermedelavallee.fr",
        contact_phone="02 31 00 00 00"
    )
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def create_default_admin(db: Session) -> User:
    """Create default admin user."""
    hashed_password = get_password_hash("admin123")
    admin = User(
        email="admin@lavidaluca.com",
        hashed_password=hashed_password,
        full_name="Administrateur LaVidaLuca",
        role=UserRole.ADMIN,
        is_active=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def create_default_instructor(db: Session) -> User:
    """Create default instructor user."""
    hashed_password = get_password_hash("instructor123")
    instructor = User(
        email="instructor@lavidaluca.com",
        hashed_password=hashed_password,
        full_name="Marie Durand",
        role=UserRole.INSTRUCTOR,
        is_active=True,
        bio="Encadrante agricole avec 10 ans d'expérience en pédagogie.",
        phone="06 12 34 56 78"
    )
    db.add(instructor)
    db.commit()
    db.refresh(instructor)
    return instructor


def create_activities(db: Session, location: Location):
    """Create activities from the frontend data."""
    for activity_data in ACTIVITIES_DATA:
        activity = Activity(
            title=activity_data["title"],
            slug=activity_data["slug"],
            description=activity_data.get("summary", activity_data["title"]),
            summary=activity_data.get("summary"),
            category=activity_data["category"],
            duration_min=activity_data["duration_min"],
            max_participants=10,  # Default value
            difficulty_level=min(3, activity_data["safety_level"] + 1),  # Convert safety to difficulty
            materials=activity_data["materials"],
            skill_tags=activity_data["skill_tags"],
            seasonality=activity_data["seasonality"],
            safety_level=activity_data["safety_level"],
            location_id=location.id,
            is_active=True
        )
        db.add(activity)
    
    db.commit()


def seed_database():
    """Seed the database with initial data."""
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_admin = db.query(User).filter(User.email == "admin@lavidaluca.com").first()
        if existing_admin:
            print("Database already seeded!")
            return

        print("Seeding database...")
        
        # Create default users
        admin = create_default_admin(db)
        instructor = create_default_instructor(db)
        print(f"Created admin user: {admin.email}")
        print(f"Created instructor user: {instructor.email}")
        
        # Create default location
        location = create_default_location(db)
        print(f"Created location: {location.name}")
        
        # Create activities
        create_activities(db, location)
        print(f"Created {len(ACTIVITIES_DATA)} activities")
        
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()