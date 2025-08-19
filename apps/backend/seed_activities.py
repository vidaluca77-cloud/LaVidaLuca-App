#!/usr/bin/env python3
"""
Database seeding script for LaVidaLuca activities
This script populates the database with the 30 activities defined in the frontend
"""

import sys
import os
from sqlalchemy.orm import Session

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.database import SessionLocal, create_tables
from app.models.activity import Activity

# The 30 activities from the frontend (src/app/page.tsx)
ACTIVITIES_DATA = [
    # Agriculture
    {"id": "1", "slug": "nourrir-soigner-moutons", "title": "Nourrir et soigner les moutons", "category": "agri", "summary": "Gestes quotidiens : alimentation, eau, observation.", "duration_min": 60, "skill_tags": ["elevage", "responsabilite"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["bottes", "gants"]},
    {"id": "2", "slug": "tonte-entretien-troupeau", "title": "Tonte & entretien du troupeau", "category": "agri", "summary": "Hygiène, tonte (démo), soins courants.", "duration_min": 90, "skill_tags": ["elevage", "hygiene"], "seasonality": ["printemps"], "safety_level": 2, "materials": ["bottes", "gants"]},
    {"id": "3", "slug": "basse-cour-soins", "title": "Soins basse-cour", "category": "agri", "summary": "Poules/canards/lapins : alimentation, abris, propreté.", "duration_min": 60, "skill_tags": ["soins_animaux"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["bottes", "gants"]},
    {"id": "4", "slug": "plantation-cultures", "title": "Plantation de cultures", "category": "agri", "summary": "Semis, arrosage, paillage, suivi de plants.", "duration_min": 90, "skill_tags": ["sol", "plantes"], "seasonality": ["printemps", "ete"], "safety_level": 1, "materials": ["gants"]},
    {"id": "5", "slug": "init-maraichage", "title": "Initiation maraîchage", "category": "agri", "summary": "Plan de culture, entretien, récolte respectueuse.", "duration_min": 120, "skill_tags": ["sol", "organisation"], "seasonality": ["printemps", "ete", "automne"], "safety_level": 1, "materials": ["gants", "bottes"]},
    {"id": "6", "slug": "clotures-abris", "title": "Gestion des clôtures & abris", "category": "agri", "summary": "Identifier, réparer, sécuriser parcs et abris.", "duration_min": 120, "skill_tags": ["securite", "bois"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    
    # Transformation
    {"id": "7", "slug": "fromage", "title": "Fabrication de fromage", "category": "transfo", "summary": "Du lait au caillé : hygiène, moulage, affinage (découverte).", "duration_min": 90, "skill_tags": ["hygiene", "precision"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["tablier"]},
    {"id": "8", "slug": "conserves", "title": "Conserves & bocaux", "category": "transfo", "summary": "Légumes de saison : stérilisation, étiquetage.", "duration_min": 120, "skill_tags": ["precision", "hygiene"], "seasonality": ["ete", "automne"], "safety_level": 2, "materials": ["tablier"]},
    {"id": "9", "slug": "confitures", "title": "Confitures artisanales", "category": "transfo", "summary": "Fruits locaux : cuisson, texture, mise en pot.", "duration_min": 90, "skill_tags": ["creativite", "precision"], "seasonality": ["ete", "automne"], "safety_level": 1, "materials": ["tablier"]},
    {"id": "10", "slug": "plantes-sechees", "title": "Séchage de plantes", "category": "transfo", "summary": "Herbes aromatiques : cueillette, séchage, conservation.", "duration_min": 60, "skill_tags": ["plantes", "patience"], "seasonality": ["ete"], "safety_level": 1, "materials": []},
    {"id": "11", "slug": "huiles-essentielles", "title": "Extraction d'huiles", "category": "transfo", "summary": "Distillation simple d'herbes locales.", "duration_min": 120, "skill_tags": ["precision", "plantes"], "seasonality": ["ete"], "safety_level": 2, "materials": ["gants"]},
    {"id": "12", "slug": "pain-four-bois", "title": "Pain au four à bois", "category": "transfo", "summary": "Pétrissage, façonnage, cuisson : respect des temps.", "duration_min": 120, "skill_tags": ["precision", "rythme"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["tablier"]},
    
    # Artisanat
    {"id": "13", "slug": "abris-bois", "title": "Construction d'abris", "category": "artisanat", "summary": "Petites structures bois : plan, coupe, assemblage.", "duration_min": 120, "skill_tags": ["bois", "precision", "securite"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    {"id": "14", "slug": "reparation-outils", "title": "Réparation d'outils", "category": "artisanat", "summary": "Entretenir, affûter, réparer les outils de la ferme.", "duration_min": 90, "skill_tags": ["bois", "precision"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    {"id": "15", "slug": "vannerie", "title": "Vannerie simple", "category": "artisanat", "summary": "Paniers et objets en osier ou matériaux locaux.", "duration_min": 120, "skill_tags": ["creativite", "patience"], "seasonality": ["automne", "hiver"], "safety_level": 1, "materials": []},
    {"id": "16", "slug": "menuiserie", "title": "Menuiserie de base", "category": "artisanat", "summary": "Nichoirs, jardinières : mesure, découpe, assemblage.", "duration_min": 120, "skill_tags": ["bois", "precision"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    {"id": "17", "slug": "forge", "title": "Initiation forge", "category": "artisanat", "summary": "Découverte du feu et du métal : objets simples.", "duration_min": 90, "skill_tags": ["precision", "securite"], "seasonality": ["toutes"], "safety_level": 3, "materials": ["gants", "lunettes"]},
    {"id": "18", "slug": "ceramique", "title": "Poterie & céramique", "category": "artisanat", "summary": "Modelage de terre locale : bols, pots, déco.", "duration_min": 120, "skill_tags": ["creativite", "patience"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier"]},
    
    # Environnement
    {"id": "19", "slug": "plantation-arbres", "title": "Plantation d'arbres", "category": "nature", "summary": "Haies, vergers : choix d'essences, plantation, protection.", "duration_min": 120, "skill_tags": ["plantes", "ecologie"], "seasonality": ["automne", "hiver"], "safety_level": 1, "materials": ["gants", "bottes"]},
    {"id": "20", "slug": "compostage", "title": "Compostage & vers", "category": "nature", "summary": "Déchets organiques : tas, bacs, lombricomposteur.", "duration_min": 60, "skill_tags": ["ecologie", "organisation"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["gants"]},
    {"id": "21", "slug": "mare-biodiversite", "title": "Création de mare", "category": "nature", "summary": "Point d'eau : creusement, étanchéité, plantation.", "duration_min": 180, "skill_tags": ["ecologie", "endurance"], "seasonality": ["printemps"], "safety_level": 2, "materials": ["bottes", "gants"]},
    {"id": "22", "slug": "hotel-insectes", "title": "Hôtel à insectes", "category": "nature", "summary": "Refuge pour auxiliaires : design, matériaux, installation.", "duration_min": 90, "skill_tags": ["creativite", "ecologie"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"id": "23", "slug": "sentier-nature", "title": "Aménagement sentier", "category": "nature", "summary": "Baliser, nettoyer, sécuriser un parcours nature.", "duration_min": 120, "skill_tags": ["organisation", "endurance"], "seasonality": ["printemps", "ete"], "safety_level": 1, "materials": ["gants"]},
    {"id": "24", "slug": "ruches", "title": "Initiation apiculture", "category": "nature", "summary": "Observation des abeilles : ruche, miel, écosystème.", "duration_min": 60, "skill_tags": ["observation", "ecologie"], "seasonality": ["printemps", "ete"], "safety_level": 2, "materials": ["combinaison"]},
    
    # Animation sociale
    {"id": "25", "slug": "visite-guidee", "title": "Visite guidée", "category": "social", "summary": "Accueillir des groupes : présenter, expliquer, rassurer.", "duration_min": 90, "skill_tags": ["accueil", "pedagogie"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"id": "26", "slug": "atelier-enfants", "title": "Atelier enfants", "category": "social", "summary": "Activité adaptée aux enfants : semis, bricolage...", "duration_min": 60, "skill_tags": ["pedagogie", "patience"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"id": "27", "slug": "marche-local", "title": "Marché local", "category": "social", "summary": "Tenir un stand : présentation, vente, contact.", "duration_min": 180, "skill_tags": ["expression", "equipe"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"id": "28", "slug": "cuisine-collective", "title": "Cuisine collective (équipe)", "category": "social", "summary": "Préparer un repas simple et bon.", "duration_min": 90, "skill_tags": ["hygiene", "equipe", "temps"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier"]},
    {"id": "29", "slug": "gouter-fermier", "title": "Goûter fermier", "category": "social", "summary": "Organisation, service, convivialité, propreté.", "duration_min": 60, "skill_tags": ["rigueur", "relationnel"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier"]},
    {"id": "30", "slug": "fete-locale", "title": "Animation fête locale", "category": "social", "summary": "Participer à l'événement : jeux, démonstrations.", "duration_min": 240, "skill_tags": ["expression", "equipe"], "seasonality": ["ete"], "safety_level": 1, "materials": []},
]

def seed_activities():
    """Populate the database with the 30 activities"""
    print("Creating database tables...")
    create_tables()
    
    db = SessionLocal()
    
    try:
        # Check if activities already exist
        existing_count = db.query(Activity).count()
        if existing_count > 0:
            print(f"Found {existing_count} existing activities. Skipping seed.")
            return
        
        print("Seeding activities...")
        
        for activity_data in ACTIVITIES_DATA:
            # Convert the data to match our model
            db_activity = Activity(
                slug=activity_data["slug"],
                title=activity_data["title"],
                category=activity_data["category"],
                summary=activity_data["summary"],
                duration_min=activity_data["duration_min"],
                skill_tags=activity_data["skill_tags"],
                seasonality=activity_data["seasonality"],
                safety_level=activity_data["safety_level"],
                materials=activity_data["materials"],
                is_active=True,
                is_mfr_only=False,  # Initially all activities are public
                difficulty_level=activity_data["safety_level"],  # Use safety level as difficulty
                learning_objectives=[],
                prerequisites=[]
            )
            
            db.add(db_activity)
        
        db.commit()
        print(f"Successfully seeded {len(ACTIVITIES_DATA)} activities!")
        
    except Exception as e:
        print(f"Error seeding activities: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_activities()