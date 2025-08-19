from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, users, activities

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(activities.router, prefix="/api/v1/activities", tags=["Activities"])


@app.get("/")
async def root():
    """
    Point d'entrée de l'API LaVidaLuca
    """
    return {
        "message": "Bienvenue sur l'API LaVidaLuca",
        "version": settings.VERSION,
        "docs": "/api/v1/docs"
    }


@app.get("/health")
async def health_check():
    """
    Vérification de l'état de l'API
    """
    return {"status": "healthy", "service": "LaVidaLuca Backend API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)