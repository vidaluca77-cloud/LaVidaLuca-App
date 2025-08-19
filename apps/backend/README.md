# La Vida Luca Backend

FastAPI backend for the La Vida Luca educational platform.

## Features

- **FastAPI** framework with async support
- **PostgreSQL** database with SQLAlchemy ORM
- **JWT authentication** with role-based access control
- **OpenAI integration** for personalized activity suggestions
- **Rate limiting** and security middleware
- **Prometheus metrics** for monitoring
- **Docker** deployment ready
- **Comprehensive testing** with pytest

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Poetry (recommended) or pip

### Installation

1. **Clone and navigate to backend directory:**
```bash
cd apps/backend
```

2. **Install dependencies:**
```bash
# Using Poetry (recommended)
poetry install

# Or using pip
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Set up database:**
```bash
# Create database
createdb lavidaluca

# Run migrations
poetry run alembic upgrade head
```

5. **Start the application:**
```bash
# Development
poetry run uvicorn src.main:app --reload

# Or using Docker Compose
docker-compose up
```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | JWT signing secret | Required |
| `OPENAI_API_KEY` | OpenAI API key for AI features | Required |
| `ENVIRONMENT` | Application environment | development |
| `DEBUG` | Enable debug mode | false |
| `ALLOWED_ORIGINS` | CORS allowed origins | http://localhost:3000 |

See `.env.example` for complete list.

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/change-password` - Change password

### Users
- `GET /api/v1/users/` - List users (admin/moderator)
- `GET /api/v1/users/{id}` - Get user
- `PUT /api/v1/users/{id}` - Update user
- `PUT /api/v1/users/profile` - Update profile

### Activities
- `GET /api/v1/activities/` - List activities
- `GET /api/v1/activities/{id}` - Get activity
- `POST /api/v1/activities/` - Create activity (instructor+)
- `PUT /api/v1/activities/{id}` - Update activity
- `GET /api/v1/activities/suggestions` - Get AI suggestions

### Contact
- `POST /api/v1/contact/` - Submit contact form
- `GET /api/v1/contact/info` - Get contact information

## Database Schema

### Users
- Authentication and profile information
- Role-based access (student, instructor, moderator, admin)
- Profile data with skills and preferences

### Activities
- Educational activities with metadata
- Categories: agri, transfo, artisanat, nature, social
- Difficulty and safety levels
- Required materials and skills

### Activity Submissions
- User submissions for activities
- Progress tracking and assessment
- File attachments support

## Development

### Running Tests
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src

# Run specific test file
poetry run pytest tests/test_auth.py
```

### Code Quality
```bash
# Format code
poetry run black src tests

# Sort imports
poetry run isort src tests

# Lint code
poetry run flake8 src tests

# Type checking
poetry run mypy src
```

### Database Migrations
```bash
# Create new migration
poetry run alembic revision --autogenerate -m "Description"

# Apply migrations
poetry run alembic upgrade head

# Rollback migration
poetry run alembic downgrade -1
```

## Docker Deployment

### Development
```bash
docker-compose up
```

### Production
```bash
# Build image
docker build -t lavidaluca-backend .

# Run container
docker run -p 8000:8000 --env-file .env lavidaluca-backend
```

## Monitoring

### Metrics
- Prometheus metrics available at `/metrics`
- Custom application metrics
- System resource monitoring

### Logging
- Structured JSON logging
- Request/response logging
- Error tracking with context

### Health Checks
- Health endpoint at `/health`
- Database connectivity checks
- Service dependency monitoring

## Security

### Authentication
- JWT tokens with configurable expiration
- Password hashing with bcrypt
- Role-based access control

### Rate Limiting
- Per-endpoint rate limits
- IP-based limiting
- Configurable limits

### Input Validation
- Pydantic schemas for request validation
- Content type verification
- File size limits

### OpenAI Integration
- Content moderation for user-generated content
- Safe AI prompt engineering
- Error handling and fallbacks

## Architecture

```
apps/backend/
├── src/
│   ├── api/v1/          # API endpoints
│   ├── core/            # Core utilities
│   ├── db/              # Database configuration
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   └── main.py          # FastAPI application
├── tests/               # Test suite
├── alembic/             # Database migrations
├── docker-compose.yml   # Docker setup
└── pyproject.toml       # Dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run quality checks
5. Submit a pull request

### Code Standards
- Python 3.11+ with type hints
- Black code formatting
- isort import sorting
- Flake8 linting
- pytest for testing
- 90%+ test coverage

## License

MIT License - see LICENSE file for details.

## Support

- Documentation: `/docs` endpoint
- Issues: GitHub Issues
- Email: tech@lavidaluca.fr