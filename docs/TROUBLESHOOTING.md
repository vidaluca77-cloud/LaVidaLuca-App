# Troubleshooting Guide

## Overview

This guide helps you diagnose and resolve common issues with the La Vida Luca application across development, staging, and production environments.

## Quick Diagnosis

Use these commands to quickly check system health:

```bash
# Check frontend health
curl https://la-vida-luca.vercel.app/api/health

# Check backend health  
curl https://la-vida-luca-ia.onrender.com/health

# Check application metrics
curl https://la-vida-luca.vercel.app/api/metrics

# Check GitHub Actions status
gh run list --limit 5
```

## Common Issues

### 1. Build Failures

#### Frontend Build Issues

**Symptom**: `npm run build` fails
```
Error: Missing required environment variable: NEXT_PUBLIC_SUPABASE_URL
```

**Solution**:
```bash
# Check environment variables
cat .env.local | grep NEXT_PUBLIC

# Copy from example if missing
cp .env.example .env.local

# Edit with correct values
nano .env.local
```

**Symptom**: TypeScript compilation errors
```
Type error: Property 'xxx' does not exist on type 'yyy'
```

**Solution**:
```bash
# Run type check to see all errors
npx tsc --noEmit

# Check for missing type definitions
npm install @types/node @types/react @types/react-dom

# Clear Next.js cache
rm -rf .next/
npm run build
```

**Symptom**: Font loading errors (Google Fonts)
```
Failed to fetch 'Inter' from Google Fonts
```

**Solution**: Already fixed in current version. If issue persists:
```typescript
// Use system fonts fallback
const inter = { className: "font-sans" };
```

#### Backend Build Issues

**Symptom**: Poetry dependency conflicts
```
SolverProblemError: Because no versions of X match >Y,<Z...
```

**Solution**:
```bash
cd apps/ia

# Clear poetry cache
poetry cache clear --all pypi

# Remove lock file and reinstall
rm poetry.lock
poetry install

# If still failing, update constraints
poetry update
```

**Symptom**: Python version compatibility
```
RuntimeError: Python 3.x is not supported
```

**Solution**:
```bash
# Check Python version
python --version

# Install correct version with pyenv
pyenv install 3.11.0
pyenv local 3.11.0

# Recreate virtual environment
poetry env remove python
poetry install
```

### 2. Deployment Issues

#### Vercel Deployment Problems

**Symptom**: Build succeeds locally but fails on Vercel
```
Error: Command "npm run build" exited with 1
```

**Diagnostics**:
1. Check Vercel build logs in dashboard
2. Verify Node.js version in Vercel settings
3. Check environment variables are set

**Solution**:
```bash
# Set Node.js version in package.json
{
  "engines": {
    "node": ">=18.0.0"
  }
}

# Or create .nvmrc file
echo "18" > .nvmrc
```

**Symptom**: Environment variables not available
```
ReferenceError: process is not defined
```

**Solution**:
1. Verify environment variables are set in Vercel dashboard
2. Check they are prefixed with `NEXT_PUBLIC_` for client-side access
3. Restart deployment after setting variables

#### Render Deployment Problems

**Symptom**: Service fails to start
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution**:
```yaml
# Check render.yaml build command
buildCommand: cd apps/ia && poetry install --no-dev

# Or update Docker build
FROM python:3.11-slim
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev
```

**Symptom**: Health check failures
```
Health check failed: Connection refused
```

**Solution**:
1. Check service is listening on `0.0.0.0:$PORT`
2. Verify health check path: `/health`
3. Check startup time isn't exceeding timeout

```python
# Ensure correct host binding
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 3. Database Issues

#### Connection Problems

**Symptom**: Cannot connect to Supabase
```
Error: Invalid API key or URL
```

**Diagnostics**:
```bash
# Test connection manually
curl "${NEXT_PUBLIC_SUPABASE_URL}/rest/v1/" \
  -H "apikey: ${NEXT_PUBLIC_SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${NEXT_PUBLIC_SUPABASE_ANON_KEY}"
```

**Solution**:
1. Verify URL format: `https://project-id.supabase.co`
2. Check API key is correct and active
3. Ensure project isn't paused

#### Migration Issues

**Symptom**: Schema migration fails
```
Error: relation "activities" already exists
```

**Solution**:
```bash
# Check current schema state
supabase db diff --db-url "your-db-url"

# Reset if needed (development only!)
supabase db reset --db-url "your-db-url"

# Apply specific migration
supabase db push --db-url "your-db-url"
```

#### RLS Policy Issues

**Symptom**: User cannot access data
```
Error: permission denied for table activities
```

**Solution**:
1. Check RLS policies are correct
2. Verify user authentication
3. Review policy conditions

```sql
-- Check current policies
SELECT * FROM pg_policies WHERE tablename = 'activities';

-- Test policy with specific user
SET ROLE anon;
SELECT * FROM activities;
```

### 4. API Connectivity Issues

#### CORS Errors

**Symptom**: Browser CORS errors
```
Access to fetch at 'backend-url' from origin 'frontend-url' has been blocked by CORS policy
```

