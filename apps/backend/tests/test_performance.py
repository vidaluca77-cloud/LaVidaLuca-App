"""
Performance tests for LaVidaLuca Backend API.
"""

import pytest
import time
import asyncio
import concurrent.futures
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.models import User, Activity


@pytest.mark.performance
@pytest.mark.slow
class TestAPIPerformance:
    """Test API endpoint performance."""
    
    def test_health_endpoint_performance(self, client: TestClient):
        """Test health endpoint response time."""
        # Warm up
        client.get("/health")
        
        # Measure response time
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 0.1  # Should respond within 100ms
    
    def test_activities_list_performance(self, client: TestClient, test_activities: list):
        """Test activities list endpoint performance."""
        # Warm up
        client.get("/api/v1/activities/")
        
        # Measure response time for listing activities
        start_time = time.time()
        response = client.get("/api/v1/activities/")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 0.5  # Should respond within 500ms
        assert len(response.json()) > 0
    
    def test_activities_pagination_performance(self, client: TestClient, db_session: Session, test_user: User):
        """Test pagination performance with large dataset."""
        # Create a large number of activities
        activities = []
        for i in range(100):
            activity = Activity(
                title=f"Performance Test Activity {i}",
                category=f"category_{i % 10}",
                creator_id=test_user.id
            )
            activities.append(activity)
        
        db_session.add_all(activities)
        db_session.commit()
        
        # Test pagination performance
        start_time = time.time()
        response = client.get("/api/v1/activities/?skip=50&limit=20")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # Should respond within 1 second
        assert len(response.json()) == 20
    
    def test_single_activity_lookup_performance(self, client: TestClient, test_activity: Activity):
        """Test single activity lookup performance."""
        # Warm up
        client.get(f"/api/v1/activities/{test_activity.id}")
        
        # Measure response time
        start_time = time.time()
        response = client.get(f"/api/v1/activities/{test_activity.id}")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 0.2  # Should respond within 200ms
    
    def test_user_registration_performance(self, client: TestClient):
        """Test user registration performance."""
        user_data = {
            "email": "performance@example.com",
            "username": "perfuser",
            "password": "testpassword",
            "full_name": "Performance Test User"
        }
        
        start_time = time.time()
        response = client.post("/api/v1/auth/register", json=user_data)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # Should complete within 1 second
    
    def test_user_login_performance(self, client: TestClient, test_user: User):
        """Test user login performance."""
        login_data = {
            "username": test_user.username,
            "password": "testpassword"
        }
        
        # Warm up
        client.post("/api/v1/auth/login", json=login_data)
        
        # Measure response time
        start_time = time.time()
        response = client.post("/api/v1/auth/login", json=login_data)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 0.5  # Should respond within 500ms
    
    def test_activity_creation_performance(self, client: TestClient, auth_headers: dict):
        """Test activity creation performance."""
        activity_data = {
            "title": "Performance Test Activity",
            "description": "Testing activity creation performance",
            "category": "technology",
            "difficulty_level": "beginner",
            "duration_minutes": 60
        }
        
        start_time = time.time()
        response = client.post(
            "/api/v1/activities/", 
            json=activity_data, 
            headers=auth_headers
        )
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # Should complete within 1 second


