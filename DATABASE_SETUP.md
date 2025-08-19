# Database Setup Instructions for La Vida Luca

## 🎯 Quick Start

### Step 1: Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Save your project URL and anon key

### Step 2: Configure Environment
```bash
# Copy the template
cp .env.template .env.local

# Edit .env.local with your Supabase credentials
```

### Step 3: Run Database Setup
In your Supabase SQL Editor (https://app.supabase.com/project/YOUR_PROJECT_ID/sql):

1. **Run the migration**:
   ```sql
   -- Copy and paste infra/supabase/migrations/001_initial_schema.sql
   ```

2. **Add seed data**:
   ```sql
   -- Copy and paste infra/supabase/seed/activities.sql
   ```

### Step 4: Verify Setup
```sql
-- Check that tables were created
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Verify activities were inserted
SELECT COUNT(*) as total_activities FROM activities;
-- Should return: 30

-- Check categories distribution
SELECT category, COUNT(*) as count 
FROM activities 
GROUP BY category 
ORDER BY category;
-- Should show 6 activities per category
```

## 🗄️ What Was Created

- **3 Main Tables**: users, activities, activity_registrations
- **30 Activities**: Complete catalogue with French descriptions
- **Security**: Row Level Security policies
- **Performance**: Indexes for common queries
- **Views**: Pre-built queries for common data needs

## 🔧 Next Steps

1. **Deploy Frontend**: Update your Next.js app to use the database
2. **Test Auth**: Verify Supabase authentication works
3. **Add Features**: Build registration and user profile features
4. **Add Admin**: Create admin interface for activity management

## 📞 Need Help?

Check `/infra/supabase/README.md` for detailed documentation.