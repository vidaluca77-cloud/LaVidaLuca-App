-- Migration: 001_initial_schema.sql
-- Description: Initial database schema for La Vida Luca App
-- Date: 2025-01-19
-- Author: Database Setup Script

-- This migration creates the initial schema for:
-- 1. User profiles (extending Supabase Auth)
-- 2. Activities catalogue
-- 3. Activity registrations system

BEGIN;

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    auth_user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    location VARCHAR(255),
    skills JSONB DEFAULT '[]'::jsonb,
    availability JSONB DEFAULT '[]'::jsonb,
    preferences JSONB DEFAULT '[]'::jsonb,
    profile_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create activities table
CREATE TABLE IF NOT EXISTS activities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    activity_id VARCHAR(10) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(20) NOT NULL CHECK (category IN ('agri', 'transfo', 'artisanat', 'nature', 'social')),
    summary TEXT NOT NULL,
    description TEXT,
    duration_min INTEGER NOT NULL,
    skill_tags JSONB DEFAULT '[]'::jsonb,
    seasonality JSONB DEFAULT '[]'::jsonb,
    safety_level INTEGER NOT NULL CHECK (safety_level BETWEEN 1 AND 3),
    materials JSONB DEFAULT '[]'::jsonb,
    max_participants INTEGER DEFAULT 8,
    min_age INTEGER DEFAULT 16,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create activity_registrations table
CREATE TABLE IF NOT EXISTS activity_registrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    activity_id UUID REFERENCES activities(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'completed', 'cancelled')),
    registration_date TIMESTAMPTZ DEFAULT NOW(),
    scheduled_date TIMESTAMPTZ,
    notes TEXT,
    feedback TEXT,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, activity_id, scheduled_date)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_auth_user_id ON users(auth_user_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_activities_category ON activities(category);
CREATE INDEX IF NOT EXISTS idx_activities_slug ON activities(slug);
CREATE INDEX IF NOT EXISTS idx_activities_activity_id ON activities(activity_id);
CREATE INDEX IF NOT EXISTS idx_registrations_user_id ON activity_registrations(user_id);
CREATE INDEX IF NOT EXISTS idx_registrations_activity_id ON activity_registrations(activity_id);
CREATE INDEX IF NOT EXISTS idx_registrations_status ON activity_registrations(status);
CREATE INDEX IF NOT EXISTS idx_registrations_scheduled_date ON activity_registrations(scheduled_date);

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_registrations ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Users can view their own profile" ON users
    FOR SELECT USING (auth.uid() = auth_user_id);

CREATE POLICY "Users can update their own profile" ON users
    FOR UPDATE USING (auth.uid() = auth_user_id);

CREATE POLICY "Users can insert their own profile" ON users
    FOR INSERT WITH CHECK (auth.uid() = auth_user_id);

CREATE POLICY "Anyone can view active activities" ON activities
    FOR SELECT USING (is_active = true);

CREATE POLICY "Authenticated users can view activities" ON activities
    FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY "Users can view their own registrations" ON activity_registrations
    FOR SELECT USING (user_id IN (SELECT id FROM users WHERE auth_user_id = auth.uid()));

CREATE POLICY "Users can create their own registrations" ON activity_registrations
    FOR INSERT WITH CHECK (user_id IN (SELECT id FROM users WHERE auth_user_id = auth.uid()));

CREATE POLICY "Users can update their own registrations" ON activity_registrations
    FOR UPDATE USING (user_id IN (SELECT id FROM users WHERE auth_user_id = auth.uid()));

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_activities_updated_at BEFORE UPDATE ON activities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_registrations_updated_at BEFORE UPDATE ON activity_registrations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create views
CREATE OR REPLACE VIEW user_profiles AS
SELECT 
    u.*,
    COUNT(ar.id) as total_registrations,
    COUNT(CASE WHEN ar.status = 'completed' THEN 1 END) as completed_activities
FROM users u
LEFT JOIN activity_registrations ar ON u.id = ar.user_id
GROUP BY u.id;

CREATE OR REPLACE VIEW activity_summary AS
SELECT 
    a.*,
    COUNT(ar.id) as total_registrations,
    COUNT(CASE WHEN ar.status = 'confirmed' THEN 1 END) as confirmed_registrations,
    COUNT(CASE WHEN ar.status = 'completed' THEN 1 END) as completed_registrations,
    ROUND(AVG(ar.rating), 2) as average_rating
FROM activities a
LEFT JOIN activity_registrations ar ON a.id = ar.activity_id
WHERE a.is_active = true
GROUP BY a.id;

COMMIT;