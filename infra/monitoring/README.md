# Monitoring configuration for La Vida Luca

## Health Checks

The application includes automated health monitoring:

### Services Monitored
- **Frontend** (Vercel): Check homepage accessibility
- **Backend Health** (Render): Check `/health` endpoint
- **Backend API** (Render): Check `/activities` endpoint functionality

### Scripts
- `health-check.sh`: Main health check script
- Can be run manually or via cron job

### Setup Monitoring

1. **Manual Check**:
   ```bash
   ./infra/monitoring/health-check.sh
   ```

2. **Automated Monitoring** (Cron):
   ```bash
   # Add to crontab for checks every 5 minutes
   */5 * * * * /path/to/infra/monitoring/health-check.sh
   ```

3. **Environment Variables**:
   ```bash
   export FRONTEND_URL="https://your-frontend.vercel.app"
   export BACKEND_URL="https://your-backend.onrender.com"
   export WEBHOOK_URL="https://discord.com/api/webhooks/..."  # Optional
   ```

### Notifications

Configure webhook URL for Discord/Slack notifications:
- Set `WEBHOOK_URL` environment variable
- Notifications sent on service failures and recoveries
- Includes timestamp and service status

### GitHub Actions Integration

The CI/CD pipeline includes:
- Automated testing on push/PR
- Security scanning with Trivy
- Deployment on main branch
- Health checks after deployment

### Recommended Monitoring Tools

For production, consider:
- **Uptime Robot**: External monitoring service
- **Better Stack**: Application monitoring
- **Sentry**: Error tracking
- **LogRocket**: Session replay and monitoring

### Render Monitoring

Render provides built-in monitoring:
- Service health checks
- Automatic restarts on failure
- Logs and metrics dashboard
- Custom health check endpoints

### Vercel Monitoring

Vercel Analytics provides:
- Page load performance
- Core Web Vitals
- User experience metrics
- Error tracking