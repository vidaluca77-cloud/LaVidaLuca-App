"""
FastAPI Configuration and Settings
"""
from decouple import config
from typing import List


class Settings:
    """Application settings."""
    
    # Database
    DATABASE_URL: str = config("DATABASE_URL", default="sqlite:///./lavidaluca.db")
    
    # JWT Settings
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-change-me")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
    
    # OpenAI
    OPENAI_API_KEY: str = config("OPENAI_API_KEY", default="")
    OPENAI_MODEL: str = config("OPENAI_MODEL", default="gpt-3.5-turbo")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = config(
        "ALLOWED_ORIGINS", 
        default="http://localhost:3000,https://la-vida-luca.vercel.app",
        cast=lambda v: [origin.strip() for origin in v.split(",")]
    )
    
    # Environment
    ENVIRONMENT: str = config("ENVIRONMENT", default="development")
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "La Vida Luca API"
    PROJECT_VERSION: str = "1.0.0"
    DESCRIPTION: str = "API pour les recommandations d'activités La Vida Luca"


settings = Settings()