#!/usr/bin/env python3
"""
Simple API validation script to test OpenAPI documentation setup.
This script validates that the FastAPI app can be imported and that
the OpenAPI schema is properly configured.
"""

import sys
import os
import json

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_app_import():
    """Test that the FastAPI app can be imported successfully."""
    try:
        from app.main import app
        print("✅ FastAPI app imported successfully")
        return app
    except Exception as e:
        print(f"❌ Failed to import FastAPI app: {e}")
        return None

def test_openapi_schema(app):
    """Test that the OpenAPI schema can be generated."""
    try:
        schema = app.openapi()
        print("✅ OpenAPI schema generated successfully")
        print(f"   - Title: {schema.get('info', {}).get('title', 'N/A')}")
        print(f"   - Version: {schema.get('info', {}).get('version', 'N/A')}")
        print(f"   - Paths: {len(schema.get('paths', {}))}")
        print(f"   - Components: {len(schema.get('components', {}).get('schemas', {}))}")
        return schema
    except Exception as e:
        print(f"❌ Failed to generate OpenAPI schema: {e}")
        return None

def test_custom_openapi_file():
    """Test that the custom OpenAPI file exists and is valid JSON."""
    docs_path = os.path.join(os.path.dirname(__file__), "openapi.json")
    try:
        with open(docs_path, "r", encoding="utf-8") as f:
            custom_schema = json.load(f)
        print("✅ Custom OpenAPI file loaded successfully")
        print(f"   - Title: {custom_schema.get('info', {}).get('title', 'N/A')}")
        print(f"   - Paths: {len(custom_schema.get('paths', {}))}")
        return custom_schema
    except FileNotFoundError:
        print(f"❌ Custom OpenAPI file not found at {docs_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in custom OpenAPI file: {e}")
        return None

def test_api_routes(app):
    """Test that API routes are properly configured."""
    try:
        routes = []
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                routes.append(f"{list(route.methods)[0] if route.methods else 'GET'} {route.path}")
        
        print("✅ API routes configured:")
        for route in sorted(routes):
            print(f"   - {route}")
        return routes
    except Exception as e:
        print(f"❌ Failed to get API routes: {e}")
        return []

def main():
    """Run all validation tests."""
    print("🔍 Validating LaVidaLuca Backend API Documentation Setup\n")
    
    # Test 1: Import the app
    app = test_app_import()
    if not app:
        print("\n❌ Critical failure: Cannot proceed without app import")
        sys.exit(1)
    
    print()
    
    # Test 2: Generate OpenAPI schema
    schema = test_openapi_schema(app)
    print()
    
    # Test 3: Load custom OpenAPI file
    custom_schema = test_custom_openapi_file()
    print()
    
    # Test 4: Check API routes
    routes = test_api_routes(app)
    print()
    
    # Summary
    tests_passed = sum([
        app is not None,
        schema is not None,
        custom_schema is not None,
        len(routes) > 0
    ])
    
    print(f"📊 Summary: {tests_passed}/4 tests passed")
    
    if tests_passed == 4:
        print("🎉 All tests passed! OpenAPI documentation is properly configured.")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()