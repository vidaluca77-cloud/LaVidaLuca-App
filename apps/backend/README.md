# LaVidaLuca Backend API

FastAPI backend for the LaVidaLuca platform - Agricultural education and social insertion.

## Features

- FastAPI with automatic OpenAPI documentation
- JWT-based authentication
- PostgreSQL database with SQLAlchemy ORM
- Alembic database migrations
- CORS configuration for frontend integration
- Docker containerization
- Comprehensive test suite

## Project Structure

```
apps/backend/
├── alembic/              # Database migrations
├── app/
│   ├── api/             # API routes
│   │   ├── auth.py      # Authentication endpoints
│   │   ├── users.py     # User management
│   │   └── activities.py # Activity management
│   ├── core/            # Core configuration
│   │   ├── config.py    # Environment settings
│   │   ├── security.py  # JWT and password hashing
│   │   └── database.py  # Database connection
│   ├── models/          # SQLAlchemy models
│   │   ├── user.py      # User model
│   │   └── activity.py  # Activity model
│   └── schemas/         # Pydantic schemas
├── tests/               # Unit tests
├── Dockerfile          # Container configuration
├── docker-compose.yml   # Local development setup
├── requirements.txt     # Python dependencies
└── main.py             # Application entry point
```

## Quick Start

### Using Docker (Recommended)

1. Copy environment file:
```bash
cp .env.example .env
```

2. Start the services:
```bash
docker-compose up -d
```

3. Run database migrations:
```bash
docker-compose exec backend alembic upgrade head
```

4. Access the API:
- API: http://localhost:8000
- Documentation: http://localhost:8000/api/v1/docs
- Database Admin: http://localhost:5050 (admin@lavidaluca.dev / admin)

### Local Development

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Start PostgreSQL database (or use Docker for just the database)

5. Run migrations:
```bash
alembic upgrade head
```

6. Start the development server:
```bash
python main.py
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/token` - Login and get access token
- `GET /api/v1/auth/me` - Get current user profile

### Users
- `POST /api/v1/users/` - Register new user
- `GET /api/v1/users/profile/{username}` - Get public user profile
- `PUT /api/v1/users/me` - Update current user profile

### Activities
- `GET /api/v1/activities/` - List activities (with filtering)
- `GET /api/v1/activities/{id}` - Get activity by ID
- `GET /api/v1/activities/slug/{slug}` - Get activity by slug
- `GET /api/v1/activities/categories/` - Get available categories

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app
```

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

## Configuration

Key environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT signing secret
- `ALLOWED_ORIGINS`: CORS allowed origins (comma-separated)
- `DEBUG`: Enable debug mode
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration

## Production Deployment

1. Set production environment variables
2. Use a production WSGI server (uvicorn with gunicorn)
3. Set up proper database backup and monitoring
4. Configure SSL/TLS termination
5. Set up logging and error tracking

## Contributing

1. Create feature branch from main
2. Make changes with tests
3. Run test suite
4. Submit pull request