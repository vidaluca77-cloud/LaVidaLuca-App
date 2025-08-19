from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LaVidaLuca API"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./lavidaluca.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://lavidaluca.vercel.app"
    ]
    
    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # External APIs
    CONTACT_EMAIL: str = "contact@lavidaluca.fr"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()