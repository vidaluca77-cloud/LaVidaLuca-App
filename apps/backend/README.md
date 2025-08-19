# La Vida Luca Backend API

## Overview

Complete FastAPI backend implementation for the La Vida Luca MFR (Maison Familiale Rurale) platform. This backend provides authentication, activity management, and AI-powered recommendations for agricultural, artisanal, and environmental activities.

## Features

### 🔐 Authentication & User Management
- JWT-based authentication
- User registration and login
- Profile management
- Admin and regular user roles

### 📚 Activity Management
- Full CRUD operations for activities
- 30+ activity categories (agriculture, artisanat, environnement, etc.)
- Difficulty levels (débutant, intermédiaire, avancé)
- Featured activities system
- Advanced filtering and search

### 🤖 AI-Powered Recommendations
- OpenAI integration for personalized activity suggestions
- Trending activities
- Similar activity recommendations
- Context-aware suggestions based on user profile

### 🛡️ Security & Best Practices
- Password hashing with bcrypt
- JWT token validation
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy ORM

## Quick Start

### 1. Installation

```bash
cd apps/backend
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon key
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key (generate a secure one)
- `OPENAI_API_KEY`: OpenAI API key for recommendations

### 3. Start the Server

```bash
python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/login` - Login user
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile

### Activities
- `GET /api/v1/activities/` - List activities (with filters)
- `POST /api/v1/activities/` - Create activity (authenticated)
- `GET /api/v1/activities/{id}` - Get activity details
- `PUT /api/v1/activities/{id}` - Update activity (creator/admin only)
- `DELETE /api/v1/activities/{id}` - Delete activity (creator/admin only)
- `GET /api/v1/activities/categories/` - Get activity categories
- `GET /api/v1/activities/featured/` - Get featured activities

### Recommendations
- `GET /api/v1/recommendations/` - Get personalized recommendations (authenticated)
- `GET /api/v1/recommendations/similar/{id}` - Get similar activities
- `GET /api/v1/recommendations/trending/` - Get trending activities

## Database Schema

### User Model
- `id`: Primary key
- `email`: Unique email address
- `username`: Unique username
- `full_name`: User's full name
- `hashed_password`: Bcrypt hashed password
- `is_active`: Account status
- `is_admin`: Admin privileges
- `school`: MFR school name
- `level`: Student level
- `bio`: User biography
- `phone`: Phone number
- `location`: User location
- `created_at`: Registration timestamp
- `updated_at`: Last update timestamp

### Activity Model
- `id`: Primary key
- `title`: Activity title
- `description`: Detailed description
- `category`: Activity category (enum)
- `difficulty`: Difficulty level (enum)
- `duration_hours`: Estimated duration
- `materials_needed`: Required materials
- `prerequisites`: Prerequisites
- `learning_objectives`: Learning goals
- `location_type`: Location type (indoor/outdoor/etc.)
- `max_participants`: Maximum participants
- `is_active`: Activity status
- `is_featured`: Featured status
- `created_by`: Creator user ID
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Example Usage

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@mfr.fr",
    "username": "student1",
    "full_name": "Jean Dupont",
    "password": "securepassword",
    "school": "MFR de Bretagne",
    "level": "debutant"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/users/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=student1&password=securepassword"
```

### 3. Create an Activity

```bash
curl -X POST http://localhost:8000/api/v1/activities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Initiation à l'\''apiculture",
    "description": "Découverte du monde des abeilles et de la production de miel",
    "category": "agriculture",
    "difficulty": "debutant",
    "duration_hours": 6,
    "materials_needed": "Combinaison, enfumoir, lève-cadres",
    "location_type": "outdoor",
    "max_participants": 12
  }'
```

### 4. Get Recommendations

```bash
curl -X GET http://localhost:8000/api/v1/recommendations/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Development

### Testing

Start the server and test endpoints:

```bash
# Health check
curl http://localhost:8000/health

# List activities
curl http://localhost:8000/api/v1/activities/

# Get activity categories
curl http://localhost:8000/api/v1/activities/categories/
```

### Database Migrations

Using Alembic for database migrations:

```bash
# Generate migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## Deployment

### Environment Variables for Production

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
DATABASE_URL=postgresql://postgres:password@db.your-project.supabase.co:5432/postgres
SECRET_KEY=your-super-secure-secret-key-minimum-32-characters
OPENAI_API_KEY=sk-your-openai-api-key
BACKEND_CORS_ORIGINS=https://your-frontend-domain.com,https://another-domain.com
DEBUG=false
```

### Production Considerations

1. Use a strong, randomly generated `SECRET_KEY`
2. Configure proper CORS origins
3. Set up SSL/TLS certificates
4. Use environment variables for sensitive data
5. Set up monitoring and logging
6. Configure database connection pooling
7. Use a production WSGI server (uvicorn with gunicorn)

## Error Handling

The API includes comprehensive error handling:
- **400**: Bad Request (validation errors)
- **401**: Unauthorized (authentication required)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found (resource doesn't exist)
- **422**: Unprocessable Entity (validation errors)
- **500**: Internal Server Error (server errors)

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- CORS configuration
- SQL injection prevention
- Input validation and sanitization
- Rate limiting ready (can be added with slowapi)
- Trusted host middleware

## OpenAI Integration

The recommendations system uses OpenAI GPT-3.5-turbo to provide:
- Personalized activity recommendations based on user profile
- Context-aware suggestions considering past activities
- Progressive difficulty recommendations
- Regional relevance when location is available
- Fallback logic when OpenAI is unavailable

## Contributing

1. Follow the existing code structure
2. Use type hints throughout
3. Add docstrings to functions and classes
4. Test endpoints before committing
5. Update this documentation for new features

## Support

For issues or questions:
1. Check the interactive API docs at `/docs`
2. Review the error messages in the response
3. Check the server logs for detailed error information
4. Ensure all environment variables are properly configured