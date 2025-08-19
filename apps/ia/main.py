from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from typing import Optional, List
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from supabase import create_client, Client
import logging

# Configuration
class Settings(BaseSettings):
    supabase_url: str = ""
    supabase_service_key: str = ""
    jwt_secret: str = "your-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    allowed_origins: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Initialize FastAPI
app = FastAPI(
    title="La Vida Luca API",
    description="API pour l'application La Vida Luca - Formation agricole et insertion sociale",
    version="1.0.0"
)

# CORS configuration
origins = settings.allowed_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Supabase client
supabase: Client = create_client(settings.supabase_url, settings.supabase_service_key)

# Security
security = HTTPBearer()

# Pydantic models
class UserProfile(BaseModel):
    id: Optional[str] = None
    email: str
    full_name: str
    role: str = "user"  # user, mfr_student, educator, admin
    skills: List[str] = []
    availability: List[str] = []
    location: str = ""
    preferences: List[str] = []
    created_at: Optional[datetime] = None

class ActivityBase(BaseModel):
    title: str
    description: str
    category: str  # agri, transfo, artisanat, nature, social
    duration_min: int
    skill_tags: List[str] = []
    seasonality: List[str] = []
    safety_level: int = Field(ge=1, le=3)
    materials: List[str] = []

class Activity(ActivityBase):
    id: str
    slug: str
    created_at: Optional[datetime] = None

class ContactMessage(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    message: str
    type: str = "general"  # general, rejoindre, support

# Authentication functions
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide"
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )

async def get_current_user(user_id: str = Depends(verify_token)) -> UserProfile:
    try:
        result = supabase.table("users").select("*").eq("id", user_id).execute()
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        return UserProfile(**result.data[0])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération de l'utilisateur"
        )

# Routes
@app.get("/")
async def root():
    return {
        "message": "API La Vida Luca",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Activities routes
@app.get("/api/activities", response_model=List[Activity])
async def get_activities():
    try:
        result = supabase.table("activities").select("*").execute()
        return [Activity(**activity) for activity in result.data]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des activités"
        )

@app.get("/api/activities/{activity_id}", response_model=Activity)
async def get_activity(activity_id: str):
    try:
        result = supabase.table("activities").select("*").eq("id", activity_id).execute()
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activité non trouvée"
            )
        return Activity(**result.data[0])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération de l'activité"
        )

# Protected routes (require authentication)
@app.get("/api/profile", response_model=UserProfile)
async def get_profile(current_user: UserProfile = Depends(get_current_user)):
    return current_user

@app.put("/api/profile", response_model=UserProfile)
async def update_profile(
    profile_update: UserProfile,
    current_user: UserProfile = Depends(get_current_user)
):
    try:
        result = supabase.table("users").update(
            profile_update.dict(exclude={"id", "created_at"})
        ).eq("id", current_user.id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        return UserProfile(**result.data[0])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la mise à jour du profil"
        )

# Contact route
@app.post("/api/contact")
async def send_contact_message(message: ContactMessage):
    try:
        # Store in database
        result = supabase.table("contact_messages").insert(
            message.dict()
        ).execute()
        
        # TODO: Send email notification
        
        return {"message": "Message envoyé avec succès", "id": result.data[0]["id"]}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de l'envoi du message"
        )

# Admin routes
@app.get("/api/admin/users", response_model=List[UserProfile])
async def get_all_users(current_user: UserProfile = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès administrateur requis"
        )
    
    try:
        result = supabase.table("users").select("*").execute()
        return [UserProfile(**user) for user in result.data]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des utilisateurs"
        )

@app.post("/api/admin/activities", response_model=Activity)
async def create_activity(
    activity: ActivityBase,
    current_user: UserProfile = Depends(get_current_user)
):
    if current_user.role not in ["admin", "educator"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès éducateur ou administrateur requis"
        )
    
    try:
        # Generate slug from title
        slug = activity.title.lower().replace(" ", "-").replace("'", "")
        
        activity_data = activity.dict()
        activity_data["slug"] = slug
        activity_data["created_at"] = datetime.utcnow().isoformat()
        
        result = supabase.table("activities").insert(activity_data).execute()
        
        return Activity(**result.data[0])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la création de l'activité"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)