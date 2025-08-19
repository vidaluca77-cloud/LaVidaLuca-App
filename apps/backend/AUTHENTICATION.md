# Enhanced Authentication System

This document describes the enhanced authentication system implemented for La Vida Luca API.

## Features

### 1. Refresh Token Support

The system now supports refresh tokens for improved security:

- **Access tokens**: Short-lived (24 hours by default)
- **Refresh tokens**: Long-lived (7 days by default)
- **Token rotation**: New refresh token issued on each refresh

#### Usage

```python
# Login returns both tokens
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "password"
}

# Response
{
  "success": true,
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "secure_random_token",
    "token_type": "bearer",
    "expires_in": 86400
  }
}

# Refresh access token
POST /api/v1/auth/refresh
{
  "refresh_token": "secure_random_token"
}
```

### 2. Role-Based Access Control (RBAC)

Four user roles with hierarchical permissions:

- **USER**: Basic user permissions
- **MODERATOR**: Can moderate content
- **ADMIN**: Can manage users and system settings
- **SUPERUSER**: Full system access

#### Usage in endpoints

```python
from ..auth.dependencies import require_admin, require_moderator, require_permission

@router.get("/admin-only")
async def admin_endpoint(user: User = Depends(require_admin)):
    return {"message": "Admin access granted"}

@router.get("/moderate")
async def moderate_endpoint(user: User = Depends(require_moderator)):
    return {"message": "Moderator access granted"}

@router.get("/manage-users")
async def manage_users(user: User = Depends(require_permission("manage_users"))):
    return {"message": "User management access"}
```

### 3. OAuth Integration

Support for social login providers:

- **Google OAuth**
- **GitHub OAuth**
- Extensible for other providers

#### Configuration

```python
# Environment variables
GOOGLE_OAUTH_CLIENT_ID=your_google_client_id
GOOGLE_OAUTH_CLIENT_SECRET=your_google_client_secret
GITHUB_OAUTH_CLIENT_ID=your_github_client_id
GITHUB_OAUTH_CLIENT_SECRET=your_github_client_secret
```

#### Usage

```python
# Get available providers
GET /api/v1/auth/oauth/providers

# Start OAuth flow
GET /api/v1/auth/oauth/google/authorize?redirect_url=https://yourapp.com

# Handle callback (automatically called by OAuth provider)
GET /api/v1/auth/oauth/google/callback?code=...&state=...
```

### 4. Session Management

Track and manage user sessions:

- Session creation on login
- Session tracking with IP and user agent
- Session invalidation
- Multiple session support

#### Usage

```python
# Get user sessions
GET /api/v1/auth/user-sessions
Authorization: Bearer <access_token>

# Revoke specific session
DELETE /api/v1/auth/revoke-session/{session_id}
Authorization: Bearer <access_token>
```

### 5. Enhanced Security Middleware

#### Security Headers

Automatically adds security headers to all responses:

- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `X-Frame-Options: DENY`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `Content-Security-Policy: ...`
- `Permissions-Policy: ...`

#### Rate Limiting

Protects against abuse with configurable limits:

- **Authenticated users**: 100 requests/minute (default)
- **Anonymous users**: 20 requests/minute (default)
- **Burst protection**: 10 requests in 10 seconds (default)

#### Configuration

```python
RATE_LIMIT_REQUESTS_PER_MINUTE=100
RATE_LIMIT_REQUESTS_PER_MINUTE_ANONYMOUS=20
```

## Database Migration

Add the role field to existing users:

```bash
# Run migration
cd apps/backend
alembic upgrade head
```

## Testing

Run the enhanced authentication tests:

```bash
cd apps/backend
pytest tests/test_enhanced_auth.py -v
```

## Security Considerations

1. **Refresh Token Storage**: Currently stored in user profile JSON field. For production, consider using Redis or dedicated session table.

2. **OAuth State**: CSRF protection states are stored in memory. For production scaling, use Redis or database storage.

3. **Rate Limiting**: In-memory implementation. For production scaling across multiple servers, use Redis.

4. **Token Secrets**: Ensure `JWT_SECRET_KEY` is properly secured and rotated regularly.

5. **HTTPS**: Always use HTTPS in production to protect tokens in transit.

## Migration from Old System

The enhanced system is backward compatible:

1. Existing access tokens continue to work
2. New logins get refresh tokens
3. Existing users get `USER` role by default
4. No breaking changes to existing endpoints

## Examples

See `routes/examples.py` for complete examples of:

- Role-based endpoint protection
- Permission checking
- User promotion
- Session management

## API Endpoints

### Authentication Endpoints

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login (returns token pair)
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout and revoke refresh token
- `POST /api/v1/auth/verify-token` - Verify current token

### OAuth Endpoints

- `GET /api/v1/auth/oauth/providers` - List available providers
- `GET /api/v1/auth/oauth/{provider}/authorize` - Start OAuth flow
- `GET /api/v1/auth/oauth/{provider}/callback` - OAuth callback

### Session Management

- `GET /api/v1/auth/user-sessions` - Get user sessions
- `DELETE /api/v1/auth/revoke-session/{session_id}` - Revoke session

## Error Handling

The system provides detailed error responses:

```json
{
  "success": false,
  "detail": "Token has expired",
  "status_code": 401
}
```

Common error codes:
- `400`: Bad request (invalid data)
- `401`: Unauthorized (invalid/expired token)
- `403`: Forbidden (insufficient permissions)
- `429`: Too many requests (rate limited)