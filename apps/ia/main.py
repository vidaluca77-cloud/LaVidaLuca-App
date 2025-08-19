from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users, profiles, activities, recommendations
from config import settings

# Créer l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(profiles.router, prefix="/profiles", tags=["User Profiles"])
app.include_router(activities.router, prefix="/activities", tags=["Activities"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])

@app.get("/")
def read_root():
    """Endpoint racine de l'API"""
    return {
        "message": "Bienvenue sur l'API La Vida Luca",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """Endpoint de santé pour les vérifications de déploiement"""
    return {"status": "healthy", "version": settings.VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)