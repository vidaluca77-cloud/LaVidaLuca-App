from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Activity
from config import settings
import os

# Données des 30 activités du catalogue
ACTIVITIES_DATA = [
    # Agriculture
    {"slug": "nourrir-soigner-moutons", "title": "Nourrir et soigner les moutons", "category": "agri", "summary": "Gestes quotidiens : alimentation, eau, observation.", "duration_min": 60, "skill_tags": ["elevage", "responsabilite"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["bottes", "gants"]},
    {"slug": "poules-oeufs", "title": "Soins aux poules & récolte œufs", "category": "agri", "summary": "Nourrissage, nettoyage, collecte respectueuse.", "duration_min": 45, "skill_tags": ["elevage", "douceur"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["gants"]},
    {"slug": "soins-animaux", "title": "Soins de base aux animaux", "category": "agri", "summary": "Observation, brossage, petits soins vétérinaires.", "duration_min": 90, "skill_tags": ["soins_animaux", "patience"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    {"slug": "plantation-cultures", "title": "Plantation de cultures", "category": "agri", "summary": "Semis, arrosage, paillage, suivi de plants.", "duration_min": 90, "skill_tags": ["sol", "plantes"], "seasonality": ["printemps", "ete"], "safety_level": 1, "materials": ["gants"]},
    {"slug": "init-maraichage", "title": "Initiation maraîchage", "category": "agri", "summary": "Plan de culture, entretien, récolte respectueuse.", "duration_min": 120, "skill_tags": ["sol", "organisation"], "seasonality": ["printemps", "ete", "automne"], "safety_level": 1, "materials": ["gants", "bottes"]},
    {"slug": "clotures-abris", "title": "Gestion des clôtures & abris", "category": "agri", "summary": "Identifier, réparer, sécuriser parcs et abris.", "duration_min": 120, "skill_tags": ["securite", "bois"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},

    # Transformation
    {"slug": "fromage", "title": "Fabrication de fromage", "category": "transfo", "summary": "Du lait au caillé : hygiène, moulage, affinage (découverte).", "duration_min": 90, "skill_tags": ["hygiene", "precision"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["tablier"]},
    {"slug": "conserves", "title": "Confitures & conserves", "category": "transfo", "summary": "Préparation, stérilisation, mise en pot, étiquetage.", "duration_min": 90, "skill_tags": ["organisation", "hygiene"], "seasonality": ["ete", "automne"], "safety_level": 1, "materials": ["tablier"]},
    {"slug": "laine", "title": "Transformation de la laine", "category": "transfo", "summary": "Lavage, cardage, petite création textile.", "duration_min": 90, "skill_tags": ["patience", "creativite"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier", "gants"]},
    {"slug": "jus", "title": "Fabrication de jus", "category": "transfo", "summary": "Du verger à la bouteille : tri, pressage, filtration.", "duration_min": 90, "skill_tags": ["hygiene", "securite"], "seasonality": ["automne"], "safety_level": 2, "materials": ["tablier", "gants"]},
    {"slug": "aromatiques-sechage", "title": "Séchage d'herbes aromatiques", "category": "transfo", "summary": "Cueillette, séchage, conditionnement doux.", "duration_min": 60, "skill_tags": ["douceur", "organisation"], "seasonality": ["ete"], "safety_level": 1, "materials": ["tablier"]},
    {"slug": "pain-four-bois", "title": "Pain au four à bois", "category": "transfo", "summary": "Pétrissage, façonnage, cuisson : respect des temps.", "duration_min": 120, "skill_tags": ["precision", "rythme"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["tablier"]},

    # Artisanat
    {"slug": "abris-bois", "title": "Construction d'abris", "category": "artisanat", "summary": "Petites structures bois : plan, coupe, assemblage.", "duration_min": 120, "skill_tags": ["bois", "precision", "securite"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    {"slug": "reparations-simples", "title": "Réparations simples", "category": "artisanat", "summary": "Outils, équipements, petites réparations du quotidien.", "duration_min": 90, "skill_tags": ["securite", "logique"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    {"slug": "objets-recup", "title": "Création d'objets de récup", "category": "artisanat", "summary": "Imagination, assemblage, finitions créatives.", "duration_min": 90, "skill_tags": ["creativite", "endurance"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["gants"]},
    {"slug": "peinture-deco", "title": "Peinture & décoration d'espaces", "category": "artisanat", "summary": "Préparer, protéger, peindre proprement.", "duration_min": 90, "skill_tags": ["proprete", "finitions"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier", "gants"]},
    {"slug": "amenagement-verts", "title": "Aménagement d'espaces verts", "category": "artisanat", "summary": "Désherbage doux, paillage, plantations.", "duration_min": 90, "skill_tags": ["endurance", "esthetique"], "seasonality": ["printemps", "ete"], "safety_level": 1, "materials": ["gants", "bottes"]},
    {"slug": "poterie-simple", "title": "Poterie simple", "category": "artisanat", "summary": "Modelage, séchage, petites créations utiles.", "duration_min": 120, "skill_tags": ["creativite", "patience"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier"]},

    # Environnement
    {"slug": "compostage", "title": "Gestion du compostage", "category": "nature", "summary": "Tri, retournement, suivi de l'équilibre.", "duration_min": 60, "skill_tags": ["ecologie", "observation"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["gants", "bottes"]},
    {"slug": "biodiversite", "title": "Observation de la biodiversité", "category": "nature", "summary": "Identifier, noter, protéger faune et flore.", "duration_min": 90, "skill_tags": ["ecologie", "patience"], "seasonality": ["printemps", "ete"], "safety_level": 1, "materials": []},
    {"slug": "sentiers-nature", "title": "Entretien de sentiers nature", "category": "nature", "summary": "Débroussaillage léger, signalétique, sécurisation.", "duration_min": 120, "skill_tags": ["endurance", "securite"], "seasonality": ["printemps", "ete", "automne"], "safety_level": 2, "materials": ["gants", "bottes"]},
    {"slug": "plantations-haies", "title": "Plantations de haies", "category": "nature", "summary": "Creuser, planter, protéger, arroser.", "duration_min": 120, "skill_tags": ["sol", "plantes"], "seasonality": ["automne", "hiver"], "safety_level": 1, "materials": ["gants", "bottes"]},
    {"slug": "ressources-eau", "title": "Gestion des ressources en eau", "category": "nature", "summary": "Récupération, économie, qualité de l'eau.", "duration_min": 90, "skill_tags": ["ecologie", "organisation"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["gants"]},
    {"slug": "dechets-tri", "title": "Tri et valorisation des déchets", "category": "nature", "summary": "Identification, tri, valorisation créative.", "duration_min": 60, "skill_tags": ["ecologie", "organisation"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["gants"]},

    # Animation sociale
    {"slug": "accueil-visiteurs", "title": "Accueil de visiteurs", "category": "social", "summary": "Présentation, visite guidée, échanges.", "duration_min": 90, "skill_tags": ["accueil", "expression"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"slug": "ateliers-enfants", "title": "Animation d'ateliers enfants", "category": "social", "summary": "Expliquer, encadrer, faire participer.", "duration_min": 120, "skill_tags": ["pedagogie", "patience"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"slug": "documentation", "title": "Création de documentation", "category": "social", "summary": "Photos, vidéos, rédaction de fiches.", "duration_min": 90, "skill_tags": ["organisation", "expression"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"slug": "evenements", "title": "Organisation d'événements", "category": "social", "summary": "Planification, logistique, coordination.", "duration_min": 180, "skill_tags": ["organisation", "equipe"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"slug": "communication", "title": "Communication & réseaux", "category": "social", "summary": "Réseaux sociaux, newsletters, relations.", "duration_min": 60, "skill_tags": ["expression", "organisation"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"slug": "marche-local", "title": "Participation à un marché local", "category": "social", "summary": "Stand, présentation, caisse symbolique (simulation).", "duration_min": 180, "skill_tags": ["contact", "compter_simple", "equipe"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
]

def create_database():
    """Créer la base de données et les tables"""
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    return engine

def seed_activities(engine):
    """Insérer les données d'activités en base"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Vérifier si les activités existent déjà
        existing_count = db.query(Activity).count()
        if existing_count > 0:
            print(f"Base déjà initialisée avec {existing_count} activités.")
            return
        
        # Insérer les activités
        for activity_data in ACTIVITIES_DATA:
            activity = Activity(**activity_data)
            db.add(activity)
        
        db.commit()
        print(f"✅ {len(ACTIVITIES_DATA)} activités ajoutées avec succès.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de l'insertion : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Initialisation de la base de données...")
    
    # Créer la base de données
    engine = create_database()
    print("✅ Tables créées.")
    
    # Insérer les données
    seed_activities(engine)
    
    print("🎉 Base de données initialisée !")