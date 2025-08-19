from sqlalchemy.orm import Session
from app.models.models import Activity, User
from app.utils.auth import get_password_hash


def create_sample_activities(db: Session):
    """Create sample activities from the 30 activities catalogue."""
    
    activities_data = [
        # Agriculture
        {
            "slug": "nourrir-soigner-moutons",
            "title": "Nourrir et soigner les moutons",
            "category": "agri",
            "summary": "Gestes quotidiens : alimentation, eau, observation.",
            "description": "Apprentissage des soins de base aux moutons : distribution de foin et d'eau, observation du comportement, identification des signes de bonne santé.",
            "duration_min": 60,
            "skill_tags": ["elevage", "responsabilite"],
            "seasonality": ["toutes"],
            "safety_level": 1,
            "materials": ["bottes", "gants"],
            "max_participants": 8,
            "difficulty_level": 1,
            "location": "Calvados (14)"
        },
        {
            "slug": "tonte-entretien-troupeau",
            "title": "Tonte & entretien du troupeau",
            "category": "agri", 
            "summary": "Hygiène, tonte (démo), soins courants.",
            "description": "Découverte de la tonte des moutons, techniques d'hygiène du troupeau, soins préventifs et observation sanitaire.",
            "duration_min": 90,
            "skill_tags": ["elevage", "hygiene"],
            "seasonality": ["printemps"],
            "safety_level": 2,
            "materials": ["bottes", "gants"],
            "max_participants": 6,
            "difficulty_level": 2,
            "location": "Calvados (14)"
        },
        {
            "slug": "soins-basse-cour",
            "title": "Soins basse-cour",
            "category": "agri",
            "summary": "Poules/canards/lapins : alimentation, abris, propreté.",
            "description": "Gestion quotidienne des volailles et lapins : alimentation adaptée, nettoyage des abris, collecte des œufs, observation sanitaire.",
            "duration_min": 60,
            "skill_tags": ["soins_animaux"],
            "seasonality": ["toutes"],
            "safety_level": 1,
            "materials": ["bottes", "gants"],
            "max_participants": 10,
            "difficulty_level": 1,
            "location": "Calvados (14)"
        },
        {
            "slug": "plantation-cultures",
            "title": "Plantation de cultures",
            "category": "agri",
            "summary": "Semis, arrosage, paillage, suivi de plants.",
            "description": "Initiation au maraîchage : préparation du sol, semis en ligne, techniques d'arrosage, paillage naturel et suivi des cultures.",
            "duration_min": 90,
            "skill_tags": ["sol", "plantes"],
            "seasonality": ["printemps", "ete"],
            "safety_level": 1,
            "materials": ["gants"],
            "max_participants": 12,
            "difficulty_level": 1,
            "location": "Calvados (14)"
        },
        {
            "slug": "init-maraichage",
            "title": "Initiation maraîchage",
            "category": "agri",
            "summary": "Plan de culture, entretien, récolte respectueuse.",
            "description": "Approche complète du maraîchage : planification des cultures, techniques d'entretien écologique, récolte au bon stade de maturité.",
            "duration_min": 120,
            "skill_tags": ["sol", "organisation"],
            "seasonality": ["printemps", "ete", "automne"],
            "safety_level": 1,
            "materials": ["gants", "bottes"],
            "max_participants": 8,
            "difficulty_level": 2,
            "location": "Calvados (14)"
        },
        
        # Transformation
        {
            "slug": "fromage",
            "title": "Fabrication de fromage",
            "category": "transfo",
            "summary": "Du lait au caillé : hygiène, moulage, affinage (découverte).",
            "description": "Découverte de la transformation laitière : techniques de caillage, moulage, principes d'affinage et respect des règles d'hygiène.",
            "duration_min": 90,
            "skill_tags": ["hygiene", "precision"],
            "seasonality": ["toutes"],
            "safety_level": 2,
            "materials": ["tablier"],
            "max_participants": 6,
            "difficulty_level": 2,
            "location": "Calvados (14)"
        },
        {
            "slug": "pain-four-bois",
            "title": "Pain au four à bois",
            "category": "transfo",
            "summary": "Pétrissage, façonnage, cuisson : respect des temps.",
            "description": "Art de la boulangerie traditionnelle : préparation de la pâte, techniques de façonnage, gestion du four à bois et timing de cuisson.",
            "duration_min": 120,
            "skill_tags": ["precision", "rythme"],
            "seasonality": ["toutes"],
            "safety_level": 2,
            "materials": ["tablier"],
            "max_participants": 6,
            "difficulty_level": 3,
            "location": "Calvados (14)"
        },
        
        # Artisanat
        {
            "slug": "abris-bois",
            "title": "Construction d'abris",
            "category": "artisanat",
            "summary": "Petites structures bois : plan, coupe, assemblage.",
            "description": "Construction de petites structures en bois : lecture de plans, techniques de coupe, assemblage et finitions.",
            "duration_min": 120,
            "skill_tags": ["bois", "precision", "securite"],
            "seasonality": ["toutes"],
            "safety_level": 2,
            "materials": ["gants"],
            "max_participants": 6,
            "difficulty_level": 3,
            "location": "Calvados (14)"
        },
        {
            "slug": "peinture-deco",
            "title": "Peinture & décoration d'espaces",
            "category": "artisanat",
            "summary": "Préparer, protéger, peindre proprement.",
            "description": "Techniques de peinture et décoration : préparation des surfaces, protection des espaces, application propre et finitions soignées.",
            "duration_min": 90,
            "skill_tags": ["proprete", "finitions"],
            "seasonality": ["toutes"],
            "safety_level": 1,
            "materials": ["tablier", "gants"],
            "max_participants": 8,
            "difficulty_level": 1,
            "location": "Calvados (14)"
        },
        
        # Nature/Environnement
        {
            "slug": "biodiversite-obs",
            "title": "Observation de la biodiversité",
            "category": "nature",
            "summary": "Identifier, comprendre, respecter les écosystèmes.",
            "description": "Découverte de la biodiversité locale : identification des espèces, compréhension des écosystèmes, techniques d'observation respectueuses.",
            "duration_min": 90,
            "skill_tags": ["ecologie", "observation"],
            "seasonality": ["printemps", "ete"],
            "safety_level": 1,
            "materials": [],
            "max_participants": 12,
            "difficulty_level": 1,
            "location": "Calvados (14)"
        },
        {
            "slug": "compostage",
            "title": "Compostage et recyclage organique",
            "category": "nature",
            "summary": "Tri, compost, valorisation des déchets verts.",
            "description": "Techniques de compostage : tri des matières organiques, montage de compost, suivi de décomposition et valorisation des déchets verts.",
            "duration_min": 60,
            "skill_tags": ["ecologie", "organisation"],
            "seasonality": ["toutes"],
            "safety_level": 1,
            "materials": ["gants"],
            "max_participants": 10,
            "difficulty_level": 1,
            "location": "Calvados (14)"
        },
        
        # Social/Animation
        {
            "slug": "visites-guidees",
            "title": "Visites guidées de la ferme",
            "category": "social",
            "summary": "Présenter la ferme, répondre simplement.",
            "description": "Animation de visites : présentation des activités de la ferme, techniques de communication simple, accueil de différents publics.",
            "duration_min": 60,
            "skill_tags": ["expression", "pedagogie"],
            "seasonality": ["toutes"],
            "safety_level": 1,
            "materials": [],
            "max_participants": 4,
            "difficulty_level": 2,
            "location": "Calvados (14)"
        },
        {
            "slug": "ateliers-enfants",
            "title": "Ateliers pour enfants",
            "category": "social",
            "summary": "Jeux, découvertes nature, mini-gestes encadrés.",
            "description": "Animation d'activités pour enfants : jeux nature, découvertes sensorielles, gestes agricoles adaptés à l'âge et encadrement sécurisé.",
            "duration_min": 90,
            "skill_tags": ["patience", "creativite", "securite"],
            "seasonality": ["toutes"],
            "safety_level": 2,
            "materials": [],
            "max_participants": 8,
            "difficulty_level": 2,
            "location": "Calvados (14)"
        },
        {
            "slug": "cuisine-collective",
            "title": "Cuisine collective (équipe)",
            "category": "social",
            "summary": "Préparer un repas simple et bon.",
            "description": "Cuisine en équipe : planification d'un repas, répartition des tâches, techniques culinaires simples et convivialité du partage.",
            "duration_min": 90,
            "skill_tags": ["hygiene", "equipe", "temps"],
            "seasonality": ["toutes"],
            "safety_level": 1,
            "materials": ["tablier"],
            "max_participants": 8,
            "difficulty_level": 1,
            "location": "Calvados (14)"
        },
        {
            "slug": "marche-local",
            "title": "Participation à un marché local",
            "category": "social",
            "summary": "Stand, présentation, caisse symbolique (simulation).",
            "description": "Expérience de vente directe : tenue d'un stand, présentation des produits, relation client et simulation de transactions.",
            "duration_min": 180,
            "skill_tags": ["contact", "compter_simple", "equipe"],
            "seasonality": ["toutes"],
            "safety_level": 1,
            "materials": [],
            "max_participants": 6,
            "difficulty_level": 2,
            "location": "Calvados (14)"
        }
    ]
    
    for activity_data in activities_data:
        activity = Activity(**activity_data)
        db.add(activity)
    
    db.commit()


