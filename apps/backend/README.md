# LaVidaLuca Backend API

FastAPI backend for the LaVidaLuca educational farm activities platform.

## Features

- **User Management**: Authentication, authorization with role-based access (Student, Mentor, Admin, Visitor)
- **Activities Management**: Catalog of 30+ agricultural, artisanal and environmental activities
- **Location Management**: Farm and location management with geolocation
- **Reservations**: Activity booking and scheduling system
- **Evaluations**: Progress tracking and skill assessment
- **AI Recommendations**: Personalized activity suggestions based on user profile

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Database via Supabase
- **SQLAlchemy**: ORM for database interactions
- **Pydantic**: Data validation and serialization
- **JWT**: Authentication and authorization
- **OpenAI**: AI-powered recommendations
- **Pytest**: Testing framework

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (create `.env` file):
```env
DATABASE_URL=postgresql://user:password@localhost/lavidaluca
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SECRET_KEY=your_secret_key_for_jwt
OPENAI_API_KEY=your_openai_key
```

3. Run the development server:
```bash
uvicorn main:app --reload
```

4. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests with pytest:
```bash
pytest
```

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user profile
- `POST /auth/logout` - Logout

### Users
- `GET /users/` - List users (admin/mentor)
- `GET /users/{id}` - Get user by ID
- `PUT /users/{id}` - Update user profile
- `PUT /users/{id}/role` - Update user role (admin)

### Activities
- `GET /activities/` - List activities with filtering
- `GET /activities/categories` - Get activity categories
- `POST /activities/` - Create activity (mentor/admin)
- `GET /activities/{id}` - Get activity details
- `PUT /activities/{id}` - Update activity (mentor/admin)
- `POST /activities/recommend` - Get AI recommendations

### Locations
- `GET /locations/` - List locations
- `POST /locations/` - Create location (mentor/admin)
- `GET /locations/{id}` - Get location details
- `PUT /locations/{id}` - Update location (mentor/admin)

## Database Schema

The database schema includes:
- Users with roles and profiles
- Activities with categories, skills, materials
- Locations with contact and capacity information
- Reservations for activity booking
- Evaluations for progress tracking
- Many-to-many relationships for skills and materials

See `/infra/supabase/schema.sql` for the complete database schema.

## Deployment

This backend is designed to be deployed on Render with Supabase as the database provider.

Environment variables for production:
- `DATABASE_URL` - Supabase PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- `ALLOWED_ORIGINS` - CORS allowed origins
- `OPENAI_API_KEY` - OpenAI API key for recommendations