from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LaVidaLuca Backend"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Backend API for LaVidaLuca - MFR training platform"
    
    # Database
    DATABASE_URL: Optional[str] = None
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "lavidaluca"
    POSTGRES_PORT: int = 5432
    
    # Security
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # Rate limiting
    LOGIN_RATE_LIMIT_ATTEMPTS: int = 5
    LOGIN_RATE_LIMIT_WINDOW: int = 15  # minutes
    
    # Account lockout
    MAX_FAILED_LOGIN_ATTEMPTS: int = 5
    ACCOUNT_LOCKOUT_DURATION: int = 30  # minutes
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    
    # CORS
    ALLOWED_HOSTS: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
    
    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()