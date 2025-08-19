# LaVidaLuca FastAPI Backend

This is the complete FastAPI backend for the LaVidaLuca App - an agricultural activities platform for MFR (Maison Familiale Rurale) students.

## Features

### 🔐 Authentication & Security
- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control (Student, Instructor, Admin)
- CORS configuration
- Rate limiting
- Input validation with Pydantic

### 👥 User Management
- User registration and login
- User profiles with detailed information
- MFR location tracking
- Experience level management

### 🌱 Activity Management
- Create and manage agricultural/artisanal activities
- Categories: Agriculture, Artisanat, Environnement
- Skill levels: Débutant, Intermédiaire, Avancé
- Activity sessions with scheduling
- Materials and prerequisites tracking

### 📝 Registration System
- Students can register for activity sessions
- Instructors can manage registrations
- Status tracking (Pending, Confirmed, Completed, Cancelled)
- Completion tracking with ratings and feedback

### 🗄️ Database
- SQLAlchemy models with proper relationships
- Alembic migrations
- PostgreSQL/SQLite support
- Data validation and constraints

### 🧪 Testing
- Comprehensive test suite with pytest
- Unit and integration tests
- Test fixtures and factories
- Database isolation for tests

### 🐳 Production Ready
- Docker configuration
- Environment-based configuration
- Logging
- Health checks
- Production-optimized Dockerfile

## Quick Start

### Development Setup

1. **Clone and navigate to the API directory:**
   ```bash
   cd apps/ia
   ```

2. **Create virtual environment and install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize database:**
   ```bash
   alembic upgrade head
   ```

5. **Run the server:**
   ```bash
   ./start.sh
   # OR manually:
   uvicorn app.main:app --reload
   ```

6. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Using Docker

1. **Start with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

2. **Or build and run manually:**
   ```bash
   docker build -t lavidaluca-api .
   docker run -p 8000:8000 lavidaluca-api
   ```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/login/form` - Login with form data (OAuth2 compatible)

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/me/profile` - Get user profile
- `POST /api/v1/users/me/profile` - Create user profile
- `PUT /api/v1/users/me/profile` - Update user profile
- `GET /api/v1/users/` - List all users (admin only)
- `GET /api/v1/users/{id}` - Get user by ID (admin only)
- `PUT /api/v1/users/{id}` - Update user (admin only)

### Activities
- `GET /api/v1/activities/` - List activities (public)
- `GET /api/v1/activities/{id}` - Get activity details
- `POST /api/v1/activities/` - Create activity (instructor/admin)
- `PUT /api/v1/activities/{id}` - Update activity (owner/admin)
- `DELETE /api/v1/activities/{id}` - Delete activity (owner/admin)
- `GET /api/v1/activities/categories/` - List categories
- `GET /api/v1/activities/levels/` - List levels
- `GET /api/v1/activities/instructor/{id}` - Get activities by instructor

### Registrations
- `GET /api/v1/registrations/` - Get user's registrations
- `GET /api/v1/registrations/{id}` - Get registration details
- `POST /api/v1/registrations/` - Register for activity
- `PUT /api/v1/registrations/{id}` - Update registration
- `DELETE /api/v1/registrations/{id}` - Cancel registration

### Activity Sessions
- `GET /api/v1/registrations/sessions/activity/{id}` - Get sessions for activity
- `POST /api/v1/registrations/sessions/` - Create session (instructor/admin)

## Data Models

### User Roles
- **Student**: Can view and register for activities
- **Instructor**: Can create and manage activities, view registrations
- **Admin**: Full access to all features

### Activity Categories
- **Agriculture**: Farming, cultivation, livestock
- **Artisanat**: Crafts, traditional skills
- **Environnement**: Environmental conservation, sustainability

### Activity Levels
- **Débutant**: Beginner level
- **Intermédiaire**: Intermediate level  
- **Avancé**: Advanced level

## Testing

Run the test suite:

```bash
# All tests
pytest

# Specific test file
pytest tests/test_auth.py -v

# With coverage
pytest --cov=app tests/
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `postgresql://user:password@localhost/lavidaluca` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-here-change-in-production` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | `30` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |
| `ENVIRONMENT` | Environment mode | `development` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Development

### Adding New Features

1. **Create database models** in `app/models/models.py`
2. **Create Pydantic schemas** in `app/schemas/schemas.py` 
3. **Create API routes** in `app/api/`
4. **Write tests** in `tests/`
5. **Generate migration**: `alembic revision --autogenerate -m "Description"`
6. **Apply migration**: `alembic upgrade head`

### Code Quality

The project uses:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **pytest** for testing

Run quality checks:
```bash
black app tests
isort app tests
flake8 app tests
pytest
```

## Deployment

### Production Configuration

1. **Set secure environment variables**
2. **Use PostgreSQL database**
3. **Configure reverse proxy (nginx)**
4. **Set up SSL/TLS**
5. **Configure monitoring and logging**

### Render.com Deployment

The API is designed to be deployed on Render.com as specified in the project structure.

## Architecture

```
apps/ia/
├── app/
│   ├── api/          # API routes
│   ├── auth/         # Authentication logic
│   ├── core/         # Core configuration
│   ├── db/           # Database setup
│   ├── models/       # SQLAlchemy models
│   └── schemas/      # Pydantic schemas
├── alembic/          # Database migrations
├── tests/            # Test suite
├── Dockerfile        # Docker configuration
└── requirements.txt  # Python dependencies
```

This FastAPI backend provides a complete, production-ready API for managing agricultural activities and student registrations in the MFR education system.