from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "LaVidaLuca Backend API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API pour la plateforme LaVidaLuca - Formation des jeunes en MFR"
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "https://localhost:3000"]
    
    # Database settings
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/lavidaluca"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-in-production-very-long-and-random"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Supabase settings (for production)
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"


settings = Settings()