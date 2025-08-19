# LaVidaLuca FastAPI Backend

This is the complete FastAPI backend for the LaVidaLuca agricultural education platform.

## Features

- **Authentication**: JWT-based user authentication and authorization
- **User Management**: User registration, login, profile management
- **Activity Management**: CRUD operations for agricultural activities
- **AI Recommendations**: OpenAI-powered activity recommendations
- **Database**: SQLAlchemy with PostgreSQL (SQLite for development)
- **API Documentation**: Automatic OpenAPI/Swagger documentation

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL (optional, SQLite works for development)
- OpenAI API key (optional, falls back to rule-based recommendations)

### Installation

1. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Create sample data:
```bash
python seed_data.py
```

5. Run the server:
```bash
python main.py
```

The API will be available at http://localhost:8000

## API Documentation

- Swagger UI: http://localhost:8000/docs (development only)
- ReDoc: http://localhost:8000/redoc (development only)

## Default Users

After running `seed_data.py`:

- **Admin**: admin@lavidaluca.fr / admin123
- **Student**: etudiant@mfr.fr / password123

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user info

### Users
- `GET /api/v1/users/` - List users (admin only)
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user (admin only)

### Activities
- `GET /api/v1/activities/` - List activities with filtering
- `POST /api/v1/activities/` - Create activity
- `GET /api/v1/activities/{id}` - Get activity by ID
- `PUT /api/v1/activities/{id}` - Update activity
- `DELETE /api/v1/activities/{id}` - Delete activity

### Recommendations
- `POST /api/v1/recommendations/generate` - Generate AI recommendations
- `GET /api/v1/recommendations/` - Get user recommendations
- `PUT /api/v1/recommendations/{id}` - Update recommendation (feedback)

## Configuration

Key environment variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/lavidaluca

# JWT Authentication
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI (optional)
OPENAI_API_KEY=your-openai-api-key

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.com
```

## Project Structure

```
apps/ia/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── seed_data.py           # Database seeding script
├── app/
│   ├── api/v1/            # API endpoints
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── users.py       # User management
│   │   ├── activities.py  # Activity management
│   │   └── recommendations.py # AI recommendations
│   ├── core/              # Core functionality
│   │   ├── config.py      # Configuration settings
│   │   ├── database.py    # Database setup
│   │   └── security.py    # Authentication utilities
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   └── middleware/        # Custom middleware
└── tests/                 # Test suite
```

## Testing

Run tests with:

```bash
pytest
```

## Deployment

The application is designed to be deployed on platforms like Render, Railway, or similar. Key considerations:

1. Set `DEBUG=False` in production
2. Use PostgreSQL for production database
3. Configure proper CORS origins
4. Set a strong `SECRET_KEY`
5. Add OpenAI API key for AI features

## Integration with Frontend

This backend is designed to work with the Next.js frontend in `/src`. The API provides:

- CORS headers for frontend communication
- JWT tokens for authentication
- JSON responses compatible with frontend expectations
- Pagination and filtering for data lists

## AI Features

The recommendation system supports:

1. **OpenAI Integration**: Uses GPT-3.5-turbo for intelligent recommendations
2. **Fallback System**: Rule-based recommendations when OpenAI is unavailable
3. **User Preferences**: Filters based on difficulty, duration, and interests
4. **Feedback Loop**: Users can rate and provide feedback on recommendations

## License

This project is part of the LaVidaLuca educational platform.