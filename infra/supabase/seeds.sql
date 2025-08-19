-- LaVidaLuca Database Seeds
-- Initial data for the LaVidaLuca application

-- Insert skills
INSERT INTO skills (name, description, category) VALUES
-- Technical skills
('elevage', 'Soins et gestion des animaux d''élevage', 'technical'),
('hygiene', 'Pratiques d''hygiène et de sécurité alimentaire', 'technical'),
('soins_animaux', 'Soins vétérinaires de base et bien-être animal', 'technical'),
('sol', 'Connaissance et gestion des sols agricoles', 'technical'),
('plantes', 'Botanique et culture des végétaux', 'technical'),
('organisation', 'Planification et gestion de projet', 'soft'),
('securite', 'Sécurité au travail et prévention des risques', 'safety'),
('bois', 'Travail du bois et menuiserie', 'technical'),
('precision', 'Travail minutieux et précis', 'soft'),
('creativite', 'Créativité et innovation', 'soft'),
('patience', 'Patience et persévérance', 'soft'),
('endurance', 'Résistance physique et endurance', 'physical'),
('ecologie', 'Écologie et développement durable', 'environmental'),
('accueil', 'Accueil et service client', 'social'),
('pedagogie', 'Pédagogie et transmission de savoir', 'social'),
('expression', 'Expression orale et communication', 'social'),
('equipe', 'Travail en équipe et collaboration', 'social'),
('responsabilite', 'Sens des responsabilités', 'soft'),
('douceur', 'Douceur et délicatesse dans les gestes', 'soft'),
('rythme', 'Respect des rythmes et des temps', 'soft'),
('concentration', 'Capacité de concentration', 'soft'),
('dexterite', 'Dextérité manuelle', 'physical'),
('chimie_naturelle', 'Chimie naturelle et transformations', 'technical'),
('observation', 'Observation et analyse', 'soft'),
('memoire', 'Mémoire et mémorisation', 'soft'),
('calme', 'Calme et sérénité', 'soft'),
('respect', 'Respect de la nature et des êtres vivants', 'environmental'),
('ingenierie', 'Ingénierie et conception technique', 'technical'),
('relationnel', 'Compétences relationnelles', 'social'),
('presentation', 'Présentation et mise en valeur', 'social'),
('communication', 'Communication efficace', 'social'),
('temps', 'Gestion du temps', 'soft'),
('rigueur', 'Rigueur et méthode', 'soft'),
('contact', 'Contact client et commercial', 'social'),
('compter_simple', 'Calcul et comptage de base', 'technical');

-- Insert activities with their data
INSERT INTO activities (slug, title, category, summary, duration_min, seasonality, safety_level, materials, is_student_only) VALUES
-- Agriculture
('nourrir-soigner-moutons', 'Nourrir et soigner les moutons', 'agri', 'Gestes quotidiens : alimentation, eau, observation.', 60, '["toutes"]', 1, '["bottes", "gants"]', false),
('tonte-entretien-troupeau', 'Tonte & entretien du troupeau', 'agri', 'Hygiène, tonte (démo), soins courants.', 90, '["printemps"]', 2, '["bottes", "gants"]', false),
('basse-cour-soins', 'Soins basse-cour', 'agri', 'Poules/canards/lapins : alimentation, abris, propreté.', 60, '["toutes"]', 1, '["bottes", "gants"]', false),
('plantation-cultures', 'Plantation de cultures', 'agri', 'Semis, arrosage, paillage, suivi de plants.', 90, '["printemps", "ete"]', 1, '["gants"]', false),
('init-maraichage', 'Initiation maraîchage', 'agri', 'Plan de culture, entretien, récolte respectueuse.', 120, '["printemps", "ete", "automne"]', 1, '["gants", "bottes"]', false),
('clotures-abris', 'Gestion des clôtures & abris', 'agri', 'Identifier, réparer, sécuriser parcs et abris.', 120, '["toutes"]', 2, '["gants"]', false),

