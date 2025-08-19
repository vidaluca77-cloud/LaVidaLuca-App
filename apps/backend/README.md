# LaVidaLuca Backend

FastAPI backend for the LaVidaLuca application - a platform for agricultural education and social integration.

## Features

- **Authentication & Authorization**: JWT-based authentication with role-based access control
- **User Management**: Support for students, instructors, and administrators
- **Activity Management**: CRUD operations for agricultural and educational activities
- **Location Management**: Farm and location management
- **Booking System**: Activity booking and scheduling
- **Progress Tracking**: Student progress and skill development tracking
- **Messaging System**: Internal messaging between users

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **PostgreSQL**: Database (via Supabase)
- **Pydantic**: Data validation using Python type annotations
- **JWT**: Authentication tokens
- **Pytest**: Testing framework

## Setup

### Requirements

- Python 3.11+
- Poetry
- PostgreSQL (Supabase)

### Installation

1. Install dependencies:
```bash
poetry install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run database migrations:
```bash
poetry run alembic upgrade head
```

4. Start the development server:
```bash
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- Interactive API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost/db` |
| `SECRET_KEY` | JWT secret key | `your-secret-key` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |

## Project Structure

```
src/
├── api/                    # API routes
│   ├── v1/                # API version 1
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── users.py       # User management
│   │   ├── activities.py  # Activity management
│   │   ├── locations.py   # Location management
│   │   ├── bookings.py    # Booking management
│   │   └── progress.py    # Progress tracking
│   └── deps.py            # API dependencies
├── core/                  # Core configuration
│   ├── config.py          # Application configuration
│   ├── security.py        # Security utilities
│   └── settings.py        # Application settings
├── db/                    # Database
│   ├── base.py            # Base model and imports
│   └── session.py         # Database session
├── models/                # SQLAlchemy models
│   ├── user.py            # User model
│   ├── activity.py        # Activity model
│   ├── location.py        # Location model
│   ├── booking.py         # Booking model
│   ├── progress.py        # Progress model
│   └── message.py         # Message model
├── schemas/               # Pydantic schemas
│   └── ...                # Request/response schemas
├── services/              # Business logic
│   └── ...                # Service layer
└── main.py                # FastAPI application
```

## Testing

Run tests:
```bash
poetry run pytest
```

Run tests with coverage:
```bash
poetry run pytest --cov=src
```

## Development

Format code:
```bash
poetry run black src tests
poetry run isort src tests
```

Lint code:
```bash
poetry run flake8 src tests
poetry run mypy src
```