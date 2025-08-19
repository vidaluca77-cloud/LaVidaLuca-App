from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    # Try relative imports first
    from .auth.router import router as auth_router
    from .activities import router as activities_router
    from .config import settings
    from .database import engine
    from .models import Base
except ImportError:
    # Fallback to absolute imports for testing
    from auth.router import router as auth_router
    from activities import router as activities_router
    from config import settings
    from database import engine
    from models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="La Vida Luca API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(activities_router)


@app.get("/")
def read_root():
    return {"message": "La Vida Luca API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}