"""
Application configuration settings
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
import os

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LaVidaLuca API"
    DEBUG: bool = False
    
    # CORS Settings
    ALLOWED_ORIGINS: List[AnyHttpUrl] = []
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return []
    
    # Database Settings
    DATABASE_URL: str = "postgresql://user:password@localhost/lavidaluca"
    
    # Authentication Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # OpenAI Settings
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Supabase Settings (if using Supabase instead of direct PostgreSQL)
    SUPABASE_URL: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SERVICE_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()