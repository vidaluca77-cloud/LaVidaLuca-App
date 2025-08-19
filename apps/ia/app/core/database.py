"""
Database configuration and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .config import settings

# Create the database engine
if "sqlite" in settings.database_url:
    # SQLite configuration
    engine = create_engine(
        settings.database_url,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True
    )
else:
    # PostgreSQL configuration
    engine = create_engine(
        settings.database_url,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
        pool_pre_ping=True
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()