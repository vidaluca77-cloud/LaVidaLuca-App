#!/usr/bin/env python3
"""
Quick validation script for the test suite.
Run this to verify the test structure is correct before running full tests.
"""

import os
import glob

def validate_test_structure():
    """Validate test directory structure and files."""
    print("🧪 Validating LaVidaLuca Backend Test Suite")
    print("=" * 45)
    
    # Check required test files
    required_files = [
        "tests/conftest.py",
        "tests/test_api.py", 
        "tests/test_db.py",
        "tests/test_services.py",
        "tests/test_performance.py",
        "tests/test_security.py",
        "tests/README.md",
        "pytest.ini"
    ]
    
    print("📋 Checking required files:")
    all_present = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (missing)")
            all_present = False
    
    # Count test functions
    test_files = glob.glob("tests/test_*.py")
    total_tests = 0
    
    print(f"\n📊 Test file analysis:")
    for test_file in sorted(test_files):
        with open(test_file, 'r') as f:
            content = f.read()
            test_count = content.count("def test_")
            class_count = content.count("class Test")
            total_tests += test_count
            print(f"  📄 {os.path.basename(test_file)}: {test_count} tests, {class_count} test classes")
    
    print(f"\n📈 Summary:")
    print(f"  Total test files: {len(test_files)}")
    print(f"  Total test functions: {total_tests}")
    print(f"  All required files present: {'Yes' if all_present else 'No'}")
    
    # Check test categories
    print(f"\n🏷️  Test Categories:")
    categories = ["unit", "integration", "performance", "security", "db", "slow"]
    for category in categories:
        found = any(f"@pytest.mark.{category}" in open(tf).read() for tf in test_files if os.path.exists(tf))
        print(f"  {category}: {'✅' if found else '❌'}")
    
    return all_present and total_tests > 0

if __name__ == "__main__":
    success = validate_test_structure()
    
    if success:
        print(f"\n✅ Test suite validation successful!")
        print(f"\n🚀 Ready to run tests:")
        print(f"  pytest                    # Run all tests")
        print(f"  pytest -m unit           # Run unit tests only") 
        print(f"  pytest --cov=app         # Run with coverage")
        print(f"  pytest -k test_security  # Run security tests only")
    else:
        print(f"\n❌ Test suite validation failed!")
        print(f"   Please check missing files and try again.")
        exit(1)