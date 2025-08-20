"""
Database configuration and SQLAlchemy setup.

This module provides database connectivity and session management
for the FastAPI application using SQLAlchemy ORM.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings


# Create database engine
engine = create_engine(
    settings.database_url,
    echo=True,  # Enable SQL query logging for development
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create declarative base for models
Base = declarative_base()


def get_db():
    """
    Database dependency for FastAPI.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()