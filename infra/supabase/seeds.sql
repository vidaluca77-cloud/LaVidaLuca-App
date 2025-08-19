-- Seed data for La Vida Luca application
-- Inserts initial activities and test data

-- Insert sample activities (the 30 activities from the catalog)
INSERT INTO activities (slug, title, category, summary, duration_min, skill_tags, seasonality, safety_level, materials) VALUES
-- Agriculture
('soins-animaux', 'Soins aux animaux', 'agri', 'Nourrir, nettoyer, observer l''état des animaux.', 60, '{"patience", "observation"}', '{"toutes"}', 1, '{"bottes"}'),
('nettoyage-batiments', 'Nettoyage des bâtiments', 'agri', 'Désinfecter, ranger, entretenir les espaces.', 90, '{"organisation", "hygiene"}', '{"toutes"}', 1, '{"gants", "bottes"}'),
('entretien-materiel', 'Entretien du matériel', 'agri', 'Nettoyer, vérifier, réparer les outils agricoles.', 60, '{"soin_materiel", "autonomie"}', '{"toutes"}', 2, '{"gants"}'),
('plantation-cultures', 'Plantation de cultures', 'agri', 'Semis, arrosage, paillage, suivi de plants.', 90, '{"sol", "plantes"}', '{"printemps", "ete"}', 1, '{"gants"}'),
('init-maraichage', 'Initiation maraîchage', 'agri', 'Plan de culture, entretien, récolte respectueuse.', 120, '{"sol", "organisation"}', '{"printemps", "ete", "automne"}', 1, '{"gants", "bottes"}'),
('clotures-abris', 'Gestion des clôtures & abris', 'agri', 'Identifier, réparer, sécuriser parcs et abris.', 120, '{"securite", "bois"}', '{"toutes"}', 2, '{"gants"}'),

-- Transformation
('fromage', 'Fabrication de fromage', 'transfo', 'Du lait au caillé : hygiène, moulage, affinage (découverte).', 90, '{"hygiene", "precision"}', '{"toutes"}', 2, '{"tablier"}'),
('conserves', 'Confitures & conserves', 'transfo', 'Préparation, stérilisation, mise en pot, étiquetage.', 90, '{"organisation", "hygiene"}', '{"ete", "automne"}', 1, '{"tablier"}'),
('laine', 'Transformation de la laine', 'transfo', 'Lavage, cardage, petite création textile.', 90, '{"patience", "creativite"}', '{"toutes"}', 1, '{"tablier", "gants"}'),
('jus', 'Fabrication de jus', 'transfo', 'Du verger à la bouteille : tri, pressage, filtration.', 90, '{"hygiene", "securite"}', '{"automne"}', 2, '{"tablier", "gants"}'),
('aromatiques-sechage', 'Séchage d''herbes aromatiques', 'transfo', 'Cueillette, séchage, conditionnement doux.', 60, '{"douceur", "organisation"}', '{"ete"}', 1, '{"tablier"}'),
('pain-four-bois', 'Pain au four à bois', 'transfo', 'Pétrissage, façonnage, cuisson : respect des temps.', 120, '{"precision", "rythme"}', '{"toutes"}', 2, '{"tablier"}'),

-- Artisanat
('abris-bois', 'Construction d''abris', 'artisanat', 'Petites structures bois : plan, coupe, assemblage.', 120, '{"bois", "precision", "securite"}', '{"toutes"}', 2, '{"gants"}'),
('reparation-outils', 'Réparation & entretien des outils', 'artisanat', 'Affûtage, graissage, petites réparations.', 60, '{"autonomie", "responsabilite"}', '{"toutes"}', 1, '{"gants"}'),
('menuiserie-simple', 'Menuiserie simple', 'artisanat', 'Mesure, coupe, ponçage, finitions d''un objet.', 120, '{"precision", "creativite"}', '{"toutes"}', 2, '{"gants", "lunettes"}'),
('peinture-deco', 'Peinture & décoration d''espaces', 'artisanat', 'Préparer, protéger, peindre proprement.', 90, '{"proprete", "finitions"}', '{"toutes"}', 1, '{"tablier", "gants"}'),
('amenagement-verts', 'Aménagement d''espaces verts', 'artisanat', 'Désherbage doux, paillage, plantations.', 90, '{"endurance", "esthetique"}', '{"printemps", "ete"}', 1, '{"gants", "bottes"}'),
('panneaux-orientation', 'Panneaux & orientation', 'artisanat', 'Concevoir/poser une signalétique claire.', 90, '{"clarte", "precision"}', '{"toutes"}', 1, '{"gants"}'),

