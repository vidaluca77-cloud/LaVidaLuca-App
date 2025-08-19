"""
Database seeder script to populate initial data.
"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User
from app.models.activity import Activity


def create_sample_data():
    """Create sample data for development and testing."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create admin user
        admin_user = User(
            email="admin@lavidaluca.fr",
            username="admin",
            full_name="Administrateur LaVidaLuca",
            bio="Administrateur de la plateforme LaVidaLuca",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)
        
        # Create sample user
        sample_user = User(
            email="etudiant@mfr.fr",
            username="etudiant_mfr",
            full_name="Étudiant MFR",
            bio="Étudiant en formation agricole à la MFR",
            hashed_password=get_password_hash("password123"),
            is_active=True,
            is_superuser=False
        )
        db.add(sample_user)
        
        db.commit()
        db.refresh(admin_user)
        db.refresh(sample_user)
        
        # Create sample activities
        activities_data = [
            {
                "title": "Élevage de poules pondeuses",
                "description": "Initiation à l'élevage de poules pondeuses en parcours libre. Apprentissage des soins quotidiens, de l'alimentation et de la gestion d'un poulailler.",
                "category": "Élevage",
                "difficulty_level": 2,
                "duration_hours": 4.0,
                "max_participants": 8,
                "location": "Ferme pédagogique",
                "equipment_needed": "Gants, seau, nourriture pour volailles",
                "learning_objectives": "Comprendre les besoins des volailles, maîtriser les gestes de soins, sensibilisation au bien-être animal",
                "is_featured": True,
                "creator_id": admin_user.id
            },
            {
                "title": "Culture de légumes en permaculture",
                "description": "Initiation aux techniques de permaculture pour la culture de légumes. Approche écologique et durable de l'agriculture.",
                "category": "Agriculture",
                "difficulty_level": 3,
                "duration_hours": 6.0,
                "max_participants": 12,
                "location": "Jardin pédagogique",
                "equipment_needed": "Bêche, serfouette, graines, paillis",
                "learning_objectives": "Maîtriser les principes de la permaculture, planifier un potager, comprendre les associations de plantes",
                "is_featured": True,
                "creator_id": admin_user.id
            },
            {
                "title": "Fabrication de fromage artisanal",
                "description": "Découverte de la transformation du lait en fromage selon des méthodes traditionnelles. De la traite à l'affinage.",
                "category": "Transformation",
                "difficulty_level": 4,
                "duration_hours": 8.0,
                "max_participants": 6,
                "location": "Fromagerie pédagogique",
                "equipment_needed": "Tablier, charlotte, matériel de fromagerie",
                "learning_objectives": "Comprendre le processus de transformation, maîtriser les techniques de base, hygiène alimentaire",
                "is_featured": False,
                "creator_id": admin_user.id
            },
            {
                "title": "Apiculture et récolte de miel",
                "description": "Introduction à l'apiculture: vie des abeilles, gestion d'une ruche, récolte du miel et autres produits de la ruche.",
                "category": "Apiculture",
                "difficulty_level": 3,
                "duration_hours": 5.0,
                "max_participants": 10,
                "location": "Rucher pédagogique",
                "equipment_needed": "Combinaison d'apiculteur, enfumoir, outils de ruche",
                "learning_objectives": "Comprendre la biologie des abeilles, maîtriser les gestes de l'apiculteur, sensibilisation à l'environnement",
                "is_featured": True,
                "creator_id": sample_user.id
            },
            {
                "title": "Taille et entretien des arbres fruitiers",
                "description": "Techniques de taille des arbres fruitiers selon les saisons. Entretien du verger et prévention des maladies.",
                "category": "Arboriculture",
                "difficulty_level": 2,
                "duration_hours": 3.0,
                "max_participants": 15,
                "location": "Verger pédagogique",
                "equipment_needed": "Sécateur, échelle, gants de protection",
                "learning_objectives": "Maîtriser les techniques de taille, identifier les maladies, planifier l'entretien annuel",
                "is_featured": False,
                "creator_id": sample_user.id
            }
        ]
        
        for activity_data in activities_data:
            activity = Activity(**activity_data)
            db.add(activity)
        
        db.commit()
        
        print("✅ Sample data created successfully!")
        print(f"Admin user: admin@lavidaluca.fr / admin123")
        print(f"Sample user: etudiant@mfr.fr / password123")
        print(f"Created {len(activities_data)} sample activities")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()