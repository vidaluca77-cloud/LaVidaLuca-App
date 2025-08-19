from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/lavidaluca"
)

# For SQLite fallback during development
if not os.getenv("DATABASE_URL"):
    DATABASE_URL = "sqlite:///./lavidaluca.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("ENVIRONMENT", "development") == "development"
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()