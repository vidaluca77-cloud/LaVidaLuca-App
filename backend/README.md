# La Vida Luca - Backend API

A complete FastAPI backend implementation for the La Vida Luca collaborative platform.

## 🚀 Quick Start

### Development Setup

1. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Copy environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Run the server:**
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. **Access the API:**
- API Root: http://localhost:8000/
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## 🏗️ Architecture

### Tech Stack
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM with async support
- **PostgreSQL/SQLite** - Database (SQLite for dev, PostgreSQL for prod)
- **JWT** - Authentication tokens
- **OpenAI** - AI-powered suggestions
- **Pydantic** - Data validation and serialization
- **pytest** - Testing framework

### Project Structure
```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker container definition
├── .env.example           # Environment variables template
├── database/              # Database models and configuration
│   ├── database.py        # Database connection and session management
│   └── models.py          # SQLAlchemy models
├── schemas/               # Pydantic schemas for API
│   └── schemas.py         # Request/response models
├── auth/                  # Authentication logic
│   └── auth.py            # JWT handling and password management
├── routers/               # API route handlers
│   ├── auth.py            # Authentication endpoints
│   ├── activities.py      # Activity management endpoints
│   ├── users.py           # User profile endpoints
│   └── suggestions.py     # AI suggestions endpoints
├── ai/                    # AI integration
│   └── suggestions.py     # OpenAI-powered recommendations
├── monitoring/            # Logging and metrics
│   ├── logger.py          # Structured logging
│   └── metrics.py         # Prometheus metrics
├── docs/                  # API documentation
│   └── openapi.py         # Custom OpenAPI configuration
└── tests/                 # Unit tests
    ├── conftest.py        # Test configuration and fixtures
    ├── test_auth.py       # Authentication tests
    └── test_activities.py # Activity tests
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Registration
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "first_name": "John",
    "last_name": "Doe",
    "skills": ["agriculture", "sustainability"],
    "availability": ["weekends"],
    "location": "Rural France"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login-json \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

### Using Tokens
Include the JWT token in the Authorization header:
```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8000/api/auth/me
```

## 📚 API Endpoints

### Health & Info
- `GET /` - API information
- `GET /health` - Health check endpoint

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login (form-based)
- `POST /api/auth/login-json` - Login (JSON)
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/refresh` - Refresh JWT token

### Activities
- `GET /api/activities/` - List activities (paginated, filterable)
- `POST /api/activities/` - Create new activity
- `GET /api/activities/{id}` - Get specific activity
- `PUT /api/activities/{id}` - Update activity
- `DELETE /api/activities/{id}` - Delete activity
- `GET /api/activities/categories/list` - Get available categories

### Users
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update current user profile
- `GET /api/users/{id}` - Get public user profile
- `POST /api/users/activities` - Add activity interaction
- `GET /api/users/activities/me` - Get user's activity history
- `DELETE /api/users/activities/{id}` - Remove activity interaction

### AI Suggestions
- `GET /api/suggestions/` - Get personalized suggestions
- `PUT /api/suggestions/{id}` - Update suggestion (mark viewed/clicked)
- `DELETE /api/suggestions/{id}` - Dismiss suggestion
- `GET /api/suggestions/stats` - Get suggestion statistics

## 🎯 Key Features

### 1. **Activity Management**
- CRUD operations for activities
- Categorization (agri, transfo, artisanat, nature, social)
- Skill tagging and safety levels
- Material requirements and location types
- Search and filtering capabilities

### 2. **User Profiles**
- Skills and availability tracking
- Activity completion history
- Favorites and interests
- Location-based preferences

### 3. **AI-Powered Suggestions**
- OpenAI integration for personalized recommendations
- Fallback to rule-based suggestions
- User interaction tracking (viewed, clicked, dismissed)
- Performance metrics and analytics

### 4. **Authentication & Security**
- JWT-based authentication
- Password hashing with bcrypt
- Token refresh mechanism
- User session management

### 5. **Database Design**
- Async SQLAlchemy for performance
- Proper relationships and constraints
- Migration support with Alembic
- Flexible JSON fields for dynamic data

## 🐳 Deployment

### Docker
```bash
cd backend
docker build -t lavidaluca-backend .
docker run -p 8000:8000 -e DATABASE_URL="your_db_url" lavidaluca-backend
```

### Render.com
The project includes `render.yaml` for easy deployment to Render:
1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Deploy automatically

### Environment Variables
Required environment variables:
```bash
DATABASE_URL=postgresql://user:pass@host:port/db
JWT_SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key  # Optional
CORS_ORIGINS=https://yourdomain.com
```

## 🧪 Testing

Run the test suite:
```bash
cd backend
python -m pytest tests/ -v
```

Run with coverage:
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

## 📊 Monitoring

The API includes built-in monitoring:
- **Structured JSON logging** for all requests and errors
- **Prometheus metrics** for performance monitoring
- **Request/response tracking** with timing
- **AI service monitoring** with success/failure rates

Access metrics at: `http://localhost:8000/metrics`

## 🔧 Development

### Code Quality
```bash
# Linting
flake8 --max-line-length=100 .

# Formatting
black .
isort .
```

### Database Migrations
```bash
# Generate migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## 🌐 Production Considerations

1. **Database**: Use PostgreSQL for production
2. **Environment**: Set `ENVIRONMENT=production`
3. **Secrets**: Use proper secret management
4. **CORS**: Configure allowed origins
5. **Monitoring**: Set up Sentry for error tracking
6. **Scaling**: Use gunicorn with multiple workers

## 📖 API Documentation

When the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

The documentation is automatically generated from the code and includes:
- Interactive API explorer
- Request/response schemas
- Authentication examples
- Error response formats

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.