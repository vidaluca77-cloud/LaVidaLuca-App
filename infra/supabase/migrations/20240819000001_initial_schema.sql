-- Migration: Initial schema for La Vida Luca
-- Created: 2024-08-19
-- Description: Creates the initial database schema for the La Vida Luca platform

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create custom types
CREATE TYPE activity_category AS ENUM ('agri', 'transfo', 'artisanat', 'nature', 'social');
CREATE TYPE seasonality AS ENUM ('printemps', 'ete', 'automne', 'hiver', 'toutes');
CREATE TYPE user_role AS ENUM ('student', 'teacher', 'admin', 'visitor');

-- Users table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.user_profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    role user_role DEFAULT 'visitor',
    full_name TEXT,
    bio TEXT,
    skills TEXT[] DEFAULT '{}',
    availability seasonality[] DEFAULT '{}',
    location TEXT,
    preferences activity_category[] DEFAULT '{}',
    school_affiliation TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Activities table
CREATE TABLE IF NOT EXISTS public.activities (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    category activity_category NOT NULL,
    summary TEXT NOT NULL,
    description TEXT,
    duration_min INTEGER NOT NULL,
    skill_tags TEXT[] DEFAULT '{}',
    seasonality seasonality[] DEFAULT '{}',
    safety_level INTEGER DEFAULT 1 CHECK (safety_level BETWEEN 1 AND 3),
    materials TEXT[] DEFAULT '{}',
    max_participants INTEGER DEFAULT 10,
    min_age INTEGER DEFAULT 14,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Activity sessions/bookings
CREATE TABLE IF NOT EXISTS public.activity_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    activity_id UUID REFERENCES public.activities(id) ON DELETE CASCADE,
    instructor_id UUID REFERENCES public.user_profiles(id),
    scheduled_date DATE NOT NULL,
    scheduled_time TIME NOT NULL,
    max_participants INTEGER NOT NULL,
    current_participants INTEGER DEFAULT 0,
    location TEXT,
    notes TEXT,
    is_cancelled BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User activity bookings
CREATE TABLE IF NOT EXISTS public.activity_bookings (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.user_profiles(id) ON DELETE CASCADE,
    session_id UUID REFERENCES public.activity_sessions(id) ON DELETE CASCADE,
    booking_status TEXT DEFAULT 'confirmed' CHECK (booking_status IN ('pending', 'confirmed', 'cancelled', 'completed')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, session_id)
);

-- Activity recommendations log
CREATE TABLE IF NOT EXISTS public.activity_recommendations (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.user_profiles(id),
    activity_id UUID REFERENCES public.activities(id),
    score DECIMAL(3,2) NOT NULL CHECK (score BETWEEN 0 AND 1),
    reasons TEXT[] DEFAULT '{}',
    recommended_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_feedback INTEGER CHECK (user_feedback BETWEEN 1 AND 5),
    user_followed BOOLEAN DEFAULT false
);

-- Contact messages
CREATE TABLE IF NOT EXISTS public.contact_messages (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    subject TEXT NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT false,
    responded_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Locations/farms
CREATE TABLE IF NOT EXISTS public.locations (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    coordinates POINT,
    description TEXT,
    contact_person TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_activities_category ON public.activities(category);
CREATE INDEX IF NOT EXISTS idx_activities_slug ON public.activities(slug);
CREATE INDEX IF NOT EXISTS idx_activities_seasonality ON public.activities USING GIN(seasonality);
CREATE INDEX IF NOT EXISTS idx_activities_skill_tags ON public.activities USING GIN(skill_tags);
CREATE INDEX IF NOT EXISTS idx_user_profiles_role ON public.user_profiles(role);
CREATE INDEX IF NOT EXISTS idx_user_profiles_skills ON public.user_profiles USING GIN(skills);
CREATE INDEX IF NOT EXISTS idx_activity_sessions_date ON public.activity_sessions(scheduled_date);
CREATE INDEX IF NOT EXISTS idx_activity_bookings_user ON public.activity_bookings(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_bookings_session ON public.activity_bookings(session_id);
CREATE INDEX IF NOT EXISTS idx_contact_messages_created ON public.contact_messages(created_at);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at triggers
CREATE TRIGGER tr_user_profiles_updated_at
    BEFORE UPDATE ON public.user_profiles
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER tr_activities_updated_at
    BEFORE UPDATE ON public.activities
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER tr_activity_sessions_updated_at
    BEFORE UPDATE ON public.activity_sessions
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER tr_activity_bookings_updated_at
    BEFORE UPDATE ON public.activity_bookings
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER tr_locations_updated_at
    BEFORE UPDATE ON public.locations
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- Row Level Security (RLS) policies
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activity_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activity_bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activity_recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.contact_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.locations ENABLE ROW LEVEL SECURITY;

-- Basic RLS policies (can be refined based on requirements)

-- Users can view their own profile and public profiles
CREATE POLICY "Users can view profiles" ON public.user_profiles
    FOR SELECT USING (true);

CREATE POLICY "Users can update own profile" ON public.user_profiles
    FOR UPDATE USING (auth.uid() = id);

-- Activities are publicly viewable
CREATE POLICY "Activities are publicly viewable" ON public.activities
    FOR SELECT USING (is_active = true);

-- Activity sessions are publicly viewable
CREATE POLICY "Activity sessions are publicly viewable" ON public.activity_sessions
    FOR SELECT USING (is_cancelled = false);

-- Users can view and manage their own bookings
CREATE POLICY "Users can view own bookings" ON public.activity_bookings
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own bookings" ON public.activity_bookings
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own bookings" ON public.activity_bookings
    FOR UPDATE USING (auth.uid() = user_id);

-- Users can view their own recommendations
CREATE POLICY "Users can view own recommendations" ON public.activity_recommendations
    FOR SELECT USING (auth.uid() = user_id);

-- Contact messages can be inserted by anyone
CREATE POLICY "Anyone can create contact messages" ON public.contact_messages
    FOR INSERT WITH CHECK (true);

-- Locations are publicly viewable
CREATE POLICY "Locations are publicly viewable" ON public.locations
    FOR SELECT USING (is_active = true);