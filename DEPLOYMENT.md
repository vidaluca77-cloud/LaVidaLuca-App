# LaVidaLuca Deployment Guide

This guide covers the deployment of the LaVidaLuca platform with:
- **Frontend**: Next.js on Vercel
- **Backend**: FastAPI on Render
- **Database**: PostgreSQL on Supabase

## 🚀 Quick Deployment

### 1. Database Setup (Supabase)

1. Create a new project on [Supabase](https://supabase.com)
2. Go to SQL Editor and run the schema:
   ```sql
   -- Copy and paste content from /infra/supabase/schema.sql
   ```
3. Optionally, run the seed data:
   ```sql
   -- Copy and paste content from /infra/supabase/seeds.sql
   ```
4. Get your database URL and API keys from Settings > API

### 2. Backend Deployment (Render)

#### Option A: Manual Deployment
1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: `lavidaluca-backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `cd apps/backend && pip install -r requirements.txt`
   - **Start Command**: `cd apps/backend && ./start.sh`
   - **Root Directory**: `apps/backend`

#### Option B: Infrastructure as Code
1. Use the provided `render.yaml` configuration
2. Deploy with: `render blueprint:apply`

#### Environment Variables (Render)
```env
DEBUG=false
DATABASE_URL=postgresql://...  # From Supabase
SECRET_KEY=your-jwt-secret-key
ALLOWED_ORIGINS=["https://your-frontend.vercel.app"]
OPENAI_API_KEY=your-openai-key  # Optional
```

### 3. Frontend Deployment (Vercel)

1. Deploy the Next.js app to [Vercel](https://vercel.com)
2. Set environment variables:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
   NEXT_PUBLIC_IA_API_URL=https://your-backend.render.com
   NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.org
   NEXT_PUBLIC_CONTACT_PHONE=+33 X XX XX XX XX
   ```

## 🔧 Configuration Details

### Database Schema Features
- **User Management**: Role-based access control
- **Activity Catalog**: 30+ predefined activities
- **Location Management**: Farm and site information
- **Reservation System**: Booking and scheduling
- **Evaluation System**: Progress tracking
- **Skills & Materials**: Many-to-many relationships
- **Row Level Security**: Supabase RLS policies

### Backend API Features
- **Authentication**: JWT-based with role permissions
- **Activity Recommendations**: AI-powered suggestions
- **CRUD Operations**: Full REST API
- **Data Validation**: Pydantic schemas
- **OpenAPI Documentation**: Auto-generated docs
- **Health Monitoring**: Health check endpoints

### Security Configuration
- **CORS**: Properly configured for frontend domains
- **Authentication**: JWT tokens with expiration
- **Role-based Access**: Student, Mentor, Admin, Visitor
- **Database Security**: RLS policies in Supabase
- **Input Validation**: Pydantic models

## 🔍 Testing the Deployment

### Health Checks
```bash
# Backend health
curl https://your-backend.render.com/health

# API endpoints
curl https://your-backend.render.com/activities/categories
```

### Sample API Calls
```bash
# Register a new user
curl -X POST https://your-backend.render.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123",
    "role": "student"
  }'

# Login
curl -X POST https://your-backend.render.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# Get activities
curl https://your-backend.render.com/activities/
```

## 📊 Monitoring

### Application Monitoring
- **Render**: Built-in logs and metrics
- **Supabase**: Database monitoring dashboard
- **Vercel**: Frontend performance analytics

### Health Endpoints
- Backend: `GET /health`
- Database: Monitor via Supabase dashboard
- Frontend: Built-in Vercel monitoring

## 🔄 Updates and Maintenance

### Database Migrations
```bash
# If using Alembic (optional)
cd apps/backend
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Backend Updates
1. Push changes to GitHub
2. Render automatically rebuilds and deploys
3. Check deployment logs for issues

### Frontend Updates
1. Push changes to GitHub
2. Vercel automatically rebuilds and deploys
3. Verify functionality

## 🚨 Troubleshooting

### Common Issues

#### Backend won't start
- Check environment variables are set
- Verify database connectivity
- Review Render service logs

#### Database connection errors
- Verify DATABASE_URL format
- Check Supabase project status
- Ensure IP allowlisting if required

#### CORS errors
- Update ALLOWED_ORIGINS environment variable
- Ensure frontend domain is included
- Check protocol (http vs https)

### Debug Mode
Enable debug mode for development:
```env
DEBUG=true
```
This enables:
- Detailed error messages
- OpenAPI documentation at `/docs`
- Database query logging

## 📁 File Structure Summary

```
/apps/backend/          # FastAPI backend
  ├── main.py          # FastAPI application
  ├── config.py        # Configuration management
  ├── models.py        # Database models
  ├── schemas.py       # Pydantic schemas
  ├── database.py      # Database connection
  ├── routes/          # API routes
  ├── tests/           # Test suite
  └── requirements.txt # Python dependencies

/infra/supabase/       # Database schema
  ├── schema.sql       # Database structure
  └── seeds.sql        # Sample data

/apps/web/             # Next.js frontend
  └── ...              # (existing frontend code)
```

This deployment setup provides a production-ready, scalable platform for the LaVidaLuca educational farm activities system.