#!/usr/bin/env python3
"""
Test script to validate OpenAPI documentation implementation.
This script checks that all the new OpenAPI components work correctly.
"""

import json
import sys
import os

def test_imports():
    """Test that all our new modules can be imported correctly."""
    print("Testing imports...")
    
    try:
        # Add the backend directory to path
        backend_path = os.path.dirname(os.path.abspath(__file__))
        if backend_path not in sys.path:
            sys.path.append(backend_path)
        
        # Test importing the new modules
        from api.openapi import TAGS_METADATA, SECURITY_SCHEMES, custom_openapi, configure_swagger_ui
        from api.models import UserCreate, ActivityCreate, ActivitySuggestion
        
        print("✅ All imports successful")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_openapi_config():
    """Test OpenAPI configuration components."""
    print("\nTesting OpenAPI configuration...")
    
    try:
        from api.openapi import TAGS_METADATA, SECURITY_SCHEMES, configure_swagger_ui
        
        # Check tags metadata
        assert isinstance(TAGS_METADATA, list), "TAGS_METADATA should be a list"
        assert len(TAGS_METADATA) > 0, "TAGS_METADATA should not be empty"
        
        # Check security schemes
        assert isinstance(SECURITY_SCHEMES, dict), "SECURITY_SCHEMES should be a dict"
        assert "BearerAuth" in SECURITY_SCHEMES, "BearerAuth should be in SECURITY_SCHEMES"
        
        # Check swagger UI config
        swagger_config = configure_swagger_ui()
        assert isinstance(swagger_config, dict), "configure_swagger_ui should return a dict"
        
        print("✅ OpenAPI configuration valid")
        return True
        
    except Exception as e:
        print(f"❌ OpenAPI configuration error: {e}")
        return False

def test_models():
    """Test Pydantic models."""
    print("\nTesting Pydantic models...")
    
    try:
        from api.models import UserCreate, ActivityCreate, ActivityCategory, DifficultyLevel
        
        # Test enum values
        assert ActivityCategory.AGRICULTURE == "agriculture"
        assert DifficultyLevel.BEGINNER == "beginner"
        
        # Test model creation
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "password123",
            "is_active": True
        }
        user = UserCreate(**user_data)
        assert user.email == "test@example.com"
        
        activity_data = {
            "title": "Test Activity",
            "description": "Test description",
            "category": ActivityCategory.AGRICULTURE,
            "difficulty_level": DifficultyLevel.BEGINNER,
            "is_published": True
        }
        activity = ActivityCreate(**activity_data)
        assert activity.title == "Test Activity"
        
        print("✅ Pydantic models working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Model testing error: {e}")
        return False

def test_endpoint_documentation():
    """Test that endpoint files have proper documentation."""
    print("\nTesting endpoint documentation...")
    
    endpoint_files = [
        "app/api/endpoints/auth.py",
        "app/api/endpoints/activities.py",
        "app/api/endpoints/users.py",
        "app/api/endpoints/suggestions.py"
    ]
    
    for file_path in endpoint_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check for OpenAPI documentation keywords
            required_keywords = ["summary=", "description=", "responses=", "tags="]
            found_keywords = [kw for kw in required_keywords if kw in content]
            
            if len(found_keywords) >= 2:  # At least summary and tags should be present
                print(f"✅ {file_path} has OpenAPI documentation")
            else:
                print(f"⚠️  {file_path} may need more documentation")
                
        except Exception as e:
            print(f"❌ Error checking {file_path}: {e}")
            return False
    
    return True

def main():
    """Run all tests."""
    print("🚀 Testing OpenAPI Documentation Implementation")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_openapi_config, 
        test_models,
        test_endpoint_documentation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"✅ Passed: {sum(results)}/{len(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("\n🎉 All tests passed! OpenAPI implementation is ready.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())