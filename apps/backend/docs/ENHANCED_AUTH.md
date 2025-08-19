# Enhanced Authentication System

This document describes the enhanced authentication system implemented for the LaVidaLuca application, providing comprehensive security features including refresh tokens, session management, 2FA, and advanced security controls.

## 🔐 Features Overview

### Core Authentication
- **JWT Access Tokens**: Short-lived tokens (30 minutes) for API access
- **Refresh Tokens**: Long-lived tokens (30 days) with rotation for security
- **Device Fingerprinting**: Track sessions across different devices
- **Session Management**: Multi-device session tracking and control

### Security Features
- **Rate Limiting**: Configurable per-endpoint rate limits
- **Account Lockout**: Automatic lockout after failed login attempts
- **Password Policies**: Strong password requirements with validation
- **Two-Factor Authentication (2FA)**: TOTP-based with backup codes
- **Audit Logging**: Comprehensive security event tracking

### User Management
- **Admin Controls**: User activation, lockout, password reset
- **Session Control**: Terminate sessions remotely
- **Security Monitoring**: Dashboard for suspicious activities
- **User Analytics**: Login patterns and security statistics

## 🏗️ Architecture

### Models

#### User Model (`models/user.py`)
Enhanced user model with security features:
```python
class User(Base):
    # Basic user info
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    
    # Security features
    failed_login_attempts = Column(Integer, default=0)
    account_locked_until = Column(DateTime(timezone=True))
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(32))
    backup_codes = Column(JSON, default=list)
```

#### Session Models (`models/session.py`)
- **RefreshToken**: Stores refresh token hashes with expiration
- **UserSession**: Tracks active user sessions with device info
- **LoginAttempt**: Records all login attempts for monitoring
- **AccountLockout**: Tracks account lockout events

#### Audit Model (`models/audit.py`)
- **AuditLog**: Comprehensive audit trail for security events

### Services

#### SessionService (`services/session_service.py`)
Manages user sessions and refresh tokens:
- Create and manage sessions
- Token refresh with rotation
- Device fingerprinting
- Session termination
- Rate limiting checks

#### TwoFactorService (`services/two_factor_service.py`)
Handles 2FA functionality:
- TOTP secret generation
- QR code generation for setup
- Token verification
- Backup code management

#### UserManagementService (`services/user_management_service.py`)
Admin operations for user management:
- User lifecycle management
- Security statistics
- Suspicious activity monitoring
- Bulk operations

#### AuditLogService (`services/audit_service.py`)
Comprehensive audit logging:
- Event tracking
- Security summaries
- Log retention management

### Middleware

#### RateLimitMiddleware (`middleware/rate_limit.py`)
Configurable rate limiting:
- Per-endpoint limits
- IP-based and user-based limiting
- Automatic cleanup of old records

## 🔧 Configuration

### Security Settings (`core/config.py`)
```python
class Settings(BaseSettings):
    # JWT Configuration
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # Rate Limiting
    LOGIN_RATE_LIMIT_ATTEMPTS: int = 5
    LOGIN_RATE_LIMIT_WINDOW: int = 15  # minutes
    
    # Account Security
    MAX_FAILED_LOGIN_ATTEMPTS: int = 5
    ACCOUNT_LOCKOUT_DURATION: int = 30  # minutes
```

### Rate Limiting Configuration
```python
rate_limits = {
    "/api/v1/auth/login": {"max_requests": 5, "window_minutes": 15},
    "/api/v1/auth/register": {"max_requests": 3, "window_minutes": 60},
    "/api/v1/auth/2fa/verify": {"max_requests": 5, "window_minutes": 15},
    "default": {"max_requests": 100, "window_minutes": 15}
}
```

## 📝 API Endpoints

### Authentication Endpoints

#### Registration
```http
POST /api/v1/auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "StrongPassword123!",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "StrongPassword123!",
    "device_name": "iPhone 12",
    "remember_me": false
}
```

Response:
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "def50200abc123...",
    "token_type": "bearer",
    "expires_in": 1800,
    "session_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

