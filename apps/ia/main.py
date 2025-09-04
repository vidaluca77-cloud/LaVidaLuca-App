"""
Main FastAPI application for LaVidaLuca App
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.api import api_router

app = FastAPI(
    title="LaVidaLuca API",
    description="API pour l'application La Vida Luca - Formation des jeunes en MFR",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "message": "LaVidaLuca API is running",
            "version": "1.0.0",
            "status": "healthy"
        }
    )

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "lavidaluca-api",
            "version": "1.0.0"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )