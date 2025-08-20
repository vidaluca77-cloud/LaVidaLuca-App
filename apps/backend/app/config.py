"""
Configuration management for the FastAPI application.

This module handles environment variables and application settings
following PEP 8 conventions.
"""

import os
from typing import Optional
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database configuration
    database_url: str = "postgresql://user:pass@localhost:5432/lavidaluca"
    
    # API configuration
    api_v1_prefix: str = "/api/v1"
    
    # Application metadata
    app_name: str = "La Vida Luca API"
    version: str = "1.0.0"
    description: str = "API pour l'assistant agricole La Vida Luca"
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Global settings instance
settings = Settings()