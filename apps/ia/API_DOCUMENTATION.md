# La Vida Luca - FastAPI Backend

Complete FastAPI backend implementation for the La Vida Luca educational platform.

## 🚀 Features

- **Authentication System**: JWT-based authentication with user registration and login
- **User Management**: User profiles with skills, availability, and preferences 
- **Activity Management**: CRUD operations for agricultural/educational activities
- **AI Recommendations**: OpenAI-powered activity recommendations based on user profiles
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Testing**: Comprehensive test suite with pytest
- **Security**: Password hashing, CORS middleware, input validation

## 📁 Project Structure

```
apps/ia/
├── app/
│   ├── api/               # API route handlers
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── users.py       # User management endpoints
│   │   ├── activities.py  # Activity CRUD endpoints
│   │   └── recommendations.py # AI recommendation endpoints
│   ├── core/              # Core configuration
│   │   ├── config.py      # Settings and configuration
│   │   └── security.py    # JWT and password utilities
│   ├── db/                # Database configuration
│   │   └── database.py    # Database session management
│   ├── models/            # SQLAlchemy models
│   │   └── models.py      # User, Activity, Recommendation models
│   ├── schemas/           # Pydantic schemas
│   │   └── schemas.py     # Request/response schemas
│   ├── services/          # Business logic services
│   │   └── openai_service.py # OpenAI integration
│   ├── utils/             # Utility functions
│   │   └── dependencies.py # FastAPI dependencies
│   └── main.py            # FastAPI application
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
├── init_db.py            # Database initialization script
├── Dockerfile            # Docker configuration
└── README.md             # This file
```

## 🛠️ Setup & Installation

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key (generate a random string)
- `OPENAI_API_KEY`: OpenAI API key for recommendations
- `ALLOWED_ORIGINS`: Frontend domains for CORS

### 3. Database Setup

```bash
# Initialize database with sample data
python init_db.py
```

This will:
- Create all database tables
- Seed with sample activities
- Create an admin user (username: `admin`, password: `admin123`)

### 4. Start Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## 🧪 Testing

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app

# Run specific test file
python -m pytest tests/test_auth.py -v
```

## 🐳 Docker Deployment

```bash
# Build image
docker build -t lavidaluca-api .

# Run container
docker run -p 8000:8000 --env-file .env lavidaluca-api
```

## 🚀 Production Deployment

### Render.com

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in the Render dashboard

### Environment Variables for Production

```bash
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-production-secret-key
OPENAI_API_KEY=sk-your-openai-api-key
ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
ENVIRONMENT=production
```

## 🔐 API Authentication

Most endpoints require authentication. To access protected endpoints:

1. **Register a user**: `POST /auth/register`
2. **Login**: `POST /auth/login`
3. **Use the token**: Include `Authorization: Bearer <token>` header

Example:
```bash
# Register
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"testpass"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'

# Use authenticated endpoint
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer <your-token>"
```

## 🎯 Key Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /auth/token` - OAuth2 compatible token endpoint

### Users
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update current user profile
- `GET /users/` - List users (admin only)

### Activities
- `GET /activities/` - List all activities
- `GET /activities/{id}` - Get activity by ID
- `GET /activities/slug/{slug}` - Get activity by slug
- `POST /activities/` - Create activity (admin only)
- `PUT /activities/{id}` - Update activity (admin only)

### Recommendations
- `POST /recommendations/` - Get AI-powered recommendations
- `GET /recommendations/history` - Get user's recommendation history

## 🧠 AI Integration

The recommendation system uses OpenAI's GPT-3.5-turbo to analyze user profiles and suggest relevant activities. It considers:

- User skills and experience
- Availability and preferences  
- Activity difficulty and requirements
- Seasonal appropriateness
- Safety considerations

If OpenAI is not configured, it falls back to a rule-based recommendation system.

## 🔧 Configuration

### Settings (app/core/config.py)

The application uses Pydantic Settings for configuration management. All settings can be configured via environment variables.

### Database Models

- **User**: Authentication and profile information
- **Activity**: Educational activities with metadata
- **Recommendation**: AI-generated recommendations with scoring

### Security

- JWT tokens for authentication
- Password hashing with bcrypt
- CORS middleware for frontend integration
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy

## 🤝 Integration with Frontend

This API is designed to work with the Next.js frontend in `/apps/web`. Key integration points:

- User authentication and session management
- Activity catalog display and filtering
- Personalized activity recommendations
- User profile management

## 📝 Development Notes

### Database Compatibility

The models use JSON columns for array data to maintain compatibility with both PostgreSQL (production) and SQLite (testing).

### Error Handling

Global exception handlers provide consistent error responses and logging.

### Testing Strategy

- Unit tests for individual components
- Integration tests for API endpoints
- Test database isolation for reliable testing

## 🐛 Troubleshooting

### Common Issues

1. **Database connection errors**: Check `DATABASE_URL` format
2. **Import errors**: Ensure virtual environment is activated
3. **Authentication failures**: Verify `SECRET_KEY` is set
4. **CORS errors**: Check `ALLOWED_ORIGINS` includes your frontend domain

### Logs

The application logs to stdout. In production, configure your hosting platform to capture and store logs.

## 📄 License

This project is part of the La Vida Luca educational platform.