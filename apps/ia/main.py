from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.routers import auth, activities, registrations, ai

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="API for La Vida Luca platform - Formation des jeunes en MFR, développement d'une agriculture nouvelle et insertion sociale.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.api_v1_str)
app.include_router(activities.router, prefix=settings.api_v1_str)
app.include_router(registrations.router, prefix=settings.api_v1_str)
app.include_router(ai.router, prefix=settings.api_v1_str)

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to La Vida Luca API",
        "version": "1.0.0",
        "docs": "/docs",
        "description": "API for La Vida Luca platform - Formation des jeunes en MFR"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "la-vida-luca-api"}

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )