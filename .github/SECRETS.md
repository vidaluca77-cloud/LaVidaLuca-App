# Secrets Management Guide for La Vida Luca

This guide provides detailed instructions for managing secrets across all deployment environments.

## 🔐 GitHub Secrets Setup

### Required GitHub Repository Secrets

#### Core Application Secrets
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Authentication  
JWT_SECRET_KEY=your-32-character-secret-key

# External APIs
OPENAI_API_KEY=sk-your-openai-key
SENTRY_DSN=https://key@sentry.io/project

# Email/SMTP
SMTP_USERNAME=your-email@domain.com
SMTP_PASSWORD=your-app-password
```

#### Deployment Secrets
```bash
# Render.com
RENDER_API_KEY=rnd_your-render-api-key
RENDER_SERVICE_ID=srv-your-service-id
RENDER_STAGING_SERVICE_ID=srv-your-staging-service-id

# Vercel
VERCEL_TOKEN=your-vercel-token
VERCEL_ORG_ID=your-org-id
VERCEL_PROJECT_ID=your-project-id

# Production URLs
PRODUCTION_API_URL=https://your-backend.onrender.com
PRODUCTION_FRONTEND_URL=https://your-app.vercel.app
STAGING_API_URL=https://your-staging-backend.onrender.com
```

### Setting Up Secrets in GitHub

1. **Navigate to Repository Settings**
   ```
   GitHub Repository → Settings → Secrets and variables → Actions
   ```

2. **Add Repository Secrets**
   - Click "New repository secret"
   - Enter name exactly as shown above
   - Paste the value (no quotes needed)
   - Click "Add secret"

3. **Environment-Specific Secrets**
   - Create environments: `staging` and `production`
   - Add environment-specific secrets under each environment

## 🚀 Vercel Environment Variables

### Required Environment Variables in Vercel Dashboard

#### Build Variables
```bash
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api/v1
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_SENTRY_DSN=https://key@sentry.io/project
```

#### Build-time Only Variables
```bash
SENTRY_ORG=your-sentry-org
SENTRY_PROJECT=your-sentry-project  
SENTRY_AUTH_TOKEN=your-sentry-auth-token
```

### Setting Up Vercel Environment Variables

1. **Via Vercel Dashboard**
   ```
   Vercel Project → Settings → Environment Variables
   ```

2. **Via Vercel CLI**
   ```bash
   # Set production variable
   vercel env add NEXT_PUBLIC_API_URL production
   
   # Set for all environments
   vercel env add NEXT_PUBLIC_SENTRY_DSN
   ```

3. **Via `vercel.json` (for non-sensitive values)**
   ```json
   {
     "env": {
       "NEXT_PUBLIC_ENVIRONMENT": "production"
     }
   }
   ```

## 🔧 Render Environment Variables

### Required Environment Variables in Render Dashboard

#### Automatic Variables (set via render.yaml)
- `ENVIRONMENT=production`
- `DATABASE_URL` (from connected database)
- `JWT_SECRET_KEY` (auto-generated)

#### Manual Variables (set in dashboard)
```bash
# External APIs
OPENAI_API_KEY=sk-your-openai-key
SENTRY_DSN=https://key@sentry.io/project

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_USERNAME=your-email@domain.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@yourdomain.com
```

### Setting Up Render Environment Variables

1. **Via Render Dashboard**
   ```
   Render Service → Environment → Environment Variables
   ```

2. **Important Notes**
   - Variables marked with `sync: false` in `render.yaml` must be set manually
   - Use "Generate Value" for secrets like JWT keys
   - Database URL is automatically set when database is connected

## 🔒 Security Best Practices

### 1. Secret Generation
```bash
# Generate JWT secret (32+ characters)
openssl rand -base64 32

# Generate random password
openssl rand -base64 24

# Generate API key format
echo "$(date +%s)_$(openssl rand -hex 16)"
```

### 2. Secret Rotation Schedule
- **JWT Keys**: Every 6 months
- **API Keys**: Every 3 months  
- **Database Passwords**: Every 6 months
- **SMTP Passwords**: When compromised or annually

### 3. Environment Separation
```bash
# Development
JWT_SECRET_KEY=dev-secret-key-not-for-production

