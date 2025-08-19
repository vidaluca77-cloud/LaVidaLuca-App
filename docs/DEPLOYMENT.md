# Deployment Guide - La Vida Luca

This guide covers deploying the La Vida Luca application to production using Vercel (frontend) and Render (backend).

## Prerequisites

- Node.js 18.x or higher
- Python 3.11 or higher
- Git
- Vercel CLI (optional)
- Render account

## Environment Variables

### Frontend (.env.local)
```bash
# Backend API Configuration
NEXT_PUBLIC_API_URL=https://your-backend-url.render.com/api/v1

# Application Configuration
NEXT_PUBLIC_APP_NAME=La Vida Luca
NEXT_PUBLIC_APP_DESCRIPTION=Plateforme collaborative dédiée à la formation des jeunes en MFR

# Contact Information
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789

# Sentry (optional, for monitoring)
NEXT_PUBLIC_SENTRY_DSN=your_sentry_dsn
```

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Security
JWT_SECRET_KEY=your_super_secure_secret_key_here
CORS_ORIGINS=["https://your-frontend-domain.vercel.app"]

# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=1000

# Application
ENVIRONMENT=production
LOG_LEVEL=INFO

# Sentry (optional)
SENTRY_DSN=your_sentry_backend_dsn
```

## Frontend Deployment (Vercel)

### Automatic Deployment (Recommended)

1. **Connect GitHub Repository**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository `vidaluca77-cloud/LaVidaLuca-App`

2. **Configure Project Settings**
   - Framework Preset: Next.js
   - Root Directory: `./` (leave empty)
   - Build Command: `npm run build`
   - Output Directory: `.next`

3. **Set Environment Variables**
   - In Vercel Dashboard → Project Settings → Environment Variables
   - Add all variables from the frontend .env.local template above

4. **Deploy**
   - Click "Deploy"
   - Vercel will automatically deploy on every push to main branch

### Manual Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
cd /path/to/LaVidaLuca-App
vercel --prod
```

## Backend Deployment (Render)

### Automatic Deployment (Recommended)

1. **Create Render Account**
   - Go to [Render.com](https://render.com)
   - Sign up/login with GitHub

2. **Create PostgreSQL Database**
   - In Render Dashboard → New → PostgreSQL
   - Database Name: `lavidaluca-db`
   - Plan: Free or Starter
   - Region: Oregon (or closest to your users)

3. **Create Web Service**
   - In Render Dashboard → New → Web Service
   - Connect GitHub repository
   - Use existing configuration: `apps/backend/render.yaml`

4. **Configure Environment Variables**
   - The render.yaml will auto-configure most variables
   - Manually set in Render Dashboard:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `JWT_SECRET_KEY`: Generate a secure secret
     - `SENTRY_DSN`: Your Sentry DSN (optional)

5. **Deploy**
   - Render will automatically deploy from `render.yaml`
   - Subsequent deployments happen on every push to main

### Manual Database Setup

If you need to set up the database manually:

```bash
# Connect to your Render PostgreSQL
psql $DATABASE_URL

# Run migrations (will happen automatically on deploy)
cd apps/backend
alembic upgrade head

# Optional: Seed data
python seed.py
```

## CI/CD Pipeline

The application includes a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that:

1. **Tests** both frontend and backend on every PR
2. **Security scans** dependencies
3. **Deploys** automatically to production on main branch pushes

### Required GitHub Secrets

Add these secrets in GitHub repository settings:

```bash
# Vercel Deployment
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=your_vercel_org_id
VERCEL_PROJECT_ID=your_vercel_project_id

# Render Deployment
RENDER_API_KEY=your_render_api_key
RENDER_SERVICE_ID=your_render_service_id

# Optional: Slack Notifications
SLACK_WEBHOOK_URL=your_slack_webhook_url
```

## Domain Configuration

### Custom Domain (Vercel)

1. **Add Domain in Vercel**
   - Dashboard → Project → Settings → Domains
   - Add your domain (e.g., `lavidaluca.fr`)

2. **Configure DNS**
   - Add CNAME record: `www` → `cname.vercel-dns.com`
   - Add A record: `@` → `76.76.19.61`

### Backend Domain (Render)

1. **Custom Domain**
   - Render Dashboard → Service → Settings → Custom Domains
   - Add domain (e.g., `api.lavidaluca.fr`)

2. **Update Frontend Environment**
   - Update `NEXT_PUBLIC_API_URL` to your custom domain
   - Redeploy frontend

## SSL/HTTPS

Both Vercel and Render provide automatic SSL certificates:
- **Vercel**: Automatic Let's Encrypt certificates
- **Render**: Automatic SSL for custom domains

## Monitoring and Observability

### Sentry Setup

1. **Create Sentry Project**
   - Go to [Sentry.io](https://sentry.io)
   - Create new project for React (frontend) and Python (backend)

2. **Configure Environment Variables**
   - Add Sentry DSNs to both frontend and backend env vars
   - Redeploy both services

### Health Checks

- **Frontend**: Automatic Vercel monitoring
- **Backend**: `/health` endpoint monitored by Render
- **Custom**: `/monitoring` page for detailed metrics

## Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   # Check build logs in Vercel/Render dashboard
   # Ensure all environment variables are set
   # Verify Node.js/Python versions
   ```

2. **Database Connection Issues**
   ```bash
   # Check DATABASE_URL format
   # Ensure database is running
   # Verify firewall/network settings
   ```

3. **CORS Errors**
   ```bash
   # Update CORS_ORIGINS in backend
   # Ensure frontend domain is included
   # Check protocol (https vs http)
   ```

4. **API Key Issues**
   ```bash
   # Verify OpenAI API key is valid
   # Check API key permissions
   # Monitor API usage/quotas
   ```

### Performance Optimization

1. **Frontend**
   - Enable Vercel Analytics
   - Configure caching headers
   - Optimize images and assets

2. **Backend**
   - Database connection pooling
   - Redis caching (upgrade Render plan)
   - API response caching

### Scaling

1. **Frontend**: Automatic with Vercel
2. **Backend**: Upgrade Render plan for:
   - More CPU/RAM
   - Database scaling
   - Multiple regions

## Security Checklist

- [ ] All secrets in environment variables (not code)
- [ ] HTTPS enforced on both frontend and backend
- [ ] CORS properly configured
- [ ] Database credentials secure
- [ ] API keys rotated regularly
- [ ] Dependency security scans enabled
- [ ] Error reporting configured
- [ ] Backup strategy in place

## Support

- **Documentation**: See main README.md
- **Issues**: GitHub Issues
- **Monitoring**: Sentry dashboard
- **Logs**: Vercel/Render dashboards

---

**Last Updated**: 2024
**Version**: 1.0.0