-- La Vida Luca Database Schema
-- Base de données pour la plateforme La Vida Luca

-- Extension pour UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table des activités
CREATE TABLE activities (
    id VARCHAR PRIMARY KEY,
    slug VARCHAR UNIQUE NOT NULL,
    title VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    summary TEXT,
    duration_min INTEGER,
    skill_tags JSONB,
    seasonality JSONB,
    safety_level INTEGER,
    materials JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Table des profils utilisateurs
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    skills JSONB,
    availability JSONB,
    location VARCHAR,
    preferences JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Table des soumissions de contact
CREATE TABLE contact_submissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    email VARCHAR,
    message TEXT,
    type VARCHAR DEFAULT 'contact',
    status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE
);

-- Table des lieux d'action
CREATE TABLE action_sites (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    address TEXT,
    city VARCHAR,
    department VARCHAR,
    coordinates POINT,
    contact_info JSONB,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Table des articles/actualités
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    slug VARCHAR UNIQUE NOT NULL,
    content TEXT,
    excerpt TEXT,
    author VARCHAR,
    published BOOLEAN DEFAULT false,
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Index pour améliorer les performances
CREATE INDEX idx_activities_category ON activities(category);
CREATE INDEX idx_activities_skill_tags ON activities USING GIN (skill_tags);
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_contact_submissions_status ON contact_submissions(status);
CREATE INDEX idx_contact_submissions_created_at ON contact_submissions(created_at);
CREATE INDEX idx_action_sites_department ON action_sites(department);
CREATE INDEX idx_articles_published ON articles(published);
CREATE INDEX idx_articles_published_at ON articles(published_at);

-- RLS (Row Level Security) policies si nécessaire pour Supabase
-- ALTER TABLE activities ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE contact_submissions ENABLE ROW LEVEL SECURITY;

-- Trigger pour mettre à jour updated_at automatiquement
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_activities_updated_at BEFORE UPDATE ON activities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_action_sites_updated_at BEFORE UPDATE ON action_sites
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_articles_updated_at BEFORE UPDATE ON articles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();