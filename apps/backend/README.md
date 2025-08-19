# La Vida Luca Backend API

FastAPI backend for the La Vida Luca project - activity management and AI-powered recommendations.

## Features

- 🔐 **Authentication**: JWT-based user authentication
- 👥 **User Management**: Registration, login, profile management
- 🎯 **Activity Management**: CRUD operations for activities
- 🤖 **AI Recommendations**: OpenAI-powered activity suggestions
- 🗄️ **Database Integration**: SQLAlchemy with Supabase support
- 🔒 **Security**: Password hashing, CORS protection
- 📚 **API Documentation**: Auto-generated with FastAPI

## Quick Start

1. **Navigate to backend directory:**
   ```bash
   cd apps/backend
   ```

2. **Run the startup script:**
   ```bash
   ./start.sh
   ```

3. **Or manually setup:**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Setup environment
   cp .env.example .env
   # Edit .env with your configuration
   
   # Setup database and seed data
   python seed_data.py
   
   # Start server
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## Environment Configuration

Copy `.env.example` to `.env` and configure:

- `DATABASE_URL`: PostgreSQL connection string
- `SUPABASE_URL` & `SUPABASE_KEY`: Supabase configuration
- `SECRET_KEY`: JWT secret key (change in production!)
- `OPENAI_API_KEY`: OpenAI API key for recommendations
- `ALLOWED_ORIGINS`: CORS allowed origins

## API Endpoints

### Authentication
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/login` - Login user
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update user profile

### Activities
- `GET /api/v1/activities/` - List activities (with filtering)
- `GET /api/v1/activities/{id}` - Get specific activity
- `POST /api/v1/activities/` - Create activity (admin)
- `PUT /api/v1/activities/{id}` - Update activity (admin)
- `DELETE /api/v1/activities/{id}` - Delete activity (admin)

### Recommendations
- `GET /api/v1/recommendations/` - Get personalized recommendations
- `GET /api/v1/recommendations/ai` - Get AI-powered recommendations

## Database Models

### User
- Profile information (name, email, skills, availability)
- Authentication data (hashed password, tokens)
- Preferences and location data

### Activity
- Activity details (title, category, description)
- Metadata (duration, skills, safety level)
- Seasonality and materials information

## Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ CORS protection
- ✅ Input validation with Pydantic
- ✅ SQL injection protection with SQLAlchemy ORM

## Development

The backend is structured following FastAPI best practices:

```
apps/backend/
├── app/
│   ├── api/v1/endpoints/     # API route handlers
│   ├── core/                 # Core functionality (config, db, security)
│   ├── models/              # SQLAlchemy models
│   └── schemas/             # Pydantic schemas
├── main.py                  # FastAPI application
├── requirements.txt         # Python dependencies
└── seed_data.py            # Database seeding script
```