from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import settings

# Database setup - use SQLite for local development if PostgreSQL is not available
try:
    database_url = settings.database_url or "postgresql://user:password@localhost/lavidaluca"
    engine = create_engine(database_url, echo=settings.debug)
except Exception:
    # Fallback to SQLite for development/testing
    database_url = "sqlite:///./lavidaluca.db"
    engine = create_engine(
        database_url,
        echo=settings.debug,
        connect_args={"check_same_thread": False}  # SQLite specific
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()