-- Nature
('entretien-riviere', 'Entretien de la rivière', 'nature', 'Nettoyage doux, observation des berges.', 90, '{"prudence", "ecologie"}', '{"printemps", "ete"}', 2, '{"bottes", "gants"}'),
('chemins-sentiers', 'Entretien chemins & sentiers', 'nature', 'Débroussaillage, réfection, balisage léger.', 120, '{"endurance", "orientation"}', '{"printemps", "ete", "automne"}', 2, '{"gants", "bottes"}'),
('verger-taille', 'Taille et entretien du verger', 'nature', 'Élagage doux, observation de la santé des arbres.', 90, '{"patience", "observation"}', '{"hiver", "printemps"}', 2, '{"gants", "lunettes"}'),
('compostage', 'Compostage', 'nature', 'Tri, compost, valorisation des déchets verts.', 60, '{"geste_utile", "hygiene"}', '{"toutes"}', 1, '{"gants"}'),
('faune-locale', 'Observation de la faune locale', 'nature', 'Discrétion, repérage, traces/indices.', 60, '{"patience", "respect"}', '{"toutes"}', 1, '{}'),
('nichoirs-hotels', 'Nichoirs & hôtels à insectes', 'nature', 'Concevoir, fabriquer, installer des abris.', 120, '{"precision", "pedagogie"}', '{"toutes"}', 1, '{"gants"}'),

-- Social
('portes-ouvertes', 'Journée portes ouvertes', 'social', 'Préparer, accueillir, guider un public.', 180, '{"accueil", "organisation"}', '{"toutes"}', 1, '{}'),
('animations-enfants', 'Animations pour enfants', 'social', 'Jeux nature, découverte, sensibilisation douce.', 120, '{"pedagogie", "enthousiasme"}', '{"toutes"}', 1, '{}'),
('ateliers-cuisine', 'Ateliers cuisine partagée', 'social', 'Préparer un repas collectif avec les produits.', 150, '{"partage", "organisation"}', '{"toutes"}', 2, '{"tablier"}'),
('vente-locale', 'Vente directe locale', 'social', 'Préparation, présentation, accueil clients.', 120, '{"contact", "comptage"}', '{"toutes"}', 1, '{}'),
('documentation-projet', 'Documentation de projets', 'social', 'Photos, vidéos, témoignages, communication.', 90, '{"communication", "creativite"}', '{"toutes"}', 1, '{}'),
('marche-local', 'Participation à un marché local', 'social', 'Stand, présentation, caisse symbolique (simulation).', 180, '{"contact", "compter_simple", "equipe"}', '{"toutes"}', 1, '{}');

-- Insert a demo admin user (password is hashed 'demo123')
INSERT INTO users (email, encrypted_password, full_name, role) VALUES
('admin@lavidaluca.fr', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLuijww80I2/0S2', 'Administrateur La Vida Luca', 'admin');

-- Insert demo mentor users
INSERT INTO users (email, encrypted_password, full_name, role, location) VALUES
('mentor1@lavidaluca.fr', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLuijww80I2/0S2', 'Marie Dubois', 'mentor', 'Ferme de la Vallée Verte'),
('mentor2@lavidaluca.fr', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLuijww80I2/0S2', 'Pierre Martin', 'mentor', 'Domaine des Collines');

-- Insert demo student users
INSERT INTO users (email, encrypted_password, full_name, role, location) VALUES
('student1@lavidaluca.fr', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLuijww80I2/0S2', 'Julie Moreau', 'student', 'MFR de Bretagne'),
('student2@lavidaluca.fr', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLuijww80I2/0S2', 'Thomas Leroy', 'student', 'MFR de Normandie');

-- Insert user profiles for demo users
INSERT INTO user_profiles (id, skills, availability, preferences) 
SELECT id, 
       '{"patience", "observation", "organisation"}',
       '{"weekend", "semaine"}',
       '{"agri", "nature"}'
FROM users WHERE email = 'student1@lavidaluca.fr';

INSERT INTO user_profiles (id, skills, availability, preferences) 
SELECT id, 
       '{"bois", "precision", "creativite"}',
       '{"weekend"}',
       '{"artisanat", "transfo"}'
FROM users WHERE email = 'student2@lavidaluca.fr';

-- Insert some sample activity sessions
INSERT INTO activity_sessions (activity_id, mentor_id, title, start_time, end_time, location, max_participants)
SELECT 
    a.id,
    u.id,
    'Session découverte - ' || a.title,
    NOW() + INTERVAL '7 days',
    NOW() + INTERVAL '7 days' + (a.duration_min || ' minutes')::INTERVAL,
    'Ferme de démonstration',
    6
FROM activities a
CROSS JOIN users u
WHERE u.role = 'mentor' 
    AND a.slug IN ('soins-animaux', 'fromage', 'menuiserie-simple')
LIMIT 3;

-- Insert some sample contact submissions
INSERT INTO contact_submissions (name, email, subject, message, type) VALUES
('Jean Dupont', 'jean.dupont@email.fr', 'Candidature relais', 'Bonjour, je souhaite devenir relais La Vida Luca dans ma région.', 'relais'),
('Sophie Lambert', 'sophie.lambert@email.fr', 'Information générale', 'Pouvez-vous me donner plus d''informations sur vos formations ?', 'general'),
('Marc Rousseau', 'marc.rousseau@email.fr', 'Partenariat MFR', 'Notre MFR aimerait établir un partenariat avec votre réseau.', 'partnership');