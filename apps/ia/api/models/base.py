"""
Modèles SQLAlchemy de base
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import SQLALCHEMY_DATABASE_URL, ENGINE_KWARGS

# Configuration de SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, **ENGINE_KWARGS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour tous les modèles
Base = declarative_base()

# Métadonnées pour les migrations
metadata = MetaData()

# Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()