# La Vida Luca Backend API

Complete FastAPI backend implementation for the La Vida Luca collaborative platform.

## Features

- **FastAPI** web framework with automatic OpenAPI documentation
- **PostgreSQL** database with SQLAlchemy ORM
- **JWT Authentication** system with secure password hashing
- **Activity Management** - Full CRUD operations for educational activities
- **AI-Powered Suggestions** - OpenAI integration for personalized recommendations
- **Comprehensive Testing** - Unit tests with pytest
- **Docker Support** - Containerized deployment
- **Render Deployment** - Ready-to-deploy configuration

## Quick Start

### 1. Installation

```bash
cd apps/backend
pip install -r requirements.txt
```

### 2. Environment Setup

Copy the example environment file and configure:

```bash
cp .env.example .env
```

Configure your environment variables in `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/lavidaluca
SECRET_KEY=your-super-secret-key
OPENAI_API_KEY=your-openai-api-key
```

### 3. Database Setup

For development with SQLite:

```bash
DATABASE_URL="sqlite:///./app.db" python seed_data.py
```

### 4. Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at:
- **Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `PUT /api/auth/me` - Update user profile

### Activities
- `GET /api/activities/` - List activities (with pagination, filtering, search)
- `GET /api/activities/{id}` - Get specific activity
- `POST /api/activities/` - Create new activity (requires auth)
- `PUT /api/activities/{id}` - Update activity (requires auth)
- `DELETE /api/activities/{id}` - Delete activity (requires auth)
- `GET /api/activities/categories/list` - Get activity categories
- `POST /api/activities/suggestions` - Get AI-powered suggestions (requires auth)

### Health
- `GET /health` - Health check endpoint

## Project Structure

```
apps/backend/
├── main.py              # FastAPI application
├── database.py          # Database configuration
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── auth.py              # Authentication utilities
├── seed_data.py         # Database seeding script
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
├── pytest.ini          # Test configuration
├── .env.example         # Environment template
├── routers/
│   ├── auth.py          # Authentication routes
│   └── activities.py    # Activity routes
├── ai/
│   └── suggestions.py   # AI suggestion engine
└── tests/
    ├── test_auth.py     # Authentication tests
    └── test_activities.py # Activity tests
```

## Database Models

### User
- `id` - Unique identifier
- `email` - User email (unique)
- `hashed_password` - Secure password hash
- `profile` - JSON profile data (skills, interests, location, etc.)
- `is_active` - Account status
- `created_at` / `updated_at` - Timestamps

### Activity
- `id` - Unique identifier
- `title` - Activity title
- `category` - Activity category (agri, transfo, artisanat, nature, social)
- `summary` - Brief description
- `description` - Detailed description
- `duration_min` - Duration in minutes
- `skill_tags` - Associated skills (JSON array)
- `materials` - Required materials (JSON array)
- `safety_level` - Safety rating (1-5)
- `difficulty_level` - Difficulty rating (1-5)
- `location` - Activity location
- `creator_id` - Foreign key to creator user
- `engagement_score` / `success_rate` - AI metrics
- Timestamps and status fields

## Testing

Run the test suite:

```bash
# All tests
DATABASE_URL="sqlite:///./test.db" python -m pytest

# Specific test file
DATABASE_URL="sqlite:///./test.db" python -m pytest tests/test_auth.py -v

# With coverage
DATABASE_URL="sqlite:///./test.db" python -m pytest --cov=. tests/
```

## AI Suggestions

The suggestion system provides personalized activity recommendations based on:

- User skills and interests
- Activity difficulty vs user experience level
- Location proximity
- Safety considerations
- Engagement metrics

The system uses OpenAI GPT-3.5-turbo for enhanced suggestions but falls back to a rule-based system if the API is unavailable.

## Deployment

### Docker

```bash
docker build -t lavidaluca-backend .
docker run -p 8000:8000 -e DATABASE_URL="your-db-url" lavidaluca-backend
```

### Render

The application is configured for Render deployment with `render.yaml`. It automatically:

- Sets up PostgreSQL database
- Configures environment variables
- Deploys the application

## Security

- JWT tokens for authentication
- Password hashing with bcrypt
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy
- CORS configuration for cross-origin requests

## Monitoring

Integration with existing monitoring utilities:
- Structured JSON logging
- Prometheus metrics
- Request/response tracking
- Error monitoring
- Performance metrics

## Development

### Adding New Features

1. **New Models**: Add to `models.py` and create migration
2. **New Endpoints**: Add routes in appropriate router file
3. **Schemas**: Define request/response schemas in `schemas.py`
4. **Tests**: Add comprehensive tests in `tests/` directory

### Code Quality

- Type hints throughout the codebase
- Pydantic for data validation
- Comprehensive error handling
- Consistent code structure
- Automated testing

## Sample Data

Use the seeding script to populate the database with sample data:

```bash
python seed_data.py
```

This creates:
- 3 sample users with different profiles
- 5 sample activities across all categories
- Realistic engagement scores and success rates

## API Documentation

Interactive API documentation is automatically generated and available at:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

The documentation includes:
- All endpoint definitions
- Request/response schemas
- Authentication requirements
- Example requests and responses
- Error codes and descriptions

---

**La Vida Luca** - Empowering young farmers through collaborative education and sustainable practices.