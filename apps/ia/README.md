# LaVidaLuca FastAPI Backend

API backend for the LaVidaLuca application - a platform for agricultural education and training for young people in MFR (Maisons Familiales Rurales).

## Features

- **Authentication**: JWT-based user authentication and authorization
- **Activities Management**: CRUD operations for 30 agricultural, craft, and social activities
- **Bookings System**: Complete booking management with status tracking
- **User Profiles**: User management with skills, availability, and preferences
- **AI Recommendations**: OpenAI-powered activity suggestions based on user profiles
- **Analytics**: User activity tracking and platform analytics
- **Database**: PostgreSQL with Supabase integration and proper migrations

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+ or Supabase account
- Optional: OpenAI API key for AI recommendations

### Installation

1. **Clone and navigate to the backend directory:**
   ```bash
   cd apps/ia
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

4. **Set up database:**
   
   **Option A: Using Docker (recommended for development):**
   ```bash
   docker-compose up -d db
   ```
   
   **Option B: Using Supabase:**
   - Create a new Supabase project
   - Run the SQL from `infra/supabase/schema.sql` in the Supabase SQL editor
   - Run the SQL from `infra/supabase/seeds.sql` for sample data
   - Update your `.env` with Supabase credentials

5. **Run database migrations (if using local PostgreSQL):**
   ```bash
   alembic upgrade head
   ```

6. **Seed database with sample data:**
   ```bash
   python app/db/seed_data.py
   ```

7. **Start the development server:**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

## Docker Deployment

### Development with Docker Compose

```bash
docker-compose up
```

This starts both the API server and PostgreSQL database.

### Production Deployment

1. **Build the Docker image:**
   ```bash
   docker build -t lavidaluca-api .
   ```

2. **Run with environment variables:**
   ```bash
   docker run -p 8000:8000 \
     -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
     -e SECRET_KEY="your-secret-key" \
     -e OPENAI_API_KEY="your-openai-key" \
     lavidaluca-api
   ```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - Logout user

### Activities
- `GET /api/v1/activities/` - List activities (with pagination)
- `GET /api/v1/activities/{id}` - Get activity by ID
- `GET /api/v1/activities/slug/{slug}` - Get activity by slug
- `POST /api/v1/activities/` - Create activity (admin)
- `PUT /api/v1/activities/{id}` - Update activity (admin)
- `DELETE /api/v1/activities/{id}` - Delete activity (admin)

### Bookings
- `GET /api/v1/bookings/` - Get user's bookings
- `GET /api/v1/bookings/{id}` - Get specific booking
- `POST /api/v1/bookings/` - Create booking
- `PUT /api/v1/bookings/{id}` - Update booking
- `DELETE /api/v1/bookings/{id}` - Cancel booking

### User Profiles
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile
- `GET /api/v1/users/{id}` - Get public user profile

### AI Recommendations
- `POST /api/v1/recommendations/suggest` - Get AI-powered suggestions
- `GET /api/v1/recommendations/suggest/me` - Get suggestions for current user
- `GET /api/v1/recommendations/ai-status` - Check AI service status

### Analytics
- `POST /api/v1/analytics/events` - Track analytics event
- `GET /api/v1/analytics/dashboard` - Get user analytics dashboard
- `GET /api/v1/analytics/global` - Get global platform analytics
- `GET /api/v1/analytics/trends` - Get booking trends

## Environment Variables

```bash
# API Settings
DEBUG=True
API_V1_STR=/api/v1
PROJECT_NAME=LaVidaLuca API

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,https://la-vida-luca.vercel.app

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/lavidaluca

# Authentication
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# OpenAI (optional)
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-3.5-turbo

# Supabase (alternative to direct PostgreSQL)
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key
```

## Database Schema

The database includes the following main tables:

- **users**: User accounts with authentication and profile data
- **activities**: The 30 MFR activities with details and requirements
- **bookings**: Activity bookings with scheduling and status
- **activity_suggestions**: AI-generated activity recommendations
- **analytics_events**: User activity tracking for analytics

See `infra/supabase/schema.sql` for the complete schema.

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## Development

### Adding New Endpoints

1. Create endpoint in `app/api/endpoints/`
2. Add to router in `app/api/api.py`
3. Add tests in `tests/`
4. Update documentation

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Downgrade
alembic downgrade -1
```

### Code Quality

```bash
# Format code
black app/

# Lint code  
flake8 app/

# Type checking
mypy app/
```

## Deployment to Render

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set environment variables in Render dashboard
4. Deploy from `apps/ia` directory

## AI Integration

The API includes OpenAI integration for intelligent activity recommendations:

- **Fallback Mode**: If OpenAI API key is not provided, uses rule-based recommendations
- **Contextual**: Considers user skills, availability, preferences, and safety levels
- **Educational**: Optimized for MFR agricultural education context

## Security

- JWT authentication with configurable expiration
- Password hashing with bcrypt
- Row Level Security (RLS) policies for Supabase
- CORS configuration for frontend integration
- Input validation with Pydantic

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is part of the LaVidaLuca educational platform.