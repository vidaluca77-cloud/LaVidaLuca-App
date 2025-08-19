# La Vida Luca Backend API

FastAPI backend application for the La Vida Luca platform - a collaborative platform for rural education (MFR) and sustainable agriculture development.

## Features

- **FastAPI** web framework with automatic API documentation
- **PostgreSQL** database with SQLAlchemy ORM
- **JWT Authentication** for secure API access
- **OpenAI Integration** for AI-powered activity suggestions
- **Comprehensive API** for activities, users, and contacts management
- **Database Migrations** with Alembic
- **Testing Suite** with pytest
- **Production Ready** with Docker and Render deployment

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- OpenAI API key (optional, for AI features)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
cd LaVidaLuca-App/apps/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the backend directory:
```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/lavidaluca_dev

# JWT Secret (generate a secure random key)
JWT_SECRET_KEY=your-super-secret-jwt-key-here

# OpenAI (optional)
OPENAI_API_KEY=your-openai-api-key

# Environment
ENVIRONMENT=development
DEBUG=true
```

5. **Set up database**
```bash
# Create database
createdb lavidaluca_dev

# Run migrations
alembic upgrade head
```

6. **Start the development server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Documentation

### Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Main Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/verify-token` - Verify token

#### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile
- `GET /api/v1/users/{user_id}` - Get user by ID

#### Activities
- `GET /api/v1/activities/` - List activities with filters
- `POST /api/v1/activities/` - Create new activity
- `GET /api/v1/activities/{id}` - Get activity by ID
- `PUT /api/v1/activities/{id}` - Update activity
- `DELETE /api/v1/activities/{id}` - Delete activity

#### Contacts
- `POST /api/v1/contacts/` - Submit contact form
- `GET /api/v1/contacts/` - List contacts (admin only)
- `GET /api/v1/contacts/{id}` - Get contact by ID (admin only)
- `PUT /api/v1/contacts/{id}` - Update contact (admin only)

#### AI Suggestions
- `POST /api/v1/suggestions/` - Get personalized suggestions
- `GET /api/v1/suggestions/featured` - Get featured activities
- `GET /api/v1/suggestions/similar/{id}` - Get similar activities

## Database Schema

### Users
- User authentication and profile management
- JWT-based authentication
- Role-based access control

### Activities
- Educational activities and learning experiences
- Categorization by type (agriculture, crafts, nature, etc.)
- Skills and competencies mapping
- Safety and difficulty levels

### Contacts
- Contact form submissions
- Status tracking and assignment
- Admin management interface

## Testing

Run the test suite:
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

## Database Migrations

Create and apply database migrations:
```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Downgrade one revision
alembic downgrade -1
```

## Deployment

### Render Deployment

1. **Create a new Web Service** on Render
2. **Connect your GitHub repository**
3. **Configure build settings**:
   - Build Command: `cd apps/backend && pip install -r requirements.txt`
   - Start Command: `cd apps/backend && gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT`

4. **Set environment variables**:
```env
DATABASE_URL=postgresql://user:password@host:port/database
JWT_SECRET_KEY=your-production-jwt-secret
OPENAI_API_KEY=your-openai-api-key
ENVIRONMENT=production
```

5. **Deploy**
   - Render will automatically deploy when you push to the main branch

### Docker Deployment

```bash
# Build image
docker build -t lavidaluca-backend .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e JWT_SECRET_KEY=your-secret \
  lavidaluca-backend
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | Required |
| `JWT_EXPIRATION_HOURS` | JWT token expiration time | 24 |
| `OPENAI_API_KEY` | OpenAI API key for suggestions | Optional |
| `ENVIRONMENT` | Environment (development/production) | development |
| `DEBUG` | Enable debug mode | true |
| `CORS_ORIGINS` | Allowed CORS origins | localhost:3000 |

## Development

### Project Structure

```
apps/backend/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── database.py            # Database connection and setup
├── middleware.py          # Custom middleware
├── exceptions.py          # Exception handlers
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── alembic.ini           # Database migration config
├── auth/                 # Authentication utilities
│   ├── jwt_handler.py
│   ├── password.py
│   └── dependencies.py
├── models/               # SQLAlchemy models
│   ├── user.py
│   ├── activity.py
│   └── contact.py
├── schemas/              # Pydantic schemas
│   ├── auth.py
│   ├── user.py
│   ├── activity.py
│   ├── contact.py
│   └── common.py
├── routes/               # API endpoints
│   ├── auth.py
│   ├── users.py
│   ├── activities.py
│   ├── contacts.py
│   └── suggestions.py
├── services/             # Business logic
│   └── openai_service.py
├── migrations/           # Database migrations
│   └── versions/
└── tests/               # Test suite
    ├── conftest.py
    ├── test_auth.py
    └── test_activities.py
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and add tests
4. Run tests: `pytest`
5. Commit your changes: `git commit -m 'Add my feature'`
6. Push to the branch: `git push origin feature/my-feature`
7. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- **Documentation**: API docs available at `/docs` endpoint
- **Issues**: Report bugs and request features on GitHub Issues
- **Contact**: tech@lavidaluca.fr

---

**La Vida Luca** - Collaborative platform for rural education and sustainable agriculture development.