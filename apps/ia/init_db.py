"""
Database initialization script with default activities
"""

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal, create_tables
from app.models.models import Activity, User
from app.core.security import get_password_hash
import logging

logger = logging.getLogger(__name__)

# Default activities based on the frontend data
DEFAULT_ACTIVITIES = [
    # Agriculture
    {
        "slug": "nourrir-soigner-moutons",
        "title": "Nourrir et soigner les moutons",
        "category": "agri",
        "summary": "Gestes quotidiens : alimentation, eau, observation.",
        "description": "Apprentissage des soins de base aux moutons : distribution de foin et de grains, vérification des points d'eau, observation du comportement du troupeau. Initiation aux gestes d'élevage responsable.",
        "duration_min": 60,
        "skill_tags": ["elevage", "responsabilite"],
        "seasonality": ["toutes"],
        "safety_level": 1,
        "materials": ["bottes", "gants"],
        "difficulty_level": "beginner"
    },
    {
        "slug": "tonte-entretien-troupeau",
        "title": "Tonte & entretien du troupeau",
        "category": "agri",
        "summary": "Hygiène, tonte (démo), soins courants.",
        "description": "Découverte des techniques de tonte et de soins au troupeau. Observation des gestes professionnels, participation aux soins d'hygiène et de prévention.",
        "duration_min": 90,
        "skill_tags": ["elevage", "hygiene"],
        "seasonality": ["printemps"],
        "safety_level": 2,
        "materials": ["bottes", "gants"],
        "difficulty_level": "intermediate"
    },
    {
        "slug": "basse-cour-soins",
        "title": "Soins basse-cour",
        "category": "agri",
        "summary": "Poules/canards/lapins : alimentation, abris, propreté.",
        "description": "Gestion quotidienne de la basse-cour : alimentation adaptée, nettoyage des espaces, vérification de la santé des animaux, ramassage des œufs.",
        "duration_min": 60,
        "skill_tags": ["soins_animaux"],
        "seasonality": ["toutes"],
        "safety_level": 1,
        "materials": ["bottes", "gants"],
        "difficulty_level": "beginner"
    },
    {
        "slug": "plantation-cultures",
        "title": "Plantation de cultures",
        "category": "agri",
        "summary": "Semis, arrosage, paillage, suivi de plants.",
        "description": "Initiation aux techniques de plantation : préparation du sol, semis en ligne, arrosage raisonné, mise en place du paillage, suivi de la croissance.",
        "duration_min": 90,
        "skill_tags": ["sol", "plantes"],
        "seasonality": ["printemps", "ete"],
        "safety_level": 1,
        "materials": ["gants"],
        "difficulty_level": "beginner"
    },
    {
        "slug": "init-maraichage",
        "title": "Initiation maraîchage",
        "category": "agri",
        "summary": "Plan de culture, entretien, récolte respectueuse.",
        "description": "Découverte du maraîchage diversifié : planification des cultures, rotations, associations de plantes, techniques de récolte respectueuses.",
        "duration_min": 120,
        "skill_tags": ["sol", "organisation"],
        "seasonality": ["printemps", "ete", "automne"],
        "safety_level": 1,
        "materials": ["gants", "bottes"],
        "difficulty_level": "intermediate"
    },
    
    # Transformation
    {
        "slug": "transformation-lait",
        "title": "Transformation du lait",
        "category": "transfo",
        "summary": "Fromage frais, yaourt, respect de l'hygiène.",
        "description": "Apprentissage des bases de la transformation laitière : fabrication de fromage blanc, yaourts, respect strict des règles d'hygiène alimentaire.",
        "duration_min": 120,
        "skill_tags": ["hygiene", "precision"],
        "seasonality": ["toutes"],
        "safety_level": 2,
        "materials": ["tablier", "gants"],
        "difficulty_level": "intermediate"
    },
    {
        "slug": "conserves-legumes",
        "title": "Conserves de légumes",
        "category": "transfo",
        "summary": "Bocaux, stérilisation, valorisation des récoltes.",
        "description": "Techniques de conservation : préparation des légumes, mise en bocaux, stérilisation, étiquetage. Valorisation des surplus de récolte.",
        "duration_min": 90,
        "skill_tags": ["organisation", "hygiene"],
        "seasonality": ["ete", "automne"],
        "safety_level": 2,
        "materials": ["tablier", "gants"],
        "difficulty_level": "beginner"
    },
    {
        "slug": "fabrication-pain",
        "title": "Fabrication du pain",
        "category": "transfo",
        "summary": "Pétrissage, fermentation, cuisson au four.",
        "description": "Art de la boulangerie : préparation de la pâte, techniques de pétrissage, gestion de la fermentation, cuisson au four traditionnel.",
        "duration_min": 180,
        "skill_tags": ["patience", "precision"],
        "seasonality": ["toutes"],
        "safety_level": 2,
        "materials": ["tablier"],
        "difficulty_level": "intermediate"
    },
    
    # Artisanat
    {
        "slug": "menuiserie-base",
        "title": "Menuiserie de base",
        "category": "artisanat",
        "summary": "Assemblage, ponçage, découverte des outils.",
        "description": "Initiation à la menuiserie : reconnaissance des essences de bois, maniement des outils de base, techniques d'assemblage simple, finitions.",
        "duration_min": 120,
        "skill_tags": ["bois", "precision"],
        "seasonality": ["toutes"],
        "safety_level": 3,
        "materials": ["lunettes", "gants"],
        "difficulty_level": "beginner"
    },
    {
        "slug": "reparation-clôtures",
        "title": "Réparation de clôtures",
        "category": "artisanat",
        "summary": "Tension des fils, changement de piquets.",
        "description": "Maintenance des clôtures : évaluation des dégâts, tension des fils, remplacement des piquets, utilisation des outils spécialisés.",
        "duration_min": 90,
        "skill_tags": ["organisation", "endurance"],
        "seasonality": ["printemps", "automne"],
        "safety_level": 2,
        "materials": ["gants", "bottes"],
        "difficulty_level": "beginner"
    },
    
    # Nature/Environnement
    {
        "slug": "plantation-arbres",
        "title": "Plantation d'arbres",
        "category": "nature",
        "summary": "Trous, plants, arrosage, protection.",
        "description": "Reforestation et agroforesterie : choix des essences, techniques de plantation, protection contre les nuisibles, suivi de croissance.",
        "duration_min": 120,
        "skill_tags": ["ecologie", "endurance"],
        "seasonality": ["automne", "hiver"],
        "safety_level": 1,
        "materials": ["gants", "bottes"],
        "difficulty_level": "beginner"
    },
    {
        "slug": "compostage",
        "title": "Compostage",
        "category": "nature",
        "summary": "Tri, compost, valorisation des déchets verts.",
        "description": "Gestion écologique des déchets : tri des matières organiques, construction du compost, retournement, utilisation du compost mûr.",
        "duration_min": 60,
        "skill_tags": ["geste_utile", "hygiene"],
        "seasonality": ["toutes"],
        "safety_level": 1,
        "materials": ["gants"],
        "difficulty_level": "beginner"
    },
    
    # Social/Animation
    {
        "slug": "accueil-groupes",
        "title": "Accueil de groupes",
        "category": "social",
        "summary": "Présentation, visite guidée, pédagogie.",
        "description": "Animation pédagogique : accueil des visiteurs, présentation du projet, visite guidée des installations, transmission des valeurs.",
        "duration_min": 90,
        "skill_tags": ["accueil", "pedagogie"],
        "seasonality": ["toutes"],
        "safety_level": 1,
        "materials": [],
        "difficulty_level": "intermediate"
    },
    {
        "slug": "ateliers-enfants",
        "title": "Ateliers enfants",
        "category": "social",
        "summary": "Animations nature, activités manuelles.",
        "description": "Animation jeune public : ateliers créatifs, découverte de la nature, jeux éducatifs, sensibilisation à l'environnement.",
        "duration_min": 120,
        "skill_tags": ["creativite", "pedagogie"],
        "seasonality": ["toutes"],
        "safety_level": 1,
        "materials": [],
        "difficulty_level": "intermediate"
    }
]


def init_database():
    """Initialize database with tables and default data"""
    logger.info("Creating database tables...")
    create_tables()
    
    db = SessionLocal()
    try:
        # Create default admin user if not exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            logger.info("Creating default admin user...")
            admin_user = User(
                email="admin@lavidaluca.fr",
                username="admin",
                full_name="Administrator",
                hashed_password=get_password_hash("admin123"),
                is_active=True,
                is_superuser=True
            )
            db.add(admin_user)
            db.commit()
            logger.info("Default admin user created (username: admin, password: admin123)")
        
        # Create default activities if not exist
        existing_activities = db.query(Activity).count()
        if existing_activities == 0:
            logger.info("Creating default activities...")
            for activity_data in DEFAULT_ACTIVITIES:
                activity = Activity(**activity_data)
                db.add(activity)
            db.commit()
            logger.info(f"Created {len(DEFAULT_ACTIVITIES)} default activities")
        else:
            logger.info(f"Database already contains {existing_activities} activities")
            
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
    print("Database initialization completed!")