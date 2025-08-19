# Database Setup for La Vida Luca App

This directory contains the database configuration files for the La Vida Luca application using PostgreSQL on Supabase.

## 📁 Directory Structure

```
infra/supabase/
├── schema.sql              # Complete database schema
├── migrations/
│   └── 001_initial_schema.sql  # Initial migration file
└── seed/
    └── activities.sql      # Seed data for 30 activities
```

## 🚀 Quick Setup

### 1. Create Supabase Project
1. Go to [supabase.com](https://supabase.com) and create a new project
2. Note your project URL and anon key from the dashboard

### 2. Run Database Schema
In your Supabase SQL Editor, run the following files in order:

1. **Initial Schema**: Run `migrations/001_initial_schema.sql`
2. **Seed Data**: Run `seed/activities.sql`

Or run the complete schema file:
```sql
-- Run this in Supabase SQL Editor
\i schema.sql
\i seed/activities.sql
```

### 3. Configure Environment Variables
1. Copy `.env.template` to `.env.local`
2. Fill in your Supabase URL and keys
3. Update other configuration values as needed

## 📋 Database Schema

### Tables

#### `users`
Extended user profiles linked to Supabase Auth
- Personal information (name, location)
- Skills, availability, and preferences (JSONB)
- Profile completion tracking

#### `activities`
Catalogue of 30 educational agricultural activities
- Complete activity details (title, description, duration)
- Skills required and materials needed
- Safety levels and participant limits
- Seasonal availability

#### `activity_registrations`
User participation tracking
- Registration status (pending, confirmed, completed, cancelled)
- Scheduling and feedback system
- Rating system for completed activities

### Key Features

- **Row Level Security (RLS)**: Users can only access their own data
- **Automatic timestamps**: Created/updated timestamps with triggers
- **Data validation**: Check constraints for enums and ranges
- **Performance indexes**: Optimized for common queries
- **Views**: Pre-built queries for user profiles and activity summaries

## 🔧 Development

### Local Development with Docker (Optional)
```bash
# Start local PostgreSQL (if not using Supabase)
docker run --name lavidaluca-db -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# Connect and run schema
psql -h localhost -U postgres -d postgres -f infra/supabase/schema.sql
psql -h localhost -U postgres -d postgres -f infra/supabase/seed/activities.sql
```

### Migrations
For future schema changes, create new migration files:
- `002_add_feature.sql`
- `003_update_table.sql`
- etc.

## 📊 Sample Queries

### Get all activities by category
```sql
SELECT title, summary, duration_min 
FROM activities 
WHERE category = 'agri' AND is_active = true
ORDER BY title;
```

### User registration summary
```sql
SELECT u.full_name, up.total_registrations, up.completed_activities
FROM user_profiles up
JOIN users u ON u.id = up.id
WHERE u.auth_user_id = auth.uid();
```

### Activity popularity
```sql
SELECT a.title, a.category, as.total_registrations, as.average_rating
FROM activity_summary as
JOIN activities a ON a.id = as.id
ORDER BY as.total_registrations DESC;
```

## 🛡️ Security

- All tables have Row Level Security enabled
- Users can only access their own profile and registrations
- Activities are publicly readable but only admin-writable
- Authentication handled by Supabase Auth

## 📚 Activity Categories

- **agri**: Agriculture (6 activities) - Animal care, cultivation
- **transfo**: Transformation (6 activities) - Food processing, crafts
- **artisanat**: Artisanat (6 activities) - Construction, maintenance
- **nature**: Nature (6 activities) - Environmental care, observation
- **social**: Social (6 activities) - Events, education, community

## 🔄 Data Synchronization

The seed data matches the frontend activity data in `src/app/page.tsx`. When updating activities:

1. Update the frontend `ACTIVITIES` array
2. Update the corresponding database records
3. Consider creating a migration file for the changes

## 🆘 Troubleshooting

### Common Issues

1. **Permission denied**: Check RLS policies and user authentication
2. **Foreign key constraints**: Ensure referenced records exist
3. **JSON validation**: Verify JSONB structure for arrays
4. **Migration conflicts**: Run migrations in correct order

### Useful Commands

```sql
-- Check table permissions
\dp activities

-- View RLS policies
\d+ activities

-- Reset data (development only)
TRUNCATE activity_registrations, activities, users CASCADE;
```

## 📞 Support

For database-related issues:
1. Check Supabase logs in the dashboard
2. Verify RLS policies are correctly applied
3. Ensure environment variables are set correctly
4. Review the schema comments for field explanations