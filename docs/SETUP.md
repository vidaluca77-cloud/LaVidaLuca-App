# Setup Instructions

## Prerequisites

Before setting up La Vida Luca App, ensure you have the following installed:

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Poetry** (for Python dependency management)
- **Git**
- **Docker** (optional, for containerized development)

## Initial Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
cd LaVidaLuca-App
```

### 2. Frontend Setup

```bash
# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Update .env.local with your configuration
# See docs/ENVIRONMENT_VARIABLES.md for details
```

### 3. Backend Setup

```bash
# Navigate to backend directory
cd apps/ia

# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Copy environment file
cp .env.example .env

# Update .env with your configuration
```

### 4. Database Setup

#### Option A: Use Supabase Cloud (Recommended)

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Copy the project URL and anon key
4. Update your `.env.local` and `apps/ia/.env` files
5. Run the database schema:

```bash
# Install Supabase CLI
npm install -g @supabase/cli

# Set up the database
cd infra/supabase
supabase db push --db-url "your-database-url"
```

#### Option B: Local Supabase (Development)

```bash
# Install Docker if not already installed
# Install Supabase CLI
npm install -g @supabase/cli

# Initialize Supabase in your project
cd infra/supabase
supabase init

# Start local Supabase
supabase start

# Apply schema
supabase db reset

# Your local Supabase will be available at:
# API URL: http://localhost:54321
# Dashboard: http://localhost:54323
```

## Development Workflow

### 1. Start Frontend Development Server

```bash
# From project root
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 2. Start Backend Development Server

```bash
# From apps/ia directory
cd apps/ia
poetry run uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### 3. Development Commands

```bash
# Frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript checks

# Backend
cd apps/ia
poetry run uvicorn main:app --reload  # Start development server
poetry run pytest                     # Run tests
poetry run flake8 .                   # Run linting
poetry run mypy .                     # Run type checking
poetry run black .                    # Format code
```

## Production Deployment

### 1. Vercel (Frontend)

#### Automatic Deployment (Recommended)

1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main/develop

#### Manual Deployment

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

### 2. Render (Backend)

#### Automatic Deployment (Recommended)

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set build and start commands:
   - Build Command: `cd apps/ia && poetry install --no-dev`
   - Start Command: `cd apps/ia && poetry run uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set environment variables
5. Deploy automatically on push

#### Manual Deployment

Use the provided `render.yaml` configuration file for automated setup.

### 3. Database (Supabase)

1. Create production Supabase project
2. Run schema migration:
```bash
supabase db push --db-url "your-production-database-url"
```
3. Optionally seed with data:
```bash
supabase db reset --db-url "your-production-database-url"
```

## Configuration

### Environment Variables

Create environment-specific files:

**Development (`.env.local`)**:
```env
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-local-anon-key
NEXT_PUBLIC_IA_API_URL=http://localhost:8000
NEXT_PUBLIC_CONTACT_EMAIL=dev@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789
```

**Production**:
Set these in your deployment platform:
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-production-anon-key
NEXT_PUBLIC_IA_API_URL=https://your-backend.onrender.com
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789
```

### Security Configuration

1. **Supabase RLS (Row Level Security)**:
   - Enabled by default in schema
   - Configure policies for user access

2. **CORS Configuration**:
   - Update `ALLOWED_ORIGINS` in backend
   - Include all frontend domains

3. **Environment Separation**:
   - Use different Supabase projects for staging/production
   - Separate service accounts for each environment

## Testing

### Frontend Testing

```bash
# Unit tests (when implemented)
npm test

# Linting
npm run lint

# Type checking
npm run type-check

# Build test
npm run build
```

### Backend Testing

```bash
cd apps/ia

# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=. --cov-report=html

# Run specific test file
poetry run pytest tests/test_main.py
```

### Integration Testing

```bash
# Test health endpoints
curl http://localhost:3000/api/health
curl http://localhost:8000/health

# Test API connectivity
curl http://localhost:8000/api/v1/status
```

## Monitoring Setup

### 1. Health Checks

Health check endpoints are available:
- Frontend: `/api/health`
- Backend: `/health`
- Metrics: `/api/metrics`

### 2. Error Tracking (Sentry)

1. Create Sentry project
2. Add DSN to environment variables:
```env
NEXT_PUBLIC_SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
```

### 3. Analytics (Google Analytics)

```env
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
NEXT_PUBLIC_ENABLE_ANALYTICS=true
```

### 4. Monitoring Alerts

Set up GitHub Actions workflows for:
- Continuous health checks
- Performance monitoring
- Security scanning

## Backup Strategy

### 1. Database Backups

```bash
# Manual backup
pg_dump "your-database-url" > backup-$(date +%Y%m%d).sql

# Restore
psql "your-database-url" < backup-file.sql
```

### 2. Automated Backups

Use the provided GitHub Actions workflow:
- Daily automated backups
- 30-day retention
- S3 storage with encryption

### 3. Code Backups

- Git repository with multiple remotes
- Automated CI/CD pipeline backups
- Configuration as code

## Troubleshooting

### Common Issues

#### Build Failures

**Node.js version mismatch**:
```bash
# Check version
node --version
# Should be 18+

# Use nvm to manage versions
nvm install 18
nvm use 18
```

**Python version issues**:
```bash
# Check version
python --version
# Should be 3.11+

# Install specific version with pyenv
pyenv install 3.11.0
pyenv local 3.11.0
```

#### Database Connection Issues

**Local Supabase not starting**:
```bash
# Check Docker is running
docker ps

# Reset Supabase
supabase stop
supabase start
```

**Production database access**:
- Verify environment variables
- Check network connectivity
- Review RLS policies

#### Deployment Issues

**Vercel build failures**:
- Check Node.js version in Vercel settings
- Verify environment variables are set
- Review build logs

**Render deployment issues**:
- Check Python version compatibility
- Verify Poetry installation
- Review service logs

### Debug Commands

```bash
# Check environment variables
printenv | grep NEXT_PUBLIC

# Test database connectivity
curl "${NEXT_PUBLIC_SUPABASE_URL}/rest/v1/" \
  -H "apikey: ${NEXT_PUBLIC_SUPABASE_ANON_KEY}"

# Check backend health
curl "${NEXT_PUBLIC_IA_API_URL}/health"

# View logs
# Vercel: vercel logs
# Render: check dashboard logs
```

### Getting Help

1. Check this documentation
2. Review GitHub Issues
3. Check deployment platform logs
4. Contact the development team

## Next Steps

After successful setup:

1. **Configure CI/CD**: Set up GitHub Actions workflows
2. **Set up monitoring**: Configure health checks and alerts
3. **Security review**: Enable security scanning and best practices
4. **Performance optimization**: Set up analytics and monitoring
5. **Backup testing**: Verify backup and restore procedures

## Development Guidelines

### Git Workflow

1. Create feature branch from `develop`
2. Make changes and test locally
3. Create pull request to `develop`
4. After review, merge to `develop`
5. Periodically merge `develop` to `main` for production

### Code Style

- **Frontend**: ESLint + Prettier configuration
- **Backend**: Black + flake8 + mypy
- **Commits**: Conventional commit messages

### Testing Requirements

- Unit tests for critical functions
- Integration tests for API endpoints
- Health check tests for all services
- Performance tests for critical paths