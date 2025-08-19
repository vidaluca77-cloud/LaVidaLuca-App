# La Vida Luca Backend API

FastAPI backend for the La Vida Luca application providing user authentication and activity management.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Activity Management**: CRUD operations for user activities
- **Database Integration**: SQLAlchemy with SQLite (configurable)
- **API Documentation**: Automatic Swagger/OpenAPI documentation
- **CORS Support**: Configurable CORS for frontend integration

## Quick Start

1. **Start the server**:
   ```bash
   ./start.sh
   ```

2. **Manual setup** (if needed):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn src.main:app --reload
   ```

3. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user (returns JWT token)

### Activities (requires authentication)
- `GET /activities/` - Get user's activities
- `POST /activities/` - Create new activity
- `GET /activities/{id}` - Get specific activity

## Testing

Run the test suite:
```bash
source venv/bin/activate
python -m pytest tests/ -v
```

## Configuration

Environment variables (create `.env` file):
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./lavidaluca.db
ALLOWED_ORIGINS=["http://localhost:3000"]
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Project Structure

```
apps/backend/
├── src/
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database configuration
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── activities.py     # Activities router
│   └── auth/
│       ├── router.py     # Authentication router
│       └── utils.py      # Auth utilities (JWT, passwords)
├── tests/
│   ├── test_auth.py      # Authentication tests
│   └── test_api.py       # API endpoint tests
├── requirements.txt      # Python dependencies
└── start.sh             # Startup script
```

## Dependencies

- **FastAPI**: Modern web framework for APIs
- **SQLAlchemy**: Database ORM
- **Passlib**: Password hashing
- **python-jose**: JWT token handling
- **Uvicorn**: ASGI server
- **Pytest**: Testing framework