# LaVidaLuca Backend API

FastAPI backend for the LaVidaLuca platform providing authentication, activity management, and user profile services.

## Features

- **JWT Authentication**: Secure authentication with Bearer tokens
- **Activity Management**: Browse and register for activities
- **User Profiles**: Complete user profile management
- **Database Integration**: SQLAlchemy ORM with SQLite/PostgreSQL support
- **API Documentation**: Auto-generated OpenAPI/Swagger docs
- **Comprehensive Testing**: Full test suite with pytest

## Quick Start

### Prerequisites

- Python 3.12+
- pip (Python package manager)

### Installation

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize database:**
   ```bash
   python init_db.py
   ```

5. **Start the server:**
   ```bash
   python run.py
   ```

The API will be available at:
- **Main API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login with email/password to get JWT token

### Activities
- `GET /api/v1/activities` - List all activities (with optional category filter)
- `GET /api/v1/activities/{slug}` - Get activity details by slug
- `POST /api/v1/activities/{id}/register` - Register for an activity (requires auth)

### Users
- `GET /api/v1/users/me` - Get current user profile (requires auth)
- `PUT /api/v1/users/me` - Update user profile (requires auth)
- `GET /api/v1/users/me/activities` - List user's registered activities (requires auth)

## Authentication

The API uses JWT Bearer tokens for authentication. To access protected endpoints:

1. **Get a token:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=demo@lavidaluca.fr&password=demo123"
   ```

2. **Use the token:**
   ```bash
   curl -X GET "http://localhost:8000/api/v1/users/me" \
     -H "Authorization: Bearer <your-token>"
   ```

## Testing

Run the complete test suite:

```bash
python -m pytest app/tests/ -v
```

Run specific test files:

```bash
python -m pytest app/tests/test_activities.py -v
python -m pytest app/tests/test_users.py -v
```

## Database

The backend uses SQLAlchemy ORM with support for both SQLite (development) and PostgreSQL (production).

### Models

- **User**: User profiles with skills, availability, and preferences
- **Activity**: Activities with categories, durations, and requirements
- **UserActivityRegistration**: Many-to-many relationship for activity registrations

### Database Setup

For development (SQLite):
```bash
python init_db.py
```

For production, set `DATABASE_URL` in your environment:
```
DATABASE_URL=postgresql://user:password@localhost/lavidaluca
```

## Configuration

Environment variables (set in `.env` file):

```env
DATABASE_URL=sqlite:///./lavidaluca.db
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Project Structure

```
apps/backend/
├── app/
│   ├── api/v1/          # API route modules
│   ├── core/            # Core functionality (auth, config, deps)
│   ├── db/              # Database configuration
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   └── tests/           # Test suite
├── requirements.txt     # Python dependencies
├── run.py              # Development server
├── init_db.py          # Database initialization
└── .env.example        # Environment template
```

## Demo Data

The `init_db.py` script creates:

- **Demo User**: `demo@lavidaluca.fr` / `demo123`
- **Sample Activities**: 5 activities across different categories (agri, transfo, artisanat, nature)

## Development

### Adding New Endpoints

1. Create new route in `app/api/v1/`
2. Add Pydantic schemas in `app/schemas/`
3. Update database models if needed in `app/models/`
4. Add tests in `app/tests/`
5. Include router in `app/api/v1/router.py`

### Code Style

The project follows FastAPI best practices:
- Dependency injection for database sessions
- Pydantic for request/response validation
- SQLAlchemy for database operations
- JWT for authentication
- Comprehensive error handling

## Deployment

### Production Setup

1. Set environment variables for production
2. Use PostgreSQL for the database
3. Set a strong SECRET_KEY
4. Configure CORS origins
5. Use a production WSGI server like Gunicorn

Example production command:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## License

This project is part of the LaVidaLuca platform.