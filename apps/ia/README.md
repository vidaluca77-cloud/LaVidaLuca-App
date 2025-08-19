# La Vida Luca FastAPI Backend

This directory contains the FastAPI backend for the La Vida Luca platform, providing APIs for authentication, activities management, registrations, and AI-powered activity suggestions.

## Features

- **Authentication**: User registration, login, JWT token management
- **Activities API**: CRUD operations for farm activities with filtering and search
- **Registrations API**: User registration for activities with status management
- **AI Suggestions**: Intelligent activity recommendations based on user profiles
- **Database Integration**: Supabase/PostgreSQL backend with proper schema
- **Comprehensive Testing**: Full test suite with pytest
- **API Documentation**: Automatic OpenAPI/Swagger documentation

## Project Structure

```
apps/ia/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application setup
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   ├── models.py            # Pydantic models
│   ├── auth/
│   │   ├── __init__.py
│   │   └── auth.py          # Authentication utilities
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       ├── activities.py    # Activities CRUD endpoints
│       ├── registrations.py # Registration management
│       └── ai.py            # AI suggestion endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   ├── test_main.py         # Main app tests
│   ├── test_auth.py         # Authentication tests
│   ├── test_activities.py   # Activities API tests
│   ├── test_registrations.py # Registration tests
│   └── test_ai.py           # AI suggestions tests
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── start.sh                # Development startup script
└── README.md               # This file
```

## Quick Start

1. **Setup Environment**:
   ```bash
   cd apps/ia
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

2. **Install Dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Setup Database**:
   - Create a Supabase project
   - Run the SQL from `../../infra/supabase/schema.sql`
   - Optionally run `../../infra/supabase/seeds.sql` for test data

4. **Start the Application**:
   ```bash
   ./start.sh
   # Or manually: uvicorn main:app --reload
   ```

5. **Access API Documentation**:
   - Open http://localhost:8000/docs for Swagger UI
   - Open http://localhost:8000/redoc for ReDoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - Logout

### Activities
- `GET /api/v1/activities/` - List activities (with filters)
- `GET /api/v1/activities/{id}` - Get specific activity
- `POST /api/v1/activities/` - Create new activity (admin)
- `PUT /api/v1/activities/{id}` - Update activity (admin)
- `DELETE /api/v1/activities/{id}` - Delete activity (admin)

### Registrations
- `GET /api/v1/registrations/` - List user registrations
- `GET /api/v1/registrations/{id}` - Get specific registration
- `POST /api/v1/registrations/` - Create new registration
- `PUT /api/v1/registrations/{id}` - Update registration
- `DELETE /api/v1/registrations/{id}` - Cancel registration

### AI Suggestions
- `POST /api/v1/ai/suggestions` - Get activity suggestions
- `GET /api/v1/ai/categories` - Get activity categories with counts
- `GET /api/v1/ai/skills` - Get available skills

## Testing

Run the test suite:

```bash
# Install test dependencies (included in requirements.txt)
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_activities.py
```

## Environment Variables

Create a `.env` file with the following variables:

```env
# FastAPI Settings
DEBUG=true
APP_NAME="La Vida Luca API"

# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# JWT Configuration
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Settings
ALLOWED_ORIGINS=["http://localhost:3000", "https://la-vida-luca.vercel.app"]
```

## Deployment

For production deployment on Render:

1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Use the following build command: `pip install -r requirements.txt`
4. Use the following start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Database Schema

The application uses the following main tables:
- `users` - User accounts and profiles
- `activities` - Farm activities with metadata
- `registrations` - User registrations for activities

See `../../infra/supabase/schema.sql` for the complete schema.

## Contributing

1. Follow PEP 8 style guidelines
2. Add tests for new features
3. Update documentation as needed
4. Ensure all tests pass before submitting PRs