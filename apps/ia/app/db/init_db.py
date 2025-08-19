"""
Database initialization utilities
"""
from sqlalchemy import create_engine
from app.models.models import Base
from app.core.config import settings

def create_tables():
    """Create all database tables"""
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()