# Development Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
# Root dependencies (frontend)
npm install

# Backend dependencies  
npm run backend:install
```

### 2. Environment Setup
```bash
# Copy environment templates
cp .env.local.example .env.local
cp apps/backend/.env.example apps/backend/.env

# Edit .env.local with your values
nano .env.local

# Edit apps/backend/.env with your values  
nano apps/backend/.env
```

### 3. Database Setup (Optional - SQLite used by default in development)
```bash
# For PostgreSQL (production-like):
createdb lavidaluca_dev
npm run backend:migrate

# For SQLite (default):
# No setup needed, database created automatically
```

### 4. Run Development Servers
```bash
# Option 1: Run both frontend and backend
npm run dev:full

# Option 2: Run separately
npm run dev          # Frontend on :3000
npm run backend:dev  # Backend on :8000
```

## Environment Variables

### Frontend (.env.local)
```bash
# Required
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME=La Vida Luca

# Optional
NEXT_PUBLIC_SENTRY_DSN=your_sentry_dsn
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
```

### Backend (.env)
```bash
# Database (SQLite default, PostgreSQL for production)
DATABASE_URL=sqlite:///./app.db
# DATABASE_URL=postgresql://user:pass@localhost/lavidaluca_dev

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI (optional for development)
OPENAI_API_KEY=your-openai-key-here

# CORS
ALLOWED_HOSTS=["http://localhost:3000"]
```

## Development Workflow

### Running Tests
```bash
# Frontend tests
npm test

# Backend tests  
npm run backend:test

# Backend tests with coverage
npm run backend:test:coverage
```

### Code Quality
```bash
# Frontend linting
npm run lint

# Type checking
npm run type-check

# Build verification
npm run build
```

### Database Operations
```bash
# Create migration
npm run backend:migration

# Apply migrations  
npm run backend:migrate

# Seed development data
cd apps/backend && python seed.py
```

## API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## Frontend Development

### Key Directories
- `src/app/` - Next.js 13+ app router pages
- `src/components/` - Reusable React components  
- `src/lib/` - Redux store, API clients, utilities
- `apps/web/src/` - Web app specific code

### Available Routes
- `/` - Home page
- `/catalogue` - Activities catalog
- `/contact` - Contact form
- `/rejoindre` - Join/signup page
- `/monitoring` - Development monitoring dashboard

## Backend Development

### Key Directories
- `app/models/` - SQLAlchemy models
- `app/schemas/` - Pydantic schemas
- `app/api/endpoints/` - API route handlers
- `app/services/` - Business logic (OpenAI, etc.)
- `app/tests/` - Test files

### Key Features
- **Authentication**: JWT-based auth system
- **Activities**: Full CRUD for learning activities
- **AI Suggestions**: OpenAI-powered recommendations
- **Contacts**: Contact form management
- **Models**: Enhanced with educational metadata

## Troubleshooting

### Common Issues

1. **Frontend build fails**
   ```bash
   # Clear cache and reinstall
   rm -rf .next node_modules
   npm install
   npm run build
   ```

2. **Backend import errors**
   ```bash
   # Ensure PYTHONPATH is set
   cd apps/backend
   PYTHONPATH=. python -m pytest
   ```

3. **Database connection issues**
   ```bash
   # Check DATABASE_URL format
   # SQLite: sqlite:///./app.db
   # PostgreSQL: postgresql://user:pass@host:port/db
   ```

4. **API calls failing**
   ```bash
   # Check CORS settings in backend
   # Verify NEXT_PUBLIC_API_URL in frontend
   ```

### Debug Mode

Enable debug mode for more verbose logging:

```bash
# Backend debug
DEBUG=1 npm run backend:dev

# Frontend debug  
NODE_ENV=development npm run dev
```

## Production Considerations

Before deploying to production:

1. **Security**
   - [ ] Change all secret keys
   - [ ] Enable HTTPS
   - [ ] Set proper CORS origins
   - [ ] Review environment variables

2. **Database**
   - [ ] Use PostgreSQL  
   - [ ] Run migrations
   - [ ] Set up backups

3. **Performance**
   - [ ] Enable caching
   - [ ] Optimize images
   - [ ] Set up CDN

See `docs/DEPLOYMENT.md` for full deployment guide.