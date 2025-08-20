# Production Deployment Configuration Guide

This document outlines the production environment configuration for LaVidaLuca App.

## GitHub Secrets Required

Configure the following secrets in your GitHub repository settings (Settings > Secrets and variables > Actions):

### Vercel (Frontend) Secrets
- `VERCEL_TOKEN` - Your Vercel deployment token
- `VERCEL_ORG_ID` - Your Vercel organization ID  
- `VERCEL_PROJECT_ID` - Your Vercel project ID

### Render (Backend) Secrets
- `RENDER_DEPLOY_HOOK_BACKEND` - Render deploy hook URL for backend service
- `RENDER_DEPLOY_HOOK_IA` - Render deploy hook URL for IA service (if applicable)

### Production URLs
- `PRODUCTION_BACKEND_URL` - Full backend URL (e.g., https://lavidaluca-backend.onrender.com)
- `PRODUCTION_FRONTEND_URL` - Full frontend URL (e.g., https://lavidaluca.vercel.app)
- `PRODUCTION_API_URL` - API endpoint URL (e.g., https://lavidaluca-backend.onrender.com/api/v1)

### Sentry Monitoring Secrets
- `SENTRY_DSN_FRONTEND` - Sentry DSN for frontend monitoring
- `SENTRY_DSN_BACKEND` - Sentry DSN for backend monitoring
- `SENTRY_ORG` - Your Sentry organization slug
- `SENTRY_PROJECT_FRONTEND` - Sentry project name for frontend
- `SENTRY_PROJECT_BACKEND` - Sentry project name for backend
- `SENTRY_AUTH_TOKEN` - Sentry authentication token

## Backend Production Environment (Render)

Configure these environment variables in your Render backend service:

```bash
# Environment
ENVIRONMENT=production
DEBUG=false

# Database (PostgreSQL)
DATABASE_URL=postgresql://username:password@hostname:port/database

# Security
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-production-jwt-secret

# CORS
CORS_ORIGINS=["https://lavidaluca.vercel.app","https://*.vercel.app"]
ALLOWED_HOSTS=["lavidaluca-backend.onrender.com"]

# Sentry
SENTRY_DSN=your-backend-sentry-dsn
SENTRY_ENVIRONMENT=production
SENTRY_RELEASE=1.0.0

# Security Settings  
SECURE_COOKIES=true
SECURE_HEADERS=true
RATE_LIMIT_ENABLED=true

# External Services
OPENAI_API_KEY=your-openai-api-key
```

## Frontend Production Environment (Vercel)

The `.env.production` file will be used automatically by Vercel. Additional environment variables can be configured in Vercel dashboard:

```bash
NEXT_PUBLIC_API_URL=https://lavidaluca-backend.onrender.com/api/v1
NEXT_PUBLIC_SENTRY_DSN=your-frontend-sentry-dsn
SENTRY_ORG=your-sentry-org
SENTRY_PROJECT=lavidaluca-frontend
SENTRY_AUTH_TOKEN=your-sentry-token
```

## Deployment Process

1. **Setup Secrets**: Configure all required GitHub secrets
2. **Backend Setup**: Deploy backend to Render with production environment variables
3. **Frontend Setup**: Deploy frontend to Vercel with production configuration
4. **Health Checks**: The deployment workflow will automatically run health checks
5. **Monitoring**: Sentry will monitor both frontend and backend in production

## Health Check Endpoints

The backend now includes health check endpoints:

- `GET /health` - Basic health status
- `GET /ready` - Readiness check for deployment verification
- `GET /api/v1/health` - API health check

## Security Considerations

- All secrets use strong, unique values in production
- CORS is properly configured for production domains
- Rate limiting is enabled
- Secure cookies and headers are enforced
- Database connections use SSL in production

## Monitoring & Observability

- Frontend errors tracked via Sentry
- Backend errors and performance tracked via Sentry
- Health checks verify deployment success
- Deployment notifications provide status updates

## Testing the Configuration

Run the health check script locally to test URLs:

```bash
# Test with custom URLs
BACKEND_URL="https://your-backend.onrender.com" \
FRONTEND_URL="https://your-app.vercel.app" \
./scripts/health-check.sh
```

## Troubleshooting

1. **Deployment failures**: Check GitHub Actions logs for specific errors
2. **Health check failures**: Verify URLs and service availability
3. **CORS errors**: Ensure frontend URL is in CORS_ORIGINS
4. **Database issues**: Check DATABASE_URL and PostgreSQL configuration
5. **Sentry issues**: Verify DSN URLs and authentication tokens