"""
Database seeding script to populate initial activities data
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from database.models import Base, Activity
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Activities data from the frontend
ACTIVITIES_DATA = [
    # Agriculture
    {'slug': 'nourrir-soigner-moutons', 'title': 'Nourrir et soigner les moutons', 'category': 'agri', 'summary': 'Gestes quotidiens : alimentation, eau, observation.', 'duration_min': 60, 'skill_tags': ['elevage', 'responsabilite'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['bottes', 'gants']},
    {'slug': 'traite-chevre', 'title': 'Traite des chèvres', 'category': 'agri', 'summary': 'Technique, hygiène, régularité.', 'duration_min': 45, 'skill_tags': ['precision', 'hygiene'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['gants']},
    {'slug': 'plantation-legumes', 'title': 'Plantation de légumes', 'category': 'agri', 'summary': 'Préparation du sol, semis, arrosage.', 'duration_min': 90, 'skill_tags': ['sol', 'plantes'], 'seasonality': ['printemps', 'ete'], 'safety_level': 1, 'materials': ['gants', 'outils']},
    {'slug': 'ramassage-oeufs', 'title': 'Ramassage des œufs', 'category': 'agri', 'summary': 'Collecte douce, tri, nettoyage.', 'duration_min': 30, 'skill_tags': ['hygiene', 'delicatesse'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['panier']},
    {'slug': 'soins-poules', 'title': 'Soins aux poules', 'category': 'agri', 'summary': 'Alimentation, eau propre, observation.', 'duration_min': 45, 'skill_tags': ['soins_animaux', 'observation'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['gants']},
    {'slug': 'entretien-jardin', 'title': 'Entretien du jardin', 'category': 'agri', 'summary': 'Binage, désherbage, arrosage selon les besoins.', 'duration_min': 120, 'skill_tags': ['endurance', 'plantes'], 'seasonality': ['printemps', 'ete', 'automne'], 'safety_level': 1, 'materials': ['outils', 'gants']},
    
    # Transformation
    {'slug': 'fabrication-fromage', 'title': 'Fabrication du fromage', 'category': 'transfo', 'summary': 'Caillage, moulage, affinage : étapes précises.', 'duration_min': 120, 'skill_tags': ['precision', 'hygiene'], 'seasonality': ['toutes'], 'safety_level': 2, 'materials': ['tablier', 'gants']},
    {'slug': 'conserves', 'title': 'Confitures & conserves', 'category': 'transfo', 'summary': 'Préparation, stérilisation, mise en pot, étiquetage.', 'duration_min': 90, 'skill_tags': ['organisation', 'hygiene'], 'seasonality': ['ete', 'automne'], 'safety_level': 1, 'materials': ['tablier']},
    {'slug': 'laine', 'title': 'Transformation de la laine', 'category': 'transfo', 'summary': 'Lavage, cardage, petite création textile.', 'duration_min': 90, 'skill_tags': ['patience', 'creativite'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['tablier', 'gants']},
    {'slug': 'beurre', 'title': 'Fabrication du beurre', 'category': 'transfo', 'summary': 'Barattage, malaxage, moulage.', 'duration_min': 60, 'skill_tags': ['rythme', 'hygiene'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['tablier']},
    {'slug': 'pain', 'title': 'Fabrication du pain', 'category': 'transfo', 'summary': 'Pétrissage, fermentation, cuisson.', 'duration_min': 180, 'skill_tags': ['patience', 'rythme'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['tablier']},
    {'slug': 'pain-four-bois', 'title': 'Pain au four à bois', 'category': 'transfo', 'summary': 'Pétrissage, façonnage, cuisson : respect des temps.', 'duration_min': 120, 'skill_tags': ['precision', 'rythme'], 'seasonality': ['toutes'], 'safety_level': 2, 'materials': ['tablier']},
    
    # Artisanat
    {'slug': 'abris-bois', 'title': 'Construction d\'abris', 'category': 'artisanat', 'summary': 'Petites structures bois : plan, coupe, assemblage.', 'duration_min': 120, 'skill_tags': ['bois', 'precision', 'securite'], 'seasonality': ['toutes'], 'safety_level': 2, 'materials': ['gants']},
    {'slug': 'reparation-outils', 'title': 'Réparation d\'outils', 'category': 'artisanat', 'summary': 'Diagnostic, démontage, remise en état.', 'duration_min': 90, 'skill_tags': ['mecanique', 'logique'], 'seasonality': ['toutes'], 'safety_level': 2, 'materials': ['gants', 'outils']},
    {'slug': 'clotures', 'title': 'Pose de clôtures', 'category': 'artisanat', 'summary': 'Mesure, creusage, pose, tension.', 'duration_min': 150, 'skill_tags': ['precision', 'endurance'], 'seasonality': ['printemps', 'ete', 'automne'], 'safety_level': 2, 'materials': ['gants', 'outils']},
    {'slug': 'creation-objets', 'title': 'Création d\'objets utiles', 'category': 'artisanat', 'summary': 'Bricolage, récupération, créativité.', 'duration_min': 120, 'skill_tags': ['creativite', 'bricolage'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['outils']},
    {'slug': 'poterie', 'title': 'Poterie/céramique', 'category': 'artisanat', 'summary': 'Modelage, cuisson, émaillage.', 'duration_min': 150, 'skill_tags': ['creativite', 'patience'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['tablier']},
    {'slug': 'vannerie', 'title': 'Vannerie', 'category': 'artisanat', 'summary': 'Tressage, formes, finitions.', 'duration_min': 120, 'skill_tags': ['patience', 'dexterite'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': []},
    {'slug': 'menuiserie', 'title': 'Petite menuiserie', 'category': 'artisanat', 'summary': 'Mesure, découpe, assemblage simple.', 'duration_min': 180, 'skill_tags': ['bois', 'precision'], 'seasonality': ['toutes'], 'safety_level': 2, 'materials': ['gants', 'outils']},
    
    # Nature
    {'slug': 'cueillette', 'title': 'Cueillette sauvage', 'category': 'nature', 'summary': 'Reconnaissance, récolte respectueuse.', 'duration_min': 90, 'skill_tags': ['botanique', 'respect'], 'seasonality': ['printemps', 'ete', 'automne'], 'safety_level': 1, 'materials': ['panier']},
    {'slug': 'plantations-arbres', 'title': 'Plantations d\'arbres', 'category': 'nature', 'summary': 'Préparation du terrain, plantation, arrosage.', 'duration_min': 120, 'skill_tags': ['ecologie', 'endurance'], 'seasonality': ['automne', 'hiver'], 'safety_level': 1, 'materials': ['gants', 'outils']},
    {'slug': 'entretien-sentiers', 'title': 'Entretien des sentiers', 'category': 'nature', 'summary': 'Débroussaillage, balisage, sécurisation.', 'duration_min': 150, 'skill_tags': ['endurance', 'securite'], 'seasonality': ['printemps', 'ete', 'automne'], 'safety_level': 2, 'materials': ['gants', 'outils']},
    {'slug': 'compostage', 'title': 'Compostage', 'category': 'nature', 'summary': 'Tri, compost, valorisation des déchets verts.', 'duration_min': 60, 'skill_tags': ['geste_utile', 'hygiene'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['gants']},
    {'slug': 'faune-locale', 'title': 'Observation de la faune locale', 'category': 'nature', 'summary': 'Discrétion, repérage, traces/indices.', 'duration_min': 60, 'skill_tags': ['patience', 'respect'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': []},
    {'slug': 'creation-habitats', 'title': 'Création d\'habitats pour la faune', 'category': 'nature', 'summary': 'Nichoirs, abris, points d\'eau.', 'duration_min': 120, 'skill_tags': ['ecologie', 'bricolage'], 'seasonality': ['automne', 'hiver'], 'safety_level': 1, 'materials': ['outils']},
    
    # Social
    {'slug': 'accueil-visiteurs', 'title': 'Accueil des visiteurs', 'category': 'social', 'summary': 'Présentation, explication, accompagnement.', 'duration_min': 90, 'skill_tags': ['accueil', 'expression'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': []},
    {'slug': 'animation-enfants', 'title': 'Animation pour enfants', 'category': 'social', 'summary': 'Jeux, découverte, sécurité.', 'duration_min': 120, 'skill_tags': ['pedagogie', 'patience'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': []},
    {'slug': 'marche-local', 'title': 'Marché local', 'category': 'social', 'summary': 'Installation, vente, contact client.', 'duration_min': 180, 'skill_tags': ['relationnel', 'organisation'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': []},
    {'slug': 'cuisine-collective', 'title': 'Cuisine collective (équipe)', 'category': 'social', 'summary': 'Préparer un repas simple et bon.', 'duration_min': 90, 'skill_tags': ['hygiene', 'equipe', 'temps'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['tablier']},
    {'slug': 'gouter-fermier', 'title': 'Goûter fermier', 'category': 'social', 'summary': 'Organisation, service, convivialité, propreté.', 'duration_min': 60, 'skill_tags': ['rigueur', 'relationnel'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['tablier']},
    {'slug': 'rangement-materiel', 'title': 'Rangement du matériel', 'category': 'social', 'summary': 'Tri, nettoyage, rangement méthodique.', 'duration_min': 45, 'skill_tags': ['organisation', 'rigueur'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': []}
]


def seed_activities():
    """Seed the database with activity data"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if activities already exist
        existing_count = db.query(Activity).count()
        if existing_count > 0:
            logger.info(f"Database already contains {existing_count} activities. Skipping seed.")
            return
        
        # Add activities
        for activity_data in ACTIVITIES_DATA:
            # Check if activity already exists by slug
            existing = db.query(Activity).filter(Activity.slug == activity_data['slug']).first()
            if not existing:
                activity = Activity(**activity_data)
                db.add(activity)
                logger.info(f"Added activity: {activity_data['title']}")
        
        db.commit()
        logger.info(f"Successfully seeded {len(ACTIVITIES_DATA)} activities")
        
    except Exception as e:
        logger.error(f"Error seeding activities: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_activities()