-- Transformation
('fromage', 'Fabrication de fromage', 'transfo', 'Du lait au caillé : hygiène, moulage, affinage (découverte).', 90, '["toutes"]', 2, '["tablier"]', false),
('conserves', 'Confitures & conserves', 'transfo', 'Préparation, stérilisation, mise en pot, étiquetage.', 90, '["ete", "automne"]', 1, '["tablier"]', false),
('laine', 'Transformation de la laine', 'transfo', 'Lavage, cardage, petite création textile.', 90, '["toutes"]', 1, '["tablier", "gants"]', false),
('jus', 'Fabrication de jus', 'transfo', 'Du verger à la bouteille : tri, pressage, filtration.', 90, '["automne"]', 2, '["tablier", "gants"]', false),
('aromatiques-sechage', 'Séchage d''herbes aromatiques', 'transfo', 'Cueillette, séchage, conditionnement doux.', 60, '["ete"]', 1, '["tablier"]', false),
('pain-four-bois', 'Pain au four à bois', 'transfo', 'Pétrissage, façonnage, cuisson : respect des temps.', 120, '["toutes"]', 2, '["tablier"]', false),

-- Artisanat
('poterie-argile', 'Poterie (terre locale)', 'artisanat', 'Façonnage, décoration, séchage (initiation).', 90, '["toutes"]', 1, '["tablier"]', false),
('tissage-simple', 'Tissage simple', 'artisanat', 'Métier à tisser : base, matières naturelles.', 90, '["toutes"]', 1, '[]', false),
('vannerie', 'Vannerie', 'artisanat', 'Osier, ronce : corbeilles et objets utiles.', 120, '["automne", "hiver"]', 1, '["gants"]', false),
('savon-maison', 'Fabrication de savon', 'artisanat', 'Méthode froide, plantes locales, sécurité.', 90, '["toutes"]', 3, '["gants", "lunettes"]', false),
('menuiserie-simple', 'Menuiserie simple', 'artisanat', 'Petit mobilier : mesure, découpe, assemblage.', 120, '["toutes"]', 3, '["gants", "lunettes"]', false),
('teinture-naturelle', 'Teinture naturelle', 'artisanat', 'Plantes tinctoriales : extraction, mordancage, teinture.', 120, '["ete", "automne"]', 2, '["gants", "tablier"]', false),

-- Nature
('reconnaissance-plantes', 'Reconnaissance des plantes', 'nature', 'Botanique de terrain : familles, usages, respect.', 90, '["printemps", "ete"]', 1, '[]', false),
('compost-permaculture', 'Compost & permaculture', 'nature', 'Cycles, déchets organiques, équilibre, patience.', 90, '["toutes"]', 1, '["gants"]', false),
('apiculture-decouverte', 'Apiculture (découverte)', 'nature', 'Observer, comprendre, premiers gestes (accompagné).', 90, '["printemps", "ete"]', 2, '["combinaison"]', false),
('eau-gestion', 'Gestion de l''eau', 'nature', 'Récupération, filtration, économie, irrigation.', 90, '["toutes"]', 1, '[]', false),
('graines-semences', 'Graines & semences', 'nature', 'Récolte, séchage, conservation, échange.', 60, '["automne"]', 1, '[]', false),
('foret-gestion', 'Gestion forestière', 'nature', 'Identifier, nettoyer, planter, protéger.', 120, '["automne", "hiver"]', 2, '["bottes", "gants"]', false),

-- Social
('accueil-visiteurs', 'Accueil de visiteurs', 'social', 'Présentation, tour guidé, partage d''expérience.', 60, '["toutes"]', 1, '[]', false),
('pedagogie-enfants', 'Pédagogie avec les enfants', 'social', 'Expliquer, montrer, sécuriser, s''adapter.', 90, '["toutes"]', 1, '[]', false),
('organisation-evenement', 'Organisation d''un événement', 'social', 'Planification, logistique, communication.', 180, '["toutes"]', 1, '[]', false),
('cuisine-collective', 'Cuisine collective (équipe)', 'social', 'Préparer un repas simple et bon.', 90, '["toutes"]', 1, '["tablier"]', false),
('gouter-fermier', 'Goûter fermier', 'social', 'Organisation, service, convivialité, propreté.', 60, '["toutes"]', 1, '["tablier"]', false),
('marche-local', 'Participation à un marché local', 'social', 'Stand, présentation, caisse symbolique (simulation).', 180, '["toutes"]', 1, '[]', false);

