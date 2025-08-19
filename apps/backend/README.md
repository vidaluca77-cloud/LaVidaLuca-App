# LaVidaLuca Backend API

Backend API for the LaVidaLuca-App project built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- **User Authentication**: JWT-based authentication with user registration and login
- **Activity Management**: CRUD operations for the 30 activities catalog
- **Personalized Recommendations**: AI-powered activity recommendations using OpenAI
- **Database Integration**: SQLAlchemy with PostgreSQL and Supabase support
- **Security**: Password hashing, JWT tokens, CORS protection
- **Documentation**: Auto-generated API docs with FastAPI

## Directory Structure

```
apps/backend/
├── app/
│   ├── core/
│   │   ├── config.py          # Application configuration
│   │   ├── database.py        # Database setup and session management
│   │   └── security.py        # Authentication and security utilities
│   ├── api/v1/endpoints/
│   │   ├── users.py           # User management endpoints
│   │   ├── activities.py      # Activity management endpoints
│   │   └── recommendations.py # AI recommendation endpoints
│   ├── models/
│   │   ├── user.py           # User SQLAlchemy model
│   │   └── activity.py       # Activity SQLAlchemy model
│   └── schemas/
│       ├── user.py           # User Pydantic schemas
│       └── activity.py       # Activity Pydantic schemas
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── cli.py                   # CLI utilities for setup and admin tasks
├── seed_activities.py       # Database seeding script
├── .env.example             # Environment variables template
└── Dockerfile               # Docker configuration
```

## Setup

### 1. Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_ANON_KEY`: Supabase anonymous key
- `OPENAI_API_KEY`: OpenAI API key for recommendations

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Setup database and seed activities
python cli.py setup

# Create admin user
python cli.py create-admin --email admin@lavidaluca.com --username admin --password your_password

# Check environment configuration
python cli.py check-env
```

### 4. Run the Application

```bash
# Development mode
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/login` - User login
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile

### Activities
- `GET /api/v1/activities/` - List all activities (with filtering)
- `GET /api/v1/activities/{id}` - Get activity by ID
- `GET /api/v1/activities/slug/{slug}` - Get activity by slug
- `POST /api/v1/activities/` - Create activity (admin only)
- `PUT /api/v1/activities/{id}` - Update activity (admin only)
- `DELETE /api/v1/activities/{id}` - Delete activity (admin only)

### Recommendations
- `GET /api/v1/recommendations/` - Get personalized recommendations
- `GET /api/v1/recommendations/ai-insights` - Get AI-powered insights

### System
- `GET /health` - Health check
- `GET /` - API information
- `GET /docs` - Interactive API documentation (development only)

## User Types

- **participant**: General users who can participate in public activities
- **mfr_student**: MFR students with access to exclusive activities
- **educator**: Educators who can see all activities
- **admin**: Full system access

## Activity Categories

- **agri**: Agriculture (livestock, crops, animal care)
- **transfo**: Transformation (cheese, preserves, bread)
- **artisanat**: Crafts (construction, repairs, woodwork)
- **nature**: Environment (planting, composting, biodiversity)
- **social**: Social activities (tours, workshops, events)

## Security Features

- Password hashing with bcrypt
- JWT tokens with expiration
- CORS protection
- Request logging and monitoring
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy

## Deployment

### Docker

```bash
# Build image
docker build -t lavidaluca-backend .

# Run container
docker run -p 8000:8000 --env-file .env lavidaluca-backend
```

### Render

The application is configured for deployment on Render:

1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Deploy with the provided Dockerfile

## Development

### Database Migrations

For database schema changes, use Alembic:

```bash
# Generate migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## API Testing

The backend has been tested and verified to work correctly. Here are some examples:

### 1. Health Check
```bash
curl http://localhost:8000/health
# Response: {"status":"healthy","version":"1.0.0","environment":"development"}
```

### 2. User Registration
```bash
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser", 
    "password": "testpassword123",
    "skills": ["sol", "plantes"],
    "preferences": ["agri", "nature"]
  }'
# Returns: JWT tokens and user profile
```

### 3. Get Activity Categories
```bash
curl http://localhost:8000/api/v1/activities/categories/
# Response: ["agri","transfo","artisanat","nature","social"]
```

### 4. Get Personalized Recommendations
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/v1/recommendations/
# Returns: Personalized activity recommendations with scores
```

The recommendation system successfully analyzes user skills and preferences to provide relevant activity suggestions with match scores.