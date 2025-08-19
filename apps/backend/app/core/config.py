from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # App
    app_name: str = "LaVidaLuca Backend API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./lavidaluca.db")
    
    # Supabase
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_ANON_KEY", "")
    
    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # CORS
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "https://*.vercel.app",
        "https://localhost:3000"
    ]
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()