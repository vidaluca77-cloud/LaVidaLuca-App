"""
Performance tests for LaVidaLuca backend using Locust.

Tests load testing, stress testing, and endpoint benchmarks.
"""

from locust import HttpUser, task, between, events
import json
import random
import string
import time
from datetime import datetime


class LaVidaLucaUser(HttpUser):
    """Simulated user for load testing."""
    
    wait_time = between(1, 5)  # Wait 1-5 seconds between requests
    
    def on_start(self):
        """Set up user session."""
        self.register_and_login()
        self.activity_ids = []
    
    def register_and_login(self):
        """Register a new user and login to get auth token."""
        # Generate random user data
        random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        self.user_data = {
            "email": f"loadtest_{random_id}@example.com",
            "password": "LoadTestPassword123!",
            "first_name": f"Load{random_id}",
            "last_name": "Test"
        }
        
        # Register user
        response = self.client.post("/api/v1/auth/register", json=self.user_data)
        if response.status_code != 201:
            print(f"Registration failed: {response.text}")
            return
        
        # Login to get token
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        response = self.client.post("/api/v1/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json()["data"]["access_token"]
            self.headers = {"Authorization": f"Bearer {token}"}
        else:
            print(f"Login failed: {response.text}")
            self.headers = {}
    
    @task(10)
    def view_homepage(self):
        """View the homepage."""
        self.client.get("/")
    
    @task(5)
    def health_check(self):
        """Check application health."""
        self.client.get("/health")
    
    @task(20)
    def browse_activities(self):
        """Browse public activities."""
        # Get activities list
        params = {
            "page": random.randint(1, 3),
            "size": random.randint(10, 20)
        }
        response = self.client.get("/api/v1/activities/", params=params)
        
        # If we get activities, randomly view one
        if response.status_code == 200:
            activities = response.json().get("data", [])
            if activities:
                activity = random.choice(activities)
                self.client.get(f"/api/v1/activities/{activity['id']}")
    
    @task(15)
    def search_activities(self):
        """Search activities with filters."""
        categories = ["sports", "art", "cooking", "outdoor", "indoor"]
        difficulties = ["beginner", "intermediate", "advanced"]
        
        params = {
            "category": random.choice(categories),
            "difficulty_level": random.choice(difficulties),
            "max_duration": random.choice([30, 60, 120])
        }
        self.client.get("/api/v1/activities/", params=params)
    
    @task(8)
    def create_activity(self):
        """Create a new activity."""
        if not hasattr(self, 'headers') or not self.headers:
            return
        
        activity_data = {
            "title": f"Load Test Activity {random.randint(1000, 9999)}",
            "description": "This is a load test activity created for performance testing.",
            "category": random.choice(["sports", "art", "cooking", "outdoor"]),
            "difficulty_level": random.choice(["beginner", "intermediate", "advanced"]),
            "estimated_duration": random.choice([30, 45, 60, 90, 120]),
            "materials": [f"Material {i}" for i in range(random.randint(1, 5))],
            "instructions": [f"Step {i}: Do something" for i in range(random.randint(2, 8))],
            "tags": [f"tag{i}" for i in range(random.randint(1, 4))]
        }
        
        response = self.client.post("/api/v1/activities/", 
                                  json=activity_data, headers=self.headers)
        if response.status_code == 201:
            activity_id = response.json()["data"]["id"]
            self.activity_ids.append(activity_id)
    
    @task(5)
    def view_my_activities(self):
        """View user's own activities."""
        if not hasattr(self, 'headers') or not self.headers:
            return
        
        self.client.get("/api/v1/activities/my", headers=self.headers)
    
    @task(3)
    def update_activity(self):
        """Update an existing activity."""
        if not hasattr(self, 'headers') or not self.headers or not self.activity_ids:
            return
        
        activity_id = random.choice(self.activity_ids)
        update_data = {
            "title": f"Updated Activity {random.randint(1000, 9999)}",
            "description": "Updated description for load testing."
        }
        
        self.client.put(f"/api/v1/activities/{activity_id}", 
                       json=update_data, headers=self.headers)
    
    @task(2)
    def delete_activity(self):
        """Delete an activity."""
        if not hasattr(self, 'headers') or not self.headers or not self.activity_ids:
            return
        
        activity_id = self.activity_ids.pop()
        self.client.delete(f"/api/v1/activities/{activity_id}", 
                          headers=self.headers)
    
    @task(7)
    def get_suggestions(self):
        """Get activity suggestions."""
        if not hasattr(self, 'headers') or not self.headers:
            return
        
        suggestion_data = {
            "preferences": {
                "categories": random.sample(["sports", "art", "cooking", "outdoor"], 
                                          random.randint(1, 3)),
                "difficulty_level": random.choice(["beginner", "intermediate", "advanced"]),
                "max_duration": random.choice([30, 60, 120])
            },
            "context": "Load testing context for suggestions"
        }
        
        self.client.post("/api/v1/suggestions/generate", 
                        json=suggestion_data, headers=self.headers)
    
    @task(3)
    def update_profile(self):
        """Update user profile."""
        if not hasattr(self, 'headers') or not self.headers:
            return
        
        profile_data = {
            "profile": {
                "bio": f"Updated bio at {datetime.now().isoformat()}",
                "location": f"Test Location {random.randint(1, 100)}",
                "interests": random.sample(["sports", "art", "cooking", "reading"], 
                                         random.randint(1, 3))
            }
        }
        
        self.client.put("/api/v1/users/me", json=profile_data, headers=self.headers)


class AuthenticatedUser(HttpUser):
    """User that stays logged in for the entire test."""
    
    wait_time = between(1, 3)
    
    def on_start(self):
        """Login once at the start."""
        self.register_and_login()
    
    def register_and_login(self):
        """Register and login user."""
        random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        user_data = {
            "email": f"authtest_{random_id}@example.com",
            "password": "AuthTestPassword123!",
            "first_name": f"Auth{random_id}",
            "last_name": "Test"
        }
        
        # Register
        self.client.post("/api/v1/auth/register", json=user_data)
        
        # Login
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        response = self.client.post("/api/v1/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json()["data"]["access_token"]
            self.headers = {"Authorization": f"Bearer {token}"}
    
    @task
    def authenticated_request(self):
        """Make authenticated requests."""
        endpoints = [
            "/api/v1/users/me",
            "/api/v1/activities/my"
        ]
        endpoint = random.choice(endpoints)
        self.client.get(endpoint, headers=self.headers)


class StressTestUser(HttpUser):
    """User for stress testing with minimal wait time."""
    
    wait_time = between(0.1, 0.5)  # Very short wait time for stress testing
    
    @task(30)
    def rapid_health_checks(self):
        """Rapid health check requests."""
        self.client.get("/health")
    
    @task(20)
    def rapid_activity_browsing(self):
        """Rapid activity browsing."""
        self.client.get("/api/v1/activities/")
    
    @task(10)
    def rapid_auth_attempts(self):
        """Rapid authentication attempts."""
        random_id = random.randint(10000, 99999)
        login_data = {
            "email": f"stress_{random_id}@example.com",
            "password": "StressTestPassword123!"
        }
        self.client.post("/api/v1/auth/login", json=login_data)


# Custom events and metrics
@events.request.add_listener
def request_handler(request_type, name, response_time, response_length, exception, context, **kwargs):
    """Handle request events for custom metrics."""
    if exception:
        print(f"Request failed: {name} - {exception}")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Actions to perform when test starts."""
    print("Starting LaVidaLuca performance test...")
    print(f"Target host: {environment.host}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Actions to perform when test stops."""
    print("LaVidaLuca performance test completed.")
    print(f"Total requests: {environment.stats.total.num_requests}")
    print(f"Total failures: {environment.stats.total.num_failures}")
    print(f"Average response time: {environment.stats.total.avg_response_time:.2f}ms")
    print(f"RPS: {environment.stats.total.current_rps:.2f}")


# Endpoint-specific performance tests
class EndpointBenchmarkUser(HttpUser):
    """User for benchmarking specific endpoints."""
    
    wait_time = between(0.5, 1.0)
    
    def on_start(self):
        """Set up for benchmarking."""
        self.setup_test_data()
    
    def setup_test_data(self):
        """Create test data for benchmarking."""
        # Register and login
        random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        user_data = {
            "email": f"benchmark_{random_id}@example.com",
            "password": "BenchmarkPassword123!",
            "first_name": f"Benchmark{random_id}",
            "last_name": "Test"
        }
        
        self.client.post("/api/v1/auth/register", json=user_data)
        
        login_response = self.client.post("/api/v1/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        
        if login_response.status_code == 200:
            token = login_response.json()["data"]["access_token"]
            self.headers = {"Authorization": f"Bearer {token}"}
            
            # Create some test activities
            self.activity_ids = []
            for i in range(5):
                activity_data = {
                    "title": f"Benchmark Activity {i}",
                    "description": "Benchmark test activity",
                    "category": "test",
                    "difficulty_level": "beginner",
                    "estimated_duration": 30
                }
                response = self.client.post("/api/v1/activities/", 
                                          json=activity_data, headers=self.headers)
                if response.status_code == 201:
                    self.activity_ids.append(response.json()["data"]["id"])
    
    @task(1)
    def benchmark_activity_list(self):
        """Benchmark activity list endpoint."""
        with self.client.get("/api/v1/activities/", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if len(data.get("data", [])) >= 0:  # Any number of activities is fine
                    response.success()
                else:
                    response.failure("No activities returned")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def benchmark_activity_detail(self):
        """Benchmark activity detail endpoint."""
        if not self.activity_ids:
            return
        
        activity_id = random.choice(self.activity_ids)
        with self.client.get(f"/api/v1/activities/{activity_id}", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("data", {}).get("id") == activity_id:
                    response.success()
                else:
                    response.failure("Incorrect activity returned")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def benchmark_user_profile(self):
        """Benchmark user profile endpoint."""
        if not hasattr(self, 'headers'):
            return
        
        with self.client.get("/api/v1/users/me", headers=self.headers, catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("data", {}).get("email"):
                    response.success()
                else:
                    response.failure("Invalid user data returned")
            else:
                response.failure(f"Got status code {response.status_code}")


# Database performance test user
class DatabaseStressUser(HttpUser):
    """User for testing database performance under load."""
    
    wait_time = between(0.1, 0.3)
    
    def on_start(self):
        """Set up database stress test."""
        random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        self.user_data = {
            "email": f"dbtest_{random_id}@example.com",
            "password": "DBTestPassword123!",
            "first_name": f"DB{random_id}",
            "last_name": "Test"
        }
        
        # Register user
        self.client.post("/api/v1/auth/register", json=self.user_data)
        
        # Login
        login_response = self.client.post("/api/v1/auth/login", json={
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        })
        
        if login_response.status_code == 200:
            token = login_response.json()["data"]["access_token"]
            self.headers = {"Authorization": f"Bearer {token}"}
    
    @task(5)
    def create_and_read_activity(self):
        """Create activity and immediately read it."""
        if not hasattr(self, 'headers'):
            return
        
        # Create activity
        activity_data = {
            "title": f"DB Stress Activity {random.randint(10000, 99999)}",
            "description": "Database stress test activity",
            "category": "test",
            "difficulty_level": "beginner",
            "estimated_duration": 30
        }
        
        create_response = self.client.post("/api/v1/activities/", 
                                         json=activity_data, headers=self.headers)
        
        if create_response.status_code == 201:
            activity_id = create_response.json()["data"]["id"]
            # Immediately read the activity
            self.client.get(f"/api/v1/activities/{activity_id}")
    
    @task(3)
    def bulk_activity_operations(self):
        """Perform multiple operations in sequence."""
        if not hasattr(self, 'headers'):
            return
        
        # Get activities list
        self.client.get("/api/v1/activities/my", headers=self.headers)
        
        # Update profile
        profile_data = {
            "profile": {
                "last_activity": datetime.now().isoformat()
            }
        }
        self.client.put("/api/v1/users/me", json=profile_data, headers=self.headers)
    
    @task(2)
    def complex_queries(self):
        """Trigger complex database queries."""
        # Search with multiple filters
        params = {
            "category": random.choice(["sports", "art", "cooking"]),
            "difficulty_level": random.choice(["beginner", "intermediate", "advanced"]),
            "min_duration": 30,
            "max_duration": 120,
            "tags": ["test", "stress"]
        }
        self.client.get("/api/v1/activities/", params=params)


if __name__ == "__main__":
    # This allows running the file directly for testing
    print("Locust performance tests for LaVidaLuca")
    print("Use: locust -f test_performance.py --host=http://localhost:8000")
    print("Available user classes:")
    print("  - LaVidaLucaUser (default mixed load)")
    print("  - AuthenticatedUser (authenticated requests only)")
    print("  - StressTestUser (high frequency requests)")
    print("  - EndpointBenchmarkUser (endpoint-specific benchmarks)")
    print("  - DatabaseStressUser (database performance testing)")