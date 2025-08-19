"""
Seed data for LaVidaLuca database
"""
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.models import Activity, ActivityCategory, SeasonEnum

def seed_activities():
    """Seed the database with the 30 activities from the frontend"""
    db = SessionLocal()
    
    activities_data = [
        # Agriculture
        {
            "id": 1, "slug": "nourrir-soigner-moutons", "title": "Nourrir et soigner les moutons",
            "category": ActivityCategory.AGRI, "summary": "Gestes quotidiens : alimentation, eau, observation.",
            "duration_min": 60, "skill_tags": ["elevage", "responsabilite"], 
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 1, "materials": ["bottes", "gants"]
        },
        {
            "id": 2, "slug": "tonte-entretien-troupeau", "title": "Tonte & entretien du troupeau",
            "category": ActivityCategory.AGRI, "summary": "Hygiène, tonte (démo), soins courants.",
            "duration_min": 90, "skill_tags": ["elevage", "hygiene"],
            "seasonality": [SeasonEnum.PRINTEMPS], "safety_level": 2, "materials": ["bottes", "gants"]
        },
        {
            "id": 3, "slug": "basse-cour-soins", "title": "Soins basse-cour",
            "category": ActivityCategory.AGRI, "summary": "Poules/canards/lapins : alimentation, abris, propreté.",
            "duration_min": 60, "skill_tags": ["soins_animaux"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 1, "materials": ["bottes", "gants"]
        },
        {
            "id": 4, "slug": "plantation-cultures", "title": "Plantation de cultures",
            "category": ActivityCategory.AGRI, "summary": "Semis, arrosage, paillage, suivi de plants.",
            "duration_min": 90, "skill_tags": ["sol", "plantes"],
            "seasonality": [SeasonEnum.PRINTEMPS, SeasonEnum.ETE], "safety_level": 1, "materials": ["gants"]
        },
        {
            "id": 5, "slug": "init-maraichage", "title": "Initiation maraîchage",
            "category": ActivityCategory.AGRI, "summary": "Plan de culture, entretien, récolte respectueuse.",
            "duration_min": 120, "skill_tags": ["sol", "organisation"],
            "seasonality": [SeasonEnum.PRINTEMPS, SeasonEnum.ETE, SeasonEnum.AUTOMNE], 
            "safety_level": 1, "materials": ["gants", "bottes"]
        },
        {
            "id": 6, "slug": "clotures-abris", "title": "Gestion des clôtures & abris",
            "category": ActivityCategory.AGRI, "summary": "Identifier, réparer, sécuriser parcs et abris.",
            "duration_min": 120, "skill_tags": ["securite", "bois"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 2, "materials": ["gants"]
        },

        # Transformation
        {
            "id": 7, "slug": "fromage", "title": "Fabrication de fromage",
            "category": ActivityCategory.TRANSFO, "summary": "Du lait au caillé : hygiène, moulage, affinage (découverte).",
            "duration_min": 90, "skill_tags": ["hygiene", "precision"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 2, "materials": ["tablier"]
        },
        {
            "id": 8, "slug": "conserves", "title": "Confitures & conserves",
            "category": ActivityCategory.TRANSFO, "summary": "Préparation, stérilisation, mise en pot, étiquetage.",
            "duration_min": 90, "skill_tags": ["organisation", "hygiene"],
            "seasonality": [SeasonEnum.ETE, SeasonEnum.AUTOMNE], "safety_level": 1, "materials": ["tablier"]
        },
        {
            "id": 9, "slug": "laine", "title": "Transformation de la laine",
            "category": ActivityCategory.TRANSFO, "summary": "Lavage, cardage, petite création textile.",
            "duration_min": 90, "skill_tags": ["patience", "creativite"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 1, "materials": ["tablier", "gants"]
        },
        {
            "id": 10, "slug": "jus", "title": "Fabrication de jus",
            "category": ActivityCategory.TRANSFO, "summary": "Du verger à la bouteille : tri, pressage, filtration.",
            "duration_min": 90, "skill_tags": ["hygiene", "securite"],
            "seasonality": [SeasonEnum.AUTOMNE], "safety_level": 2, "materials": ["tablier", "gants"]
        },
        {
            "id": 11, "slug": "aromatiques-sechage", "title": "Séchage d'herbes aromatiques",
            "category": ActivityCategory.TRANSFO, "summary": "Cueillette, séchage, conditionnement doux.",
            "duration_min": 60, "skill_tags": ["douceur", "organisation"],
            "seasonality": [SeasonEnum.ETE], "safety_level": 1, "materials": ["tablier"]
        },
        {
            "id": 12, "slug": "pain-four-bois", "title": "Pain au four à bois",
            "category": ActivityCategory.TRANSFO, "summary": "Pétrissage, façonnage, cuisson : respect des temps.",
            "duration_min": 120, "skill_tags": ["precision", "rythme"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 2, "materials": ["tablier"]
        },

        # Artisanat
        {
            "id": 13, "slug": "construction-simple", "title": "Construction simple",
            "category": ActivityCategory.ARTISANAT, "summary": "Assemblage, vissage, mesures : réaliser un petit ouvrage.",
            "duration_min": 120, "skill_tags": ["precision", "bois"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 2, "materials": ["gants", "lunettes"]
        },
        {
            "id": 14, "slug": "reparation-outils", "title": "Réparation & entretien des outils",
            "category": ActivityCategory.ARTISANAT, "summary": "Affûtage, graissage, petites réparations.",
            "duration_min": 60, "skill_tags": ["autonomie", "responsabilite"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 1, "materials": ["gants"]
        },
        {
            "id": 15, "slug": "menuiserie-simple", "title": "Menuiserie simple",
            "category": ActivityCategory.ARTISANAT, "summary": "Mesure, coupe, ponçage, finitions d'un objet.",
            "duration_min": 120, "skill_tags": ["precision", "creativite"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 2, "materials": ["gants", "lunettes"]
        },
        {
            "id": 16, "slug": "vannerie", "title": "Vannerie",
            "category": ActivityCategory.ARTISANAT, "summary": "Tressage d'osier : panier, corbeille, objet décoratif.",
            "duration_min": 90, "skill_tags": ["patience", "creativite"],
            "seasonality": [SeasonEnum.AUTOMNE, SeasonEnum.HIVER], "safety_level": 1, "materials": []
        },
        {
            "id": 17, "slug": "couture", "title": "Couture & retouches",
            "category": ActivityCategory.ARTISANAT, "summary": "Réparer, adapter, créer de petits objets textiles.",
            "duration_min": 90, "skill_tags": ["precision", "creativite"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 1, "materials": []
        },
        {
            "id": 18, "slug": "poterie", "title": "Poterie artisanale",
            "category": ActivityCategory.ARTISANAT, "summary": "Modelage terre : bol, vase, objets utilitaires simples.",
            "duration_min": 120, "skill_tags": ["creativite", "patience"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 1, "materials": ["tablier"]
        },

        # Nature/Environnement
        {
            "id": 19, "slug": "plantation-arbres", "title": "Plantation d'arbres",
            "category": ActivityCategory.NATURE, "summary": "Choix emplacement, creusage, mise en terre, arrosage.",
            "duration_min": 90, "skill_tags": ["ecologie", "endurance"],
            "seasonality": [SeasonEnum.AUTOMNE, SeasonEnum.PRINTEMPS], "safety_level": 1, "materials": ["gants", "bottes"]
        },
        {
            "id": 20, "slug": "compostage", "title": "Compostage & recyclage",
            "category": ActivityCategory.NATURE, "summary": "Tri, mélange, surveillance du compost collectif.",
            "duration_min": 60, "skill_tags": ["ecologie", "organisation"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 1, "materials": ["gants"]
        },
        {
            "id": 21, "slug": "observation-nature", "title": "Observation de la nature",
            "category": ActivityCategory.NATURE, "summary": "Reconnaissance faune/flore, carnet de bord, respect.",
            "duration_min": 90, "skill_tags": ["curiosite", "respect"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 1, "materials": []
        },
        {
            "id": 22, "slug": "entretien-espaces-verts", "title": "Entretien des espaces verts",
            "category": ActivityCategory.NATURE, "summary": "Taille, désherbage doux, embellissement.",
            "duration_min": 120, "skill_tags": ["organisation", "endurance"],
            "seasonality": [SeasonEnum.PRINTEMPS, SeasonEnum.ETE, SeasonEnum.AUTOMNE],
            "safety_level": 1, "materials": ["gants", "bottes"]
        },
        {
            "id": 23, "slug": "ruche-observation", "title": "Observation de la ruche",
            "category": ActivityCategory.NATURE, "summary": "Découverte apiculture : observer, comprendre (encadré).",
            "duration_min": 60, "skill_tags": ["respect", "curiosite"],
            "seasonality": [SeasonEnum.PRINTEMPS, SeasonEnum.ETE], "safety_level": 2, "materials": ["combinaison"]
        },
        {
            "id": 24, "slug": "gestion-dechets", "title": "Gestion éco-responsable des déchets",
            "category": ActivityCategory.NATURE, "summary": "Tri, valorisation, sensibilisation environnementale.",
            "duration_min": 60, "skill_tags": ["ecologie", "responsabilite"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 1, "materials": ["gants"]
        },

        # Social/Animation
        {
            "id": 25, "slug": "accueil-visiteurs", "title": "Accueil des visiteurs",
            "category": ActivityCategory.SOCIAL, "summary": "Présentation lieu, écoute, orientation simple.",
            "duration_min": 60, "skill_tags": ["accueil", "expression"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 1, "materials": []
        },
        {
            "id": 26, "slug": "visites-guidees", "title": "Visites guidées de la ferme",
            "category": ActivityCategory.SOCIAL, "summary": "Présenter la ferme, répondre simplement.",
            "duration_min": 60, "skill_tags": ["expression", "pedagogie"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 1, "materials": []
        },
        {
            "id": 27, "slug": "ateliers-enfants", "title": "Ateliers pour enfants",
            "category": ActivityCategory.SOCIAL, "summary": "Jeux, découvertes nature, mini-gestes encadrés.",
            "duration_min": 90, "skill_tags": ["patience", "creativite", "securite"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 2, "materials": []
        },
        {
            "id": 28, "slug": "communication-reseaux", "title": "Communication & réseaux",
            "category": ActivityCategory.SOCIAL, "summary": "Photos, témoignages, petites vidéos valorisantes.",
            "duration_min": 90, "skill_tags": ["expression", "creativite"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 1, "materials": []
        },
        {
            "id": 29, "slug": "organisation-evenements", "title": "Organisation d'événements",
            "category": ActivityCategory.SOCIAL, "summary": "Préparation, logistique, accueil lors de manifestations.",
            "duration_min": 180, "skill_tags": ["organisation", "equipe"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 1, "materials": []
        },
        {
            "id": 30, "slug": "marche-local", "title": "Participation à un marché local",
            "category": ActivityCategory.SOCIAL, "summary": "Stand, présentation, caisse symbolique (simulation).",
            "duration_min": 180, "skill_tags": ["contact", "compter_simple", "equipe"],
            "seasonality": [SeasonEnum.TOUTES], "safety_level": 1, "materials": []
        }
    ]
    
    try:
        # Check if activities already exist
        existing_count = db.query(Activity).count()
        if existing_count > 0:
            print(f"Activities already exist ({existing_count}). Skipping seed.")
            return
        
        # Create activities
        for activity_data in activities_data:
            activity = Activity(**activity_data)
            db.add(activity)
        
        db.commit()
        print(f"Successfully seeded {len(activities_data)} activities!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding activities: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_activities()