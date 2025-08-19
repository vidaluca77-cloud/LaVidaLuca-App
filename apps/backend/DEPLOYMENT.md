# LaVidaLuca Backend Deployment Guide

## Overview

This guide covers deploying the LaVidaLuca FastAPI backend to production.

## Prerequisites

- Python 3.11+
- PostgreSQL database (Supabase recommended)
- Docker (optional)
- Poetry for dependency management

## Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
cd LaVidaLuca-App/apps/backend
```

### 2. Install Dependencies

```bash
# Install Poetry if not installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install --only=main
```

### 3. Environment Variables

Copy the example environment file and configure:

```bash
cp .env.example .env
```

Required environment variables:

```bash
# Database
DATABASE_URL=postgresql://username:password@host:port/database
POSTGRES_SERVER=your-postgres-host
POSTGRES_USER=your-username
POSTGRES_PASSWORD=your-password
POSTGRES_DB=lavidaluca
POSTGRES_PORT=5432

# Security
SECRET_KEY=your-very-secure-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=4320

# CORS (add your frontend URLs)
BACKEND_CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Admin User
FIRST_SUPERUSER=admin@yourdomain.com
FIRST_SUPERUSER_PASSWORD=secure-admin-password
```

## Database Setup

### 1. Supabase Setup (Recommended)

1. Create a new project at [supabase.com](https://supabase.com)
2. Get your database connection string from Settings > Database
3. Update `DATABASE_URL` in your `.env` file

### 2. Run Migrations

```bash
# Initialize database
poetry run alembic upgrade head

# Seed with initial data
poetry run python seed_data.py
```

### 3. Manual Database Setup (Alternative)

If not using Supabase, run the SQL script directly:

```bash
psql -h your-host -U your-user -d your-database -f init.sql
```

## Deployment Options

### Option 1: Render (Recommended)

1. Fork the repository to your GitHub account

2. Create a new Web Service on [Render](https://render.com)

3. Connect your GitHub repository

4. Configure the service:
   - **Build Command**: `cd apps/backend && poetry install --only=main`
   - **Start Command**: `cd apps/backend && poetry run uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Add all environment variables from `.env`

5. Deploy and test

### Option 2: Docker Deployment

```bash
# Build the image
docker build -t lavidaluca-backend .

# Run with environment file
docker run --env-file .env -p 8000:8000 lavidaluca-backend
```

### Option 3: Manual Server Deployment

```bash
# Install dependencies
poetry install --only=main

# Run migrations
poetry run alembic upgrade head

# Start the server
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Production Configuration

### 1. Security

- Use a strong, unique `SECRET_KEY`
- Set up HTTPS (SSL/TLS)
- Configure proper CORS origins
- Use environment variables for sensitive data

### 2. Database

- Use connection pooling for high traffic
- Set up database backups
- Monitor database performance

### 3. Monitoring

Add logging and monitoring:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

### 4. Performance

- Use a reverse proxy (nginx)
- Enable gzip compression
- Set up caching where appropriate
- Monitor memory usage

## Testing

```bash
# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src

# Test specific modules
poetry run pytest tests/api/test_auth.py -v
```

## API Documentation

Once deployed, access the interactive API documentation:

- **Swagger UI**: `https://your-domain.com/docs`
- **ReDoc**: `https://your-domain.com/redoc`
- **OpenAPI JSON**: `https://your-domain.com/api/v1/openapi.json`

## Health Checks

The API provides health check endpoints:

- **Basic health**: `GET /health`
- **Root info**: `GET /`

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check `DATABASE_URL` format
   - Verify database credentials
   - Ensure database server is accessible

2. **Migration Errors**
   - Check if database exists
   - Verify user permissions
   - Run migrations manually if needed

3. **Authentication Errors**
   - Verify `SECRET_KEY` is set
   - Check token expiration settings
   - Ensure user accounts exist

### Logs

Check application logs for detailed error information:

```bash
# Local development
poetry run uvicorn src.main:app --log-level debug

# Production logs (depends on deployment platform)
# Render: Check the logs section in dashboard
# Docker: docker logs container-name
```

## Backup and Recovery

### Database Backup

```bash
# Create backup
pg_dump $DATABASE_URL > backup.sql

# Restore backup
psql $DATABASE_URL < backup.sql
```

### Environment Backup

- Keep `.env` file secure and backed up
- Store secrets in a secure password manager
- Document all configuration changes

## Scaling

For high traffic scenarios:

1. **Horizontal Scaling**
   - Deploy multiple instances
   - Use a load balancer
   - Ensure database can handle connections

2. **Database Scaling**
   - Use read replicas
   - Implement connection pooling
   - Consider database clustering

3. **Caching**
   - Add Redis for session storage
   - Cache frequently accessed data
   - Use CDN for static assets

## Support

For issues and questions:

- Check the GitHub repository issues
- Review the API documentation
- Contact the development team

## Version Management

Keep track of deployments:

```bash
# Tag releases
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Document changes in CHANGELOG.md
```