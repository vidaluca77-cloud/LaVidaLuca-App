"""
Test factories for creating test data using Factory Boy.

Provides consistent test data generation for models.
"""

import factory
from factory import fuzzy
from datetime import datetime, timedelta
import uuid

from app.models.user import User
from app.models.activity import Activity
from app.auth.password import hash_password


class UserFactory(factory.Factory):
    """Factory for creating User instances."""
    
    class Meta:
        model = User
    
    id = factory.LazyFunction(uuid.uuid4)
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    hashed_password = factory.LazyFunction(lambda: hash_password("TestPassword123!"))
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    
    # Profile data
    profile = factory.LazyFunction(lambda: {
        "bio": factory.Faker('text', max_nb_chars=200).generate(),
        "location": factory.Faker('city').generate(),
        "interests": factory.Faker('words', nb=3).generate()
    })
    
    # User status
    is_active = True
    is_verified = False
    is_superuser = False
    
    # Timestamps
    created_at = factory.LazyFunction(lambda: datetime.utcnow() - timedelta(days=30))
    updated_at = factory.LazyFunction(datetime.utcnow)
    last_login = factory.LazyFunction(lambda: datetime.utcnow() - timedelta(hours=1))


class AdminUserFactory(UserFactory):
    """Factory for creating admin User instances."""
    
    is_superuser = True
    is_verified = True
    email = factory.Sequence(lambda n: f"admin{n}@example.com")


class InactiveUserFactory(UserFactory):
    """Factory for creating inactive User instances."""
    
    is_active = False
    last_login = None


class ActivityFactory(factory.Factory):
    """Factory for creating Activity instances."""
    
    class Meta:
        model = Activity
    
    id = factory.LazyFunction(uuid.uuid4)
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text', max_nb_chars=500)
    
    category = fuzzy.FuzzyChoice([
        "sports", "art", "cooking", "outdoor", "indoor", 
        "education", "entertainment", "health", "social"
    ])
    
    difficulty_level = fuzzy.FuzzyChoice([
        "beginner", "intermediate", "advanced"
    ])
    
    estimated_duration = fuzzy.FuzzyInteger(15, 180)  # 15 minutes to 3 hours
    
    materials = factory.LazyFunction(lambda: [
        factory.Faker('word').generate() for _ in range(factory.Faker('random_int', min=1, max=5).generate())
    ])
    
    instructions = factory.LazyFunction(lambda: [
        f"Step {i+1}: {factory.Faker('sentence').generate()}" 
        for i in range(factory.Faker('random_int', min=3, max=8).generate())
    ])
    
    tags = factory.LazyFunction(lambda: 
        factory.Faker('words', nb=factory.Faker('random_int', min=1, max=5).generate()).generate()
    )
    
    # Timestamps
    created_at = factory.LazyFunction(lambda: datetime.utcnow() - timedelta(days=10))
    updated_at = factory.LazyFunction(datetime.utcnow)
    
    # Foreign keys (to be set when using the factory)
    creator_id = None


class PopularActivityFactory(ActivityFactory):
    """Factory for creating popular activities."""
    
    difficulty_level = "beginner"
    estimated_duration = fuzzy.FuzzyInteger(30, 60)  # 30-60 minutes
    category = fuzzy.FuzzyChoice(["sports", "art", "cooking"])


class AdvancedActivityFactory(ActivityFactory):
    """Factory for creating advanced activities."""
    
    difficulty_level = "advanced"
    estimated_duration = fuzzy.FuzzyInteger(120, 300)  # 2-5 hours
    
    materials = factory.LazyFunction(lambda: [
        factory.Faker('word').generate() for _ in range(factory.Faker('random_int', min=5, max=10).generate())
    ])
    
    instructions = factory.LazyFunction(lambda: [
        f"Step {i+1}: {factory.Faker('sentence', nb_words=10).generate()}" 
        for i in range(factory.Faker('random_int', min=8, max=15).generate())
    ])


# Utility functions for creating related objects

def create_user_with_activities(num_activities=3, **user_kwargs):
    """Create a user with associated activities."""
    user = UserFactory(**user_kwargs)
    activities = []
    
    for _ in range(num_activities):
        activity = ActivityFactory(creator_id=user.id)
        activities.append(activity)
    
    return user, activities


def create_test_dataset(num_users=5, activities_per_user=3):
    """Create a complete test dataset with users and activities."""
    users = []
    all_activities = []
    
    for _ in range(num_users):
        user, activities = create_user_with_activities(activities_per_user)
        users.append(user)
        all_activities.extend(activities)
    
    return users, all_activities


