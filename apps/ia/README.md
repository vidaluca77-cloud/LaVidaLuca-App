# LaVidaLuca FastAPI Backend

Complete FastAPI backend for the LaVidaLuca App, featuring AI-powered activity recommendations for MFR students.

## Features

- 🔐 **Authentication**: JWT-based auth with user registration/login
- 📚 **Activities Management**: Complete CRUD for 30 educational activities
- 📅 **Booking System**: Activity booking and scheduling
- 👤 **User Profiles**: User management with skills and preferences
- 🤖 **AI Recommendations**: OpenAI-powered activity suggestions
- 📊 **Analytics**: User progress and activity statistics
- 🧪 **Testing**: Comprehensive test suite with pytest
- 🐳 **Docker**: Containerized deployment
- 📖 **Documentation**: Auto-generated API docs with FastAPI

## Quick Start

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Initialize Database**
   ```bash
   python init_db.py
   ```

4. **Start the Server**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Development

```bash
docker-compose up --build
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/verify-email` - Verify email

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update user profile

### Activities
- `GET /api/v1/activities/` - List activities (with filtering)
- `GET /api/v1/activities/{id}` - Get activity details
- `GET /api/v1/activities/categories` - List categories

### Bookings
- `GET /api/v1/bookings/` - List user bookings
- `POST /api/v1/bookings/` - Create booking
- `PUT /api/v1/bookings/{id}` - Update booking

### Recommendations
- `POST /api/v1/recommendations/` - Get AI recommendations
- `GET /api/v1/recommendations/me` - Get personalized recommendations

### Analytics
- `GET /api/v1/analytics/dashboard` - User dashboard stats
- `GET /api/v1/analytics/activities/stats` - Activity statistics

## Database Models

### User
- Profile information (skills, availability, preferences)
- MFR student status
- Authentication credentials

### Activity
- 30 predefined activities from agriculture to social animation
- Categories: agri, transfo, artisanat, nature, social
- Skills, materials, duration, safety level

### Booking
- User activity reservations
- Status tracking (pending, confirmed, completed, cancelled)
- Feedback and ratings

## AI Recommendations

The system uses OpenAI GPT-3.5 to generate personalized activity recommendations based on:
- User skills and interests
- Availability preferences
- Learning progression
- Activity diversity

Fallback algorithm available when OpenAI is not configured.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest app/tests/test_auth.py
```

## Deployment

### Render (Recommended)

1. Connect your GitHub repository to Render
2. Set environment variables in Render dashboard
3. Deploy as Web Service

### Environment Variables

```bash
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
ALLOWED_ORIGINS=["https://your-frontend.vercel.app"]
```

## Development

### Project Structure

```
apps/ia/
├── app/
│   ├── api/v1/endpoints/     # API route handlers
│   ├── core/                 # Configuration and utilities
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas
│   ├── services/             # Business logic
│   └── tests/                # Test suite
├── main.py                   # FastAPI application
├── init_db.py               # Database initialization
└── requirements.txt         # Python dependencies
```

### Adding New Features

1. Create models in `app/models/`
2. Define schemas in `app/schemas/`
3. Implement business logic in `app/services/`
4. Add API endpoints in `app/api/v1/endpoints/`
5. Write tests in `app/tests/`

## Integration with Frontend

The API is designed to work seamlessly with the Next.js frontend:
- CORS configured for Vercel domains
- JWT tokens for authentication
- Data models matching frontend TypeScript interfaces
- RESTful endpoints following frontend expectations

## Support

For questions or issues, contact: contact@lavidaluca.fr