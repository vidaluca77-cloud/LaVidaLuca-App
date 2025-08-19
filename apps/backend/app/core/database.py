"""
Database configuration with connection pooling and optimization
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from databases import Database
import logging
from .config import settings

logger = logging.getLogger(__name__)

# SQLAlchemy configuration with connection pooling
def create_database_engine():
    """Create database engine with proper connection pooling"""
    engine_kwargs = {
        "poolclass": QueuePool,
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
        "pool_timeout": settings.DB_POOL_TIMEOUT,
        "pool_recycle": settings.DB_POOL_RECYCLE,
        "pool_pre_ping": settings.DB_POOL_PRE_PING,
        "echo": settings.DEBUG and settings.is_development,
        "echo_pool": settings.DEBUG and settings.is_development,
    }
    
    # Additional production optimizations
    if settings.is_production:
        engine_kwargs.update({
            "pool_size": 10,  # Smaller pool for production
            "max_overflow": 20,
            "echo": False,
            "echo_pool": False,
        })
    
    engine = create_engine(settings.database_url, **engine_kwargs)
    logger.info(f"Database engine created with pool_size={engine_kwargs['pool_size']}")
    return engine

# Create engine and session
engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async database connection
database = Database(settings.async_database_url)

# SQLAlchemy base
Base = declarative_base()
metadata = MetaData()

# Database dependency for FastAPI
def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# Async database functions
async def connect_database():
    """Connect to database"""
    try:
        await database.connect()
        logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise

async def disconnect_database():
    """Disconnect from database"""
    try:
        await database.disconnect()
        logger.info("Database disconnected successfully")
    except Exception as e:
        logger.error(f"Failed to disconnect from database: {e}")
        raise

# Health check for database
async def check_database_health() -> dict:
    """Check database connection health"""
    try:
        await database.execute("SELECT 1")
        return {
            "status": "healthy",
            "message": "Database connection is working",
            "pool_size": settings.DB_POOL_SIZE,
            "environment": settings.ENVIRONMENT
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}",
            "pool_size": settings.DB_POOL_SIZE,
            "environment": settings.ENVIRONMENT
        }

def get_sync_db():
    """Get synchronous database session for migrations etc."""
    return SessionLocal()