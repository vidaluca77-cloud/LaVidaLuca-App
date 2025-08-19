from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import os
import jwt
from datetime import datetime, timedelta
import uvicorn

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Allowed origins from environment
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app = FastAPI(
    title="La Vida Luca API",
    description="API pour la plateforme La Vida Luca - Formation et agriculture durable",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models
class UserProfile(BaseModel):
    skills: List[str]
    availability: List[str]
    location: str
    preferences: List[str]

class Activity(BaseModel):
    id: str
    slug: str
    title: str
    category: str
    summary: str
    duration_min: int
    skill_tags: List[str]
    seasonality: List[str]
    safety_level: int
    materials: List[str]

class Suggestion(BaseModel):
    activity: Activity
    score: int
    reasons: List[str]

class ContactForm(BaseModel):
    name: str
    email: str
    subject: str
    message: str
    type: Optional[str] = "general"

class Token(BaseModel):
    access_token: str
    token_type: str

# Helper functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Sample activities data (should come from database in production)
SAMPLE_ACTIVITIES = [
    {
        "id": "1",
        "slug": "soins-animaux",
        "title": "Soins aux animaux",
        "category": "agri",
        "summary": "Nourrir, nettoyer, observer l'état des animaux.",
        "duration_min": 60,
        "skill_tags": ["patience", "observation"],
        "seasonality": ["toutes"],
        "safety_level": 1,
        "materials": ["bottes"]
    },
    {
        "id": "2",
        "slug": "recolte-legumes",
        "title": "Récolte de légumes",
        "category": "agri",
        "summary": "Choisir, couper, conditionner les légumes de saison.",
        "duration_min": 90,
        "skill_tags": ["douceur", "tri"],
        "seasonality": ["printemps", "ete", "automne"],
        "safety_level": 1,
        "materials": ["gants", "panier"]
    }
]

# Routes
@app.get("/")
async def root():
    return {
        "message": "API La Vida Luca - Formation et agriculture durable",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/activities", response_model=List[Activity])
async def get_activities():
    """Récupérer toutes les activités disponibles"""
    return [Activity(**activity) for activity in SAMPLE_ACTIVITIES]

@app.post("/activities/suggestions", response_model=List[Suggestion])
async def get_activity_suggestions(profile: UserProfile):
    """Obtenir des suggestions d'activités basées sur le profil utilisateur"""
    suggestions = []
    
    for activity_data in SAMPLE_ACTIVITIES:
        activity = Activity(**activity_data)
        score = 0
        reasons = []
        
        # Calculate matching score
        common_skills = set(activity.skill_tags) & set(profile.skills)
        if common_skills:
            score += len(common_skills) * 15
            reasons.append(f"Compétences correspondantes : {', '.join(common_skills)}")
        
        if activity.category in profile.preferences:
            score += 25
            reasons.append(f"Catégorie préférée : {activity.category}")
        
        if activity.duration_min <= 90:
            score += 10
            reasons.append("Durée adaptée pour débuter")
        
        if activity.safety_level <= 2:
            score += 10
            reasons.append("Activité sans risque particulier")
        
        suggestions.append(Suggestion(
            activity=activity,
            score=score,
            reasons=reasons
        ))
    
    # Sort by score descending
    suggestions.sort(key=lambda x: x.score, reverse=True)
    return suggestions

@app.post("/contact")
async def submit_contact_form(form: ContactForm):
    """Traiter les formulaires de contact"""
    # In production, this would send email or save to database
    print(f"Contact form received from {form.name} ({form.email}): {form.subject}")
    print(f"Message: {form.message}")
    
    return {
        "success": True,
        "message": "Votre message a été reçu. Nous vous répondrons dans les plus brefs délais.",
        "id": f"contact_{datetime.utcnow().timestamp()}"
    }

@app.post("/auth/token", response_model=Token)
async def login_for_access_token(username: str, password: str):
    """Obtenir un token d'accès pour l'authentification"""
    # In production, verify against database
    if username == "demo" and password == "demo":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/protected")
async def protected_route(current_user: dict = Depends(verify_token)):
    """Route protégée nécessitant une authentification"""
    return {"message": f"Bonjour {current_user['sub']}, vous êtes authentifié!"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)