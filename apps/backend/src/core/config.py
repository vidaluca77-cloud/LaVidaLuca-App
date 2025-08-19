"""
Configuration management for La Vida Luca backend.
"""
import os
from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # App
    app_name: str = "La Vida Luca API"
    app_version: str = "1.0.0"
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    
    # Database
    database_url: str = Field(default="sqlite:///./app.db")
    test_database_url: str = Field(default="sqlite:///./test.db")
    
    # Authentication
    secret_key: str = Field(default="dev-secret-key-change-in-production")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    
    # OpenAI
    openai_api_key: str = Field(default="")
    
    # CORS
    allowed_origins: List[str] = Field(default=["http://localhost:3000"])
    
    # Logging
    log_level: str = Field(default="INFO")
    
    # Email
    smtp_host: str = Field(default="")
    smtp_port: int = Field(default=587)
    smtp_user: str = Field(default="")
    smtp_password: str = Field(default="")
    from_email: str = Field(default="noreply@lavidaluca.fr")
    
    # Rate limiting
    rate_limit_per_minute: int = Field(default=100)
    
    # File upload
    max_file_size: int = Field(default=10485760)  # 10MB
    upload_dir: str = Field(default="./uploads")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()