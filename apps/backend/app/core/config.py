import os
from typing import Any, Dict, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LaVidaLuca Backend API"
    VERSION: str = "1.0.0"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://localhost:3000",
        "https://localhost:8000",
    ]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return []
    
    # Database Settings
    SUPABASE_URL: str
    SUPABASE_KEY: str
    DATABASE_URL: Optional[str] = None
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info) -> Any:
        if isinstance(v, str):
            return v
        # Build PostgreSQL URL from Supabase URL
        supabase_url = info.data.get("SUPABASE_URL") if info.data else None
        if supabase_url:
            # Extract database connection info from Supabase URL
            # Format: https://[project_id].supabase.co
            project_id = supabase_url.replace("https://", "").replace(".supabase.co", "")
            return f"postgresql://postgres:[PASSWORD]@db.{project_id}.supabase.co:5432/postgres"
        return None
    
    # Security Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI Settings
    OPENAI_API_KEY: str
    
    # Debug mode
    DEBUG: bool = False
    
    # Email Settings (for notifications)
    CONTACT_EMAIL: Optional[str] = None
    CONTACT_PHONE: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()