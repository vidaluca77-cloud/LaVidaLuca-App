# SQLAlchemy Models and Alembic Migrations Implementation

## Overview
This implementation provides a comprehensive SQLAlchemy models structure with Alembic migrations for the La Vida Luca application.

## Files Created/Modified

### 1. `models/base.py`
- **BaseEntityMixin**: Combined mixin with UUID, timestamps, and utility methods
- **TimestampMixin**: Provides `created_at` and `updated_at` fields
- **UUIDMixin**: Provides UUID primary key
- **BaseModelMixin**: Common methods like `to_dict()`, `update_from_dict()`, `__repr__()`
- **Base**: Declarative base for all models

### 2. `models/user.py`
- Enhanced User model with role-based access control
- **New field**: `role` (user, admin, moderator)
- **Relationships**: 
  - `activities` (one-to-many with Activity)
  - `assigned_contacts` (one-to-many with Contact)
- **Indexes**: Optimized for email, role, and login tracking

### 3. `models/activity.py`
- Comprehensive Activity model for educational content
- **Relationship**: `creator` (many-to-one with User)
- **Indexes**: Optimized for search by category, difficulty, duration, age range
- **Features**: Full-text search support, categorization, metadata

### 4. `models/contact.py`
- Contact management model with status tracking
- **Relationship**: `assigned_user` (many-to-one with User)
- **Indexes**: Optimized for status tracking, assignment, and response management
- **Features**: Priority handling, response tracking, privacy consent

### 5. `migrations/env.py`
- Updated Alembic configuration
- Proper model imports and metadata setup
- Dynamic database URL loading from settings

### 6. `migrations/versions/001_initial_models.py`
- Complete initial migration
- All tables with proper constraints
- Foreign key relationships
- Comprehensive indexing strategy

## Key Features Implemented

### UUID Support
- All models use UUID primary keys
- PostgreSQL UUID type with automatic generation
- Better security and distribution capabilities

### Timestamp Management
- Automatic `created_at` and `updated_at` tracking
- Timezone-aware datetime fields
- Server-side default values

### Relationships
- **User → Activities**: One user can create many activities
- **User → Contacts**: One user can be assigned many contacts
- Proper back_populates for bidirectional relationships

### Search Optimization
Comprehensive indexing strategy:

#### User Model
- `ix_users_email_active`: Email + active status
- `ix_users_role`: Role-based queries
- `ix_users_last_login`: Login analytics

#### Activity Model
- `ix_activities_category_published`: Category filtering
- `ix_activities_difficulty_published`: Difficulty-based search
- `ix_activities_title_search`: Title search
- `ix_activities_duration`: Duration-based filtering
- `ix_activities_age_range`: Age appropriateness

#### Contact Model
- `ix_contacts_status_priority`: Status and priority management
- `ix_contacts_assigned_status`: Assignment tracking
- `ix_contacts_response_tracking`: Response management

### Validation and Constraints
- Required fields properly marked as nullable=False
- Foreign key constraints with proper references
- Default values for common fields
- Array fields for flexible multi-value storage

## Usage Examples

### Creating a User
```python
from models import User

user = User(
    email="user@example.com",
    hashed_password="...",
    role="user",
    first_name="John",
    last_name="Doe"
)
```

### Creating an Activity
```python
from models import Activity

activity = Activity(
    title="Organic Gardening Basics",
    category="agri",
    summary="Learn the fundamentals of organic gardening",
    duration_min=120,
    difficulty_level=2,
    created_by=user.id
)
```

### Creating a Contact
```python
from models import Contact

contact = Contact(
    name="Jane Smith",
    email="jane@example.com",
    subject="Partnership Inquiry",
    message="Interested in collaboration...",
    contact_type="partnership"
)
```

## Migration Management

### Run Migrations
```bash
# Apply migrations
alembic upgrade head

# Create new migration (if models change)
alembic revision --autogenerate -m "Description of changes"
```

### Check Migration Status
```bash
alembic current
alembic history
```

## Testing
Run the validation script to verify model structure:
```bash
python test_models.py
```

## Best Practices Implemented

1. **Separation of Concerns**: Mixins for reusable functionality
2. **Performance**: Strategic indexing for common queries
3. **Flexibility**: JSON fields for extensible metadata
4. **Security**: UUID primary keys, role-based access
5. **Maintainability**: Clear relationships and constraints
6. **Scalability**: Optimized for PostgreSQL features

## Future Enhancements

Potential improvements that could be added:
- Full-text search indexes for title/description fields
- Soft delete functionality
- Audit trail tracking
- Additional relationship models (tags, categories, etc.)
- Database-level constraints for enums
- Partitioning for large tables