#### Token Refresh
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
    "refresh_token": "def50200abc123..."
}
```

### Session Management

#### List Sessions
```http
GET /api/v1/auth/sessions
Authorization: Bearer <access_token>
```

#### Terminate Session
```http
DELETE /api/v1/auth/sessions/{session_id}
Authorization: Bearer <access_token>
```

#### Logout
```http
POST /api/v1/auth/logout
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "logout_all_devices": false
}
```

### Two-Factor Authentication

#### Setup 2FA
```http
POST /api/v1/auth/2fa/setup
Authorization: Bearer <access_token>
```

Response:
```json
{
    "secret": "JBSWY3DPEHPK3PXP",
    "qr_code": "data:image/png;base64,iVBOR...",
    "backup_codes": [
        "1234-5678",
        "2345-6789",
        ...
    ]
}
```

#### Enable 2FA
```http
POST /api/v1/auth/2fa/enable
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "token": "123456"
}
```

#### Disable 2FA
```http
POST /api/v1/auth/2fa/disable
Authorization: Bearer <access_token>
```

### Admin Endpoints

#### List Users
```http
GET /api/v1/admin/users?skip=0&limit=50&search=john&is_active=true
Authorization: Bearer <admin_token>
```

#### Get User Details
```http
GET /api/v1/admin/users/{user_id}
Authorization: Bearer <admin_token>
```

#### Manage User
```http
POST /api/v1/admin/users/{user_id}/manage
Authorization: Bearer <admin_token>
Content-Type: application/json

{
    "action": "lock",
    "reason": "Suspicious activity detected"
}
```

Available actions: `activate`, `deactivate`, `lock`, `unlock`, `reset_password`, `enable_2fa`, `disable_2fa`

#### Security Statistics
```http
GET /api/v1/admin/security/stats
Authorization: Bearer <admin_token>
```

## 🛡️ Security Best Practices

### Password Policy
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter  
- At least one digit
- At least one special character
- No common passwords
- No sequential characters (abc, 123)

### Session Security
- Device fingerprinting for session validation
- Automatic session cleanup
- Session termination on security events
- IP address tracking

### Rate Limiting
- Login attempts: 5 per 15 minutes per email/IP
- Registration: 3 per hour per IP
- 2FA verification: 5 per 15 minutes
- API calls: 100 per 15 minutes per IP

### Account Protection
- Account lockout after 5 failed attempts
- 30-minute lockout duration
- Automatic unlock after timeout
- Admin override capabilities

## 🔍 Monitoring and Auditing

### Audit Events
All security events are logged including:
- Authentication attempts (success/failure)
- Session creation/termination
- Admin actions
- 2FA setup/verification
- Password changes
- Account lockouts

### Security Dashboard
Admins can monitor:
- Failed login attempts
- Suspicious IP addresses
- Account lockouts
- 2FA adoption rates
- Active session counts

### Alerts
The system can be configured to alert on:
- Multiple failed login attempts
- Unusual login patterns
- Admin actions
- Security policy violations

## 🧪 Testing

### Running Tests
```bash
cd apps/backend
pytest tests/test_enhanced_auth.py -v
```

### Test Coverage
- Authentication flows
- Session management
- 2FA functionality
- Rate limiting
- Account lockout
- Admin operations
- Security features

## 🚀 Deployment Considerations

### Environment Variables
```env
SECRET_KEY=your-super-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30
LOGIN_RATE_LIMIT_ATTEMPTS=5
```

### Database Migrations
Run migrations to create new tables:
```bash
alembic upgrade head
```

### Redis (Production)
For production deployments, replace in-memory rate limiting with Redis:
```python
# In production, replace _rate_limit_storage with Redis
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
```

### Monitoring
Set up monitoring for:
- Failed authentication rates
- Session creation/termination rates  
- 2FA success rates
- Rate limiting violations
- Account lockout frequencies

## 📚 Additional Resources

- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [OWASP Authentication Guidelines](https://owasp.org/www-project-authentication-guide/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [TOTP Specification](https://tools.ietf.org/html/rfc6238)