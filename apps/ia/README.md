# La Vida Luca - FastAPI Backend

API backend for the La Vida Luca platform - AI-powered activity recommendations for MFR (Maison Familiale Rurale) educational programs.

## Features

- **Authentication**: JWT-based authentication system
- **User Management**: User registration, profiles, and preferences
- **Activity Management**: CRUD operations for educational activities
- **AI Recommendations**: OpenAI-powered activity recommendations
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **Testing**: Comprehensive test suite with pytest

## Quick Start

### Using Docker Compose (Recommended)

1. Clone and navigate to the backend directory:
```bash
cd apps/ia
```

2. Copy environment file and configure:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the services:
```bash
docker-compose up -d
```

4. The API will be available at `http://localhost:8000`
5. API documentation at `http://localhost:8000/docs`

### Manual Installation

1. Install Python 3.11+ and create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database and configure `.env`

4. Initialize database:
```bash
python init_db.py
```

5. Run the application:
```bash
uvicorn main:app --reload
```

## Configuration

Key environment variables (see `.env.example`):

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key (generate with `openssl rand -hex 32`)
- `OPENAI_API_KEY`: OpenAI API key for AI recommendations
- `ALLOWED_ORIGINS`: CORS origins (frontend URLs)

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user
- `POST /api/v1/users/me/profile` - Create user profile
- `PUT /api/v1/users/me/profile` - Update user profile

### Activities
- `GET /api/v1/activities/` - List activities (with filtering)
- `GET /api/v1/activities/{id}` - Get specific activity
- `GET /api/v1/activities/slug/{slug}` - Get activity by slug
- `GET /api/v1/activities/search/` - Search activities
- `POST /api/v1/activities/` - Create activity (admin only)
- `PUT /api/v1/activities/{id}` - Update activity (admin only)

### Recommendations
- `POST /api/v1/recommendations/generate` - Generate AI recommendations
- `GET /api/v1/recommendations/` - Get saved recommendations
- `POST /api/v1/recommendations/quick` - Quick recommendations from profile

## Database Schema

### Core Models

- **User**: Authentication and basic user info
- **UserProfile**: Detailed user preferences and skills
- **Activity**: Educational activities with metadata
- **Recommendation**: AI-generated activity recommendations
- **ActivitySession**: Track user participation in activities

### Default Data

The system includes 15 predefined activities across 5 categories:
- **agri**: Agriculture (livestock, crops)
- **transfo**: Transformation (dairy, preserves, bread)
- **artisanat**: Crafts (woodworking, repairs)
- **nature**: Environment (planting, composting)
- **social**: Animation (group hosting, children's workshops)

## AI Recommendations

The recommendation system uses OpenAI GPT-3.5-turbo to analyze user profiles and suggest relevant activities. Features:

- **Smart Matching**: Considers skills, availability, location, preferences
- **Educational Progression**: Recommends activities suited to user level
- **Safety Awareness**: Factors in safety levels and experience
- **Fallback System**: Rule-based recommendations when OpenAI unavailable

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

## Deployment

### Render (Production)

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python startup.py && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Configure environment variables in Render dashboard

### Environment Variables for Production

Required:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Strong random secret key
- `ALLOWED_ORIGINS`: Frontend domain(s)

Optional:
- `OPENAI_API_KEY`: For AI recommendations
- `SUPABASE_URL` + `SUPABASE_KEY`: Alternative to direct PostgreSQL

## Development

### Project Structure
```
apps/ia/
├── app/
│   ├── api/v1/endpoints/    # API route handlers
│   ├── core/                # Core functionality (auth, config, db)
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic (OpenAI integration)
│   └── tests/               # Test suite
├── main.py                  # FastAPI application
├── init_db.py              # Database initialization
├── requirements.txt         # Python dependencies
└── docker-compose.yml      # Local development setup
```

### Adding New Features

1. **New Model**: Add to `app/models/models.py`
2. **New Schema**: Add to `app/schemas/schemas.py` 
3. **New Endpoint**: Create in `app/api/v1/endpoints/`
4. **Add to Router**: Include in `app/api/v1/api.py`
5. **Add Tests**: Create test file in `app/tests/`

## Integration with Frontend

The API is designed to work with the Next.js frontend:

1. **CORS**: Configured to allow frontend domains
2. **Authentication**: JWT tokens for frontend auth
3. **Activity Data**: Matches frontend Activity interface
4. **Recommendations**: Provides AI suggestions for user onboarding

Set frontend environment variable:
```
NEXT_PUBLIC_IA_API_URL=https://your-api-domain.render.com
```

## Security

- JWT token authentication
- Password hashing with bcrypt
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy
- CORS configuration
- Request size limits
- Error handling without data leakage

## Monitoring

- Health check endpoint: `GET /health`
- Structured logging
- Error tracking and alerting
- Performance monitoring

## Support

For issues and questions:
- Check API documentation at `/docs`
- Review test examples in `app/tests/`
- Check logs for error details
- Verify environment configuration