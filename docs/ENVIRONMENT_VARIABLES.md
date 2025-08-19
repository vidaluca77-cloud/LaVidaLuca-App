# Environment Variables Guide

## Overview

This guide explains all environment variables used in the La Vida Luca application across different environments and services.

## Frontend Environment Variables

### Core Configuration

#### `NEXT_PUBLIC_SUPABASE_URL`
- **Required**: Yes
- **Description**: URL of your Supabase project
- **Format**: `https://your-project-id.supabase.co`
- **Example**: `https://abcdefghijklmnop.supabase.co`

#### `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- **Required**: Yes
- **Description**: Anonymous key for Supabase client-side access
- **Format**: JWT token string
- **Security**: Safe to expose in client-side code

#### `NEXT_PUBLIC_IA_API_URL`
- **Required**: Yes
- **Description**: URL of the IA API backend service
- **Development**: `http://localhost:8000`
- **Staging**: `https://la-vida-luca-ia-staging.onrender.com`
- **Production**: `https://la-vida-luca-ia.onrender.com`

### Contact Information

#### `NEXT_PUBLIC_CONTACT_EMAIL`
- **Required**: Yes
- **Description**: Contact email displayed on the website
- **Example**: `contact@lavidaluca.fr`

#### `NEXT_PUBLIC_CONTACT_PHONE`
- **Required**: Yes
- **Description**: Contact phone number displayed on the website
- **Example**: `+33123456789`

### Feature Flags

#### `NEXT_PUBLIC_ENABLE_ANALYTICS`
- **Required**: No
- **Description**: Enable/disable analytics tracking
- **Values**: `true` | `false`
- **Default**: `false`

#### `NEXT_PUBLIC_ENABLE_ERROR_TRACKING`
- **Required**: No
- **Description**: Enable/disable Sentry error tracking
- **Values**: `true` | `false`
- **Default**: `false`

#### `NEXT_PUBLIC_MAINTENANCE_MODE`
- **Required**: No
- **Description**: Enable maintenance mode banner
- **Values**: `true` | `false`
- **Default**: `false`

### Analytics & Monitoring

#### `NEXT_PUBLIC_GOOGLE_ANALYTICS_ID`
- **Required**: No (if analytics enabled)
- **Description**: Google Analytics measurement ID
- **Format**: `G-XXXXXXXXXX`

#### `NEXT_PUBLIC_HOTJAR_ID`
- **Required**: No
- **Description**: Hotjar site ID for user behavior tracking
- **Format**: Numeric ID

#### `NEXT_PUBLIC_SENTRY_DSN`
- **Required**: No (if error tracking enabled)
- **Description**: Sentry DSN for error tracking
- **Format**: `https://xxx@xxx.ingest.sentry.io/xxx`

## Backend Environment Variables

### Core Configuration

#### `ENVIRONMENT`
- **Required**: Yes
- **Description**: Current environment name
- **Values**: `development` | `staging` | `production`

#### `PORT`
- **Required**: No
- **Description**: Port for the FastAPI server
- **Default**: `8000`

#### `ALLOWED_ORIGINS`
- **Required**: Yes
- **Description**: Comma-separated list of allowed CORS origins
- **Example**: `https://la-vida-luca.vercel.app,https://la-vida-luca-staging.vercel.app`

### Database Configuration

#### `SUPABASE_URL`
- **Required**: Yes
- **Description**: Supabase project URL for server-side access
- **Format**: `https://your-project-id.supabase.co`

#### `SUPABASE_KEY`
- **Required**: Yes
- **Description**: Supabase service key for server-side access
- **Security**: Keep secret, has elevated privileges

#### `SUPABASE_DB_URL`
- **Required**: Yes (for direct database access)
- **Description**: Direct PostgreSQL connection string
- **Format**: `postgresql://user:password@host:port/database`
- **Security**: Keep secret

### External Services

#### `OPENAI_API_KEY`
- **Required**: No (if using OpenAI)
- **Description**: OpenAI API key for AI features
- **Security**: Keep secret

#### `SENTRY_DSN`
- **Required**: No (if error tracking enabled)
- **Description**: Sentry DSN for backend error tracking
- **Format**: `https://xxx@xxx.ingest.sentry.io/xxx`

## Database Environment Variables

#### `POSTGRES_DB`
- **Required**: Yes (for local development)
- **Description**: PostgreSQL database name
- **Default**: `lavidaluca`

#### `POSTGRES_USER`
- **Required**: Yes (for local development)
- **Description**: PostgreSQL username
- **Default**: `postgres`

#### `POSTGRES_PASSWORD`
- **Required**: Yes (for local development)
- **Description**: PostgreSQL password
- **Security**: Keep secret

## CI/CD Environment Variables

### GitHub Secrets

#### Vercel Deployment
```
VERCEL_TOKEN=your-vercel-token
VERCEL_ORG_ID=your-vercel-org-id
VERCEL_PROJECT_ID=your-vercel-project-id
```

