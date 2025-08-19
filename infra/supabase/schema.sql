-- LaVidaLuca Database Schema for Supabase PostgreSQL
-- This schema supports the educational farm activities platform

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom types/enums
CREATE TYPE user_role AS ENUM ('student', 'mentor', 'admin', 'visitor');
CREATE TYPE activity_category AS ENUM ('agri', 'transfo', 'artisanat', 'nature', 'social');
CREATE TYPE reservation_status AS ENUM ('pending', 'confirmed', 'cancelled', 'completed');
CREATE TYPE safety_level AS ENUM ('1', '2', '3');

-- Users table with authentication and profile information
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role user_role DEFAULT 'visitor',
    
    -- Profile information
    location VARCHAR(255),
    phone VARCHAR(20),
    bio TEXT,
    availability JSONB DEFAULT '[]'::jsonb, -- ["weekend", "semaine", "matin", etc.]
    preferences JSONB DEFAULT '[]'::jsonb,  -- ["agri", "nature", etc.]
    
    -- Status fields
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Locations/farms table
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    address TEXT,
    departement VARCHAR(100),
    coordinates JSONB, -- {"lat": x, "lng": y}
    
    -- Contact information
    contact_person VARCHAR(255),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20),
    
    -- Capacities and features
    max_capacity INTEGER DEFAULT 10,
    facilities JSONB DEFAULT '[]'::jsonb, -- ["parking", "sanitaires", etc.]
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Activities table
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    category activity_category NOT NULL,
    summary TEXT,
    description TEXT,
    
    -- Duration and scheduling
    duration_min INTEGER NOT NULL,
    seasonality JSONB DEFAULT '[]'::jsonb, -- ["printemps", "ete", "automne", "hiver", "toutes"]
    
    -- Safety and requirements
    safety_level safety_level DEFAULT '1',
    min_age INTEGER DEFAULT 16,
    max_participants INTEGER DEFAULT 8,
    prerequisites TEXT,
    
    -- Location reference
    location_id INTEGER REFERENCES locations(id),
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Skills lookup table
CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(50)
);

-- Materials lookup table
CREATE TABLE materials (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    safety_required BOOLEAN DEFAULT false
);

-- Many-to-many: User skills
CREATE TABLE user_skills (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    proficiency_level INTEGER DEFAULT 1 CHECK (proficiency_level BETWEEN 1 AND 5),
    acquired_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, skill_id)
);

-- Many-to-many: Activity required skills
CREATE TABLE activity_skills (
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    required_level INTEGER DEFAULT 1 CHECK (required_level BETWEEN 1 AND 5),
    PRIMARY KEY (activity_id, skill_id)
);

-- Many-to-many: Activity required materials
CREATE TABLE activity_materials (
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    material_id INTEGER REFERENCES materials(id) ON DELETE CASCADE,
    quantity INTEGER DEFAULT 1,
    is_mandatory BOOLEAN DEFAULT true,
    PRIMARY KEY (activity_id, material_id)
);

-- Reservations table
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE NOT NULL,
    
    -- Scheduling
    scheduled_date TIMESTAMP WITH TIME ZONE,
    duration_actual INTEGER, -- Actual duration in minutes
    
    -- Status and management
    status reservation_status DEFAULT 'pending',
    notes TEXT,
    mentor_notes TEXT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Evaluations table
CREATE TABLE evaluations (
    id SERIAL PRIMARY KEY,
    reservation_id INTEGER REFERENCES reservations(id) ON DELETE CASCADE NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    
    -- Evaluation scores (1-5 scale)
    skill_demonstration DECIMAL(3,2) CHECK (skill_demonstration BETWEEN 1 AND 5),
    safety_compliance DECIMAL(3,2) CHECK (safety_compliance BETWEEN 1 AND 5),
    teamwork DECIMAL(3,2) CHECK (teamwork BETWEEN 1 AND 5),
    initiative DECIMAL(3,2) CHECK (initiative BETWEEN 1 AND 5),
    overall_rating DECIMAL(3,2) CHECK (overall_rating BETWEEN 1 AND 5),
    
    -- Comments
    strengths TEXT,
    areas_for_improvement TEXT,
    mentor_comments TEXT,
    student_feedback TEXT,
    
    -- Progress tracking
    goals_achieved JSONB DEFAULT '[]'::jsonb, -- List of achieved goals
    next_recommendations JSONB DEFAULT '[]'::jsonb, -- Recommended next activities
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);

CREATE INDEX idx_activities_slug ON activities(slug);
CREATE INDEX idx_activities_category ON activities(category);
CREATE INDEX idx_activities_location_id ON activities(location_id);
CREATE INDEX idx_activities_is_active ON activities(is_active);