# Staging  
JWT_SECRET_KEY=staging-secret-key-different-from-prod

# Production
JWT_SECRET_KEY=production-secret-key-ultra-secure
```

### 4. Secret Validation
Add to your deployment pipeline:
```bash
# Check JWT key length
if [ ${#JWT_SECRET_KEY} -lt 32 ]; then
  echo "JWT_SECRET_KEY must be at least 32 characters"
  exit 1
fi

# Check for example values
if [[ "$JWT_SECRET_KEY" == *"example"* ]]; then
  echo "JWT_SECRET_KEY cannot contain 'example'"
  exit 1
fi
```

## 📋 Deployment Checklist

### Pre-Deployment Security Check
- [ ] All secrets are environment-specific (no shared secrets)
- [ ] No example/placeholder values in production
- [ ] JWT secret is at least 32 characters
- [ ] Database URL uses SSL in production
- [ ] CORS origins are restricted to production domains
- [ ] Debug mode is disabled in production
- [ ] Sentry DSN is configured for error monitoring

### GitHub Secrets Checklist
- [ ] `DATABASE_URL` - Production database connection
- [ ] `JWT_SECRET_KEY` - Unique 32+ character string
- [ ] `OPENAI_API_KEY` - Valid OpenAI API key
- [ ] `SENTRY_DSN` - Sentry error monitoring DSN
- [ ] `RENDER_API_KEY` - Render deployment key
- [ ] `VERCEL_TOKEN` - Vercel deployment token
- [ ] `SMTP_*` variables - Email configuration

### Vercel Environment Variables Checklist  
- [ ] `NEXT_PUBLIC_API_URL` - Production backend URL
- [ ] `NEXT_PUBLIC_ENVIRONMENT` - Set to "production"
- [ ] `NEXT_PUBLIC_SENTRY_DSN` - Frontend error monitoring
- [ ] `SENTRY_ORG` and `SENTRY_PROJECT` - Build-time Sentry config

### Render Environment Variables Checklist
- [ ] `ENVIRONMENT=production` - Runtime environment
- [ ] `DATABASE_URL` - Connected to production database
- [ ] `JWT_SECRET_KEY` - Auto-generated secure key
- [ ] `OPENAI_API_KEY` - Manually set in dashboard
- [ ] `SENTRY_DSN` - Manually set in dashboard
- [ ] `SMTP_*` variables - Manually set email config

## 🚨 Incident Response

### If Secrets Are Compromised

1. **Immediate Actions**
   - Rotate the compromised secret immediately
   - Update all environments with new secret
   - Monitor for unauthorized access

2. **Update Process**
   ```bash
   # Generate new secret
   NEW_SECRET=$(openssl rand -base64 32)
   
   # Update in GitHub
   # (via GitHub UI: Settings → Secrets → Actions)
   
   # Update in Vercel
   vercel env rm JWT_SECRET_KEY production
   vercel env add JWT_SECRET_KEY production
   
   # Update in Render
   # (via Render Dashboard: Environment → Environment Variables)
   ```

3. **Verification**
   - Test all deployments with new secrets
   - Verify health check endpoints respond correctly
   - Monitor application logs for authentication errors

### Emergency Contacts
- **GitHub**: Repository admins
- **Vercel**: Team owners with deployment access  
- **Render**: Service admins
- **Database**: Database administrator

## 🔍 Monitoring & Validation

### Automated Secret Validation
The application includes validation endpoints:
- `/validate/deployment` - Checks all secrets are properly configured
- `/health/detailed` - Validates external service connectivity

### Manual Verification
```bash
# Test health endpoints
curl https://your-api.onrender.com/health/ready
curl https://your-api.onrender.com/validate/deployment

# Test frontend
curl https://your-app.vercel.app

# Verify environment
curl https://your-api.onrender.com/health | jq '.environment'
```