"""
Database configuration and connection management.
"""

import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from databases import Database

from config import settings


# Create async database instance
database = Database(settings.DATABASE_URL)

# Create async engine with optimized pool settings
engine_kwargs = {
    "pool_size": settings.DATABASE_POOL_SIZE,
    "max_overflow": settings.DATABASE_MAX_OVERFLOW,
    "echo": settings.DEBUG,
    "pool_timeout": settings.DATABASE_POOL_TIMEOUT,
    "pool_recycle": settings.DATABASE_POOL_RECYCLE,
}

# For testing, use a different pooling strategy
if settings.ENVIRONMENT == "testing":
    engine_kwargs.update({
        "poolclass": StaticPool,
        "connect_args": {"check_same_thread": False},
        "pool_size": 1,
        "max_overflow": 0,
    })

engine = create_async_engine(
    settings.DATABASE_URL,
    **engine_kwargs
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=True,
    autocommit=False
)

# Create declarative base for models
Base = declarative_base()


async def get_database() -> Database:
    """Get database instance."""
    return database


async def get_db_session() -> AsyncSession:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_database():
    """Initialize database connection."""
    try:
        await database.connect()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise


async def close_database():
    """Close database connection."""
    try:
        await database.disconnect()
    except Exception as e:
        print(f"Error disconnecting from database: {e}")
        raise


# Health check function
async def check_database_health() -> bool:
    """Check if database connection is healthy."""
    try:
        await database.fetch_one("SELECT 1")
        return True
    except Exception:
        return False