def create_admin_with_activities(num_activities=5):
    """Create an admin user with activities."""
    admin = AdminUserFactory()
    activities = []
    
    for _ in range(num_activities):
        activity = ActivityFactory(creator_id=admin.id)
        activities.append(activity)
    
    return admin, activities


# Batch creation utilities

class BatchUserFactory:
    """Utility for creating multiple users efficiently."""
    
    @staticmethod
    def create_batch(size=10, **kwargs):
        """Create a batch of users."""
        return [UserFactory(**kwargs) for _ in range(size)]
    
    @staticmethod
    def create_diverse_batch(size=10):
        """Create a diverse batch of users with different characteristics."""
        users = []
        for i in range(size):
            if i % 5 == 0:
                user = AdminUserFactory()
            elif i % 7 == 0:
                user = InactiveUserFactory()
            else:
                user = UserFactory()
            users.append(user)
        return users


class BatchActivityFactory:
    """Utility for creating multiple activities efficiently."""
    
    @staticmethod
    def create_batch(size=10, creator_id=None, **kwargs):
        """Create a batch of activities."""
        activities = []
        for _ in range(size):
            activity_kwargs = kwargs.copy()
            if creator_id:
                activity_kwargs['creator_id'] = creator_id
            activities.append(ActivityFactory(**activity_kwargs))
        return activities
    
    @staticmethod
    def create_category_batch(category, size=5, **kwargs):
        """Create a batch of activities in a specific category."""
        kwargs['category'] = category
        return BatchActivityFactory.create_batch(size, **kwargs)
    
    @staticmethod
    def create_difficulty_batch(difficulty, size=5, **kwargs):
        """Create a batch of activities with specific difficulty."""
        kwargs['difficulty_level'] = difficulty
        return BatchActivityFactory.create_batch(size, **kwargs)


# Performance testing data generators

def generate_load_test_users(count=100):
    """Generate users for load testing."""
    return [
        {
            "email": f"loadtest_{i}@example.com",
            "password": "LoadTestPassword123!",
            "first_name": f"Load{i}",
            "last_name": "Test"
        }
        for i in range(count)
    ]


def generate_load_test_activities(count=500):
    """Generate activities for load testing."""
    categories = ["sports", "art", "cooking", "outdoor", "indoor"]
    difficulties = ["beginner", "intermediate", "advanced"]
    
    activities = []
    for i in range(count):
        activity = {
            "title": f"Load Test Activity {i}",
            "description": f"This is load test activity number {i} for performance testing.",
            "category": categories[i % len(categories)],
            "difficulty_level": difficulties[i % len(difficulties)],
            "estimated_duration": 30 + (i % 120),  # 30-150 minutes
            "materials": [f"Material {j}" for j in range(1, (i % 5) + 2)],
            "instructions": [f"Step {j}: Do something" for j in range(1, (i % 8) + 3)],
            "tags": [f"tag{j}" for j in range(1, (i % 4) + 2)]
        }
        activities.append(activity)
    
    return activities


# Test data validation utilities

def validate_user_data(user):
    """Validate user data for testing."""
    assert user.email is not None
    assert "@" in user.email
    assert user.hashed_password is not None
    assert len(user.hashed_password) > 20  # Hashed passwords should be long
    assert user.first_name is not None
    assert user.last_name is not None
    assert isinstance(user.is_active, bool)
    assert isinstance(user.is_verified, bool)
    assert isinstance(user.is_superuser, bool)


def validate_activity_data(activity):
    """Validate activity data for testing."""
    assert activity.title is not None
    assert len(activity.title) > 0
    assert activity.description is not None
    assert activity.category in [
        "sports", "art", "cooking", "outdoor", "indoor", 
        "education", "entertainment", "health", "social"
    ]
    assert activity.difficulty_level in ["beginner", "intermediate", "advanced"]
    assert activity.estimated_duration > 0
    assert isinstance(activity.materials, list)
    assert isinstance(activity.instructions, list)
    assert isinstance(activity.tags, list)


# Cleanup utilities for tests

def cleanup_test_data():
    """Clean up test data after tests."""
    # This would be implemented based on the database setup
    # For now, it's a placeholder for cleanup operations
    pass


# Export commonly used factories and utilities
__all__ = [
    'UserFactory',
    'AdminUserFactory', 
    'InactiveUserFactory',
    'ActivityFactory',
    'PopularActivityFactory',
    'AdvancedActivityFactory',
    'create_user_with_activities',
    'create_test_dataset',
    'create_admin_with_activities',
    'BatchUserFactory',
    'BatchActivityFactory',
    'generate_load_test_users',
    'generate_load_test_activities',
    'validate_user_data',
    'validate_activity_data',
    'cleanup_test_data'
]