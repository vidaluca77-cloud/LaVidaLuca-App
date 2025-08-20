#!/usr/bin/env python3
"""
Example client script showing how to interact with the LaVidaLuca Backend API.
This demonstrates the main API endpoints and authentication flow.
"""

import requests
import json
from typing import Optional

class LaVidaLucaAPIClient:
    """Simple client for the LaVidaLuca Backend API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.token: Optional[str] = None
        self.session = requests.Session()
    
    def _get_headers(self) -> dict:
        """Get headers for API requests."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def register(self, email: str, username: str, password: str, full_name: Optional[str] = None) -> dict:
        """Register a new user account."""
        data = {
            "email": email,
            "username": username,
            "password": password,
            "is_active": True
        }
        if full_name:
            data["full_name"] = full_name
        
        response = self.session.post(
            f"{self.base_url}/api/v1/auth/register",
            json=data,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def login(self, username: str, password: str) -> dict:
        """Login and store the JWT token."""
        data = {
            "username": username,
            "password": password
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/auth/login",
            json=data,
            headers=self._get_headers()
        )
        response.raise_for_status()
        
        token_data = response.json()
        self.token = token_data["access_token"]
        return token_data
    
    def get_current_user(self) -> dict:
        """Get current user profile."""
        response = self.session.get(
            f"{self.base_url}/api/v1/users/me",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_activities(self, **filters) -> list:
        """Get list of activities with optional filters."""
        params = {k: v for k, v in filters.items() if v is not None}
        
        response = self.session.get(
            f"{self.base_url}/api/v1/activities/",
            params=params,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def create_activity(self, activity_data: dict) -> dict:
        """Create a new activity."""
        response = self.session.post(
            f"{self.base_url}/api/v1/activities/",
            json=activity_data,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_activity_categories(self) -> list:
        """Get available activity categories."""
        response = self.session.get(
            f"{self.base_url}/api/v1/activities/categories/",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def submit_contact_form(self, contact_data: dict) -> dict:
        """Submit a contact form."""
        response = self.session.post(
            f"{self.base_url}/api/v1/contacts/",
            json=contact_data,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_contact_types(self) -> list:
        """Get available contact form types."""
        response = self.session.get(
            f"{self.base_url}/api/v1/contacts/types",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_suggestions(self) -> list:
        """Get activity suggestions for current user."""
        response = self.session.get(
            f"{self.base_url}/api/v1/suggestions/",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def generate_suggestions(self, preferences: Optional[str] = None) -> list:
        """Generate new AI activity suggestions."""
        params = {}
        if preferences:
            params["preferences"] = preferences
        
        response = self.session.post(
            f"{self.base_url}/api/v1/suggestions/generate",
            params=params,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()


def example_usage():
    """Example of how to use the API client."""
    
    # Initialize client
    client = LaVidaLucaAPIClient("http://localhost:8000")
    
    print("🚀 LaVidaLuca API Client Example")
    print("=" * 40)
    
    try:
        # Example 1: Submit a contact form (no auth required)
        print("\n1️⃣ Submitting contact form...")
        contact_data = {
            "name": "Jean Dupont",
            "email": "jean.dupont@example.com",
            "subject": "Question about your platform",
            "message": "Hello, I would like to know more about your collaborative learning platform.",
            "contact_type": "general",
            "consent_privacy": True,
            "consent_marketing": False
        }
        
        contact_response = client.submit_contact_form(contact_data)
        print(f"✅ Contact form submitted! ID: {contact_response['id']}")
        
        # Example 2: Get contact types
        print("\n2️⃣ Getting contact types...")
        contact_types = client.get_contact_types()
        print(f"✅ Available contact types: {', '.join(contact_types)}")
        
        # Example 3: Register a new user
        print("\n3️⃣ Registering new user...")
        user_data = client.register(
            email="testuser@example.com",
            username="testuser",
            password="testpassword123",
            full_name="Test User"
        )
        print(f"✅ User registered! ID: {user_data['id']}")
        
        # Example 4: Login
        print("\n4️⃣ Logging in...")
        token_data = client.login("testuser", "testpassword123")
        print(f"✅ Logged in! Token type: {token_data['token_type']}")
        
        # Example 5: Get current user profile
        print("\n5️⃣ Getting user profile...")
        user_profile = client.get_current_user()
        print(f"✅ User profile: {user_profile['username']} ({user_profile['email']})")
        
        # Example 6: Get activities
        print("\n6️⃣ Getting activities...")
        activities = client.get_activities(limit=5, published_only=True)
        print(f"✅ Found {len(activities)} activities")
        
        # Example 7: Get activity categories
        print("\n7️⃣ Getting activity categories...")
        categories = client.get_activity_categories()
        print(f"✅ Available categories: {', '.join(categories) if categories else 'None yet'}")
        
        # Example 8: Create a new activity
        print("\n8️⃣ Creating new activity...")
        activity_data = {
            "title": "Introduction to Sustainable Farming",
            "description": "Learn the basics of sustainable and ecological farming practices.",
            "category": "agriculture",
            "difficulty_level": "beginner",
            "duration_minutes": 120,
            "location": "Farm Training Center",
            "equipment_needed": "Notebook, work gloves, water bottle",
            "learning_objectives": "Understand sustainable farming principles and basic techniques",
            "is_published": True
        }
        
        new_activity = client.create_activity(activity_data)
        print(f"✅ Activity created! ID: {new_activity['id']}")
        
        # Example 9: Get suggestions
        print("\n9️⃣ Getting activity suggestions...")
        suggestions = client.get_suggestions()
        print(f"✅ Found {len(suggestions)} existing suggestions")
        
        # Example 10: Generate new suggestions
        print("\n🔟 Generating new suggestions...")
        new_suggestions = client.generate_suggestions(
            "I'm interested in technology and environmental sustainability"
        )
        print(f"✅ Generated {len(new_suggestions)} new suggestions")
        
        print("\n🎉 All examples completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server.")
        print("   Make sure the server is running at http://localhost:8000")
    except requests.exceptions.HTTPError as e:
        print(f"❌ API request failed: {e}")
        print(f"   Response: {e.response.text if e.response else 'No response'}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    example_usage()