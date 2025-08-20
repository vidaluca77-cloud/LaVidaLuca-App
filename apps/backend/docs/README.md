# LaVidaLuca Backend API Documentation

## Overview

The LaVidaLuca Backend API provides endpoints for managing users, activities, contact forms, and AI-powered suggestions for the MFR (Maison Familiale Rurale) training platform.

## API Documentation

### Interactive Documentation

- **Swagger UI**: Available at `/docs` when the server is running
- **ReDoc**: Available at `/redoc` when the server is running
- **OpenAPI JSON**: Available at `/api/v1/openapi.json`

### Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints:

1. Register a new account via `POST /api/v1/auth/register`
2. Login with your credentials via `POST /api/v1/auth/login`
3. Include the returned JWT token in the Authorization header: `Authorization: Bearer <token>`

### Available Endpoints

#### Authentication (`/api/v1/auth`)
- `POST /register` - Create a new user account
- `POST /login` - Authenticate and receive JWT token

#### Activities (`/api/v1/activities`)
- `GET /` - List activities with filtering and pagination
- `GET /{id}` - Get specific activity details
- `POST /` - Create new activity (auth required)
- `PUT /{id}` - Update activity (auth required, owner only)
- `DELETE /{id}` - Delete activity (auth required, owner only)
- `GET /categories/` - Get available activity categories

#### Users (`/api/v1/users`)
- `GET /me` - Get current user profile (auth required)
- `GET /` - List users (auth required, admin for full list)

#### Suggestions (`/api/v1/suggestions`)
- `GET /` - Get user's activity suggestions (auth required)
- `POST /generate` - Generate new AI suggestions (auth required)

#### Contacts (`/api/v1/contacts`)
- `POST /` - Submit contact form (public)
- `GET /types` - Get available contact types

## Data Models

### User
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Activity
```json
{
  "id": 1,
  "title": "Activity Title",
  "description": "Activity description",
  "category": "agriculture",
  "difficulty_level": "beginner",
  "duration_minutes": 120,
  "location": "Location",
  "equipment_needed": "Equipment list",
  "learning_objectives": "Learning goals",
  "is_published": true,
  "creator_id": 1,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Contact
```json
{
  "name": "Contact Name",
  "email": "contact@example.com",
  "subject": "Subject",
  "message": "Message content",
  "contact_type": "general",
  "consent_privacy": true,
  "consent_marketing": false
}
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "detail": "Error message"
}
```

Common HTTP status codes:
- `200` - Success
- `401` - Authentication required
- `403` - Insufficient permissions
- `404` - Resource not found
- `422` - Validation error

## Development

### Running the API

```bash
cd /apps/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

The API includes comprehensive test coverage. Run tests with:

```bash
pytest
```

### Environment Variables

Required environment variables:
- `DATABASE_URL` - PostgreSQL database connection string
- `SECRET_KEY` - JWT signing secret
- `OPENAI_API_KEY` - Optional, for AI suggestions

## Contact

For questions about the API, please use the contact form endpoints or reach out to the development team.