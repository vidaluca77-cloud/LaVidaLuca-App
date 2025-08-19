"""
Configuration de l'application FastAPI pour La Vida Luca
"""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Application
    app_name: str = "La Vida Luca API"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    
    # API
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "your-secret-key-change-in-production"
    jwt_secret_key: str = "your-jwt-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    # Base de données
    database_url: str = "sqlite:///./lavidaluca.db"
    
    # CORS
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "https://la-vida-luca.vercel.app",
        "https://la-vida-luca-web.onrender.com"
    ]
    
    # Supabase (optionnel)
    supabase_url: str = ""
    supabase_key: str = ""
    
    # Monitoring
    enable_monitoring: bool = True
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Overrides pour la production
        if self.environment == "production":
            self.debug = False
            self.log_level = "WARNING"
        elif self.environment == "testing":
            self.database_url = "sqlite:///./test.db"
            self.debug = True


# Instance globale des paramètres
settings = Settings()

# Configuration de la base de données
DATABASE_URL = settings.database_url

# Configuration pour SQLAlchemy
if DATABASE_URL.startswith("sqlite"):
    SQLALCHEMY_DATABASE_URL = DATABASE_URL
    ENGINE_KWARGS = {"check_same_thread": False}
else:
    SQLALCHEMY_DATABASE_URL = DATABASE_URL
    ENGINE_KWARGS = {}

# Configuration CORS
CORS_ORIGINS = settings.allowed_origins

# Configuration JWT
JWT_SECRET_KEY = settings.jwt_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes