-- LaVidaLuca Database Seeds
-- Sample data for development and testing

-- Insert sample locations first
INSERT INTO locations (name, description, address, departement, contact_person, contact_email, contact_phone, max_capacity, facilities) VALUES
(
    'Ferme Pédagogique du Calvados',
    'Ferme d''accueil spécialisée dans la formation des jeunes MFR',
    '123 Route de la Campagne, 14000 Caen',
    'Calvados (14)',
    'Marie Dupont',
    'marie@ferme-calvados.fr',
    '+33 2 31 85 XX XX',
    15,
    '["parking", "sanitaires", "cantine", "wifi"]'::jsonb
),
(
    'Centre Agricole Normandie',
    'Centre de formation agricole et environnementale',
    '456 Chemin des Champs, 14100 Lisieux',
    'Calvados (14)',
    'Jean Martin',
    'contact@centre-normandie.fr',
    '+33 2 31 62 XX XX',
    20,
    '["parking", "sanitaires", "atelier", "serre"]'::jsonb
);

-- Insert sample activities based on the frontend data
INSERT INTO activities (slug, title, category, summary, description, duration_min, seasonality, safety_level, min_age, max_participants, location_id) VALUES
(
    'soins-animaux',
    'Soins aux animaux de la ferme',
    'agri',
    'Nourrir, nettoyer, observer les animaux.',
    'Apprentissage des gestes essentiels pour le bien-être animal : alimentation, nettoyage des espaces, observation comportementale et soins de base.',
    90,
    '["toutes"]'::jsonb,
    '1',
    16,
    6,
    1
),
(
    'traite-animaux',
    'Traite et manipulation',
    'agri',
    'Technique de traite, manipulation douce.',
    'Formation à la traite manuelle et mécanique, techniques de manipulation respectueuse des animaux, hygiène et qualité du lait.',
    120,
    '["toutes"]'::jsonb,
    '2',
    16,
    4,
    1
),
(
    'plantation-cultures',
    'Plantation de cultures',
    'agri',
    'Semis, arrosage, paillage, suivi de plants.',
    'Apprentissage des techniques de plantation : préparation du sol, semis, arrosage, paillage et suivi de croissance.',
    90,
    '["printemps", "ete"]'::jsonb,
    '1',
    15,
    8,
    1
),
(
    'init-maraichage',
    'Initiation maraîchage',
    'agri',
    'Plan de culture, entretien, récolte respectueuse.',
    'Découverte complète du maraîchage : planification des cultures, techniques d''entretien, récolte et conservation.',
    120,
    '["printemps", "ete", "automne"]'::jsonb,
    '1',
    15,
    6,
    2
),
(
    'fromage',
    'Fabrication de fromage',
    'transfo',
    'Du lait au caillé : hygiène, moulage, affinage (découverte).',
    'Initiation à la fabrication fromagère : techniques de caillage, moulage, saumurage et bases de l''affinage.',
    90,
    '["toutes"]'::jsonb,
    '2',
    16,
    4,
    1
),
(
    'conserves',
    'Confitures & conserves',
    'transfo',
    'Préparation, stérilisation, mise en pot, étiquetage.',
    'Apprentissage de la conservation : préparation des fruits et légumes, techniques de stérilisation et conditionnement.',
    90,
    '["ete", "automne"]'::jsonb,
    '1',
    15,
    6,
    2
),
(
    'menuiserie-simple',
    'Menuiserie simple',
    'artisanat',
    'Mesurer, scier, poncer, assembler (projets faciles).',
    'Initiation à la menuiserie : utilisation des outils de base, techniques d''assemblage et réalisation de projets simples.',
    120,
    '["toutes"]'::jsonb,
    '2',
    16,
    4,
    2
),
(
    'entretien-riviere',
    'Entretien de la rivière',
    'nature',
    'Nettoyage doux, observation des berges.',
    'Sensibilisation à l''écologie aquatique : nettoyage respectueux, observation de la faune et de la flore des berges.',
    90,
    '["printemps", "ete"]'::jsonb,
    '2',
    16,
    8,
    1
),
(
    'compostage',
    'Compostage',
    'nature',
    'Tri, compost, valorisation des déchets verts.',
    'Apprentissage du compostage : tri des déchets organiques, montage de compost et utilisation en fertilisant.',
    60,
    '["toutes"]'::jsonb,
    '1',
    15,
    10,
    2
),
(
    'visites-guidees',
    'Visites guidées de la ferme',
    'social',
    'Présenter la ferme, répondre simplement.',
    'Formation à l''accueil du public : techniques de présentation, pédagogie adaptée aux différents âges.',
    60,
    '["toutes"]'::jsonb,
    '1',
    17,
    3,
    1
);

-- Insert sample users with different roles
INSERT INTO users (email, username, hashed_password, full_name, role, location, bio, availability, preferences) VALUES
(
    'admin@lavidaluca.org',
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewXBrg3b4vEOI2Hi', -- password: admin123
    'Administrateur LaVidaLuca',
    'admin',
    'Calvados (14)',
    'Responsable de la plateforme LaVidaLuca',
    '["semaine", "weekend"]'::jsonb,
    '["agri", "nature", "social"]'::jsonb
),
(
    'mentor@ferme-calvados.fr',
    'mentor_marie',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewXBrg3b4vEOI2Hi', -- password: mentor123
    'Marie Dupont',
    'mentor',
    'Calvados (14)',
    'Formatrice en agriculture à la ferme pédagogique',
    '["semaine", "matin", "apres-midi"]'::jsonb,
    '["agri", "transfo"]'::jsonb
),
(
    'etudiant@mfr-exemple.fr',
    'etudiant_paul',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewXBrg3b4vEOI2Hi', -- password: etudiant123
    'Paul Durand',
    'student',
    'Calvados (14)',
    'Élève en MFR, passionné d''agriculture',
    '["weekend", "vacances"]'::jsonb,
    '["agri", "nature"]'::jsonb
);

-- Insert activity-skill relationships (using skill names from the skills table)
INSERT INTO activity_skills (activity_id, skill_id, required_level) 
SELECT a.id, s.id, 2
FROM activities a, skills s 
WHERE a.slug = 'soins-animaux' AND s.name IN ('elevage', 'hygiene', 'soins_animaux');

INSERT INTO activity_skills (activity_id, skill_id, required_level)
SELECT a.id, s.id, 1
FROM activities a, skills s 
WHERE a.slug = 'plantation-cultures' AND s.name IN ('sol', 'plantes');

INSERT INTO activity_skills (activity_id, skill_id, required_level)
SELECT a.id, s.id, 2
FROM activities a, skills s 
WHERE a.slug = 'fromage' AND s.name IN ('hygiene', 'precision');

-- Insert activity-material relationships
INSERT INTO activity_materials (activity_id, material_id, quantity, is_mandatory)
SELECT a.id, m.id, 1, true
FROM activities a, materials m 
WHERE a.slug = 'soins-animaux' AND m.name IN ('tablier', 'bottes');

INSERT INTO activity_materials (activity_id, material_id, quantity, is_mandatory)
SELECT a.id, m.id, 1, true
FROM activities a, materials m 
WHERE a.slug = 'fromage' AND m.name = 'tablier';

INSERT INTO activity_materials (activity_id, material_id, quantity, is_mandatory)
SELECT a.id, m.id, 1, true
FROM activities a, materials m 
WHERE a.slug = 'menuiserie-simple' AND m.name IN ('gants', 'lunettes');

-- Insert sample user skills
INSERT INTO user_skills (user_id, skill_id, proficiency_level)
SELECT u.id, s.id, 3
FROM users u, skills s 
WHERE u.username = 'etudiant_paul' AND s.name IN ('elevage', 'sol', 'plantes');

INSERT INTO user_skills (user_id, skill_id, proficiency_level)
SELECT u.id, s.id, 4
FROM users u, skills s 
WHERE u.username = 'mentor_marie' AND s.name IN ('elevage', 'hygiene', 'pedagogie', 'organisation');

COMMENT ON TABLE users IS 'Sample users: admin/admin123, mentor_marie/mentor123, etudiant_paul/etudiant123';
COMMENT ON TABLE activities IS 'Sample activities based on LaVidaLuca catalog';
COMMENT ON TABLE locations IS 'Sample farm locations in Calvados';