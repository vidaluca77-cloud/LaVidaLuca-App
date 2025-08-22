#!/usr/bin/env python3
"""
Seed the database with initial data including the 30 activities from the frontend
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.core.models import Base, Activity
from app.schemas.schemas import ActivityCreate
from app.services.activity_service import ActivityService

# Activities data from the frontend
ACTIVITIES_DATA = [
    # Agriculture
    {"id": "1", "slug": "nourrir-soigner-moutons", "title": "Nourrir et soigner les moutons", "category": "agri", "summary": "Gestes quotidiens : alimentation, eau, observation.", "duration_min": 60, "skill_tags": ["elevage", "responsabilite"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["bottes", "gants"]},
    {"id": "2", "slug": "hygiene-etables", "title": "Hygiène des étables", "category": "agri", "summary": "Nettoyage, désinfection, litière : rigueur et méthode.", "duration_min": 90, "skill_tags": ["hygiene", "rigueur"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["bottes", "gants"]},
    {"id": "3", "slug": "soins-preventifs-animaux", "title": "Soins préventifs aux animaux", "category": "agri", "summary": "Observation, premiers soins, prévention avec vétérinaire.", "duration_min": 120, "skill_tags": ["soins_animaux", "observation"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    {"id": "4", "slug": "plantation-cultures", "title": "Plantation de cultures", "category": "agri", "summary": "Semis, arrosage, paillage, suivi de plants.", "duration_min": 90, "skill_tags": ["sol", "plantes"], "seasonality": ["printemps", "ete"], "safety_level": 1, "materials": ["gants"]},
    {"id": "5", "slug": "init-maraichage", "title": "Initiation maraîchage", "category": "agri", "summary": "Plan de culture, entretien, récolte respectueuse.", "duration_min": 120, "skill_tags": ["sol", "organisation"], "seasonality": ["printemps", "ete", "automne"], "safety_level": 1, "materials": ["gants", "bottes"]},
    {"id": "6", "slug": "clotures-abris", "title": "Gestion des clôtures & abris", "category": "agri", "summary": "Identifier, réparer, sécuriser parcs et abris.", "duration_min": 120, "skill_tags": ["securite", "bois"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},

    # Transformation
    {"id": "7", "slug": "fromage", "title": "Fabrication de fromage", "category": "transfo", "summary": "Du lait au caillé : hygiène, moulage, affinage (découverte).", "duration_min": 90, "skill_tags": ["hygiene", "precision"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["tablier"]},
    {"id": "8", "slug": "conserves-legumes", "title": "Conserves de légumes", "category": "transfo", "summary": "Stérilisation, étiquetage, respect des températures.", "duration_min": 120, "skill_tags": ["hygiene", "precision"], "seasonality": ["ete", "automne"], "safety_level": 2, "materials": ["tablier"]},
    {"id": "9", "slug": "confiture", "title": "Confiture artisanale", "category": "transfo", "summary": "Choix des fruits, cuisson, mise en pot propre.", "duration_min": 90, "skill_tags": ["precision", "gout"], "seasonality": ["ete", "automne"], "safety_level": 1, "materials": ["tablier"]},
    {"id": "10", "slug": "sechage-herbes", "title": "Séchage d'herbes aromatiques", "category": "transfo", "summary": "Cueillette, séchage, conservation des arômes.", "duration_min": 60, "skill_tags": ["reconnaissance", "patience"], "seasonality": ["ete"], "safety_level": 1, "materials": []},
    {"id": "11", "slug": "huile-infusion", "title": "Huiles & infusions", "category": "transfo", "summary": "Macération, filtrage, conditionnement.", "duration_min": 75, "skill_tags": ["precision", "temps"], "seasonality": ["ete"], "safety_level": 1, "materials": ["tablier"]},
    {"id": "12", "slug": "pain-four-bois", "title": "Pain au four à bois", "category": "transfo", "summary": "Pétrissage, façonnage, cuisson : respect des temps.", "duration_min": 120, "skill_tags": ["precision", "rythme"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["tablier"]},

    # Artisanat
    {"id": "13", "slug": "abris-bois", "title": "Construction d'abris", "category": "artisanat", "summary": "Petites structures bois : plan, coupe, assemblage.", "duration_min": 120, "skill_tags": ["bois", "precision", "securite"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    {"id": "14", "slug": "reparation-outils", "title": "Réparation d'outils", "category": "artisanat", "summary": "Diagnostic, nettoyage, remise en état.", "duration_min": 90, "skill_tags": ["mecanique", "dexterite"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    {"id": "15", "slug": "vannerie", "title": "Vannerie simple", "category": "artisanat", "summary": "Tressage de paniers avec matériaux naturels.", "duration_min": 120, "skill_tags": ["creativite", "patience"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"id": "16", "slug": "peinture-deco", "title": "Peinture & décoration d'espaces", "category": "artisanat", "summary": "Préparer, protéger, peindre proprement.", "duration_min": 90, "skill_tags": ["proprete", "finitions"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier", "gants"]},
    {"id": "17", "slug": "amenagement-verts", "title": "Aménagement d'espaces verts", "category": "artisanat", "summary": "Désherbage doux, paillage, plantations.", "duration_min": 90, "skill_tags": ["endurance", "esthetique"], "seasonality": ["printemps", "ete"], "safety_level": 1, "materials": ["gants", "bottes"]},
    {"id": "18", "slug": "cloture-bois", "title": "Clôture bois", "category": "artisanat", "summary": "Pose de piquets, mise à niveau, fixation.", "duration_min": 150, "skill_tags": ["bois", "niveau"], "seasonality": ["printemps", "ete", "automne"], "safety_level": 2, "materials": ["gants"]},

    # Environnement
    {"id": "19", "slug": "plantation-arbres", "title": "Plantation d'arbres", "category": "nature", "summary": "Choix de l'emplacement, trou, tuteurage.", "duration_min": 90, "skill_tags": ["endurance", "prevoyance"], "seasonality": ["automne", "hiver", "printemps"], "safety_level": 1, "materials": ["gants", "bottes"]},
    {"id": "20", "slug": "compostage", "title": "Compostage & valorisation", "category": "nature", "summary": "Tri, montage, retournement, utilisation.", "duration_min": 60, "skill_tags": ["ecologie", "observation"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["gants"]},
    {"id": "21", "slug": "mare-biodiversite", "title": "Mare & biodiversité", "category": "nature", "summary": "Création ou entretien d'un point d'eau naturel.", "duration_min": 120, "skill_tags": ["ecologie", "endurance"], "seasonality": ["printemps", "automne"], "safety_level": 1, "materials": ["bottes"]},
    {"id": "22", "slug": "nichoirs-insectes", "title": "Nichoirs à insectes", "category": "nature", "summary": "Assemblage, installation, observation.", "duration_min": 75, "skill_tags": ["creativite", "ecologie"], "seasonality": ["printemps", "ete"], "safety_level": 1, "materials": []},
    {"id": "23", "slug": "potager-permaculture", "title": "Potager en permaculture", "category": "nature", "summary": "Associations, rotations, équilibres naturels.", "duration_min": 120, "skill_tags": ["ecologie", "observation"], "seasonality": ["printemps", "ete", "automne"], "safety_level": 1, "materials": ["gants"]},
    {"id": "24", "slug": "recuperation-eau", "title": "Récupération d'eau de pluie", "category": "nature", "summary": "Installation simple, filtrage, stockage.", "duration_min": 90, "skill_tags": ["logique", "bricolage"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},

    # Animation sociale
    {"id": "25", "slug": "accueil-visiteurs", "title": "Accueil de visiteurs", "category": "social", "summary": "Présentation, visite guidée, réponse aux questions.", "duration_min": 90, "skill_tags": ["accueil", "expression"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"id": "26", "slug": "atelier-enfants", "title": "Atelier découverte enfants", "category": "social", "summary": "Animation ludique et pédagogique.", "duration_min": 90, "skill_tags": ["pedagogie", "patience"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"id": "27", "slug": "evenement-ferme", "title": "Événement à la ferme", "category": "social", "summary": "Organisation, logistique, animation.", "duration_min": 180, "skill_tags": ["organisation", "equipe"], "seasonality": ["printemps", "ete", "automne"], "safety_level": 1, "materials": []},
    {"id": "28", "slug": "cuisine-collective", "title": "Cuisine collective (équipe)", "category": "social", "summary": "Préparer un repas simple et bon.", "duration_min": 90, "skill_tags": ["hygiene", "equipe", "temps"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier"]},
    {"id": "29", "slug": "gouter-fermier", "title": "Goûter fermier", "category": "social", "summary": "Organisation, service, convivialité, propreté.", "duration_min": 60, "skill_tags": ["rigueur", "relationnel"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier"]},
    {"id": "30", "slug": "marche-local", "title": "Participation à un marché local", "category": "social", "summary": "Stand, présentation, caisse symbolique (simulation).", "duration_min": 180, "skill_tags": ["contact", "compter_simple", "equipe"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
]

def seed_activities():
    """Seed the database with activities"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        activity_service = ActivityService(db)
        
        for activity_data in ACTIVITIES_DATA:
            # Check if activity already exists
            existing = activity_service.get_activity_by_slug(activity_data["slug"])
            if existing:
                print(f"Activity {activity_data['slug']} already exists, skipping...")
                continue
            
            # Create activity
            activity_create = ActivityCreate(
                slug=activity_data["slug"],
                title=activity_data["title"],
                category=activity_data["category"],
                summary=activity_data["summary"],
                duration_min=activity_data["duration_min"],
                safety_level=activity_data["safety_level"],
                skill_tags=activity_data["skill_tags"],
                seasonality=activity_data["seasonality"],
                materials=activity_data["materials"]
            )
            
            try:
                activity = activity_service.create_activity(activity_create)
                print(f"Created activity: {activity.title}")
            except Exception as e:
                print(f"Error creating activity {activity_data['slug']}: {e}")
        
        print("Activities seeding completed!")
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_activities()