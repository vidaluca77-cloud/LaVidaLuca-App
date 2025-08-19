-- Schema pour la base de données La Vida Luca
-- À exécuter dans Supabase SQL Editor

-- Table des activités (catalogue des 30 activités MFR)
CREATE TABLE activities (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    slug VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    summary TEXT NOT NULL,
    description TEXT,
    duration_min INTEGER NOT NULL,
    skill_tags TEXT[] DEFAULT '{}',
    seasonality TEXT[] DEFAULT '{}',
    safety_level INTEGER DEFAULT 1,
    materials TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table des profils utilisateurs
CREATE TABLE user_profiles (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    skills TEXT[] DEFAULT '{}',
    preferences TEXT[] DEFAULT '{}',
    availability TEXT[] DEFAULT '{}',
    experience_level VARCHAR(50) DEFAULT 'debutant',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table des participations aux activités
CREATE TABLE activity_participations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    activity_id UUID REFERENCES activities(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'interested', -- interested, registered, completed, cancelled
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, activity_id)
);

-- Table des recommandations IA
CREATE TABLE ai_recommendations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    activity_id UUID REFERENCES activities(id) ON DELETE CASCADE,
    match_score DECIMAL(3,2),
    reasons TEXT[],
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table des messages de contact
CREATE TABLE contact_messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL,
    phone VARCHAR(50),
    subject VARCHAR(300),
    message TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'new',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour optimiser les requêtes
CREATE INDEX idx_activities_category ON activities(category);
CREATE INDEX idx_activities_seasonality ON activities USING GIN(seasonality);
CREATE INDEX idx_activities_skill_tags ON activities USING GIN(skill_tags);
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_activity_participations_user_id ON activity_participations(user_id);
CREATE INDEX idx_activity_participations_activity_id ON activity_participations(activity_id);
CREATE INDEX idx_ai_recommendations_user_id ON ai_recommendations(user_id);
CREATE INDEX idx_contact_messages_status ON contact_messages(status);

-- RLS (Row Level Security) policies
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_participations ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_recommendations ENABLE ROW LEVEL SECURITY;

-- Politique pour les profils utilisateurs
CREATE POLICY "Users can view and edit their own profile" ON user_profiles
    FOR ALL USING (auth.uid() = user_id);

-- Politique pour les participations
CREATE POLICY "Users can view and edit their own participations" ON activity_participations
    FOR ALL USING (auth.uid() = user_id);

-- Politique pour les recommandations
CREATE POLICY "Users can view their own recommendations" ON ai_recommendations
    FOR SELECT USING (auth.uid() = user_id);

-- Les activités sont publiques (lecture seule pour tous)
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Activities are viewable by everyone" ON activities
    FOR SELECT USING (true);

-- Fonctions de trigger pour updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers pour auto-update des timestamps
CREATE TRIGGER update_activities_updated_at BEFORE UPDATE ON activities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_activity_participations_updated_at BEFORE UPDATE ON activity_participations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();