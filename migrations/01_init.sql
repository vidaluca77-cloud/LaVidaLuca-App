-- migrations/01_init.sql
-- Initialize database for La Vida Luca project

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Activities table for MFR training activities
CREATE TABLE activities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT,
    duration INTEGER, -- Duration in minutes
    category TEXT NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Activity categories for better organization
CREATE TABLE activity_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    color TEXT, -- Hex color for UI
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User activity enrollments
CREATE TABLE user_activities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    activity_id UUID REFERENCES activities(id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    UNIQUE(user_id, activity_id)
);

-- Indexes for performance
CREATE INDEX idx_activities_category ON activities(category);
CREATE INDEX idx_activities_user_id ON activities(user_id);
CREATE INDEX idx_user_activities_user_id ON user_activities(user_id);
CREATE INDEX idx_user_activities_activity_id ON user_activities(activity_id);
CREATE INDEX idx_activities_created_at ON activities(created_at);
CREATE INDEX idx_users_email ON users(email);

-- Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_activities ENABLE ROW LEVEL SECURITY;

-- RLS Policies
-- Users can view their own data
CREATE POLICY users_select ON users FOR SELECT 
TO authenticated USING (auth.uid() = id);

-- Users can update their own data
CREATE POLICY users_update ON users FOR UPDATE 
TO authenticated USING (auth.uid() = id);

-- Activities are publicly viewable
CREATE POLICY activities_select ON activities FOR SELECT 
TO authenticated USING (true);

-- Only admin users can create/update activities (for now, allow all authenticated)
CREATE POLICY activities_insert ON activities FOR INSERT 
TO authenticated WITH CHECK (true);

CREATE POLICY activities_update ON activities FOR UPDATE 
TO authenticated USING (true);

-- Activity categories are publicly viewable
CREATE POLICY activity_categories_select ON activity_categories FOR SELECT 
TO authenticated USING (true);

-- User activities - users can only see their own enrollments
CREATE POLICY user_activities_select ON user_activities FOR SELECT 
TO authenticated USING (auth.uid() = user_id);

CREATE POLICY user_activities_insert ON user_activities FOR INSERT 
TO authenticated WITH CHECK (auth.uid() = user_id);

CREATE POLICY user_activities_update ON user_activities FOR UPDATE 
TO authenticated USING (auth.uid() = user_id);

-- Functions for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_activities_updated_at BEFORE UPDATE ON activities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();