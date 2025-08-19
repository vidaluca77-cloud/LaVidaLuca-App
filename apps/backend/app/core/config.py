"""
Configuration settings for the FastAPI application.
"""
from typing import Optional, List
from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "LaVidaLuca API"
    version: str = "1.0.0"
    debug: bool = config("DEBUG", default=False, cast=bool)
    
    # Security
    secret_key: str = config("SECRET_KEY", default="your-secret-key-here-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database
    database_url: str = config(
        "DATABASE_URL", 
        default="postgresql://user:password@localhost/lavidaluca"
    )
    
    # CORS
    allowed_origins: List[str] = config(
        "ALLOWED_ORIGINS",
        default="http://localhost:3000,https://la-vida-luca.vercel.app",
        cast=lambda v: [s.strip() for s in v.split(",")]
    )
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()