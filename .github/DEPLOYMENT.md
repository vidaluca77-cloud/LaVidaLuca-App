# Deployment Configuration for La Vida Luca

This document outlines the deployment configuration for production environments including GitHub secrets, Vercel, and Render setup.

## GitHub Secrets Configuration

### Required Secrets for GitHub Actions

#### Backend/API Secrets
- `DATABASE_URL` - Production PostgreSQL connection string
- `JWT_SECRET_KEY` - Secret key for JWT token generation (minimum 32 characters)
- `OPENAI_API_KEY` - OpenAI API key for AI features
- `SENTRY_DSN` - Sentry DSN for error monitoring
- `RENDER_API_KEY` - Render.com API key for deployment

#### Frontend Secrets  
- `NEXT_PUBLIC_API_URL` - Production API URL (https://your-backend.render.com/api/v1)
- `NEXT_PUBLIC_SENTRY_DSN` - Sentry DSN for frontend error monitoring
- `VERCEL_TOKEN` - Vercel deployment token

#### Email/SMTP Secrets
- `SMTP_HOST` - SMTP server hostname
- `SMTP_PORT` - SMTP server port
- `SMTP_USERNAME` - SMTP username
- `SMTP_PASSWORD` - SMTP password or app password
- `SMTP_FROM_EMAIL` - From email address

#### Monitoring Secrets
- `PROMETHEUS_PASSWORD` - Password for Prometheus metrics endpoint
- `GRAFANA_API_KEY` - Grafana API key for dashboard management

### Setting Up GitHub Secrets

1. Go to your repository on GitHub
2. Navigate to Settings > Secrets and variables > Actions
3. Click "New repository secret"
4. Add each secret with the name and value as specified above

### Example Secret Values (Development)

```bash
# Database
DATABASE_URL=postgresql://user:password@hostname:5432/database

# JWT (Generate with: openssl rand -base64 32)
JWT_SECRET_KEY=your-32-character-secret-key-here

# External Services
OPENAI_API_KEY=sk-...
SENTRY_DSN=https://...@....ingest.sentry.io/...

# Deployment
RENDER_API_KEY=rnd_...
VERCEL_TOKEN=...
```

## Environment Variables by Service

### Vercel (Frontend)
- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_SENTRY_DSN`
- `NEXT_PUBLIC_ENVIRONMENT`
- `SENTRY_ORG`
- `SENTRY_PROJECT`

### Render (Backend)
- `ENVIRONMENT`
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `OPENAI_API_KEY`
- `SENTRY_DSN`
- `CORS_ORIGINS`
- `LOG_LEVEL`
- `SMTP_*` variables

## Security Best Practices

1. **Never commit secrets to version control**
2. **Use different secrets for each environment**
3. **Rotate secrets regularly**
4. **Use least privilege access**
5. **Monitor secret usage with alerting**

## Deployment Validation

Each deployment should validate:
- Health check endpoints respond correctly
- Database connectivity
- External service connectivity (OpenAI, SMTP)
- Environment variables are properly set
- Security headers are configured