-- Associate skills with activities
-- This is a simplified mapping - in reality you'd want to map each activity to its specific skills
INSERT INTO activity_skills (activity_id, skill_id) 
SELECT a.id, s.id 
FROM activities a, skills s 
WHERE 
    (a.slug = 'nourrir-soigner-moutons' AND s.name IN ('elevage', 'responsabilite')) OR
    (a.slug = 'tonte-entretien-troupeau' AND s.name IN ('elevage', 'hygiene')) OR
    (a.slug = 'basse-cour-soins' AND s.name IN ('soins_animaux')) OR
    (a.slug = 'plantation-cultures' AND s.name IN ('sol', 'plantes')) OR
    (a.slug = 'init-maraichage' AND s.name IN ('sol', 'organisation')) OR
    (a.slug = 'clotures-abris' AND s.name IN ('securite', 'bois')) OR
    (a.slug = 'fromage' AND s.name IN ('hygiene', 'precision')) OR
    (a.slug = 'conserves' AND s.name IN ('organisation', 'hygiene')) OR
    (a.slug = 'laine' AND s.name IN ('patience', 'creativite')) OR
    (a.slug = 'jus' AND s.name IN ('hygiene', 'securite')) OR
    (a.slug = 'aromatiques-sechage' AND s.name IN ('douceur', 'organisation')) OR
    (a.slug = 'pain-four-bois' AND s.name IN ('precision', 'rythme')) OR
    (a.slug = 'poterie-argile' AND s.name IN ('creativite', 'precision')) OR
    (a.slug = 'tissage-simple' AND s.name IN ('patience', 'concentration')) OR
    (a.slug = 'vannerie' AND s.name IN ('dexterite', 'patience')) OR
    (a.slug = 'savon-maison' AND s.name IN ('precision', 'securite')) OR
    (a.slug = 'menuiserie-simple' AND s.name IN ('precision', 'securite')) OR
    (a.slug = 'teinture-naturelle' AND s.name IN ('chimie_naturelle', 'patience')) OR
    (a.slug = 'reconnaissance-plantes' AND s.name IN ('observation', 'memoire')) OR
    (a.slug = 'compost-permaculture' AND s.name IN ('ecologie', 'observation')) OR
    (a.slug = 'apiculture-decouverte' AND s.name IN ('calme', 'respect')) OR
    (a.slug = 'eau-gestion' AND s.name IN ('ecologie', 'ingenierie')) OR
    (a.slug = 'graines-semences' AND s.name IN ('organisation', 'precision')) OR
    (a.slug = 'foret-gestion' AND s.name IN ('endurance', 'observation')) OR
    (a.slug = 'accueil-visiteurs' AND s.name IN ('relationnel', 'presentation')) OR
    (a.slug = 'pedagogie-enfants' AND s.name IN ('pedagogie', 'patience')) OR
    (a.slug = 'organisation-evenement' AND s.name IN ('organisation', 'communication')) OR
    (a.slug = 'cuisine-collective' AND s.name IN ('hygiene', 'equipe', 'temps')) OR
    (a.slug = 'gouter-fermier' AND s.name IN ('rigueur', 'relationnel')) OR
    (a.slug = 'marche-local' AND s.name IN ('contact', 'compter_simple', 'equipe'));

-- Create a demo user (password: "demo123")
-- Note: In production, this should be done through the API with proper password hashing
INSERT INTO users (email, hashed_password, full_name, location, is_student, availability, preferences) VALUES
('demo@lavidaluca.fr', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LQv3c1yqBWVHxkd0LH', 'Utilisateur Démo', 'Région Centre', false, '["weekend", "vacances"]', '["agri", "nature"]');

-- Add some skills to the demo user
INSERT INTO user_skills (user_id, skill_id)
SELECT u.id, s.id 
FROM users u, skills s 
WHERE u.email = 'demo@lavidaluca.fr' 
AND s.name IN ('elevage', 'organisation', 'patience', 'observation');

-- Create a demo student user
INSERT INTO users (email, hashed_password, full_name, location, is_student, availability, preferences) VALUES
('etudiant@mfr.fr', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LQv3c1yqBWVHxkd0LH', 'Étudiant MFR', 'MFR de Bretagne', true, '["semaine", "weekend"]', '["agri", "transfo", "social"]');

-- Add skills to the student user
INSERT INTO user_skills (user_id, skill_id)
SELECT u.id, s.id 
FROM users u, skills s 
WHERE u.email = 'etudiant@mfr.fr' 
AND s.name IN ('hygiene', 'sol', 'plantes', 'equipe', 'pedagogie');