**Solution**:
```python
# Update CORS configuration in backend
allowed_origins = [
    "http://localhost:3000",
    "https://la-vida-luca.vercel.app",
    "https://la-vida-luca-staging.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

#### API Timeout Issues

**Symptom**: API requests timeout
```
TimeoutError: Request timed out after 30s
```

**Solution**:
1. Check backend service status
2. Verify network connectivity
3. Increase timeout if needed

```typescript
// Increase fetch timeout
const response = await fetch(url, {
  signal: AbortSignal.timeout(60000), // 60s timeout
});
```

### 5. Performance Issues

#### Slow Page Loading

**Symptom**: Pages load slowly (>3 seconds)

**Diagnostics**:
```bash
# Run Lighthouse audit
npx lighthouse https://la-vida-luca.vercel.app --output=json

# Check Core Web Vitals
curl https://la-vida-luca.vercel.app/api/metrics
```

**Solution**:
1. Optimize images and assets
2. Enable caching headers
3. Use CDN for static assets
4. Implement code splitting

#### Database Query Performance

**Symptom**: API responses are slow

**Solution**:
```sql
-- Add database indexes
CREATE INDEX idx_activities_category ON activities(category);
CREATE INDEX idx_activities_is_active ON activities(is_active);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM activities WHERE category = 'agri';
```

### 6. Security Issues

#### Authentication Problems

**Symptom**: User login fails
```
Error: Invalid credentials
```

**Solution**:
1. Check Supabase authentication settings
2. Verify email/password requirements
3. Check RLS policies

#### SSL/TLS Issues

**Symptom**: SSL certificate warnings
```
NET::ERR_CERT_DATE_INVALID
```

**Solution**:
1. Check certificate expiry
2. Verify domain configuration
3. Contact hosting provider if needed

```bash
# Check SSL certificate
openssl s_client -connect la-vida-luca.vercel.app:443 -servername la-vida-luca.vercel.app
```

## Environment-Specific Issues

### Development Environment

#### Local Supabase Issues

**Symptom**: Supabase not starting
```
Error: Docker daemon not running
```

**Solution**:
```bash
# Start Docker
sudo systemctl start docker

# Restart Supabase
supabase stop
supabase start

# Check status
supabase status
```

#### Hot Reload Not Working

**Symptom**: Changes don't reflect in browser

**Solution**:
```bash
# Clear cache and restart
rm -rf .next/
npm run dev

# Check file watchers limit (Linux)
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### Staging Environment

#### Environment Variable Mismatch

**Symptom**: Wrong API URL being used

**Solution**:
1. Check environment variables in deployment platform
2. Verify branch-specific configurations
3. Clear deployment cache

### Production Environment

#### High Traffic Issues

**Symptom**: 503 Service Unavailable errors

**Solution**:
1. Check resource usage
2. Scale services if needed
3. Implement rate limiting
4. Use CDN for static assets

## Monitoring & Debugging

### Log Analysis

#### Frontend Logs (Vercel)
```bash
# View logs
vercel logs la-vida-luca

# Real-time logs
vercel logs la-vida-luca --follow
```

#### Backend Logs (Render)
Check Render dashboard for service logs

#### Database Logs (Supabase)
Check Supabase dashboard > Settings > Database > Logs

### Performance Monitoring

```bash
# Check response times
curl -o /dev/null -s -w 'Total: %{time_total}s\n' https://la-vida-luca.vercel.app

# Monitor resource usage
curl https://la-vida-luca.vercel.app/api/metrics
```

### Error Tracking

If Sentry is configured:
1. Check Sentry dashboard for errors
2. Review error frequency and patterns
3. Set up alerts for critical errors

## Recovery Procedures

### Database Recovery

#### Restore from Backup
```bash
# List available backups
aws s3 ls s3://la-vida-luca-backups/database/

# Download backup
aws s3 cp s3://la-vida-luca-backups/database/backup-20231201.sql .

# Restore (be careful!)
psql "your-database-url" < backup-20231201.sql
```

#### Point-in-Time Recovery
Use Supabase dashboard for point-in-time recovery if available.

### Service Recovery

#### Rollback Deployment
```bash
# GitHub Actions: Re-run previous successful deployment
# Or manual rollback:
git checkout previous-working-commit
git push origin main --force
```

#### Emergency Maintenance Mode
```bash
# Enable maintenance mode
vercel env add NEXT_PUBLIC_MAINTENANCE_MODE true production
vercel --prod

# Deploy maintenance page
```

## Prevention Strategies

### Monitoring Setup

1. **Health Checks**: Run every 5 minutes
2. **Performance Monitoring**: Daily Lighthouse audits
3. **Error Tracking**: Real-time error monitoring
4. **Uptime Monitoring**: External uptime services

### Testing Strategy

1. **Pre-deployment Testing**: Comprehensive test suite
2. **Staging Environment**: Test all changes in staging first
3. **Canary Deployments**: Gradual rollout for major changes
4. **Rollback Plan**: Always have a rollback strategy

### Documentation

1. **Runbooks**: Document common procedures
2. **Incident Response**: Clear escalation procedures
3. **Knowledge Base**: Maintain troubleshooting guides
4. **Post-mortems**: Learn from incidents

## Emergency Contacts

### Escalation Process

1. **Level 1**: Developer on-call
2. **Level 2**: Tech lead
3. **Level 3**: Infrastructure team
4. **Level 4**: External support (Vercel, Render, Supabase)

### Service Status Pages

- **Vercel**: https://vercel-status.com
- **Render**: https://status.render.com
- **Supabase**: https://status.supabase.com
- **GitHub**: https://githubstatus.com

Remember: When in doubt, check service status pages first to rule out provider issues.