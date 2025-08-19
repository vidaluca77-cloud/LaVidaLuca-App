# CI/CD Pipeline Documentation

## Overview

This document describes the complete CI/CD pipeline for La Vida Luca App, including deployment processes, environment management, and monitoring setup.

## Architecture

The application follows a microservices architecture:

- **Frontend**: Next.js application deployed on Vercel
- **Backend**: FastAPI application deployed on Render
- **Database**: Supabase (PostgreSQL with real-time features)
- **Monitoring**: GitHub Actions + Slack notifications

## Environments

### Development
- **Frontend**: Local development server (`npm run dev`)
- **Backend**: Local FastAPI server (`uvicorn main:app --reload`)
- **Database**: Local Supabase instance or development project
- **Domain**: localhost:3000

### Staging
- **Frontend**: https://la-vida-luca-staging.vercel.app
- **Backend**: https://la-vida-luca-ia-staging.onrender.com
- **Database**: Supabase staging project
- **Branch**: `develop`

### Production
- **Frontend**: https://la-vida-luca.vercel.app
- **Backend**: https://la-vida-luca-ia.onrender.com
- **Database**: Supabase production project
- **Branch**: `main`

## GitHub Actions Workflows

### 1. Frontend CI/CD (`.github/workflows/frontend-ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Changes to frontend files

**Jobs:**
- **Test**: Linting, type checking, unit tests
- **Build**: Build Next.js application
- **Security Scan**: Snyk vulnerability scanning
- **Deploy Preview**: Deploy PR previews to Vercel
- **Deploy Staging**: Deploy `develop` branch to staging
- **Deploy Production**: Deploy `main` branch to production

### 2. Backend CI/CD (`.github/workflows/backend-ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Changes to `apps/ia/**` or `infra/**`

**Jobs:**
- **Test**: Python linting, type checking, pytest
- **Build Image**: Build and push Docker image to GitHub Container Registry
- **Security Scan**: Trivy container vulnerability scanning
- **Deploy Staging**: Deploy to Render staging environment
- **Deploy Production**: Deploy to Render production environment

### 3. Database Operations (`.github/workflows/database-ops.yml`)

**Triggers:**
- Manual workflow dispatch
- Push to `main` or `develop` with database changes

**Jobs:**
- **Migrate**: Run database migrations
- **Seed**: Populate database with seed data
- **Backup**: Create and store database backups
- **Restore**: Restore database from backup
- **Health Check**: Verify database connectivity

### 4. Monitoring (`.github/workflows/monitoring.yml`)

**Triggers:**
- Scheduled every 5 minutes
- Manual workflow dispatch

**Jobs:**
- **Frontend Health**: Check frontend availability and performance
- **Backend Health**: Check backend API endpoints
- **Database Health**: Verify database connectivity
- **Performance Monitoring**: Lighthouse audits
- **Security Monitoring**: SSL certificate and security headers check
- **Cleanup**: Remove old artifacts and logs

## Deployment Process

### Automatic Deployments

1. **Development**: 
   - Work on feature branches
   - Create PR to `develop`
   - Automatic preview deployment on Vercel

2. **Staging**:
   - Merge PR to `develop`
   - Automatic deployment to staging environment
   - Run integration tests

3. **Production**:
   - Merge `develop` to `main`
   - Automatic deployment to production
   - Health checks and monitoring

### Manual Deployments

Use GitHub Actions workflow dispatch for:
- Emergency deployments
- Database operations
- Rollbacks

## Environment Variables

### Required Secrets

Set these in GitHub repository secrets:

#### Vercel Deployment
```
VERCEL_TOKEN=your-vercel-token
VERCEL_ORG_ID=your-org-id
VERCEL_PROJECT_ID=your-project-id
```

#### Render Deployment
```
RENDER_API_KEY=your-render-api-key
RENDER_STAGING_SERVICE_ID=staging-service-id
RENDER_PRODUCTION_SERVICE_ID=production-service-id
```

