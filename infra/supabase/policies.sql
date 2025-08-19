-- Politiques de sécurité pour La Vida Luca
-- Row Level Security (RLS) policies

-- Activer RLS sur toutes les tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE locations ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_registrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_suggestions ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

-- Politiques pour la table users
-- Les utilisateurs peuvent voir leur propre profil
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = id);

-- Les utilisateurs peuvent mettre à jour leur propre profil
CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid() = id);

-- Les admins peuvent voir tous les utilisateurs
CREATE POLICY "Admins can view all users" ON users
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- Les utilisateurs publics peuvent voir les profils publics (pour le matching d'activités)
CREATE POLICY "Public profiles viewable" ON users
    FOR SELECT USING (
        status = 'active' AND 
        (role = 'instructor' OR role = 'coordinator')
    );

-- Politiques pour la table activities
-- Tout le monde peut voir les activités actives
CREATE POLICY "Anyone can view active activities" ON activities
    FOR SELECT USING (is_active = true);

-- Seuls les admins et coordinateurs peuvent créer/modifier des activités
CREATE POLICY "Coordinators can manage activities" ON activities
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = auth.uid() AND role IN ('admin', 'coordinator')
        )
    );

-- Politiques pour la table locations
-- Tout le monde peut voir les lieux actifs
CREATE POLICY "Anyone can view active locations" ON locations
    FOR SELECT USING (is_active = true);

-- Seuls les admins peuvent gérer les lieux
CREATE POLICY "Admins can manage locations" ON locations
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- Politiques pour activity_registrations
-- Les utilisateurs peuvent voir leurs propres inscriptions
CREATE POLICY "Users can view own registrations" ON activity_registrations
    FOR SELECT USING (user_id = auth.uid());

-- Les utilisateurs peuvent créer leurs propres inscriptions
CREATE POLICY "Users can create own registrations" ON activity_registrations
    FOR INSERT WITH CHECK (user_id = auth.uid());

-- Les utilisateurs peuvent mettre à jour leurs propres inscriptions
CREATE POLICY "Users can update own registrations" ON activity_registrations
    FOR UPDATE USING (user_id = auth.uid());

-- Les coordinateurs peuvent voir toutes les inscriptions
CREATE POLICY "Coordinators can view all registrations" ON activity_registrations
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = auth.uid() AND role IN ('admin', 'coordinator', 'instructor')
        )
    );

-- Politiques pour activity_sessions
-- Tout le monde peut voir les sessions programmées
CREATE POLICY "Anyone can view scheduled sessions" ON activity_sessions
    FOR SELECT USING (status IN ('scheduled', 'in_progress'));

-- Seuls les coordinateurs et instructeurs peuvent gérer les sessions
CREATE POLICY "Instructors can manage sessions" ON activity_sessions
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = auth.uid() AND role IN ('admin', 'coordinator', 'instructor')
        )
    );

-- Politiques pour messages
-- Les utilisateurs peuvent voir leurs propres messages
CREATE POLICY "Users can view own messages" ON messages
    FOR SELECT USING (user_id = auth.uid());

-- Les utilisateurs peuvent créer leurs propres messages
CREATE POLICY "Users can create own messages" ON messages
    FOR INSERT WITH CHECK (user_id = auth.uid());

-- Les admins peuvent voir tous les messages (pour modération)
CREATE POLICY "Admins can view all messages" ON messages
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- Politiques pour ai_suggestions
-- Les utilisateurs peuvent voir leurs propres suggestions
CREATE POLICY "Users can view own suggestions" ON ai_suggestions
    FOR SELECT USING (user_id = auth.uid());

-- Les utilisateurs peuvent créer/mettre à jour leurs propres suggestions
CREATE POLICY "Users can manage own suggestions" ON ai_suggestions
    FOR ALL USING (user_id = auth.uid());

-- Politiques pour notifications
-- Les utilisateurs peuvent voir leurs propres notifications
CREATE POLICY "Users can view own notifications" ON notifications
    FOR SELECT USING (user_id = auth.uid());

-- Les utilisateurs peuvent mettre à jour leurs propres notifications (marquer comme lu)
CREATE POLICY "Users can update own notifications" ON notifications
    FOR UPDATE USING (user_id = auth.uid());

-- Le système peut créer des notifications pour n'importe quel utilisateur
CREATE POLICY "System can create notifications" ON notifications
    FOR INSERT WITH CHECK (true);

-- Fonctions de sécurité supplémentaires

-- Fonction pour vérifier si un utilisateur peut s'inscrire à une activité
CREATE OR REPLACE FUNCTION can_register_for_activity(activity_uuid UUID, user_uuid UUID)
RETURNS BOOLEAN AS $$
DECLARE
    activity_record activities;
    user_record users;
    existing_registration activity_registrations;
BEGIN
    -- Récupérer l'activité
    SELECT * INTO activity_record FROM activities WHERE id = activity_uuid AND is_active = true;
    IF NOT FOUND THEN
        RETURN FALSE;
    END IF;
    
    -- Récupérer l'utilisateur
    SELECT * INTO user_record FROM users WHERE id = user_uuid AND status = 'active';
    IF NOT FOUND THEN
        RETURN FALSE;
    END IF;
    
    -- Vérifier s'il y a déjà une inscription
    SELECT * INTO existing_registration 
    FROM activity_registrations 
    WHERE user_id = user_uuid AND activity_id = activity_uuid 
    AND status IN ('pending', 'confirmed');
    
    IF FOUND THEN
        RETURN FALSE;
    END IF;
    
    -- Autres vérifications (âge, etc.) peuvent être ajoutées ici
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour calculer la distance entre un utilisateur et un lieu
CREATE OR REPLACE FUNCTION distance_to_location(user_uuid UUID, location_uuid UUID)
RETURNS FLOAT AS $$
DECLARE
    user_location GEOGRAPHY;
    location_coords GEOGRAPHY;
BEGIN
    SELECT location INTO user_location FROM users WHERE id = user_uuid;
    SELECT coordinates INTO location_coords FROM locations WHERE id = location_uuid;
    
    IF user_location IS NULL OR location_coords IS NULL THEN
        RETURN NULL;
    END IF;
    
    RETURN ST_Distance(user_location, location_coords) / 1000; -- Distance en km
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Vue pour les activités avec informations de lieu
CREATE VIEW activities_with_location AS
SELECT 
    a.*,
    l.name as location_name,
    l.department,
    l.region,
    l.coordinates as location_coordinates
FROM activities a
LEFT JOIN locations l ON a.location_id = l.id
WHERE a.is_active = true AND (l.is_active = true OR l.is_active IS NULL);

-- Vue pour les sessions avec informations complètes
CREATE VIEW sessions_full AS
SELECT 
    s.*,
    a.title as activity_title,
    a.category as activity_category,
    a.duration_min as activity_duration,
    l.name as location_name,
    l.department,
    u.first_name || ' ' || u.last_name as instructor_name
FROM activity_sessions s
JOIN activities a ON s.activity_id = a.id
LEFT JOIN locations l ON s.location_id = l.id
LEFT JOIN users u ON s.instructor_id = u.id
WHERE a.is_active = true;

-- Grant permissions pour les vues
GRANT SELECT ON activities_with_location TO authenticated;
GRANT SELECT ON sessions_full TO authenticated;