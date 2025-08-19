# LaVidaLuca Backend API

FastAPI backend for the LaVidaLuca platform - A collaborative platform for agricultural education in MFR (Maisons Familiales Rurales).

## Features

- **FastAPI** with automatic OpenAPI documentation
- **PostgreSQL** database with SQLAlchemy ORM
- **JWT Authentication** system
- **Activities API** with CRUD operations
- **OpenAI Integration** for personalized activity suggestions
- **Database migrations** with Alembic
- **Unit tests** with pytest
- **CI/CD** with GitHub Actions
- **Deployment** ready for Render

## Quick Start

### 1. Installation

```bash
cd apps/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/lavidaluca
SECRET_KEY=your-super-secret-key
OPENAI_API_KEY=your-openai-api-key
```

### 3. Database Setup

```bash
# Initialize database (first time only)
alembic upgrade head

# Create a migration after model changes
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### 4. Run the Application

```bash
# Development server
python run.py

# Or with uvicorn directly
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **OpenAPI**: http://localhost:8000/api/v1/openapi.json

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Activities
- `GET /api/v1/activities/` - List activities (with filters)
- `GET /api/v1/activities/{id}` - Get specific activity
- `POST /api/v1/activities/` - Create activity (auth required)
- `PUT /api/v1/activities/{id}` - Update activity (auth required)
- `DELETE /api/v1/activities/{id}` - Delete activity (auth required)
- `GET /api/v1/activities/categories/` - Get activity categories

### AI Suggestions
- `GET /api/v1/suggestions/` - Get user's suggestions
- `POST /api/v1/suggestions/generate` - Generate AI suggestions

### Users
- `GET /api/v1/users/me` - Get current user profile
- `GET /api/v1/users/` - List users (superuser only)

## Project Structure

```
apps/backend/
├── app/
│   ├── api/
│   │   ├── deps.py              # Dependencies (auth, db)
│   │   ├── api.py               # API router
│   │   └── endpoints/           # API endpoints
│   │       ├── auth.py          # Authentication
│   │       ├── activities.py    # Activities CRUD
│   │       ├── users.py         # User management
│   │       └── suggestions.py   # AI suggestions
│   ├── core/
│   │   ├── config.py           # Settings
│   │   └── security.py         # JWT & password utils
│   ├── db/
│   │   └── database.py         # Database connection
│   ├── models/
│   │   └── models.py           # SQLAlchemy models
│   ├── schemas/
│   │   └── schemas.py          # Pydantic schemas
│   ├── services/
│   │   └── openai_service.py   # OpenAI integration
│   ├── tests/                  # Unit tests
│   └── main.py                 # FastAPI app
├── alembic/                    # Database migrations
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── render.yaml                 # Render deployment
└── README.md                   # This file
```

## Testing

```bash
# Run all tests
pytest app/tests/ -v

# Run with coverage
pytest app/tests/ --cov=app --cov-report=html

# Run specific test file
pytest app/tests/test_activities.py -v
```

## Deployment

### Render Deployment

1. **Fork/Clone** this repository
2. **Connect** your repository to Render
3. **Set environment variables**:
   - `DATABASE_URL` (auto-configured with PostgreSQL add-on)
   - `SECRET_KEY` (generate secure key)
   - `OPENAI_API_KEY` (your OpenAI API key)
4. **Deploy** using the `render.yaml` configuration

### Docker Deployment

```bash
# Build image
docker build -t lavidaluca-backend .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=your_db_url \
  -e SECRET_KEY=your_secret \
  -e OPENAI_API_KEY=your_key \
  lavidaluca-backend
```

## Development

### Adding New Endpoints

1. Create endpoint in `app/api/endpoints/`
2. Add schemas in `app/schemas/schemas.py`
3. Add models in `app/models/models.py` (if needed)
4. Create migration: `alembic revision --autogenerate -m "Add feature"`
5. Add tests in `app/tests/`

### Database Changes

1. Modify models in `app/models/models.py`
2. Generate migration: `alembic revision --autogenerate -m "Description"`
3. Review generated migration in `alembic/versions/`
4. Apply migration: `alembic upgrade head`

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `SECRET_KEY` | JWT signing key | Yes |
| `OPENAI_API_KEY` | OpenAI API key for suggestions | No |
| `ALLOWED_HOSTS` | CORS allowed origins | No |

## Architecture

The backend follows a clean architecture pattern:

- **FastAPI** application with dependency injection
- **SQLAlchemy** models with Alembic migrations
- **Pydantic** schemas for request/response validation
- **JWT** authentication with role-based access
- **Service layer** for business logic (OpenAI integration)
- **Repository pattern** through SQLAlchemy ORM

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License.