def create_sample_admin(db: Session):
    """Create a sample admin user."""
    admin_user = User(
        email="admin@lavidaluca.fr",
        username="admin",
        hashed_password=get_password_hash("admin123"),
        first_name="Administrateur",
        last_name="LaVidaLuca",
        is_admin=True,
        bio="Administrateur de la plateforme LaVidaLuca",
        location="Calvados (14)",
        skills=["organisation", "pedagogie", "gestion"],
        preferences=["agri", "social"],
        availability=["semaine", "weekend"]
    )
    
    db.add(admin_user)
    db.commit()


def create_sample_user(db: Session):
    """Create a sample regular user."""
    regular_user = User(
        email="marie.dupont@example.com",
        username="marie_dupont",
        hashed_password=get_password_hash("marie123"),
        first_name="Marie",
        last_name="Dupont",
        is_admin=False,
        bio="Étudiante en MFR, passionnée d'agriculture durable",
        location="Normandie",
        skills=["elevage", "hygiene", "patience"],
        preferences=["agri", "nature"],
        availability=["apres-midi", "weekend"]
    )
    
    db.add(regular_user)
    db.commit()


def init_sample_data(db: Session):
    """Initialize the database with sample data."""
    create_sample_activities(db)
    create_sample_admin(db)
    create_sample_user(db)