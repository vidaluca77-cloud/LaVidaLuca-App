from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn

from config import settings
from models import Base
from database import engine, get_db

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Backend API for LaVidaLuca - Educational farm activities platform",
    version=settings.version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.version}

# Import and include routers
from routes import auth, activities, users, locations

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(activities.router, prefix="/activities", tags=["activities"])
app.include_router(locations.router, prefix="/locations", tags=["locations"])

# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return HTTPException(status_code=404, detail="Resource not found")

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )