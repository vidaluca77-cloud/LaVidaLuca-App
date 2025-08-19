-- Schema pour La Vida Luca
-- Base de données pour les activités, utilisateurs et recommandations

-- Extension UUID pour les clés primaires
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table des utilisateurs (complète celle d'Auth de Supabase)
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    location TEXT,
    bio TEXT,
    skills TEXT[], -- Compétences de l'utilisateur
    interests TEXT[], -- Centres d'intérêt
    availability TEXT[], -- Disponibilités (jours/heures)
    experience_level TEXT DEFAULT 'debutant' CHECK (experience_level IN ('debutant', 'intermediaire', 'avance')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des activités
CREATE TABLE IF NOT EXISTS activities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('agri', 'transfo', 'artisanat', 'nature', 'social')),
    summary TEXT NOT NULL,
    description TEXT,
    duration_min INTEGER NOT NULL,
    skill_tags TEXT[] NOT NULL,
    seasonality TEXT[] NOT NULL,
    safety_level INTEGER DEFAULT 1 CHECK (safety_level BETWEEN 1 AND 3),
    materials TEXT[],
    location TEXT,
    max_participants INTEGER DEFAULT 10,
    min_age INTEGER DEFAULT 16,
    prerequisites TEXT[],
    learning_objectives TEXT[],
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des sessions d'activités
CREATE TABLE IF NOT EXISTS activity_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    activity_id UUID NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
    instructor_id UUID REFERENCES user_profiles(id),
    session_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    location TEXT,
    max_participants INTEGER DEFAULT 10,
    current_participants INTEGER DEFAULT 0,
    status TEXT DEFAULT 'planned' CHECK (status IN ('planned', 'confirmed', 'in_progress', 'completed', 'cancelled')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des inscriptions
CREATE TABLE IF NOT EXISTS activity_registrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES activity_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    registration_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status TEXT DEFAULT 'registered' CHECK (status IN ('registered', 'confirmed', 'attended', 'cancelled', 'no_show')),
    notes TEXT,
    feedback_rating INTEGER CHECK (feedback_rating BETWEEN 1 AND 5),
    feedback_comment TEXT,
    UNIQUE(session_id, user_id)
);

-- Table des recommandations IA
CREATE TABLE IF NOT EXISTS ai_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    activity_id UUID NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
    score DECIMAL(3,2) NOT NULL CHECK (score BETWEEN 0 AND 1),
    reasons TEXT[],
    recommended_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    was_accepted BOOLEAN DEFAULT NULL,
    feedback TEXT
);

-- Table des lieux d'action
CREATE TABLE IF NOT EXISTS action_locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    postal_code TEXT,
    country TEXT DEFAULT 'France',
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    contact_email TEXT,
    contact_phone TEXT,
    facilities TEXT[], -- équipements disponibles
    specialties TEXT[], -- spécialités du lieu
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour les performances
CREATE INDEX IF NOT EXISTS idx_user_profiles_location ON user_profiles(location);
CREATE INDEX IF NOT EXISTS idx_activities_category ON activities(category);
CREATE INDEX IF NOT EXISTS idx_activities_skill_tags ON activities USING GIN(skill_tags);
CREATE INDEX IF NOT EXISTS idx_activity_sessions_date ON activity_sessions(session_date);
CREATE INDEX IF NOT EXISTS idx_activity_registrations_user ON activity_registrations(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_recommendations_user ON ai_recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_recommendations_score ON ai_recommendations(score DESC);

-- Triggers pour updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE OR REPLACE TRIGGER update_user_profiles_updated_at 
    BEFORE UPDATE ON user_profiles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE TRIGGER update_activities_updated_at 
    BEFORE UPDATE ON activities 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE TRIGGER update_activity_sessions_updated_at 
    BEFORE UPDATE ON activity_sessions 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE TRIGGER update_action_locations_updated_at 
    BEFORE UPDATE ON action_locations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS)
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_registrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_recommendations ENABLE ROW LEVEL SECURITY;

-- Politiques RLS
CREATE POLICY "Users can view own profile" ON user_profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON user_profiles
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON user_profiles
    FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can view own registrations" ON activity_registrations
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own registrations" ON activity_registrations
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own registrations" ON activity_registrations
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own recommendations" ON ai_recommendations
    FOR SELECT USING (auth.uid() = user_id);

-- Politiques pour les tables publiques
CREATE POLICY "Activities are publicly readable" ON activities
    FOR SELECT USING (is_active = true);

CREATE POLICY "Activity sessions are publicly readable" ON activity_sessions
    FOR SELECT USING (status IN ('planned', 'confirmed'));

CREATE POLICY "Action locations are publicly readable" ON action_locations
    FOR SELECT USING (is_active = true);