#### Render Deployment
```
RENDER_API_KEY=your-render-api-key
RENDER_STAGING_SERVICE_ID=staging-service-id
RENDER_PRODUCTION_SERVICE_ID=production-service-id
```

#### Supabase
```
SUPABASE_URL_STAGING=https://staging-project.supabase.co
SUPABASE_ANON_KEY_STAGING=staging-anon-key
SUPABASE_URL_PROD=https://production-project.supabase.co
SUPABASE_ANON_KEY_PROD=production-anon-key
SUPABASE_DB_URL=postgres://connection-string
```

#### Monitoring
```
SLACK_WEBHOOK_URL=https://hooks.slack.com/your-webhook
SNYK_TOKEN=your-snyk-token
```

#### AWS (for backups)
```
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
```

## Environment-Specific Configurations

### Development (.env.local)
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-dev-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-dev-anon-key
NEXT_PUBLIC_IA_API_URL=http://localhost:8000
NEXT_PUBLIC_CONTACT_EMAIL=dev@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_ERROR_TRACKING=true
NEXT_PUBLIC_MAINTENANCE_MODE=false
```

### Staging (.env.staging)
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-staging-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-staging-anon-key
NEXT_PUBLIC_IA_API_URL=https://la-vida-luca-ia-staging.onrender.com
NEXT_PUBLIC_CONTACT_EMAIL=staging@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_ERROR_TRACKING=true
NEXT_PUBLIC_MAINTENANCE_MODE=false
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=G-STAGING123
NEXT_PUBLIC_SENTRY_DSN=https://staging@sentry.io/project
```

### Production (.env.production)
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-production-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-production-anon-key
NEXT_PUBLIC_IA_API_URL=https://la-vida-luca-ia.onrender.com
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_ERROR_TRACKING=true
NEXT_PUBLIC_MAINTENANCE_MODE=false
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=G-PRODUCTION123
NEXT_PUBLIC_SENTRY_DSN=https://production@sentry.io/project
```

## Security Best Practices

### 1. Secret Management
- Never commit secrets to version control
- Use different secrets for each environment
- Rotate secrets regularly
- Use environment-specific prefixes

### 2. Access Control
- Limit database access to necessary services
- Use service keys instead of user keys where possible
- Monitor access logs regularly

### 3. Environment Separation
- Keep staging and production completely separate
- Use different Supabase projects for each environment
- Isolate network access between environments

## Setting Up Environment Variables

### Local Development

1. Copy the example file:
```bash
cp .env.example .env.local
```

2. Update the values with your configuration
3. Never commit `.env.local` to version control

### Vercel Deployment

1. Go to your Vercel project settings
2. Navigate to "Environment Variables"
3. Add variables for each environment:
   - Development: for preview deployments
   - Preview: for PR deployments  
   - Production: for main branch deployments

### Render Deployment

1. Go to your Render service dashboard
2. Navigate to "Environment"
3. Add environment variables
4. Mark sensitive variables as "Secret"

### GitHub Actions

1. Go to repository Settings > Secrets and variables > Actions
2. Add secrets under "Repository secrets"
3. Use descriptive names with environment prefixes if needed

## Validation

### Frontend Validation
The application validates required environment variables at build time:

```typescript
// Check required variables
const requiredVars = [
  'NEXT_PUBLIC_SUPABASE_URL',
  'NEXT_PUBLIC_SUPABASE_ANON_KEY',
  'NEXT_PUBLIC_IA_API_URL'
];

for (const varName of requiredVars) {
  if (!process.env[varName]) {
    throw new Error(`Missing required environment variable: ${varName}`);
  }
}
```

### Backend Validation
The FastAPI application validates environment variables at startup:

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    allowed_origins: str = ""
    environment: str = "development"
    
    class Config:
        env_file = ".env"
```

## Troubleshooting

### Common Issues

#### Build fails with "Missing environment variable"
- Check that all required variables are set
- Verify variable names match exactly (case-sensitive)
- Ensure no extra spaces or quotes

#### CORS errors in browser
- Check `ALLOWED_ORIGINS` in backend
- Verify frontend URL is included in allowed origins
- Check for trailing slashes in URLs

#### Database connection fails
- Verify Supabase URL and keys are correct
- Check network connectivity
- Ensure RLS policies allow access

#### API calls fail
- Check `NEXT_PUBLIC_IA_API_URL` is correct
- Verify backend service is running
- Check for network/firewall issues

### Debug Commands

```bash
# Check environment variables in Next.js
npm run build 2>&1 | grep -i "environment"

# Test database connection
curl "${NEXT_PUBLIC_SUPABASE_URL}/rest/v1/" \
  -H "apikey: ${NEXT_PUBLIC_SUPABASE_ANON_KEY}"

# Test backend API
curl "${NEXT_PUBLIC_IA_API_URL}/health"
```

## Migration Guide

When updating environment variables:

1. Update `.env.example` with new variables
2. Update this documentation
3. Add validation for new required variables
4. Update CI/CD workflows if needed
5. Coordinate deployment across environments
6. Update monitoring and alerting if needed