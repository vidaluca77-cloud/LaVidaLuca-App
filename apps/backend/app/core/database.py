"""
Database configuration and connection management for La Vida Luca.
"""

import asyncio
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from typing import AsyncGenerator

from .config import settings


# Create database URL for async operations
database_url = settings.database_url
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Create async database instance
database = Database(database_url)

# Create async engine
async_engine = create_async_engine(
    database_url,
    echo=True if settings.PROJECT_NAME == "development" else False,
    future=True,
)

# Create sync engine for migrations
sync_engine = create_engine(settings.database_url, echo=False)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Create declarative base for models
Base = declarative_base()

# Metadata for table creation
metadata = MetaData()


async def get_database() -> Database:
    """Get database instance."""
    return database


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def connect_db():
    """Connect to the database."""
    await database.connect()


async def disconnect_db():
    """Disconnect from the database."""
    await database.disconnect()


async def create_tables():
    """Create all database tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    """Drop all database tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Dependency for FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()