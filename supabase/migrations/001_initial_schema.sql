-- Schema principal pour La Vida Luca
-- Base de données Supabase PostgreSQL

-- Extension pour UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================
-- Table des activités (catalogue MFR)
-- =====================================

CREATE TABLE public.activities (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    slug VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('agri', 'transfo', 'artisanat', 'nature', 'social')),
    summary TEXT NOT NULL,
    description TEXT,
    duration_min INTEGER NOT NULL DEFAULT 60,
    skill_tags TEXT[] DEFAULT '{}',
    seasonality TEXT[] DEFAULT '{}',
    safety_level INTEGER DEFAULT 1 CHECK (safety_level BETWEEN 1 AND 3),
    materials TEXT[] DEFAULT '{}',
    location_requirements TEXT,
    max_participants INTEGER DEFAULT 10,
    min_age INTEGER DEFAULT 14,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================
-- Table des profils utilisateurs
-- =====================================

CREATE TABLE public.user_profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(200),
    skills TEXT[] DEFAULT '{}',
    availability TEXT[] DEFAULT '{}',
    location VARCHAR(200),
    preferences TEXT[] DEFAULT '{}',
    experience_level VARCHAR(50) DEFAULT 'debutant' CHECK (experience_level IN ('debutant', 'intermediaire', 'avance')),
    role VARCHAR(50) DEFAULT 'participant' CHECK (role IN ('participant', 'encadrant', 'coordinateur', 'admin')),
    mfr_affiliation VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================
-- Table des suggestions personnalisées
-- =====================================

CREATE TABLE public.user_suggestions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.user_profiles(id) ON DELETE CASCADE,
    activity_id UUID REFERENCES public.activities(id) ON DELETE CASCADE,
    score DECIMAL(3,2) DEFAULT 0.0,
    reasons TEXT[] DEFAULT '{}',
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected', 'completed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================
-- Table des demandes de contact
-- =====================================

CREATE TABLE public.contact_requests (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    message TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'general' CHECK (type IN ('general', 'rejoindre', 'partenariat', 'education')),
    status VARCHAR(50) DEFAULT 'new' CHECK (status IN ('new', 'processing', 'resolved', 'closed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- =====================================
-- Table des lieux d'action
-- =====================================

CREATE TABLE public.locations (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    address TEXT NOT NULL,
    departement VARCHAR(50) NOT NULL,
    region VARCHAR(100) NOT NULL,
    type VARCHAR(50) DEFAULT 'ferme' CHECK (type IN ('ferme', 'mfr', 'partenaire', 'relais')),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    website VARCHAR(500),
    description TEXT,
    capacity INTEGER DEFAULT 20,
    available_activities UUID[] DEFAULT '{}',
    coordinates POINT,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================
-- Politiques RLS (Row Level Security)
-- =====================================

-- Activer RLS sur toutes les tables
ALTER TABLE public.activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_suggestions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.contact_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.locations ENABLE ROW LEVEL SECURITY;

-- Politiques pour les activités (lecture publique)
CREATE POLICY "Activities are viewable by everyone" ON public.activities
    FOR SELECT USING (true);

CREATE POLICY "Only admins can modify activities" ON public.activities
    FOR ALL USING (auth.role() = 'admin');

-- Politiques pour les profils utilisateurs
CREATE POLICY "Users can view their own profile" ON public.user_profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" ON public.user_profiles
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert their own profile" ON public.user_profiles
    FOR INSERT WITH CHECK (auth.uid() = id);

-- Politiques pour les suggestions
CREATE POLICY "Users can view their own suggestions" ON public.user_suggestions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "System can insert suggestions" ON public.user_suggestions
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can update their suggestions status" ON public.user_suggestions
    FOR UPDATE USING (auth.uid() = user_id);

-- Politiques pour les demandes de contact (insertion libre, lecture admin)
CREATE POLICY "Anyone can submit contact requests" ON public.contact_requests
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Only admins can view contact requests" ON public.contact_requests
    FOR SELECT USING (auth.role() = 'admin');

-- Politiques pour les lieux (lecture publique pour les actifs)
CREATE POLICY "Active locations are viewable by everyone" ON public.locations
    FOR SELECT USING (active = true);

CREATE POLICY "Only admins can modify locations" ON public.locations
    FOR ALL USING (auth.role() = 'admin');

-- =====================================
-- Index pour les performances
-- =====================================

CREATE INDEX idx_activities_category ON public.activities(category);
CREATE INDEX idx_activities_safety_level ON public.activities(safety_level);
CREATE INDEX idx_activities_slug ON public.activities(slug);

CREATE INDEX idx_user_suggestions_user_id ON public.user_suggestions(user_id);
CREATE INDEX idx_user_suggestions_activity_id ON public.user_suggestions(activity_id);
CREATE INDEX idx_user_suggestions_score ON public.user_suggestions(score DESC);

CREATE INDEX idx_contact_requests_status ON public.contact_requests(status);
CREATE INDEX idx_contact_requests_type ON public.contact_requests(type);
CREATE INDEX idx_contact_requests_created_at ON public.contact_requests(created_at DESC);

CREATE INDEX idx_locations_departement ON public.locations(departement);
CREATE INDEX idx_locations_type ON public.locations(type);
CREATE INDEX idx_locations_active ON public.locations(active);

-- =====================================
-- Triggers pour updated_at
-- =====================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_activities_updated_at BEFORE UPDATE ON public.activities 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON public.user_profiles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_locations_updated_at BEFORE UPDATE ON public.locations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();