"""
Database seeding script to populate activities from frontend data
"""
from app.core.database import SessionLocal, create_tables
from app.models.activity import Activity
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Activities data from frontend (src/app/page.tsx)
ACTIVITIES_DATA = [
    # Agriculture
    {
        'id': '1', 'slug': 'nourrir-soigner-moutons', 'title': 'Nourrir et soigner les moutons', 
        'category': 'agri', 'summary': 'Gestes quotidiens : alimentation, eau, observation.', 
        'duration_min': 60, 'skill_tags': ['elevage', 'responsabilite'], 
        'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['bottes', 'gants']
    },
    {
        'id': '2', 'slug': 'tonte-entretien-troupeau', 'title': 'Tonte & entretien du troupeau', 
        'category': 'agri', 'summary': 'Hygiène, tonte (démo), soins courants.', 
        'duration_min': 90, 'skill_tags': ['elevage', 'hygiene'], 
        'seasonality': ['printemps'], 'safety_level': 2, 'materials': ['bottes', 'gants']
    },
    {
        'id': '3', 'slug': 'basse-cour-soins', 'title': 'Soins basse-cour', 
        'category': 'agri', 'summary': 'Poules/canards/lapins : alimentation, abris, propreté.', 
        'duration_min': 60, 'skill_tags': ['soins_animaux'], 
        'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['bottes', 'gants']
    },
    {
        'id': '4', 'slug': 'plantation-cultures', 'title': 'Plantation de cultures', 
        'category': 'agri', 'summary': 'Semis, arrosage, paillage, suivi de plants.', 
        'duration_min': 90, 'skill_tags': ['sol', 'plantes'], 
        'seasonality': ['printemps', 'ete'], 'safety_level': 1, 'materials': ['gants']
    },
    {
        'id': '5', 'slug': 'init-maraichage', 'title': 'Initiation maraîchage', 
        'category': 'agri', 'summary': 'Plan de culture, entretien, récolte respectueuse.', 
        'duration_min': 120, 'skill_tags': ['sol', 'organisation'], 
        'seasonality': ['printemps', 'ete', 'automne'], 'safety_level': 1, 'materials': ['gants', 'bottes']
    },
    {
        'id': '6', 'slug': 'clotures-abris', 'title': 'Gestion des clôtures & abris', 
        'category': 'agri', 'summary': 'Identifier, réparer, sécuriser parcs et abris.', 
        'duration_min': 120, 'skill_tags': ['securite', 'bois'], 
        'seasonality': ['toutes'], 'safety_level': 2, 'materials': ['gants']
    },
    
    # Transformation
    {
        'id': '7', 'slug': 'fromage', 'title': 'Fabrication de fromage', 
        'category': 'transfo', 'summary': 'Du lait au caillé : hygiène, moulage, affinage (découverte).', 
        'duration_min': 90, 'skill_tags': ['hygiene', 'precision'], 
        'seasonality': ['toutes'], 'safety_level': 2, 'materials': ['tablier']
    },
    {
        'id': '8', 'slug': 'conserves', 'title': 'Conserves & lacto-fermentation', 
        'category': 'transfo', 'summary': 'Stérilisation, bocaux, lacto-fermentation de légumes.', 
        'duration_min': 120, 'skill_tags': ['hygiene', 'precision'], 
        'seasonality': ['ete', 'automne'], 'safety_level': 2, 'materials': ['tablier']
    },
    {
        'id': '9', 'slug': 'pain-boulange', 'title': 'Pain & boulange simple', 
        'category': 'transfo', 'summary': 'Pétrissage, levain, cuisson au four traditionnel.', 
        'duration_min': 180, 'skill_tags': ['patience', 'precision'], 
        'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['tablier']
    },
    
    # Add more activities as needed...
    # For brevity, I'll add a few more key ones
    {
        'id': '10', 'slug': 'menuiserie-simple', 'title': 'Menuiserie simple', 
        'category': 'artisanat', 'summary': 'Nichoirs, petits objets, assemblage, ponçage.', 
        'duration_min': 120, 'skill_tags': ['bois', 'precision'], 
        'seasonality': ['toutes'], 'safety_level': 2, 'materials': ['gants']
    },
    {
        'id': '11', 'slug': 'plantation-arbres', 'title': 'Plantation d\'arbres', 
        'category': 'nature', 'summary': 'Creuser, planter, arroser, protéger jeunes plants.', 
        'duration_min': 90, 'skill_tags': ['sol', 'endurance'], 
        'seasonality': ['automne', 'hiver'], 'safety_level': 1, 'materials': ['gants', 'bottes']
    },
    {
        'id': '12', 'slug': 'accueil-visiteurs', 'title': 'Accueil des visiteurs', 
        'category': 'social', 'summary': 'Présentation du lieu, visite guidée, échanges.', 
        'duration_min': 90, 'skill_tags': ['accueil', 'expression'], 
        'seasonality': ['toutes'], 'safety_level': 1, 'materials': []
    }
]


def seed_activities():
    """Seed the database with initial activities"""
    db = SessionLocal()
    try:
        # Check if activities already exist
        existing_count = db.query(Activity).count()
        if existing_count > 0:
            logger.info(f"Activities already exist ({existing_count} found). Skipping seed.")
            return
        
        logger.info("Seeding activities...")
        for activity_data in ACTIVITIES_DATA:
            # Remove the frontend 'id' field and let SQLAlchemy generate UUID
            activity_data_copy = activity_data.copy()
            activity_data_copy.pop('id', None)
            
            activity = Activity(**activity_data_copy)
            db.add(activity)
        
        db.commit()
        logger.info(f"Successfully seeded {len(ACTIVITIES_DATA)} activities")
        
    except Exception as e:
        logger.error(f"Error seeding activities: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_tables()
    seed_activities()