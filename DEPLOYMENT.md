# Production Deployment Guide

## Overview

This document outlines the production deployment configuration for La Vida Luca App, including security settings, environment separation, and monitoring setup.

## Architecture

- **Frontend**: Next.js deployed on Vercel
- **Backend**: FastAPI deployed on Render
- **Database**: PostgreSQL hosted on Render
- **CI/CD**: GitHub Actions

## Environment Configuration

### Frontend (.env.production)

The frontend production environment is configured in `apps/web/.env.production`. Key settings include:

- API endpoints pointing to production backend
- Security and monitoring flags enabled
- Production-optimized performance settings

### Backend (.env.production)

The backend production environment is documented in `apps/backend/.env.production`. Configuration includes:

- Database connection via Render
- Security headers and CORS settings
- Rate limiting and authentication
- External API integrations

## Deployment Configuration

### Render Backend (render.yaml)

The `apps/backend/render.yaml` file configures:

- **Service Configuration**: Python runtime with Gunicorn + Uvicorn
- **Auto-deployment**: Triggered on main branch pushes
- **Environment Variables**: All production settings
- **Database**: PostgreSQL with automatic backups
- **Health Checks**: Automated monitoring

Key security features:
- JWT secret auto-generation
- CORS configuration for allowed origins
- Rate limiting enabled
- Trusted hosts configuration

### GitHub Actions (.github/workflows/deploy.yml)

Enhanced deployment workflow with:

1. **Pre-deployment Validation**
   - Checks for required secrets
   - Validates deployment prerequisites

2. **Backend Deployment**
   - Triggers Render deployment via webhook
   - Waits for deployment completion
   - Performs health checks

3. **Frontend Deployment**
   - Deploys to Vercel with production configuration
   - Verifies deployment success

4. **Post-deployment Tasks**
   - Status reporting
   - Security reminders

## Security Configuration

### Production Security Features

1. **Environment Separation**
   - Separate configuration files for each environment
   - Production-specific security headers
   - HTTPS-only configuration

2. **Authentication & Authorization**
   - JWT tokens with secure generation
   - Rate limiting (100 req/min authenticated, 20 req/min anonymous)
   - CORS restrictions to allowed domains

3. **Security Headers**
   - X-Frame-Options: DENY
   - X-Content-Type-Options: nosniff
   - Strict Content Security Policy
   - Referrer Policy enforcement

4. **API Security**
   - Trusted hosts configuration
   - Input validation and sanitization
   - Secure cookie settings

## Monitoring Setup

### Health Checks

- **Backend**: `/health` endpoint monitored by Render
- **Frontend**: Vercel automatic monitoring
- **Database**: Built-in PostgreSQL monitoring

### Error Tracking

Configure Sentry for both frontend and backend:

```bash
# Frontend
NEXT_PUBLIC_SENTRY_DSN=your_frontend_dsn

# Backend  
SENTRY_DSN=your_backend_dsn
SENTRY_ENVIRONMENT=production
```

### Performance Monitoring

- Render provides automatic performance metrics
- Vercel Analytics for frontend performance
- Custom application metrics via `/metrics` endpoint

## Required Secrets

### GitHub Repository Secrets

Configure these in GitHub repository settings:

```bash
# Backend Deployment
RENDER_DEPLOY_HOOK_IA=https://api.render.com/deploy/...

# Frontend Deployment
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=your_org_id
VERCEL_PROJECT_ID=your_project_id
```

### Render Dashboard Configuration

Set these manually in Render dashboard:

```bash
# Required
OPENAI_API_KEY=your_production_openai_key
SENTRY_DSN=your_backend_sentry_dsn

# Optional
SMTP_HOST=your_smtp_host
SMTP_USERNAME=your_smtp_username
SMTP_PASSWORD=your_smtp_password
```

### Vercel Dashboard Configuration

Set these in Vercel project settings:

```bash
# Monitoring
NEXT_PUBLIC_SENTRY_DSN=your_frontend_sentry_dsn
SENTRY_DSN=your_backend_sentry_dsn

# Optional Analytics
NEXT_PUBLIC_GA_TRACKING_ID=your_ga_id
```

## Deployment Process

### Automatic Deployment

1. **Trigger**: Push to `main` branch
2. **Validation**: Check required secrets and prerequisites
3. **Backend**: Deploy to Render with health checks
4. **Frontend**: Deploy to Vercel with production config
5. **Verification**: Health checks and status reporting

### Manual Deployment

```bash
# Backend (via Render dashboard)
# - Go to Render dashboard
# - Select lavidaluca-backend service
# - Click "Manual Deploy" -> "Deploy latest commit"

# Frontend (via Vercel CLI)
cd apps/web
vercel --prod
```

## Monitoring & Maintenance

### Daily Checks

- Monitor application health endpoints
- Check error rates in Sentry
- Review performance metrics

### Weekly Maintenance

- Update dependencies if needed
- Review and rotate secrets as needed
- Check database performance

### Monthly Reviews

- Security audit of configuration
- Performance optimization
- Backup verification

## Troubleshooting

### Common Issues

1. **Deployment Failed**
   - Check GitHub Actions logs
   - Verify all secrets are configured
   - Check Render/Vercel dashboards for errors

2. **Health Check Failed**
   - Verify database connectivity
   - Check environment variables
   - Review application logs

3. **Frontend Not Loading**
   - Check API endpoint configuration
   - Verify CORS settings
   - Check Vercel deployment logs

### Support Contacts

- **Technical Issues**: Check repository issues
- **Production Incidents**: Contact deployment team
- **Security Concerns**: Follow security incident process

## Production URLs

- **Frontend**: https://lavidaluca.vercel.app
- **Backend API**: https://lavidaluca-backend.onrender.com
- **API Documentation**: https://lavidaluca-backend.onrender.com/docs
- **Health Check**: https://lavidaluca-backend.onrender.com/health