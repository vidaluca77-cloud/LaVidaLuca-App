#!/usr/bin/env python3
"""
Quick test to verify the API can start
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_imports():
    """Test that all main imports work"""
    try:
        from app.core.config import settings
        print("✓ Config import successful")
        
        from app.core.database import get_db
        print("✓ Database import successful")
        
        from app.core.models import User, Activity
        print("✓ Models import successful")
        
        from app.schemas.schemas import UserCreate, ActivityCreate
        print("✓ Schemas import successful")
        
        from app.services.user_service import UserService
        print("✓ Services import successful")
        
        from app.api.v1.api import api_router
        print("✓ API routes import successful")
        
        from main import app
        print("✓ Main app import successful")
        
        print("\n🎉 All imports successful! API structure is valid.")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)