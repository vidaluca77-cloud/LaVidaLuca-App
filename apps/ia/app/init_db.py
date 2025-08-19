"""
Database initialization and seed data
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .core.config import settings
from .core.database import Base
from .models.models import User, Activity, UserProfile
from .core.security import get_password_hash

# Create engine and session
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def seed_activities():
    """Seed the database with the 30 La Vida Luca activities."""
    db = SessionLocal()
    
    try:
        # Check if activities already exist
        if db.query(Activity).first():
            print("Activities already exist in database")
            return
        
        activities_data = [
            # Agriculture
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
                "slug": "nourrir-soigner-chevres",
                "title": "Nourrir et soigner les chèvres",
                "category": "agri", 
                "summary": "Alimentation, traite (découverte), soins de base.",
                "duration_min": 75,
                "skill_tags": ["elevage", "hygiene", "soins_animaux"],
                "seasonality": ["toutes"],
                "safety_level": 1,
                "materials": ["bottes", "gants"]
            },
            {
                "slug": "entretien-potager",
                "title": "Entretien du potager",
                "category": "agri",
                "summary": "Plantation, arrosage, désherbage, récolte selon saison.",
                "duration_min": 90,
                "skill_tags": ["sol", "plantes", "organisation"],
                "seasonality": ["printemps", "ete", "automne"],
                "safety_level": 1,
                "materials": ["gants", "bottes"]
            },
            {
                "slug": "preparation-patures",
                "title": "Préparation des pâtures",
                "category": "agri",
                "summary": "Clôture temporaire, débroussaillage léger, rotation.",
                "duration_min": 120,
                "skill_tags": ["organisation", "securite"],
                "seasonality": ["printemps", "ete"],
                "safety_level": 2,
                "materials": ["gants", "bottes"]
            },
            {
                "slug": "soin-terre-compost",
                "title": "Soin de la terre & compost",
                "category": "agri",
                "summary": "Retournement, enrichissement, fabrication compost.",
                "duration_min": 90,
                "skill_tags": ["sol", "organisation"],
                "seasonality": ["toutes"],
                "safety_level": 1,
                "materials": ["gants", "bottes"]
            },
            {
                "slug": "clotures-abris",
                "title": "Gestion des clôtures & abris",
                "category": "agri",
                "summary": "Identifier, réparer, sécuriser parcs et abris.",
                "duration_min": 120,
                "skill_tags": ["securite", "bois"],
                "seasonality": ["toutes"],
                "safety_level": 2,
                "materials": ["gants"]
            },
            
            # Transformation
            {
                "slug": "fromage",
                "title": "Fabrication de fromage",
                "category": "transfo",
                "summary": "Du lait au caillé : hygiène, moulage, affinage (découverte).",
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
                "duration_min": 90,
                "skill_tags": ["organisation", "hygiene"],
                "seasonality": ["ete", "automne"],
                "safety_level": 1,
                "materials": ["tablier"]
            },
            {
                "slug": "laine",
                "title": "Transformation de la laine",
                "category": "transfo",
                "summary": "Lavage, cardage, petite création textile.",
                "duration_min": 90,
                "skill_tags": ["patience", "creativite"],
                "seasonality": ["toutes"],
                "safety_level": 1,
                "materials": ["tablier", "gants"]
            },
            {
                "slug": "pain",
                "title": "Fabrication du pain",
                "category": "transfo",
                "summary": "Pétrissage, façonnage, cuisson au four.",
                "duration_min": 180,
                "skill_tags": ["precision", "patience"],
                "seasonality": ["toutes"],
                "safety_level": 2,
                "materials": ["tablier"]
            },
            
            # Artisanat
            {
                "slug": "menuiserie-simple",
                "title": "Menuiserie simple",
                "category": "artisanat",
                "summary": "Nichoirs, jardinières, petits objets utiles.",
                "duration_min": 120,
                "skill_tags": ["bois", "creativite", "precision"],
                "seasonality": ["toutes"],
                "safety_level": 3,
                "materials": ["gants"]
            },
            {
                "slug": "reparation-outils",
                "title": "Réparation d'outils",
                "category": "artisanat",
                "summary": "Entretien, affûtage, petites réparations.",
                "duration_min": 60,
                "skill_tags": ["organisation", "securite"],
                "seasonality": ["toutes"],
                "safety_level": 2,
                "materials": ["gants"]
            },
            {
                "slug": "construction-abris",
                "title": "Construction d'abris",
                "category": "artisanat",
                "summary": "Abris temporaires, réparations bâtiments.",
                "duration_min": 180,
                "skill_tags": ["bois", "organisation", "securite"],
                "seasonality": ["printemps", "ete", "automne"],
                "safety_level": 3,
                "materials": ["gants", "casque"]
            },
            
            # Environnement
            {
                "slug": "plantation-arbres",
                "title": "Plantation d'arbres",
                "category": "nature",
                "summary": "Choix emplacement, techniques, entretien jeune plant.",
                "duration_min": 90,
                "skill_tags": ["ecologie", "organisation"],
                "seasonality": ["automne", "hiver"],
                "safety_level": 1,
                "materials": ["gants", "bottes"]
            },
            {
                "slug": "creation-haies",
                "title": "Création de haies",
                "category": "nature",
                "summary": "Haies bocagères, brise-vent, biodiversité.",
                "duration_min": 120,
                "skill_tags": ["ecologie", "organisation"],
                "seasonality": ["automne", "hiver"],
                "safety_level": 2,
                "materials": ["gants", "bottes"]
            },
            {
                "slug": "gestion-dechets",
                "title": "Gestion des déchets",
                "category": "nature",
                "summary": "Tri, compostage, réduction, recyclage.",
                "duration_min": 60,
                "skill_tags": ["organisation", "ecologie"],
                "seasonality": ["toutes"],
                "safety_level": 1,
                "materials": ["gants"]
            },
            {
                "slug": "mare-biodiversite",
                "title": "Mare & biodiversité",
                "category": "nature",
                "summary": "Création/entretien mare, observation faune.",
                "duration_min": 120,
                "skill_tags": ["ecologie", "patience"],
                "seasonality": ["printemps", "ete"],
                "safety_level": 2,
                "materials": ["bottes"]
            },
            
            # Animation/Social
            {
                "slug": "accueil-visiteurs",
                "title": "Accueil de visiteurs",
                "category": "social",
                "summary": "Présentation ferme, visite guidée, pédagogie.",
                "duration_min": 90,
                "skill_tags": ["accueil", "pedagogie", "expression"],
                "seasonality": ["toutes"],
                "safety_level": 1,
                "materials": []
            },
            {
                "slug": "atelier-enfants",
                "title": "Animation atelier enfants",
                "category": "social",
                "summary": "Activités adaptées : nourrissage, jardinage, bricolage.",
                "duration_min": 120,
                "skill_tags": ["pedagogie", "patience", "creativite"],
                "seasonality": ["toutes"],
                "safety_level": 1,
                "materials": []
            },
            {
                "slug": "marche-local",
                "title": "Participation à un marché local",
                "category": "social",
                "summary": "Stand, présentation, caisse symbolique (simulation).",
                "duration_min": 180,
                "skill_tags": ["contact", "compter_simple", "equipe"],
                "seasonality": ["toutes"],
                "safety_level": 1,
                "materials": []
            }
        ]
        
        # Create activity objects and add to database
        for activity_data in activities_data:
            activity = Activity(**activity_data)
            db.add(activity)
        
        db.commit()
        print(f"Successfully seeded {len(activities_data)} activities!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding activities: {e}")
    finally:
        db.close()


def create_admin_user():
    """Create a default admin user."""
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("Admin user already exists")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@lavidaluca.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            full_name="Administrateur La Vida Luca",
            is_superuser=True
        )
        
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating admin user: {e}")
    finally:
        db.close()


def init_db():
    """Initialize the database with tables and seed data."""
    print("Initializing database...")
    create_tables()
    seed_activities()
    create_admin_user()
    print("Database initialization complete!")


if __name__ == "__main__":
    init_db()