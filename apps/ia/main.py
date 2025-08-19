"""
API IA pour La Vida Luca
API FastAPI pour le matching d'activités et l'assistance pédagogique
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = FastAPI(
    title="La Vida Luca IA API",
    description="API d'intelligence artificielle pour le matching d'activités pédagogiques",
    version="1.0.0"
)

# Configuration CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Modèles Pydantic
class UserProfile(BaseModel):
    skills: List[str]
    availability: List[str]
    location: str
    preferences: List[str]
    age: Optional[int] = None
    experience_level: Optional[str] = "debutant"

class ActivitySuggestion(BaseModel):
    activity_id: str
    title: str
    category: str
    score: float
    reasons: List[str]
    duration_min: int
    safety_level: int

class IAResponse(BaseModel):
    suggestions: List[ActivitySuggestion]
    confidence: float
    explanation: str

# Routes API

@app.get("/health")
def health_check():
    """Vérification de santé pour Render"""
    return {
        "status": "healthy",
        "service": "La Vida Luca IA API",
        "version": "1.0.0"
    }

@app.get("/")
def root():
    """Page d'accueil de l'API"""
    return {
        "message": "Bienvenue sur l'API IA de La Vida Luca",
        "documentation": "/docs",
        "health": "/health"
    }

@app.post("/api/suggestions", response_model=IAResponse)
def get_activity_suggestions(profile: UserProfile):
    """
    Générer des suggestions d'activités basées sur le profil utilisateur
    
    Cette route analyse le profil de l'utilisateur et retourne des activités
    recommandées avec des scores de correspondance.
    """
    try:
        # Simulation d'un algorithme de matching IA
        # Dans une implémentation réelle, ceci interagirait avec un modèle ML
        suggestions = calculate_matching(profile)
        
        return IAResponse(
            suggestions=suggestions,
            confidence=0.85,
            explanation="Suggestions basées sur vos compétences et préférences"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de suggestions: {str(e)}")

@app.post("/api/chat")
def chat_assistant(message: str, context: Optional[dict] = None):
    """
    Assistant conversationnel pour l'aide pédagogique
    
    Fournit des réponses aux questions sur les activités,
    la sécurité et les bonnes pratiques.
    """
    try:
        # Simulation d'un assistant IA
        response = generate_ai_response(message, context)
        
        return {
            "response": response,
            "type": "assistant",
            "confidence": 0.9
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de l'assistant: {str(e)}")

# Fonctions utilitaires (simulation d'IA)

def calculate_matching(profile: UserProfile) -> List[ActivitySuggestion]:
    """
    Algorithme simplifié de matching d'activités
    
    Dans une implémentation réelle, ceci utiliserait :
    - Un modèle de machine learning entraîné
    - Une base vectorielle pour la recherche sémantique
    - Des algorithmes de recommandation collaborative
    """
    
    # Activités d'exemple (en réalité, récupérées depuis Supabase)
    sample_activities = [
        {
            "id": "basse-cour-soins",
            "title": "Soins basse-cour", 
            "category": "agri",
            "skill_tags": ["soins_animaux"],
            "duration_min": 60,
            "safety_level": 1
        },
        {
            "id": "jardinage-legumes",
            "title": "Cultures de légumes",
            "category": "agri", 
            "skill_tags": ["jardinage", "patience"],
            "duration_min": 150,
            "safety_level": 1
        },
        {
            "id": "poterie",
            "title": "Poterie & céramique",
            "category": "artisanat",
            "skill_tags": ["creativite", "patience"], 
            "duration_min": 120,
            "safety_level": 2
        }
    ]
    
    suggestions = []
    
    for activity in sample_activities:
        score = 0.0
        reasons = []
        
        # Compétences correspondantes
        common_skills = set(activity["skill_tags"]) & set(profile.skills)
        if common_skills:
            score += len(common_skills) * 0.3
            reasons.append(f"Compétences: {', '.join(common_skills)}")
        
        # Préférences de catégorie
        if activity["category"] in profile.preferences:
            score += 0.4
            reasons.append(f"Catégorie préférée: {activity['category']}")
        
        # Adaptation débutant
        if activity["safety_level"] <= 2:
            score += 0.2
            reasons.append("Adapté aux débutants")
        
        # Durée raisonnable
        if activity["duration_min"] <= 120:
            score += 0.1
            reasons.append("Durée appropriée")
        
        if score > 0:
            suggestions.append(ActivitySuggestion(
                activity_id=activity["id"],
                title=activity["title"],
                category=activity["category"],
                score=score,
                reasons=reasons,
                duration_min=activity["duration_min"],
                safety_level=activity["safety_level"]
            ))
    
    # Trier par score décroissant
    suggestions.sort(key=lambda x: x.score, reverse=True)
    
    return suggestions[:5]  # Top 5 suggestions

def generate_ai_response(message: str, context: Optional[dict] = None) -> str:
    """
    Génération de réponse d'assistant IA (simulation)
    
    Dans une implémentation réelle :
    - Utilisation d'un modèle de langage (OpenAI, Claude, etc.)
    - RAG avec la documentation des activités
    - Personnalisation selon le contexte utilisateur
    """
    
    # Réponses préprogrammées pour la démo
    responses = {
        "sécurité": "La sécurité est primordiale dans toutes nos activités. Chaque activité a un niveau de sécurité défini et des équipements de protection requis.",
        "activités": "Nous proposons 30 activités réparties en 5 catégories : agriculture, transformation, artisanat, nature et social.",
        "inscription": "Pour vous inscrire à une activité, consultez le catalogue et contactez l'éducateur responsable de la session.",
        "matériel": "Le matériel nécessaire est fourni pour chaque activité. Vous n'avez qu'à apporter les équipements de protection mentionnés."
    }
    
    message_lower = message.lower()
    
    for keyword, response in responses.items():
        if keyword in message_lower:
            return response
    
    return "Je suis là pour vous aider avec vos questions sur les activités de La Vida Luca. Pouvez-vous être plus spécifique ?"

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)