CREATE INDEX idx_locations_departement ON locations(departement);
CREATE INDEX idx_locations_is_active ON locations(is_active);

CREATE INDEX idx_reservations_user_id ON reservations(user_id);
CREATE INDEX idx_reservations_activity_id ON reservations(activity_id);
CREATE INDEX idx_reservations_status ON reservations(status);
CREATE INDEX idx_reservations_scheduled_date ON reservations(scheduled_date);

CREATE INDEX idx_evaluations_reservation_id ON evaluations(reservation_id);
CREATE INDEX idx_evaluations_user_id ON evaluations(user_id);

-- Triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_locations_updated_at BEFORE UPDATE ON locations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_activities_updated_at BEFORE UPDATE ON activities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reservations_updated_at BEFORE UPDATE ON reservations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_evaluations_updated_at BEFORE UPDATE ON evaluations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies for Supabase
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE locations ENABLE ROW LEVEL SECURITY;
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE reservations ENABLE ROW LEVEL SECURITY;
ALTER TABLE evaluations ENABLE ROW LEVEL SECURITY;

-- Users can read their own profile, mentors/admins can read all
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid()::text = uuid::text OR 
                     EXISTS(SELECT 1 FROM users WHERE uuid::text = auth.uid()::text AND role IN ('mentor', 'admin')));

-- Users can update their own profile
CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid()::text = uuid::text);

-- Anyone can view active locations and activities
CREATE POLICY "Anyone can view active locations" ON locations
    FOR SELECT USING (is_active = true);

CREATE POLICY "Anyone can view active activities" ON activities
    FOR SELECT USING (is_active = true);

-- Users can view their own reservations, mentors/admins can view all
CREATE POLICY "Users can view own reservations" ON reservations
    FOR SELECT USING (user_id IN (SELECT id FROM users WHERE uuid::text = auth.uid()::text) OR
                     EXISTS(SELECT 1 FROM users WHERE uuid::text = auth.uid()::text AND role IN ('mentor', 'admin')));

-- Users can create their own reservations
CREATE POLICY "Users can create reservations" ON reservations
    FOR INSERT WITH CHECK (user_id IN (SELECT id FROM users WHERE uuid::text = auth.uid()::text));

-- Users can view their own evaluations, mentors/admins can view all
CREATE POLICY "Users can view own evaluations" ON evaluations
    FOR SELECT USING (user_id IN (SELECT id FROM users WHERE uuid::text = auth.uid()::text) OR
                     EXISTS(SELECT 1 FROM users WHERE uuid::text = auth.uid()::text AND role IN ('mentor', 'admin')));

-- Only mentors/admins can create/update evaluations
CREATE POLICY "Mentors can manage evaluations" ON evaluations
    FOR ALL USING (EXISTS(SELECT 1 FROM users WHERE uuid::text = auth.uid()::text AND role IN ('mentor', 'admin')));

-- Sample data inserts (can be moved to a separate seeds.sql file)
-- Insert default skills
INSERT INTO skills (name, description, category) VALUES
('elevage', 'Soins et gestion des animaux', 'agriculture'),
('hygiene', 'Respect des règles d''hygiène', 'general'),
('soins_animaux', 'Soins vétérinaires de base', 'agriculture'),
('sol', 'Connaissance et travail du sol', 'agriculture'),
('plantes', 'Botanique et culture des plantes', 'agriculture'),
('organisation', 'Capacité d''organisation', 'general'),
('securite', 'Respect des consignes de sécurité', 'general'),
('bois', 'Travail du bois et construction', 'artisanat'),
('precision', 'Travail de précision', 'general'),
('creativite', 'Créativité et innovation', 'general'),
('patience', 'Patience et persévérance', 'general'),
('endurance', 'Résistance physique', 'general'),
('ecologie', 'Connaissance en écologie', 'environnement'),
('accueil', 'Capacité d''accueil du public', 'social'),
('pedagogie', 'Aptitudes pédagogiques', 'social'),
('expression', 'Expression orale', 'social'),
('equipe', 'Travail en équipe', 'general');

-- Insert default materials
INSERT INTO materials (name, description, safety_required) VALUES
('tablier', 'Tablier de protection', false),
('gants', 'Gants de protection', true),
('bottes', 'Bottes de sécurité', true),
('casque', 'Casque de protection', true),
('lunettes', 'Lunettes de protection', true),
('masque', 'Masque de protection respiratoire', true);

COMMENT ON SCHEMA public IS 'LaVidaLuca educational farm activities platform database schema';