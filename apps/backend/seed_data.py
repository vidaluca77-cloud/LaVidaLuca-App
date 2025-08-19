"""
Database seeding script for LaVidaLuca backend
Populates the database with initial activities and skills
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Activity, Skill
import json

# Create tables
Base.metadata.create_all(bind=engine)

# Skills list from frontend
SKILLS = [
    'elevage', 'hygiene', 'soins_animaux', 'sol', 'plantes', 'organisation',
    'securite', 'bois', 'precision', 'creativite', 'patience', 'endurance',
    'ecologie', 'accueil', 'pedagogie', 'expression', 'equipe', 'responsabilite',
    'douceur', 'rythme', 'temps', 'rigueur', 'relationnel'
]

# Activities data from frontend
ACTIVITIES = [
    # Agriculture
    { 'id': 1, 'slug': 'nourrir-soigner-moutons', 'title': 'Nourrir et soigner les moutons', 'category': 'agri', 'summary': 'Gestes quotidiens : alimentation, eau, observation.', 'duration_min': 60, 'skill_tags': ['elevage', 'responsabilite'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['bottes', 'gants'] },
    { 'id': 2, 'slug': 'tonte-entretien-troupeau', 'title': 'Tonte & entretien du troupeau', 'category': 'agri', 'summary': 'Hygiène, tonte (démo), soins courants.', 'duration_min': 90, 'skill_tags': ['elevage', 'hygiene'], 'seasonality': ['printemps'], 'safety_level': 2, 'materials': ['bottes', 'gants'] },
    { 'id': 3, 'slug': 'basse-cour-soins', 'title': 'Soins basse-cour', 'category': 'agri', 'summary': 'Poules/canards/lapins : alimentation, abris, propreté.', 'duration_min': 60, 'skill_tags': ['soins_animaux'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['bottes', 'gants'] },
    { 'id': 4, 'slug': 'plantation-cultures', 'title': 'Plantation de cultures', 'category': 'agri', 'summary': 'Semis, arrosage, paillage, suivi de plants.', 'duration_min': 90, 'skill_tags': ['sol', 'plantes'], 'seasonality': ['printemps', 'ete'], 'safety_level': 1, 'materials': ['gants'] },
    { 'id': 5, 'slug': 'init-maraichage', 'title': 'Initiation maraîchage', 'category': 'agri', 'summary': 'Plan de culture, entretien, récolte respectueuse.', 'duration_min': 120, 'skill_tags': ['sol', 'organisation'], 'seasonality': ['printemps', 'ete', 'automne'], 'safety_level': 1, 'materials': ['gants', 'bottes'] },
    { 'id': 6, 'slug': 'clotures-abris', 'title': 'Gestion des clôtures & abris', 'category': 'agri', 'summary': 'Identifier, réparer, sécuriser parcs et abris.', 'duration_min': 120, 'skill_tags': ['securite', 'bois'], 'seasonality': ['toutes'], 'safety_level': 2, 'materials': ['gants'] },

    # Transformation
    { 'id': 7, 'slug': 'fromage', 'title': 'Fabrication de fromage', 'category': 'transfo', 'summary': 'Du lait au caillé : hygiène, moulage, affinage (découverte).', 'duration_min': 90, 'skill_tags': ['hygiene', 'precision'], 'seasonality': ['toutes'], 'safety_level': 2, 'materials': ['tablier'] },
    { 'id': 8, 'slug': 'conserves', 'title': 'Confitures & conserves', 'category': 'transfo', 'summary': 'Préparation, stérilisation, mise en pot, étiquetage.', 'duration_min': 90, 'skill_tags': ['organisation', 'hygiene'], 'seasonality': ['ete', 'automne'], 'safety_level': 1, 'materials': ['tablier'] },
    { 'id': 9, 'slug': 'laine', 'title': 'Transformation de la laine', 'category': 'transfo', 'summary': 'Lavage, cardage, petite création textile.', 'duration_min': 90, 'skill_tags': ['patience', 'creativite'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['tablier', 'gants'] },
    { 'id': 10, 'slug': 'jus', 'title': 'Fabrication de jus', 'category': 'transfo', 'summary': 'Du verger à la bouteille : tri, pressage, filtration.', 'duration_min': 90, 'skill_tags': ['hygiene', 'securite'], 'seasonality': ['automne'], 'safety_level': 2, 'materials': ['tablier', 'gants'] },
    { 'id': 11, 'slug': 'aromatiques-sechage', 'title': 'Séchage d\'herbes aromatiques', 'category': 'transfo', 'summary': 'Cueillette, séchage, conditionnement doux.', 'duration_min': 60, 'skill_tags': ['douceur', 'organisation'], 'seasonality': ['ete'], 'safety_level': 1, 'materials': ['tablier'] },
    { 'id': 12, 'slug': 'pain-four-bois', 'title': 'Pain au four à bois', 'category': 'transfo', 'summary': 'Pétrissage, façonnage, cuisson : respect des temps.', 'duration_min': 120, 'skill_tags': ['precision', 'rythme'], 'seasonality': ['toutes'], 'safety_level': 2, 'materials': ['tablier'] },

    # Artisanat (subset)
    { 'id': 13, 'slug': 'menuiserie-simple', 'title': 'Menuiserie simple', 'category': 'artisanat', 'summary': 'Réparations, assemblages basiques, ponçage.', 'duration_min': 120, 'skill_tags': ['bois', 'precision'], 'seasonality': ['toutes'], 'safety_level': 2, 'materials': ['gants'] },
    { 'id': 14, 'slug': 'reparation-outils', 'title': 'Réparation d\'outils', 'category': 'artisanat', 'summary': 'Maintenance, affûtage, révision matériel.', 'duration_min': 90, 'skill_tags': ['precision', 'securite'], 'seasonality': ['toutes'], 'safety_level': 2, 'materials': ['gants'] },

    # Nature (subset)
    { 'id': 15, 'slug': 'compostage', 'title': 'Compostage', 'category': 'nature', 'summary': 'Tri, compost, recyclage organique.', 'duration_min': 60, 'skill_tags': ['ecologie', 'organisation'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['gants'] },
    { 'id': 16, 'slug': 'plantation-arbres', 'title': 'Plantation d\'arbres', 'category': 'nature', 'summary': 'Choix, plantation, protection jeunes pousses.', 'duration_min': 120, 'skill_tags': ['ecologie', 'endurance'], 'seasonality': ['automne', 'hiver'], 'safety_level': 1, 'materials': ['gants', 'bottes'] },

    # Social (subset)
    { 'id': 17, 'slug': 'accueil-visiteurs', 'title': 'Accueil des visiteurs', 'category': 'social', 'summary': 'Présentation du projet, visite guidée.', 'duration_min': 90, 'skill_tags': ['accueil', 'expression'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': [] },
    { 'id': 18, 'slug': 'cuisine-collective', 'title': 'Cuisine collective (équipe)', 'category': 'social', 'summary': 'Préparer un repas simple et bon.', 'duration_min': 90, 'skill_tags': ['hygiene', 'equipe', 'temps'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['tablier'] },
    { 'id': 19, 'slug': 'gouter-fermier', 'title': 'Goûter fermier', 'category': 'social', 'summary': 'Organisation, service, convivialité, propreté.', 'duration_min': 60, 'skill_tags': ['rigueur', 'relationnel'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': ['tablier'] },
    { 'id': 20, 'slug': 'marche-local', 'title': 'Participation à un marché local', 'category': 'social', 'summary': 'Stand, présentation, caisse symbolique (simulation).', 'duration_min': 180, 'skill_tags': ['contact', 'compter_simple', 'equipe'], 'seasonality': ['toutes'], 'safety_level': 1, 'materials': [] },
]

def seed_database():
    """Seed the database with initial data"""
    db = SessionLocal()
    
    try:
        # Create skills
        print("Creating skills...")
        for skill_name in SKILLS:
            existing_skill = db.query(Skill).filter(Skill.name == skill_name).first()
            if not existing_skill:
                skill = Skill(name=skill_name)
                db.add(skill)
        
        db.commit()
        print(f"Created {len(SKILLS)} skills")
        
        # Create activities
        print("Creating activities...")
        for activity_data in ACTIVITIES:
            existing_activity = db.query(Activity).filter(Activity.slug == activity_data['slug']).first()
            if not existing_activity:
                activity = Activity(
                    slug=activity_data['slug'],
                    title=activity_data['title'],
                    category=activity_data['category'],
                    summary=activity_data['summary'],
                    duration_min=activity_data['duration_min'],
                    safety_level=activity_data['safety_level'],
                    seasonality=json.dumps(activity_data['seasonality']),
                    materials=json.dumps(activity_data['materials'])
                )
                
                # Add skill relationships
                for skill_name in activity_data['skill_tags']:
                    skill = db.query(Skill).filter(Skill.name == skill_name).first()
                    if skill:
                        activity.required_skills.append(skill)
                
                db.add(activity)
        
        db.commit()
        print(f"Created {len(ACTIVITIES)} activities")
        print("Database seeding completed successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()