@pytest.mark.performance
@pytest.mark.slow
class TestConcurrentRequests:
    """Test API performance under concurrent load."""
    
    def test_concurrent_health_checks(self, client: TestClient):
        """Test concurrent health check requests."""
        def make_health_request():
            response = client.get("/health")
            return response.status_code == 200
        
        # Make 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            start_time = time.time()
            futures = [executor.submit(make_health_request) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
            end_time = time.time()
        
        total_time = end_time - start_time
        
        # All requests should succeed
        assert all(results)
        # Should complete within reasonable time
        assert total_time < 2.0
    
    def test_concurrent_activity_reads(self, client: TestClient, test_activities: list):
        """Test concurrent activity read requests."""
        def get_activities():
            response = client.get("/api/v1/activities/")
            return response.status_code == 200 and len(response.json()) > 0
        
        # Make 20 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            start_time = time.time()
            futures = [executor.submit(get_activities) for _ in range(20)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
            end_time = time.time()
        
        total_time = end_time - start_time
        
        # All requests should succeed
        assert all(results)
        # Should handle concurrent load efficiently
        assert total_time < 5.0
    
    def test_concurrent_user_logins(self, client: TestClient, multiple_users: list):
        """Test concurrent user login requests."""
        def login_user(user):
            login_data = {
                "username": user.username,
                "password": "testpassword"
            }
            response = client.post("/api/v1/auth/login", json=login_data)
            return response.status_code == 200
        
        # Login multiple users concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(multiple_users)) as executor:
            start_time = time.time()
            futures = [executor.submit(login_user, user) for user in multiple_users]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
            end_time = time.time()
        
        total_time = end_time - start_time
        
        # All logins should succeed
        assert all(results)
        # Should handle concurrent authentication efficiently
        assert total_time < 3.0
    
    def test_mixed_concurrent_operations(self, client: TestClient, test_user: User, auth_headers: dict):
        """Test mixed read/write operations concurrently."""
        def read_activities():
            response = client.get("/api/v1/activities/")
            return response.status_code == 200
        
        def get_health():
            response = client.get("/health")
            return response.status_code == 200
        
        def login_user():
            login_data = {
                "username": test_user.username,
                "password": "testpassword"
            }
            response = client.post("/api/v1/auth/login", json=login_data)
            return response.status_code == 200
        
        operations = [
            read_activities,
            get_health,
            read_activities,
            login_user,
            get_health,
            read_activities
        ]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            start_time = time.time()
            futures = [executor.submit(op) for op in operations]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
            end_time = time.time()
        
        total_time = end_time - start_time
        
        # All operations should succeed
        assert all(results)
        # Should handle mixed operations efficiently
        assert total_time < 3.0


@pytest.mark.performance
@pytest.mark.slow
class TestDatabasePerformance:
    """Test database operation performance."""
    
    def test_bulk_activity_creation_performance(self, db_session: Session, test_user: User):
        """Test bulk creation of activities."""
        activities = []
        for i in range(50):
            activity = Activity(
                title=f"Bulk Activity {i}",
                category="test",
                creator_id=test_user.id
            )
            activities.append(activity)
        
        start_time = time.time()
        db_session.add_all(activities)
        db_session.commit()
        end_time = time.time()
        
        operation_time = end_time - start_time
        
        # Should complete bulk insert quickly
        assert operation_time < 2.0
        
        # Verify all activities were created
        count = db_session.query(Activity).filter(
            Activity.title.like("Bulk Activity%")
        ).count()
        assert count == 50
    
    def test_complex_query_performance(self, db_session: Session, test_user: User):
        """Test performance of complex database queries."""
        # Create activities with various attributes
        for i in range(100):
            activity = Activity(
                title=f"Complex Query Activity {i}",
                category=f"category_{i % 5}",
                difficulty_level="beginner" if i % 2 == 0 else "advanced",
                duration_minutes=30 + (i % 4) * 30,
                creator_id=test_user.id
            )
            db_session.add(activity)
        
        db_session.commit()
        
        # Test complex query with multiple filters
        start_time = time.time()
        results = db_session.query(Activity).filter(
            Activity.category.in_(["category_1", "category_3"]),
            Activity.difficulty_level == "beginner",
            Activity.duration_minutes >= 60
        ).order_by(Activity.created_at.desc()).limit(10).all()
        end_time = time.time()
        
        query_time = end_time - start_time
        
        # Should execute complex query quickly
        assert query_time < 0.5
        assert len(results) <= 10
    
    def test_database_connection_performance(self, db_session: Session):
        """Test database connection and query performance."""
        # Test multiple rapid queries
        start_time = time.time()
        
        for _ in range(20):
            result = db_session.execute("SELECT 1").scalar()
            assert result == 1
        
        end_time = time.time()
        
        total_time = end_time - start_time
        
        # Should handle multiple queries efficiently
        assert total_time < 1.0
    
    def test_transaction_performance(self, db_session: Session, test_user: User):
        """Test database transaction performance."""
        start_time = time.time()
        
        # Create multiple activities in a single transaction
        for i in range(20):
            activity = Activity(
                title=f"Transaction Activity {i}",
                category="test",
                creator_id=test_user.id
            )
            db_session.add(activity)
        
        db_session.commit()
        end_time = time.time()
        
        transaction_time = end_time - start_time
        
        # Should complete transaction quickly
        assert transaction_time < 1.0
        
        # Verify all activities were created
        count = db_session.query(Activity).filter(
            Activity.title.like("Transaction Activity%")
        ).count()
        assert count == 20


@pytest.mark.performance
@pytest.mark.slow
class TestMemoryUsage:
    """Test memory usage patterns."""
    
    def test_large_response_memory(self, client: TestClient, db_session: Session, test_user: User):
        """Test memory usage with large responses."""
        import psutil
        import os
        
        # Create many activities
        activities = []
        for i in range(500):
            activity = Activity(
                title=f"Memory Test Activity {i}",
                description="A" * 200,  # Larger description
                category="test",
                creator_id=test_user.id
            )
            activities.append(activity)
        
        db_session.add_all(activities)
        db_session.commit()
        
        # Measure memory before request
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss
        
        # Make request for large dataset
        response = client.get("/api/v1/activities/?limit=500")
        
        # Measure memory after request
        memory_after = process.memory_info().rss
        memory_increase = memory_after - memory_before
        
        assert response.status_code == 200
        assert len(response.json()) > 0
        
        # Memory increase should be reasonable (less than 50MB)
        assert memory_increase < 50 * 1024 * 1024
    
    def test_repeated_requests_memory_leak(self, client: TestClient):
        """Test for memory leaks with repeated requests."""
        import psutil
        import os
        import gc
        
        process = psutil.Process(os.getpid())
        
        # Measure initial memory
        gc.collect()
        initial_memory = process.memory_info().rss
        
        # Make many repeated requests
        for _ in range(100):
            response = client.get("/health")
            assert response.status_code == 200
        
        # Force garbage collection
        gc.collect()
        final_memory = process.memory_info().rss
        
        # Memory should not grow significantly
        memory_growth = final_memory - initial_memory
        
        # Allow for some memory growth but not excessive (less than 10MB)
        assert memory_growth < 10 * 1024 * 1024


@pytest.mark.performance
@pytest.mark.slow
class TestResponseTime:
    """Test response time characteristics."""
    
    def test_response_time_consistency(self, client: TestClient):
        """Test that response times are consistent."""
        response_times = []
        
        # Make multiple requests and measure response times
        for _ in range(20):
            start_time = time.time()
            response = client.get("/health")
            end_time = time.time()
            
            assert response.status_code == 200
            response_times.append(end_time - start_time)
        
        # Calculate statistics
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        min_time = min(response_times)
        
        # Response times should be consistent
        assert avg_time < 0.1  # Average should be under 100ms
        assert max_time < 0.2  # Maximum should be under 200ms
        assert (max_time - min_time) < 0.1  # Variation should be small
    
    def test_response_time_under_load(self, client: TestClient, test_activities: list):
        """Test response times under simulated load."""
        def measure_response_time():
            start_time = time.time()
            response = client.get("/api/v1/activities/")
            end_time = time.time()
            return end_time - start_time, response.status_code == 200
        
        # Simulate concurrent load
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            futures = [executor.submit(measure_response_time) for _ in range(30)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        response_times = [result[0] for result in results]
        success_rates = [result[1] for result in results]
        
        # All requests should succeed
        assert all(success_rates)
        
        # Response times should remain reasonable under load
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        
        assert avg_time < 1.0  # Average should be under 1 second
        assert max_time < 2.0  # Maximum should be under 2 seconds


@pytest.mark.performance
@pytest.mark.slow
class TestScalability:
    """Test system scalability characteristics."""
    
    def test_linear_scaling_with_data_size(self, client: TestClient, db_session: Session, test_user: User):
        """Test that response time scales reasonably with data size."""
        response_times = {}
        
        # Test with different data sizes
        for size in [10, 50, 100, 200]:
            # Clear existing data
            db_session.query(Activity).filter(
                Activity.title.like("Scaling Test%")
            ).delete()
            db_session.commit()
            
            # Create activities
            activities = []
            for i in range(size):
                activity = Activity(
                    title=f"Scaling Test Activity {i}",
                    category="test",
                    creator_id=test_user.id
                )
                activities.append(activity)
            
            db_session.add_all(activities)
            db_session.commit()
            
            # Measure response time
            start_time = time.time()
            response = client.get("/api/v1/activities/?limit=1000")
            end_time = time.time()
            
            response_times[size] = end_time - start_time
            assert response.status_code == 200
            assert len(response.json()) == size
        
        # Response time should scale reasonably (not exponentially)
        # The ratio between largest and smallest shouldn't be too high
        scaling_factor = response_times[200] / response_times[10]
        assert scaling_factor < 10  # Should not be more than 10x slower
    
    def test_concurrent_user_scaling(self, client: TestClient, multiple_users: list):
        """Test system performance with multiple concurrent users."""
        def simulate_user_session(user):
            """Simulate a typical user session."""
            start_time = time.time()
            
            # Login
            login_response = client.post("/api/v1/auth/login", json={
                "username": user.username,
                "password": "testpassword"
            })
            
            if login_response.status_code != 200:
                return False, time.time() - start_time
            
            # Browse activities
            activities_response = client.get("/api/v1/activities/")
            
            if activities_response.status_code != 200:
                return False, time.time() - start_time
            
            # Get health check
            health_response = client.get("/health")
            
            end_time = time.time()
            return health_response.status_code == 200, end_time - start_time
        
        # Simulate concurrent user sessions
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(multiple_users)) as executor:
            futures = [executor.submit(simulate_user_session, user) for user in multiple_users]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        success_rates = [result[0] for result in results]
        session_times = [result[1] for result in results]
        
        # Most sessions should succeed
        success_rate = sum(success_rates) / len(success_rates)
        assert success_rate > 0.8  # At least 80% success rate
        
        # Session times should be reasonable
        avg_session_time = sum(session_times) / len(session_times)
        assert avg_session_time < 3.0  # Average session under 3 seconds