-- La Vida Luca Database Schema
-- Base de données pour la plateforme La Vida Luca

-- Extension pour UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Extension pour les fonctionnalités géographiques
CREATE EXTENSION IF NOT EXISTS postgis;

-- Table des utilisateurs
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    date_of_birth DATE,
    location GEOGRAPHY(POINT, 4326),
    location_name VARCHAR(255),
    bio TEXT,
    skills JSONB DEFAULT '[]'::jsonb,
    interests JSONB DEFAULT '[]'::jsonb,
    availability JSONB DEFAULT '[]'::jsonb,
    role VARCHAR(50) DEFAULT 'participant',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- Table des activités
CREATE TABLE activities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    summary TEXT,
    description TEXT,
    duration_min INTEGER,
    skill_tags JSONB DEFAULT '[]'::jsonb,
    seasonality JSONB DEFAULT '[]'::jsonb,
    safety_level INTEGER DEFAULT 1,
    materials JSONB DEFAULT '[]'::jsonb,
    location_id UUID,
    max_participants INTEGER,
    min_age INTEGER,
    max_age INTEGER,
    price_euros DECIMAL(10,2),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des lieux d'action
CREATE TABLE locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    address TEXT,
    coordinates GEOGRAPHY(POINT, 4326),
    department VARCHAR(10),
    region VARCHAR(100),
    type VARCHAR(50), -- ferme, mfr, partenaire
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20),
    description TEXT,
    facilities JSONB DEFAULT '[]'::jsonb,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des inscriptions aux activités
CREATE TABLE activity_registrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    activity_id UUID REFERENCES activities(id) ON DELETE CASCADE,
    session_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'pending', -- pending, confirmed, cancelled, completed
    notes TEXT,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    feedback TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, activity_id, session_date)
);

-- Table des sessions d'activités programmées
CREATE TABLE activity_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    activity_id UUID REFERENCES activities(id) ON DELETE CASCADE,
    location_id UUID REFERENCES locations(id),
    instructor_id UUID REFERENCES users(id),
    scheduled_date TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_min INTEGER,
    max_participants INTEGER,
    current_participants INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'scheduled', -- scheduled, in_progress, completed, cancelled
    weather_conditions VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des messages/chat
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'user', -- user, ai, system
    context JSONB,
    response_to UUID REFERENCES messages(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des suggestions IA
CREATE TABLE ai_suggestions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    activity_id UUID REFERENCES activities(id) ON DELETE CASCADE,
    score DECIMAL(3,2),
    reasons JSONB DEFAULT '[]'::jsonb,
    context JSONB,
    was_accepted BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des notifications
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    type VARCHAR(50), -- activity_reminder, new_activity, system, etc.
    is_read BOOLEAN DEFAULT false,
    action_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes pour les performances
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_location ON users USING GIST(location);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_activities_category ON activities(category);
CREATE INDEX idx_activities_slug ON activities(slug);
CREATE INDEX idx_activities_location ON activities(location_id);
CREATE INDEX idx_locations_coordinates ON locations USING GIST(coordinates);
CREATE INDEX idx_locations_department ON locations(department);
CREATE INDEX idx_activity_registrations_user ON activity_registrations(user_id);
CREATE INDEX idx_activity_registrations_activity ON activity_registrations(activity_id);
CREATE INDEX idx_activity_registrations_status ON activity_registrations(status);
CREATE INDEX idx_activity_sessions_date ON activity_sessions(scheduled_date);
CREATE INDEX idx_activity_sessions_activity ON activity_sessions(activity_id);
CREATE INDEX idx_messages_user ON messages(user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_ai_suggestions_user ON ai_suggestions(user_id);
CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read) WHERE is_read = false;

-- Fonction pour mettre à jour updated_at automatiquement
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers pour updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_activities_updated_at BEFORE UPDATE ON activities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_locations_updated_at BEFORE UPDATE ON locations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_activity_registrations_updated_at BEFORE UPDATE ON activity_registrations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_activity_sessions_updated_at BEFORE UPDATE ON activity_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Fonction pour mettre à jour le nombre de participants
CREATE OR REPLACE FUNCTION update_session_participants()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' AND NEW.status = 'confirmed' THEN
        UPDATE activity_sessions 
        SET current_participants = current_participants + 1
        WHERE id = (
            SELECT session_id FROM activity_registrations 
            WHERE activity_id = NEW.activity_id 
            AND session_date = (SELECT scheduled_date FROM activity_sessions WHERE activity_id = NEW.activity_id ORDER BY scheduled_date LIMIT 1)
        );
    ELSIF TG_OP = 'UPDATE' AND OLD.status != 'confirmed' AND NEW.status = 'confirmed' THEN
        UPDATE activity_sessions 
        SET current_participants = current_participants + 1
        WHERE id = (
            SELECT session_id FROM activity_registrations 
            WHERE activity_id = NEW.activity_id 
            AND session_date = (SELECT scheduled_date FROM activity_sessions WHERE activity_id = NEW.activity_id ORDER BY scheduled_date LIMIT 1)
        );
    ELSIF TG_OP = 'UPDATE' AND OLD.status = 'confirmed' AND NEW.status != 'confirmed' THEN
        UPDATE activity_sessions 
        SET current_participants = current_participants - 1
        WHERE id = (
            SELECT session_id FROM activity_registrations 
            WHERE activity_id = NEW.activity_id 
            AND session_date = (SELECT scheduled_date FROM activity_sessions WHERE activity_id = NEW.activity_id ORDER BY scheduled_date LIMIT 1)
        );
    END IF;
    
    RETURN COALESCE(NEW, OLD);
END;
$$ language 'plpgsql';

CREATE TRIGGER update_session_participants_trigger
    AFTER INSERT OR UPDATE ON activity_registrations
    FOR EACH ROW EXECUTE FUNCTION update_session_participants();