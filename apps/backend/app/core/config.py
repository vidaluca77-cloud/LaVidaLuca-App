"""
Core configuration for La Vida Luca FastAPI application.
"""

from typing import List, Optional
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration settings for the application."""
    
    PROJECT_NAME: str = "La Vida Luca API"
    API_V1_STR: str = "/api/v1"
    
    # CORS configuration
    ALLOWED_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # Next.js dev server
        "https://la-vida-luca.vercel.app",  # Production frontend
    ]
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database configuration
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()