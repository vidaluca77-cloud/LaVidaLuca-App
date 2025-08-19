from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import create_tables
from app.api.v1.endpoints import users, activities, recommendations

# Create database tables on startup
create_tables()

app = FastAPI(
    title="La Vida Luca API",
    description="API for La Vida Luca activity management and recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(activities.router, prefix="/api/v1/activities", tags=["activities"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["recommendations"])

@app.get("/")
async def root():
    return {"message": "La Vida Luca API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)