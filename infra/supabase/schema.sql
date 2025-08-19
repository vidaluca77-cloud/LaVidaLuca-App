-- LaVidaLuca Database Schema
-- PostgreSQL/Supabase Schema for the LaVidaLuca application

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    availability JSONB DEFAULT '[]',
    preferences JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT TRUE,
    is_student BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create skills table
CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create activities table
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    summary TEXT NOT NULL,
    description TEXT,
    duration_min INTEGER NOT NULL,
    seasonality JSONB DEFAULT '[]',
    safety_level INTEGER DEFAULT 1,
    materials JSONB DEFAULT '[]',
    location_requirements TEXT,
    max_participants INTEGER DEFAULT 10,
    is_active BOOLEAN DEFAULT TRUE,
    is_student_only BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create user_skills junction table
CREATE TABLE user_skills (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, skill_id)
);

-- Create activity_skills junction table
CREATE TABLE activity_skills (
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (activity_id, skill_id)
);

-- Create user_activities junction table (for completed activities)
CREATE TABLE user_activities (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (user_id, activity_id)
);

-- Create activity_sessions table
CREATE TABLE activity_sessions (
    id SERIAL PRIMARY KEY,
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    instructor_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    scheduled_date TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_actual INTEGER,
    max_participants INTEGER DEFAULT 10,
    location VARCHAR(255),
    notes TEXT,
    status VARCHAR(50) DEFAULT 'scheduled',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create user_profiles table
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    bio TEXT,
    experience_level VARCHAR(50) DEFAULT 'beginner',
    interests JSONB DEFAULT '[]',
    goals TEXT,
    contact_preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_student ON users(is_student);
CREATE INDEX idx_activities_category ON activities(category);
CREATE INDEX idx_activities_slug ON activities(slug);
CREATE INDEX idx_activities_is_active ON activities(is_active);
CREATE INDEX idx_activity_sessions_scheduled_date ON activity_sessions(scheduled_date);
CREATE INDEX idx_user_activities_completed_at ON user_activities(completed_at);

-- Create update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply update triggers
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_activities_updated_at 
    BEFORE UPDATE ON activities 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at 
    BEFORE UPDATE ON user_profiles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add constraints
ALTER TABLE activities ADD CONSTRAINT check_safety_level CHECK (safety_level >= 1 AND safety_level <= 5);
ALTER TABLE activities ADD CONSTRAINT check_duration_positive CHECK (duration_min > 0);
ALTER TABLE activities ADD CONSTRAINT check_max_participants_positive CHECK (max_participants > 0);

-- Comments for documentation
COMMENT ON TABLE users IS 'User accounts for the LaVidaLuca platform';
COMMENT ON TABLE activities IS 'Catalog of available activities for MFR students and participants';
COMMENT ON TABLE skills IS 'Skills that can be associated with users and required for activities';
COMMENT ON TABLE user_activities IS 'Track which activities users have completed';
COMMENT ON TABLE activity_sessions IS 'Scheduled sessions for activities with instructors';
COMMENT ON COLUMN activities.safety_level IS 'Safety complexity level from 1 (basic) to 5 (advanced)';
COMMENT ON COLUMN users.is_student IS 'Whether the user is an MFR student with access to student-only activities';