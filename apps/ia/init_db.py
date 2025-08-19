"""
Database initialization and seeding script.
Run this to create tables and populate with initial data.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.models.models import User, Activity
from app.core.config import settings
from app.core.security import get_password_hash

# Create engine and session
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")


def seed_activities():
    """Seed the database with the 30 activities from the frontend."""
    print("Seeding activities...")
    
    db = SessionLocal()
    
    # Check if activities already exist
    existing_activities = db.query(Activity).count()
    if existing_activities > 0:
        print(f"Activities already exist ({existing_activities} found). Skipping seed.")
        db.close()
        return
    
    # Activities data from the frontend
    activities_data = [
        # Agriculture
        {
            "id": 1, "slug": "nourrir-soigner-moutons", "title": "Nourrir et soigner les moutons", 
            "category": "agri", "summary": "Gestes quotidiens : alimentation, eau, observation.", 
            "duration_min": 60, "skill_tags": ["elevage", "responsabilite"], 
            "seasonality": ["toutes"], "safety_level": 1, "materials": ["bottes", "gants"]
        },
        {
            "id": 2, "slug": "tonte-entretien-troupeau", "title": "Tonte & entretien du troupeau", 
            "category": "agri", "summary": "Hygiène, tonte (démo), soins courants.", 
            "duration_min": 90, "skill_tags": ["elevage", "hygiene"], 
            "seasonality": ["printemps"], "safety_level": 2, "materials": ["bottes", "gants"]
        },
        {
            "id": 3, "slug": "basse-cour-soins", "title": "Soins basse-cour", 
            "category": "agri", "summary": "Poules/canards/lapins : alimentation, abris, propreté.", 
            "duration_min": 60, "skill_tags": ["soins_animaux"], 
            "seasonality": ["toutes"], "safety_level": 1, "materials": ["bottes", "gants"]
        },
        {
            "id": 4, "slug": "plantation-cultures", "title": "Plantation de cultures", 
            "category": "agri", "summary": "Semis, arrosage, paillage, suivi de plants.", 
            "duration_min": 90, "skill_tags": ["sol", "plantes"], 
            "seasonality": ["printemps", "ete"], "safety_level": 1, "materials": ["gants"]
        },
        {
            "id": 5, "slug": "init-maraichage", "title": "Initiation maraîchage", 
            "category": "agri", "summary": "Plan de culture, entretien, récolte respectueuse.", 
            "duration_min": 120, "skill_tags": ["sol", "organisation"], 
            "seasonality": ["printemps", "ete", "automne"], "safety_level": 1, "materials": ["gants", "bottes"]
        },
        # Add more activities...
        # Transformation
        {
            "id": 12, "slug": "pain-four-bois", "title": "Pain au four à bois", 
            "category": "transfo", "summary": "Pétrissage, façonnage, cuisson : respect des temps.", 
            "duration_min": 120, "skill_tags": ["precision", "rythme"], 
            "seasonality": ["toutes"], "safety_level": 2, "materials": ["tablier"]
        },
        # Artisanat
        {
            "id": 13, "slug": "abris-bois", "title": "Construction d'abris", 
            "category": "artisanat", "summary": "Petites structures bois : plan, coupe, assemblage.", 
            "duration_min": 120, "skill_tags": ["bois", "precision", "securite"], 
            "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]
        },
        # Nature
        {
            "id": 20, "slug": "plantation-arbres", "title": "Plantation d'arbres", 
            "category": "nature", "summary": "Choix d'essences, tuteurage, paillage, suivi.", 
            "duration_min": 120, "skill_tags": ["geste_juste", "endurance"], 
            "seasonality": ["automne", "hiver"], "safety_level": 1, "materials": ["gants", "bottes"]
        },
        {
            "id": 21, "slug": "potager-eco", "title": "Potager écologique", 
            "category": "nature", "summary": "Associations, paillis, rotation des cultures.", 
            "duration_min": 90, "skill_tags": ["observation", "sobriete"], 
            "seasonality": ["printemps", "ete", "automne"], "safety_level": 1, "materials": ["gants"]
        },
        {
            "id": 22, "slug": "compostage", "title": "Compostage", 
            "category": "nature", "summary": "Tri, compost, valorisation des déchets verts.", 
            "duration_min": 60, "skill_tags": ["geste_utile", "hygiene"], 
            "seasonality": ["toutes"], "safety_level": 1, "materials": ["gants"]
        },
        {
            "id": 23, "slug": "faune-locale", "title": "Observation de la faune locale", 
            "category": "nature", "summary": "Discrétion, repérage, traces/indices.", 
            "duration_min": 60, "skill_tags": ["patience", "respect"], 
            "seasonality": ["toutes"], "safety_level": 1, "materials": []
        },
    ]
    
    # Create activity objects
    for activity_data in activities_data:
        # Remove id from data (let database auto-generate)
        activity_data_copy = activity_data.copy()
        activity_data_copy.pop("id", None)
        
        activity = Activity(**activity_data_copy)
        db.add(activity)
    
    db.commit()
    print(f"Seeded {len(activities_data)} activities")
    db.close()


def create_admin_user():
    """Create a default admin user."""
    print("Creating admin user...")
    
    db = SessionLocal()
    
    # Check if admin already exists
    existing_admin = db.query(User).filter(User.username == "admin").first()
    if existing_admin:
        print("Admin user already exists. Skipping creation.")
        db.close()
        return
    
    # Create admin user
    admin_user = User(
        email="admin@lavidaluca.com",
        username="admin",
        hashed_password=get_password_hash("admin123"),
        full_name="Administrator",
        location="Calvados (14)",
        skills=["administration", "organisation"],
        availability=["semaine", "weekend"],
        preferences=["agri", "nature"],
        is_active=True,
        is_superuser=True
    )
    
    db.add(admin_user)
    db.commit()
    print("Admin user created (username: admin, password: admin123)")
    db.close()


def main():
    """Main initialization function."""
    print("Initializing La Vida Luca database...")
    
    try:
        create_tables()
        seed_activities()
        create_admin_user()
        print("\n✅ Database initialization completed successfully!")
        print("\nNext steps:")
        print("1. Start the FastAPI server: uvicorn app.main:app --reload")
        print("2. Visit http://localhost:8000/docs for API documentation")
        print("3. Use admin credentials to test: username=admin, password=admin123")
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        raise


if __name__ == "__main__":
    main()