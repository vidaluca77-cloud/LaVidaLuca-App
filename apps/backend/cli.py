#!/usr/bin/env python3
"""
LaVidaLuca Backend Application Utilities
Provides CLI commands for database setup, user management, and deployment
"""

import argparse
import sys
import os
from sqlalchemy.orm import Session

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.database import SessionLocal, create_tables
from app.core.security import get_password_hash
from app.models.user import User
from app.models.activity import Activity

def create_admin_user(email: str, username: str, password: str, full_name: str = None):
    """Create an admin user"""
    db = SessionLocal()
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing_user:
            print(f"User with email '{email}' or username '{username}' already exists!")
            return
        
        # Create admin user
        hashed_password = get_password_hash(password)
        admin_user = User(
            email=email,
            username=username,
            full_name=full_name or f"Admin {username}",
            hashed_password=hashed_password,
            is_admin=True,
            is_active=True,
            is_verified=True,
            user_type="admin",
            skills=[],
            availability=[],
            preferences=[]
        )
        
        db.add(admin_user)
        db.commit()
        
        print(f"Admin user '{username}' created successfully!")
        print(f"Email: {email}")
        print(f"Username: {username}")
        print("Password: [HIDDEN]")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def setup_database():
    """Initialize the database with tables and seed data"""
    print("Setting up database...")
    
    try:
        # Create tables
        print("Creating database tables...")
        create_tables()
        print("Database tables created successfully!")
        
        # Check if we need to seed activities
        db = SessionLocal()
        activity_count = db.query(Activity).count()
        db.close()
        
        if activity_count == 0:
            print("No activities found. Running seed script...")
            from seed_activities import seed_activities
            seed_activities()
        else:
            print(f"Found {activity_count} activities in database. Skipping seed.")
        
        print("Database setup completed!")
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        raise

def check_environment():
    """Check environment configuration"""
    print("Checking environment configuration...")
    
    required_vars = [
        "DATABASE_URL",
        "SECRET_KEY",
        "SUPABASE_URL", 
        "SUPABASE_ANON_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def main():
    parser = argparse.ArgumentParser(description="LaVidaLuca Backend CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Setup database command
    setup_parser = subparsers.add_parser("setup", help="Setup database and seed data")
    
    # Create admin command
    admin_parser = subparsers.add_parser("create-admin", help="Create admin user")
    admin_parser.add_argument("--email", required=True, help="Admin email")
    admin_parser.add_argument("--username", required=True, help="Admin username")
    admin_parser.add_argument("--password", required=True, help="Admin password")
    admin_parser.add_argument("--full-name", help="Admin full name")
    
    # Check environment command
    env_parser = subparsers.add_parser("check-env", help="Check environment configuration")
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "setup":
            setup_database()
        elif args.command == "create-admin":
            create_admin_user(
                email=args.email,
                username=args.username,
                password=args.password,
                full_name=args.full_name
            )
        elif args.command == "check-env":
            check_environment()
    
    except Exception as e:
        print(f"Command failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()