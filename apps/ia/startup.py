#!/usr/bin/env python3
"""
Startup script for FastAPI application
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.core.database import create_tables
from init_db import init_database

async def startup():
    """Initialize the application"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting La Vida Luca API...")
    
    try:
        # Initialize database if needed
        logger.info("Initializing database...")
        init_database()
        logger.info("Database initialization complete")
        
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(startup())