#### Database (Supabase)
```
SUPABASE_URL_STAGING=https://staging-project.supabase.co
SUPABASE_ANON_KEY_STAGING=staging-anon-key
SUPABASE_URL_PROD=https://production-project.supabase.co
SUPABASE_ANON_KEY_PROD=production-anon-key
SUPABASE_DB_URL=postgres://connection-string
```

#### Monitoring & Notifications
```
SLACK_WEBHOOK_URL=https://hooks.slack.com/your-webhook
SNYK_TOKEN=your-snyk-token
SENTRY_DSN=your-sentry-dsn
```

#### AWS (for backups)
```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

### Environment Files

Copy `.env.example` to appropriate environment files:
- `.env.local` (development)
- `.env.staging` (staging)
- `.env.production` (production)

## Security Measures

### 1. Code Security
- Snyk vulnerability scanning
- Trivy container scanning
- Dependabot for dependency updates
- CodeQL security analysis

### 2. Infrastructure Security
- HTTPS enforcement
- Security headers (CSP, HSTS, etc.)
- Trusted host middleware
- CORS configuration

### 3. Database Security
- Row Level Security (RLS) policies
- Encrypted connections
- Backup encryption
- Access logging

### 4. Deployment Security
- Least privilege access
- Environment separation
- Secret management
- Audit logging

## Monitoring & Alerting

### Health Checks
- **Frontend**: `/api/health` endpoint
- **Backend**: `/health` endpoint
- **Database**: Connection and query tests

### Performance Monitoring
- Lighthouse CI for Core Web Vitals
- Response time monitoring
- Error rate tracking
- Uptime monitoring

### Error Tracking
- Sentry for application errors
- GitHub Actions for pipeline failures
- Slack notifications for critical issues

### Metrics Collection
- Application metrics via `/api/metrics`
- Infrastructure metrics from hosting providers
- Custom business metrics

## Backup Strategy

### Database Backups
- **Frequency**: Daily automated backups
- **Retention**: 30 days
- **Storage**: AWS S3 with encryption
- **Testing**: Monthly restore tests

### Application Backups
- **Code**: Git repository with multiple remotes
- **Assets**: Automated backup to cloud storage
- **Configurations**: Version controlled

### Disaster Recovery
- **RTO**: 4 hours (Recovery Time Objective)
- **RPO**: 24 hours (Recovery Point Objective)
- **Procedures**: Documented restoration steps
- **Testing**: Quarterly DR drills

## Troubleshooting

### Common Issues

#### Build Failures
1. Check Node.js/Python version compatibility
2. Verify environment variables are set
3. Review dependency conflicts
4. Check for TypeScript errors

#### Deployment Failures
1. Verify service configuration
2. Check resource quotas
3. Review deployment logs
4. Validate environment variables

#### Database Issues
1. Check connection strings
2. Verify network connectivity
3. Review migration status
4. Check database logs

#### Performance Issues
1. Monitor resource usage
2. Check database query performance
3. Review CDN cache hit rates
4. Analyze error logs

### Monitoring Commands

```bash
# Check frontend health
curl https://la-vida-luca.vercel.app/api/health

# Check backend health
curl https://la-vida-luca-ia.onrender.com/health

# Check application metrics
curl https://la-vida-luca.vercel.app/api/metrics

# View GitHub Actions logs
gh run list --workflow=frontend-ci.yml
gh run view [run-id] --log
```

### Emergency Procedures

#### Rollback Production
1. Navigate to GitHub Actions
2. Find last successful deployment
3. Re-run deployment workflow
4. Monitor health checks

#### Database Emergency
1. Stop application traffic if needed
2. Create emergency backup
3. Restore from last known good backup
4. Validate data integrity

#### Security Incident
1. Rotate all secrets immediately
2. Review access logs
3. Deploy security patches
4. Document incident response

## Maintenance

### Regular Tasks
- **Weekly**: Review monitoring alerts
- **Monthly**: Update dependencies
- **Quarterly**: Security audit
- **Annually**: Disaster recovery test

### Updates
- Monitor for security updates
- Test updates in staging first
- Schedule maintenance windows
- Communicate changes to users

## Support

For issues with the CI/CD pipeline:
1. Check this documentation
2. Review GitHub Actions logs
3. Contact the development team
4. Create issue in repository