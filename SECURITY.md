# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please follow these steps:

1. **Do NOT create a public GitHub issue**
2. Email security@lavidaluca.fr with details
3. Include steps to reproduce the vulnerability
4. Allow up to 48 hours for initial response

## Security Measures

### Application Security

- **Authentication**: Supabase Auth with RLS policies
- **Authorization**: Row Level Security (RLS) on all tables
- **Input Validation**: Server-side validation on all inputs
- **SQL Injection Protection**: Parameterized queries only
- **XSS Protection**: Content Security Policy headers
- **CSRF Protection**: SameSite cookies and CSRF tokens

### Infrastructure Security

- **HTTPS**: Enforced on all environments
- **Security Headers**: HSTS, CSP, X-Frame-Options, etc.
- **Environment Separation**: Isolated staging/production
- **Secret Management**: Encrypted environment variables
- **Container Security**: Non-root users, minimal base images

### API Security

- **Rate Limiting**: Implemented on all endpoints
- **CORS**: Properly configured allowed origins
- **Input Sanitization**: All user inputs sanitized
- **Error Handling**: No sensitive information in error messages
- **Logging**: Security events logged and monitored

### Database Security

- **Encryption**: At rest and in transit
- **Access Control**: Least privilege principle
- **Backup Security**: Encrypted backups
- **Audit Logging**: All database access logged
- **Regular Updates**: Automated security patches

## Security Monitoring

- **Vulnerability Scanning**: Automated with Snyk and Trivy
- **Dependency Updates**: Dependabot for automated updates
- **Security Alerts**: Real-time notifications
- **Access Monitoring**: Failed login attempts tracked
- **Incident Response**: 24/7 monitoring and alerting

## Compliance

- **Data Protection**: GDPR compliant data handling
- **Privacy**: Minimal data collection
- **Retention**: Automated data cleanup
- **Consent**: Clear privacy policies

## Regular Security Reviews

- **Code Reviews**: Security focus in all PR reviews
- **Penetration Testing**: Annual third-party testing
- **Security Training**: Regular team security training
- **Incident Drills**: Quarterly security incident simulations