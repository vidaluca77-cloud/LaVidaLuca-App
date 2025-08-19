-- =====================================================
-- SCHEMA SQL INITIAL POUR LA VIDA LUCA
-- =====================================================
-- Ce script crée les tables nécessaires pour la plateforme
-- La Vida Luca : formation, agriculture et insertion sociale

-- Extension pour UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Extension pour authentification (déjà incluse dans Supabase)
-- CREATE EXTENSION IF NOT EXISTS "auth";

-- =====================================================
-- TABLE: profiles 
-- Profils utilisateurs étendus
-- =====================================================
CREATE TABLE public.profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  email TEXT UNIQUE,
  full_name TEXT,
  avatar_url TEXT,
  role TEXT CHECK (role IN ('student', 'educator', 'admin', 'volunteer')) DEFAULT 'student',
  location TEXT,
  bio TEXT,
  skills TEXT[], -- Compétences déclarées
  preferences TEXT[], -- Préférences d'activités
  availability TEXT[], -- Disponibilités 
  phone TEXT,
  mfr_institution TEXT, -- Institution MFR si applicable
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLE: activities
-- Catalogue des 30 activités MFR
-- =====================================================
CREATE TABLE public.activities (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  slug TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  category TEXT CHECK (category IN ('agri', 'transfo', 'artisanat', 'nature', 'social')) NOT NULL,
  summary TEXT NOT NULL,
  description TEXT,
  duration_min INTEGER NOT NULL,
  skill_tags TEXT[] NOT NULL,
  seasonality TEXT[] NOT NULL,
  safety_level INTEGER CHECK (safety_level BETWEEN 1 AND 3) DEFAULT 1,
  materials TEXT[],
  location TEXT,
  max_participants INTEGER DEFAULT 10,
  min_age INTEGER DEFAULT 14,
  prerequisites TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLE: activity_sessions
-- Sessions programmées d'activités  
-- =====================================================
CREATE TABLE public.activity_sessions (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  activity_id UUID REFERENCES public.activities(id) ON DELETE CASCADE,
  educator_id UUID REFERENCES public.profiles(id),
  title TEXT,
  description TEXT,
  scheduled_at TIMESTAMP WITH TIME ZONE NOT NULL,
  duration_min INTEGER NOT NULL,
  max_participants INTEGER DEFAULT 10,
  location TEXT,
  status TEXT CHECK (status IN ('scheduled', 'in_progress', 'completed', 'cancelled')) DEFAULT 'scheduled',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLE: participants
-- Participation aux sessions d'activités
-- =====================================================
CREATE TABLE public.participants (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  session_id UUID REFERENCES public.activity_sessions(id) ON DELETE CASCADE,
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  status TEXT CHECK (status IN ('registered', 'confirmed', 'attended', 'absent', 'cancelled')) DEFAULT 'registered',
  feedback TEXT,
  rating INTEGER CHECK (rating BETWEEN 1 AND 5),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(session_id, user_id)
);

-- =====================================================
-- TABLE: locations
-- Lieux d'action de La Vida Luca
-- =====================================================
CREATE TABLE public.locations (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  address TEXT,
  city TEXT,
  department TEXT,
  region TEXT,
  coordinates POINT, -- Latitude, longitude
  description TEXT,
  contact_email TEXT,
  contact_phone TEXT,
  website TEXT,
  facilities TEXT[], -- Équipements disponibles
  activities_offered TEXT[], -- Types d'activités proposées
  status TEXT CHECK (status IN ('active', 'inactive', 'planning')) DEFAULT 'active',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLE: ia_interactions
-- Historique des interactions avec l'IA
-- =====================================================
CREATE TABLE public.ia_interactions (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES public.profiles(id),
  session_id TEXT, -- ID de session pour grouper les conversations
  query TEXT NOT NULL,
  response TEXT NOT NULL,
  activity_suggestions UUID[], -- IDs d'activités suggérées
  confidence_score DECIMAL(3,2), -- Score de confiance de l'IA
  feedback_rating INTEGER CHECK (feedback_rating BETWEEN 1 AND 5),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLE: catalog_items
-- Catalogue produits/services (page catalogue)
-- =====================================================
CREATE TABLE public.catalog_items (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  slug TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  price TEXT, -- Prix libre, sur devis, etc.
  category TEXT CHECK (category IN ('Produits vivants', 'Activités terrain', 'Services', 'Dons en nature')) NOT NULL,
  department TEXT,
  location_id UUID REFERENCES public.locations(id),
  tags TEXT[],
  image_url TEXT,
  contact_info JSONB, -- Informations de contact spécifiques
  status TEXT CHECK (status IN ('available', 'out_of_stock', 'seasonal', 'inactive')) DEFAULT 'available',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- POLICIES RLS (Row Level Security)
-- =====================================================

-- Activer RLS sur toutes les tables
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activities ENABLE ROW LEVEL SECURITY; 
ALTER TABLE public.activity_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.participants ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.locations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ia_interactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.catalog_items ENABLE ROW LEVEL SECURITY;

-- Politique pour profiles : les utilisateurs peuvent voir et modifier leur propre profil
CREATE POLICY "Users can view own profile" ON public.profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.profiles  
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON public.profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

-- Politique pour activities : lecture publique, modification pour admins/éducateurs
CREATE POLICY "Activities are viewable by everyone" ON public.activities
  FOR SELECT USING (true);

CREATE POLICY "Only educators and admins can modify activities" ON public.activities
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM public.profiles 
      WHERE id = auth.uid() 
      AND role IN ('educator', 'admin')
    )
  );

-- Politique pour activity_sessions : lecture publique, modification pour propriétaires/admins
CREATE POLICY "Sessions are viewable by everyone" ON public.activity_sessions
  FOR SELECT USING (true);

CREATE POLICY "Educators can manage their sessions" ON public.activity_sessions
  FOR ALL USING (
    educator_id = auth.uid() OR 
    EXISTS (
      SELECT 1 FROM public.profiles 
      WHERE id = auth.uid() AND role = 'admin'
    )
  );

-- Politique pour participants : utilisateurs voient leurs participations
CREATE POLICY "Users can view their participations" ON public.participants
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can manage their participations" ON public.participants
  FOR ALL USING (user_id = auth.uid());

-- Politique pour locations : lecture publique
CREATE POLICY "Locations are viewable by everyone" ON public.locations
  FOR SELECT USING (true);

-- Politique pour ia_interactions : utilisateurs voient leurs interactions
CREATE POLICY "Users can view their IA interactions" ON public.ia_interactions
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can create IA interactions" ON public.ia_interactions
  FOR INSERT WITH CHECK (user_id = auth.uid());

-- Politique pour catalog_items : lecture publique
CREATE POLICY "Catalog items are viewable by everyone" ON public.catalog_items
  FOR SELECT USING (true);

-- =====================================================
-- FONCTIONS ET TRIGGERS
-- =====================================================

-- Fonction pour mise à jour automatique du timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

-- Triggers pour updated_at
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_activities_updated_at BEFORE UPDATE ON public.activities  
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_activity_sessions_updated_at BEFORE UPDATE ON public.activity_sessions
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_participants_updated_at BEFORE UPDATE ON public.participants
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_locations_updated_at BEFORE UPDATE ON public.locations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_catalog_items_updated_at BEFORE UPDATE ON public.catalog_items
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- INDEX POUR PERFORMANCE
-- =====================================================

-- Index pour les recherches fréquentes
CREATE INDEX idx_activities_category ON public.activities(category);
CREATE INDEX idx_activities_skill_tags ON public.activities USING GIN(skill_tags);
CREATE INDEX idx_activities_seasonality ON public.activities USING GIN(seasonality);
CREATE INDEX idx_activity_sessions_scheduled_at ON public.activity_sessions(scheduled_at);
CREATE INDEX idx_activity_sessions_status ON public.activity_sessions(status);
CREATE INDEX idx_catalog_items_category ON public.catalog_items(category);
CREATE INDEX idx_catalog_items_tags ON public.catalog_items USING GIN(tags);
CREATE INDEX idx_locations_department ON public.locations(department);

-- =====================================================
-- COMMENTAIRES SUR LES TABLES
-- =====================================================

COMMENT ON TABLE public.profiles IS 'Profils utilisateurs étendus avec compétences et préférences';
COMMENT ON TABLE public.activities IS 'Catalogue des 30 activités pédagogiques MFR';
COMMENT ON TABLE public.activity_sessions IS 'Sessions programmées d activités avec éducateurs';
COMMENT ON TABLE public.participants IS 'Inscriptions et participation aux sessions';
COMMENT ON TABLE public.locations IS 'Lieux d action du réseau La Vida Luca';
COMMENT ON TABLE public.ia_interactions IS 'Historique des interactions avec l IA de matching';
COMMENT ON TABLE public.catalog_items IS 'Catalogue des produits et services proposés';