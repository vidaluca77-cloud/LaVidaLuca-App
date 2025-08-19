"""
Database session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator

from ..core.config import settings

# Create engine
engine = create_engine(
    settings.database_url,
    poolclass=StaticPool,
    pool_pre_ping=True,
    echo=settings.debug
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Test database setup
def get_test_engine():
    """Get test database engine."""
    return create_engine(
        settings.test_database_url,
        poolclass=StaticPool,
        echo=False
    )


def get_test_session():
    """Get test database session."""
    test_engine = get_test_engine()
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    return TestSessionLocal()