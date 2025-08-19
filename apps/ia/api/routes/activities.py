"""
Routes API pour la gestion des activités
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Modèles Pydantic pour les activités
class ActivityBase(BaseModel):
    title: str = Field(..., description="Titre de l'activité")
    category: str = Field(..., description="Catégorie: agri, transfo, artisanat, nature, social")
    summary: str = Field(..., description="Résumé de l'activité")
    duration_min: int = Field(..., description="Durée en minutes", ge=30, le=480)
    skill_tags: List[str] = Field(..., description="Compétences requises")
    seasonality: List[str] = Field(..., description="Saisonnalité: printemps, ete, automne, hiver, toutes")
    safety_level: int = Field(..., description="Niveau de sécurité (1-3)", ge=1, le=3)
    materials: List[str] = Field(default=[], description="Matériel nécessaire")

class Activity(ActivityBase):
    id: str = Field(..., description="Identifiant unique")
    slug: str = Field(..., description="Slug pour URL")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "slug": "nourrir-soigner-moutons",
                "title": "Nourrir et soigner les moutons",
                "category": "agri",
                "summary": "Gestes quotidiens : alimentation, eau, observation.",
                "duration_min": 60,
                "skill_tags": ["elevage", "responsabilite"],
                "seasonality": ["toutes"],
                "safety_level": 1,
                "materials": ["bottes", "gants"]
            }
        }

class ActivityCreate(ActivityBase):
    slug: Optional[str] = Field(None, description="Slug automatique si non fourni")

class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    summary: Optional[str] = None
    duration_min: Optional[int] = None
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[List[str]] = None
    safety_level: Optional[int] = None
    materials: Optional[List[str]] = None

class ActivitySuggestion(BaseModel):
    activity: Activity
    score: int = Field(..., description="Score de correspondance (0-100)")
    reasons: List[str] = Field(..., description="Raisons de la suggestion")

class UserProfile(BaseModel):
    skills: List[str] = Field(..., description="Compétences de l'utilisateur")
    availability: List[str] = Field(..., description="Disponibilités")
    location: str = Field(..., description="Localisation")
    preferences: List[str] = Field(..., description="Préférences de catégories")

# Données d'exemple (en production, ces données viendraient de la base de données)
ACTIVITIES_DB = [
    {
        "id": "1", "slug": "nourrir-soigner-moutons", "title": "Nourrir et soigner les moutons", 
        "category": "agri", "summary": "Gestes quotidiens : alimentation, eau, observation.", 
        "duration_min": 60, "skill_tags": ["elevage", "responsabilite"], 
        "seasonality": ["toutes"], "safety_level": 1, "materials": ["bottes", "gants"],
        "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()
    },
    {
        "id": "2", "slug": "recolte-legumes", "title": "Récolte des légumes de saison", 
        "category": "agri", "summary": "Cueillette respectueuse et tri des légumes.", 
        "duration_min": 90, "skill_tags": ["delicatesse", "tri"], 
        "seasonality": ["printemps", "ete", "automne"], "safety_level": 1, "materials": ["paniers", "gants"],
        "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()
    },
    {
        "id": "3", "slug": "fromage", "title": "Fabrication de fromage", 
        "category": "transfo", "summary": "Du lait au caillé : hygiène, moulage, affinage.", 
        "duration_min": 90, "skill_tags": ["hygiene", "precision"], 
        "seasonality": ["toutes"], "safety_level": 2, "materials": ["tablier"],
        "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()
    },
    {
        "id": "4", "slug": "jardin-aromatiques", "title": "Entretien du jardin d'aromatiques", 
        "category": "nature", "summary": "Semis, entretien et récolte des plantes aromatiques.", 
        "duration_min": 75, "skill_tags": ["plantes", "patience"], 
        "seasonality": ["printemps", "ete"], "safety_level": 1, "materials": ["gants", "sécateur"],
        "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()
    },
    {
        "id": "5", "slug": "portes-ouvertes", "title": "Journée portes ouvertes", 
        "category": "social", "summary": "Préparer, accueillir, guider un public.", 
        "duration_min": 180, "skill_tags": ["accueil", "organisation"], 
        "seasonality": ["toutes"], "safety_level": 1, "materials": [],
        "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()
    }
]

def generate_slug(title: str) -> str:
    """Génère un slug à partir du titre"""
    import re
    slug = title.lower()
    slug = re.sub(r'[àáâãäå]', 'a', slug)
    slug = re.sub(r'[èéêë]', 'e', slug)
    slug = re.sub(r'[ìíîï]', 'i', slug)
    slug = re.sub(r'[òóôõö]', 'o', slug)
    slug = re.sub(r'[ùúûü]', 'u', slug)
    slug = re.sub(r'[ç]', 'c', slug)
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')

@router.get("/", response_model=List[Activity])
async def get_activities(
    category: Optional[str] = Query(None, description="Filtrer par catégorie"),
    skill: Optional[str] = Query(None, description="Filtrer par compétence"),
    season: Optional[str] = Query(None, description="Filtrer par saison"),
    safety_level: Optional[int] = Query(None, description="Niveau de sécurité maximum", ge=1, le=3),
    limit: int = Query(50, description="Nombre maximum d'activités", le=100)
):
    """Récupère la liste des activités avec filtres optionnels"""
    
    activities = [Activity(**activity) for activity in ACTIVITIES_DB]
    
    # Appliquer les filtres
    if category:
        activities = [a for a in activities if a.category == category]
    
    if skill:
        activities = [a for a in activities if skill in a.skill_tags]
    
    if season:
        activities = [a for a in activities if season in a.seasonality or "toutes" in a.seasonality]
    
    if safety_level:
        activities = [a for a in activities if a.safety_level <= safety_level]
    
    # Limiter les résultats
    activities = activities[:limit]
    
    logger.info(f"Retour de {len(activities)} activités (filtres: category={category}, skill={skill}, season={season})")
    return activities

@router.get("/{activity_id}", response_model=Activity)
async def get_activity(activity_id: str):
    """Récupère une activité spécifique par son ID"""
    
    activity_data = next((a for a in ACTIVITIES_DB if a["id"] == activity_id), None)
    if not activity_data:
        raise HTTPException(status_code=404, detail="Activité non trouvée")
    
    return Activity(**activity_data)

@router.get("/slug/{slug}", response_model=Activity)
async def get_activity_by_slug(slug: str):
    """Récupère une activité par son slug"""
    
    activity_data = next((a for a in ACTIVITIES_DB if a["slug"] == slug), None)
    if not activity_data:
        raise HTTPException(status_code=404, detail="Activité non trouvée")
    
    return Activity(**activity_data)

@router.post("/", response_model=Activity, status_code=201)
async def create_activity(activity: ActivityCreate):
    """Crée une nouvelle activité"""
    
    # Générer un ID et un slug
    new_id = str(len(ACTIVITIES_DB) + 1)
    slug = activity.slug or generate_slug(activity.title)
    
    # Vérifier que le slug n'existe pas déjà
    if any(a["slug"] == slug for a in ACTIVITIES_DB):
        raise HTTPException(status_code=400, detail="Une activité avec ce slug existe déjà")
    
    # Créer l'activité
    now = datetime.utcnow()
    new_activity_data = {
        "id": new_id,
        "slug": slug,
        "created_at": now,
        "updated_at": now,
        **activity.dict(exclude={"slug"})
    }
    
    ACTIVITIES_DB.append(new_activity_data)
    
    logger.info(f"Nouvelle activité créée: {new_activity_data['title']} (ID: {new_id})")
    return Activity(**new_activity_data)

@router.put("/{activity_id}", response_model=Activity)
async def update_activity(activity_id: str, activity_update: ActivityUpdate):
    """Met à jour une activité existante"""
    
    activity_data = next((a for a in ACTIVITIES_DB if a["id"] == activity_id), None)
    if not activity_data:
        raise HTTPException(status_code=404, detail="Activité non trouvée")
    
    # Mettre à jour les champs fournis
    update_data = activity_update.dict(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            activity_data[field] = value
        activity_data["updated_at"] = datetime.utcnow()
    
    logger.info(f"Activité mise à jour: {activity_id}")
    return Activity(**activity_data)

@router.delete("/{activity_id}")
async def delete_activity(activity_id: str):
    """Supprime une activité"""
    
    activity_index = next((i for i, a in enumerate(ACTIVITIES_DB) if a["id"] == activity_id), None)
    if activity_index is None:
        raise HTTPException(status_code=404, detail="Activité non trouvée")
    
    deleted_activity = ACTIVITIES_DB.pop(activity_index)
    logger.info(f"Activité supprimée: {deleted_activity['title']} (ID: {activity_id})")
    
    return {"message": "Activité supprimée avec succès"}

@router.post("/suggest", response_model=List[ActivitySuggestion])
async def suggest_activities(profile: UserProfile, limit: int = Query(5, le=20)):
    """Suggère des activités basées sur le profil utilisateur (IA simplifiée)"""
    
    suggestions = []
    
    for activity_data in ACTIVITIES_DB:
        activity = Activity(**activity_data)
        score = 0
        reasons = []
        
        # Compétences communes
        common_skills = [skill for skill in activity.skill_tags if skill in profile.skills]
        if common_skills:
            score += len(common_skills) * 15
            reasons.append(f"Compétences correspondantes : {', '.join(common_skills)}")
        
        # Préférences de catégories
        if activity.category in profile.preferences:
            score += 25
            category_names = {
                'agri': 'Agriculture',
                'transfo': 'Transformation', 
                'artisanat': 'Artisanat',
                'nature': 'Environnement',
                'social': 'Animation'
            }
            reasons.append(f"Catégorie préférée : {category_names.get(activity.category, activity.category)}")
        
        # Durée adaptée
        if activity.duration_min <= 90:
            score += 10
            reasons.append('Durée adaptée pour débuter')
        
        # Sécurité
        if activity.safety_level <= 2:
            score += 10
            if activity.safety_level == 1:
                reasons.append('Activité sans risque particulier')
        
        # Disponibilité (simulation)
        if any(avail in profile.availability for avail in ['weekend', 'semaine']):
            score += 15
            reasons.append('Compatible avec vos disponibilités')
        
        if score > 0:
            suggestions.append(ActivitySuggestion(
                activity=activity,
                score=score,
                reasons=reasons
            ))
    
    # Trier par score décroissant et limiter
    suggestions.sort(key=lambda x: x.score, reverse=True)
    suggestions = suggestions[:limit]
    
    logger.info(f"Suggestions générées pour profil: {len(suggestions)} activités")
    return suggestions

@router.get("/categories/", response_model=List[dict])
async def get_categories():
    """Récupère la liste des catégories d'activités"""
    
    categories = [
        {"id": "agri", "name": "Agriculture", "description": "Élevage, cultures, soins aux animaux"},
        {"id": "transfo", "name": "Transformation", "description": "Transformation des produits de la ferme"},
        {"id": "artisanat", "name": "Artisanat", "description": "Travaux manuels et créatifs"},
        {"id": "nature", "name": "Environnement", "description": "Protection et observation de la nature"},
        {"id": "social", "name": "Animation", "description": "Accueil et animation du public"}
    ]
    
    return categories

@router.get("/skills/", response_model=List[str])
async def get_skills():
    """Récupère la liste des compétences disponibles"""
    
    all_skills = set()
    for activity in ACTIVITIES_DB:
        all_skills.update(activity["skill_tags"])
    
    return sorted(list(all_skills))