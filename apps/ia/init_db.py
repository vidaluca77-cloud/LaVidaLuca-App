#!/usr/bin/env python3
"""
Database initialization script
Populates the database with the 30 activities from the frontend
"""

import asyncio
import json
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.database import Base
from app.models.activity import Activity, ActivityCategory
from app.models.user import User
from app.models.booking import Booking

# Activities data from frontend
ACTIVITIES_DATA = [
    # Agriculture
    {"id": 1, "slug": "nourrir-soigner-moutons", "title": "Nourrir et soigner les moutons", "category": "agri", "summary": "Gestes quotidiens : alimentation, eau, observation.", "duration_min": 60, "skill_tags": ["elevage", "responsabilite"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["bottes", "gants"]},
    {"id": 2, "slug": "tonte-entretien-troupeau", "title": "Tonte & entretien du troupeau", "category": "agri", "summary": "Hygiène, tonte (démo), soins courants.", "duration_min": 90, "skill_tags": ["elevage", "hygiene"], "seasonality": ["printemps"], "safety_level": 2, "materials": ["bottes", "gants"]},
    {"id": 3, "slug": "basse-cour-soins", "title": "Soins basse-cour", "category": "agri", "summary": "Poules/canards/lapins : alimentation, abris, propreté.", "duration_min": 60, "skill_tags": ["soins_animaux"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["bottes", "gants"]},
    {"id": 4, "slug": "plantation-cultures", "title": "Plantation de cultures", "category": "agri", "summary": "Semis, arrosage, paillage, suivi de plants.", "duration_min": 90, "skill_tags": ["sol", "plantes"], "seasonality": ["printemps", "ete"], "safety_level": 1, "materials": ["gants"]},
    {"id": 5, "slug": "init-maraichage", "title": "Initiation maraîchage", "category": "agri", "summary": "Plan de culture, entretien, récolte respectueuse.", "duration_min": 120, "skill_tags": ["sol", "organisation"], "seasonality": ["printemps", "ete", "automne"], "safety_level": 1, "materials": ["gants", "bottes"]},
    {"id": 6, "slug": "clotures-abris", "title": "Gestion des clôtures & abris", "category": "agri", "summary": "Identifier, réparer, sécuriser parcs et abris.", "duration_min": 120, "skill_tags": ["securite", "bois"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    
    # Transformation
    {"id": 7, "slug": "fromage", "title": "Fabrication de fromage", "category": "transfo", "summary": "Du lait au caillé : hygiène, moulage, affinage (découverte).", "duration_min": 90, "skill_tags": ["hygiene", "precision"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["tablier"]},
    {"id": 8, "slug": "conserves", "title": "Confitures & conserves", "category": "transfo", "summary": "Préparation, stérilisation, mise en pot, étiquetage.", "duration_min": 90, "skill_tags": ["organisation", "hygiene"], "seasonality": ["ete", "automne"], "safety_level": 1, "materials": ["tablier"]},
    {"id": 9, "slug": "laine", "title": "Transformation de la laine", "category": "transfo", "summary": "Lavage, cardage, petite création textile.", "duration_min": 90, "skill_tags": ["patience", "creativite"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier", "gants"]},
    {"id": 10, "slug": "jus", "title": "Fabrication de jus", "category": "transfo", "summary": "Du verger à la bouteille : tri, pressage, filtration.", "duration_min": 90, "skill_tags": ["hygiene", "securite"], "seasonality": ["automne"], "safety_level": 2, "materials": ["tablier", "gants"]},
    {"id": 11, "slug": "aromatiques-sechage", "title": "Séchage d'herbes aromatiques", "category": "transfo", "summary": "Cueillette, séchage, conditionnement doux.", "duration_min": 60, "skill_tags": ["douceur", "organisation"], "seasonality": ["ete"], "safety_level": 1, "materials": ["tablier"]},
    {"id": 12, "slug": "pain-four-bois", "title": "Pain au four à bois", "category": "transfo", "summary": "Pétrissage, façonnage, cuisson : respect des temps.", "duration_min": 120, "skill_tags": ["precision", "rythme"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["tablier"]},
    
    # Artisanat
    {"id": 13, "slug": "abris-bois", "title": "Construction d'abris", "category": "artisanat", "summary": "Petites structures bois : plan, coupe, assemblage.", "duration_min": 120, "skill_tags": ["bois", "precision", "securite"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    {"id": 14, "slug": "outils-entretien", "title": "Entretien des outils", "category": "artisanat", "summary": "Affûtage, huilage, petites réparations, rangement.", "duration_min": 60, "skill_tags": ["precision", "soin"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    {"id": 15, "slug": "vannerie-simple", "title": "Vannerie simple", "category": "artisanat", "summary": "Tressage de paniers utilitaires avec matières locales.", "duration_min": 90, "skill_tags": ["patience", "creativite"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"id": 16, "slug": "bricolage-reparation", "title": "Bricolage & réparation", "category": "artisanat", "summary": "Petites réparations, clouage, vissage, collage.", "duration_min": 90, "skill_tags": ["bois", "creativite"], "seasonality": ["toutes"], "safety_level": 2, "materials": ["gants"]},
    {"id": 17, "slug": "ceramique-terre", "title": "Céramique & poterie", "category": "artisanat", "summary": "Modelage, cuisson simple, décoration terre locale.", "duration_min": 120, "skill_tags": ["creativite", "patience"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier"]},
    {"id": 18, "slug": "couture-textile", "title": "Couture & textile", "category": "artisanat", "summary": "Réparations textiles, créations simples et utiles.", "duration_min": 90, "skill_tags": ["precision", "creativite"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    
    # Nature/Environnement
    {"id": 19, "slug": "plantation-arbres", "title": "Plantation d'arbres", "category": "nature", "summary": "Choix des essences, plantation, protection jeunes plants.", "duration_min": 120, "skill_tags": ["ecologie", "endurance"], "seasonality": ["automne", "hiver"], "safety_level": 1, "materials": ["gants", "bottes"]},
    {"id": 20, "slug": "compostage-lombric", "title": "Compostage & lombricompostage", "category": "nature", "summary": "Recyclage organique, entretien, récolte compost.", "duration_min": 60, "skill_tags": ["ecologie", "organisation"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["gants"]},
    {"id": 21, "slug": "biodiversite-observation", "title": "Biodiversité & observation", "category": "nature", "summary": "Reconnaissance espèces, nichoirs, hôtels à insectes.", "duration_min": 90, "skill_tags": ["ecologie", "observation"], "seasonality": ["printemps", "ete"], "safety_level": 1, "materials": []},
    {"id": 22, "slug": "mare-ecosysteme", "title": "Gestion mare & écosystème", "category": "nature", "summary": "Entretien naturel, faune/flore aquatique, équilibre.", "duration_min": 90, "skill_tags": ["ecologie", "observation"], "seasonality": ["printemps", "ete"], "safety_level": 2, "materials": ["bottes"]},
    {"id": 23, "slug": "energie-renouvelable", "title": "Énergies renouvelables", "category": "nature", "summary": "Découverte solaire, éolien, démonstrations pratiques.", "duration_min": 120, "skill_tags": ["ecologie", "technique"], "seasonality": ["toutes"], "safety_level": 2, "materials": []},
    {"id": 24, "slug": "permaculture-init", "title": "Initiation permaculture", "category": "nature", "summary": "Principes de base, design simple, associations cultures.", "duration_min": 120, "skill_tags": ["ecologie", "reflexion"], "seasonality": ["printemps", "ete"], "safety_level": 1, "materials": ["gants"]},
    
    # Social/Animation
    {"id": 25, "slug": "accueil-visiteurs", "title": "Accueil de visiteurs", "category": "social", "summary": "Présentation lieu, explication activités, échange.", "duration_min": 60, "skill_tags": ["accueil", "expression"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"id": 26, "slug": "visite-guidee", "title": "Visite guidée", "category": "social", "summary": "Parcours commenté, partage savoir, pédagogie.", "duration_min": 90, "skill_tags": ["pedagogie", "expression"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"id": 27, "slug": "atelier-enfants", "title": "Atelier enfants", "category": "social", "summary": "Animation ludique, sécurité, patience, créativité.", "duration_min": 90, "skill_tags": ["pedagogie", "patience"], "seasonality": ["toutes"], "safety_level": 1, "materials": []},
    {"id": 28, "slug": "cuisine-collective", "title": "Cuisine collective (équipe)", "category": "social", "summary": "Préparer un repas simple et bon.", "duration_min": 90, "skill_tags": ["hygiene", "equipe"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier"]},
    {"id": 29, "slug": "gouter-fermier", "title": "Goûter fermier", "category": "social", "summary": "Organisation, service, convivialité, propreté.", "duration_min": 60, "skill_tags": ["rigueur", "relationnel"], "seasonality": ["toutes"], "safety_level": 1, "materials": ["tablier"]},
    {"id": 30, "slug": "evenement-participation", "title": "Participation à un événement", "category": "social", "summary": "Aide logistique, accueil, stand, représentation.", "duration_min": 180, "skill_tags": ["equipe", "adaptabilite"], "seasonality": ["toutes"], "safety_level": 1, "materials": []}
]


async def init_database():
    """Initialize database with activities data"""
    
    # Create async engine
    def get_database_url():
        """Get the appropriate database URL with async driver"""
        url = settings.DATABASE_URL
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://")
        elif url.startswith("sqlite://"):
            return url.replace("sqlite://", "sqlite+aiosqlite://")
        return url
    
    engine = create_async_engine(
        get_database_url(),
        echo=True
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Drop existing tables
        await conn.run_sync(Base.metadata.create_all)  # Create new tables
    
    # Create session
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        # Create activities
        for activity_data in ACTIVITIES_DATA:
            # Convert frontend id to match our auto-increment
            activity_dict = activity_data.copy()
            activity_dict.pop('id', None)  # Remove id, let database auto-generate
            
            activity = Activity(**activity_dict)
            session.add(activity)
        
        await session.commit()
        print(f"Created {len(ACTIVITIES_DATA)} activities")
    
    await engine.dispose()
    print("Database initialization completed!")


if __name__ == "__main__":
    asyncio.run(init_database())