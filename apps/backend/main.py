from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os
from dotenv import load_dotenv

from src.api import activities, auth, users
from src.db.database import engine, Base

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="LaVidaLuca API",
    description="API for LaVidaLuca - Agricultural training platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Configure CORS
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(activities.router, prefix="/api/activities", tags=["Activities"])

@app.get("/")
async def root():
    return {"message": "LaVidaLuca API - Agricultural training platform"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "lavidaluca-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)