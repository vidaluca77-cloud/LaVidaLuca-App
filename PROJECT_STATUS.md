# La Vida Luca - Complete Application

This repository contains the complete La Vida Luca platform consisting of a Next.js frontend and FastAPI backend.

## Project Structure

- `/src` - Next.js frontend application
- `/apps/ia` - FastAPI backend API 
- `/infra/supabase` - Database schema and seed data
- `/public` - Static assets

## Quick Start

### Frontend (Next.js)
```bash
npm install
npm run dev
# Open http://localhost:3000
```

### Backend (FastAPI)
```bash
cd apps/ia
cp .env.example .env
# Edit .env with your Supabase credentials
./start.sh
# API docs available at http://localhost:8000/docs
```

### Database Setup
1. Create a Supabase project
2. Run `infra/supabase/schema.sql` to create tables
3. Run `infra/supabase/seeds.sql` to populate sample data

## Features Implemented

### ✅ FastAPI Backend Complete
- **Authentication System**: User registration, login, JWT tokens
- **Activities Management**: CRUD operations for 30 farm activities
- **Registration System**: Users can register for activities
- **AI Suggestions**: Intelligent activity recommendations
- **Database Integration**: Full Supabase/PostgreSQL integration
- **Comprehensive Testing**: Complete test suite with pytest
- **API Documentation**: Automatic OpenAPI/Swagger docs
- **Production Ready**: Environment configuration, error handling

### ✅ Database Infrastructure
- **Complete Schema**: Users, activities, registrations tables
- **Sample Data**: 30 predefined farm activities
- **Proper Relationships**: Foreign keys, constraints, indexes
- **Supabase Integration**: Authentication and real-time features

### Frontend Integration Ready
- **CORS Configured**: Ready for frontend communication
- **API Endpoints**: All backend endpoints ready for consumption
- **Authentication Flow**: JWT-based auth ready for frontend

## Deployment

### Backend (Render)
1. Connect GitHub repository to Render
2. Select `apps/ia` as root directory
3. Use Python 3.12 runtime
4. Set environment variables in Render dashboard
5. Build command: `pip install -r requirements.txt`
6. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)
1. Connect GitHub repository to Vercel
2. Root directory: `./` (project root)
3. Framework: Next.js
4. Set environment variables for API URL

### Database (Supabase)
1. Create Supabase project
2. Run schema and seed SQL files
3. Configure authentication settings
4. Get credentials for backend configuration

## API Documentation

Once the backend is running, access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Environment Variables

See `apps/ia/.env.example` for required backend configuration.

## Contributing

1. Follow existing code structure
2. Add tests for new features
3. Update documentation
4. Ensure all tests pass

## License

See LICENSE file for details.