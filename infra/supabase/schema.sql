-- La Vida Luca Database Schema
-- Creation: Tables, indexes, RLS policies

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (extends Supabase Auth)
CREATE TABLE IF NOT EXISTS users (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('user', 'mfr_student', 'educator', 'admin')),
    skills TEXT[] DEFAULT '{}',
    availability TEXT[] DEFAULT '{}',
    location VARCHAR(255) DEFAULT '',
    preferences TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Activities table
CREATE TABLE IF NOT EXISTS activities (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('agri', 'transfo', 'artisanat', 'nature', 'social')),
    duration_min INTEGER NOT NULL,
    skill_tags TEXT[] DEFAULT '{}',
    seasonality TEXT[] DEFAULT '{}',
    safety_level INTEGER DEFAULT 1 CHECK (safety_level >= 1 AND safety_level <= 3),
    materials TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Contact messages table
CREATE TABLE IF NOT EXISTS contact_messages (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    message TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'general' CHECK (type IN ('general', 'rejoindre', 'support')),
    status VARCHAR(50) DEFAULT 'new' CHECK (status IN ('new', 'in_progress', 'resolved', 'closed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User activity enrollments
CREATE TABLE IF NOT EXISTS user_activities (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    activity_id UUID REFERENCES activities(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'enrolled' CHECK (status IN ('enrolled', 'completed', 'cancelled')),
    enrolled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    UNIQUE(user_id, activity_id)
);

-- Locations/Sites table
CREATE TABLE IF NOT EXISTS locations (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(255) NOT NULL,
    department VARCHAR(10) NOT NULL,
    region VARCHAR(255) NOT NULL,
    coordinates POINT,
    contact_person VARCHAR(255),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    description TEXT,
    facilities TEXT[] DEFAULT '{}',
    capacity INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Activity sessions (scheduled instances of activities)
CREATE TABLE IF NOT EXISTS activity_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    activity_id UUID REFERENCES activities(id) ON DELETE CASCADE,
    location_id UUID REFERENCES locations(id) ON DELETE CASCADE,
    instructor_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    max_participants INTEGER DEFAULT 10,
    current_participants INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'ongoing', 'completed', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User session enrollments
CREATE TABLE IF NOT EXISTS user_session_enrollments (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id UUID REFERENCES activity_sessions(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'enrolled' CHECK (status IN ('enrolled', 'confirmed', 'attended', 'absent', 'cancelled')),
    enrolled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    notes TEXT,
    UNIQUE(user_id, session_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
CREATE INDEX IF NOT EXISTS idx_activities_category ON activities(category);
CREATE INDEX IF NOT EXISTS idx_activities_safety_level ON activities(safety_level);
CREATE INDEX IF NOT EXISTS idx_contact_messages_status ON contact_messages(status);
CREATE INDEX IF NOT EXISTS idx_contact_messages_type ON contact_messages(type);
CREATE INDEX IF NOT EXISTS idx_user_activities_user_id ON user_activities(user_id);
CREATE INDEX IF NOT EXISTS idx_user_activities_activity_id ON user_activities(activity_id);
CREATE INDEX IF NOT EXISTS idx_activity_sessions_start_time ON activity_sessions(start_time);
CREATE INDEX IF NOT EXISTS idx_activity_sessions_status ON activity_sessions(status);
CREATE INDEX IF NOT EXISTS idx_locations_department ON locations(department);
CREATE INDEX IF NOT EXISTS idx_locations_active ON locations(active);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_activities_updated_at BEFORE UPDATE ON activities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_contact_messages_updated_at BEFORE UPDATE ON contact_messages FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_locations_updated_at BEFORE UPDATE ON locations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_activity_sessions_updated_at BEFORE UPDATE ON activity_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) Policies

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE contact_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE locations ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_session_enrollments ENABLE ROW LEVEL SECURITY;

-- Users policies
CREATE POLICY "Users can view their own profile" ON users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update their own profile" ON users FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Admins can view all users" ON users FOR SELECT USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin')
);

-- Activities policies (public read, admin/educator write)
CREATE POLICY "Anyone can view activities" ON activities FOR SELECT USING (true);
CREATE POLICY "Admins and educators can create activities" ON activities FOR INSERT WITH CHECK (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role IN ('admin', 'educator'))
);
CREATE POLICY "Admins and educators can update activities" ON activities FOR UPDATE USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role IN ('admin', 'educator'))
);

-- Contact messages policies
CREATE POLICY "Anyone can create contact messages" ON contact_messages FOR INSERT WITH CHECK (true);
CREATE POLICY "Admins can view all contact messages" ON contact_messages FOR SELECT USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin')
);
CREATE POLICY "Admins can update contact messages" ON contact_messages FOR UPDATE USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin')
);

-- User activities policies
CREATE POLICY "Users can view their own activities" ON user_activities FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can enroll in activities" ON user_activities FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own activity status" ON user_activities FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Educators can view all user activities" ON user_activities FOR SELECT USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role IN ('admin', 'educator'))
);

-- Locations policies (public read, admin write)
CREATE POLICY "Anyone can view active locations" ON locations FOR SELECT USING (active = true);
CREATE POLICY "Admins can manage locations" ON locations FOR ALL USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin')
);

-- Activity sessions policies
CREATE POLICY "Anyone can view scheduled sessions" ON activity_sessions FOR SELECT USING (status = 'scheduled');
CREATE POLICY "Educators can manage sessions" ON activity_sessions FOR ALL USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role IN ('admin', 'educator'))
);

-- User session enrollments policies
CREATE POLICY "Users can view their own enrollments" ON user_session_enrollments FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can enroll in sessions" ON user_session_enrollments FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own enrollments" ON user_session_enrollments FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Educators can view all enrollments" ON user_session_enrollments FOR SELECT USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role IN ('admin', 'educator'))
);