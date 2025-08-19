-- Seed data for LaVidaLuca database
-- Run this after schema.sql to populate with initial data

-- Insert the 30 activities from the frontend
INSERT INTO activities (id, slug, title, category, summary, duration_min, skill_tags, seasonality, safety_level, materials) VALUES
-- Agriculture
(1, 'nourrir-soigner-moutons', 'Nourrir et soigner les moutons', 'agri', 'Gestes quotidiens : alimentation, eau, observation.', 60, ARRAY['elevage', 'responsabilite'], ARRAY['toutes'], 1, ARRAY['bottes', 'gants']),
(2, 'tonte-entretien-troupeau', 'Tonte & entretien du troupeau', 'agri', 'Hygiène, tonte (démo), soins courants.', 90, ARRAY['elevage', 'hygiene'], ARRAY['printemps'], 2, ARRAY['bottes', 'gants']),
(3, 'basse-cour-soins', 'Soins basse-cour', 'agri', 'Poules/canards/lapins : alimentation, abris, propreté.', 60, ARRAY['soins_animaux'], ARRAY['toutes'], 1, ARRAY['bottes', 'gants']),
(4, 'plantation-cultures', 'Plantation de cultures', 'agri', 'Semis, arrosage, paillage, suivi de plants.', 90, ARRAY['sol', 'plantes'], ARRAY['printemps', 'ete'], 1, ARRAY['gants']),
(5, 'init-maraichage', 'Initiation maraîchage', 'agri', 'Plan de culture, entretien, récolte respectueuse.', 120, ARRAY['sol', 'organisation'], ARRAY['printemps', 'ete', 'automne'], 1, ARRAY['gants', 'bottes']),
(6, 'clotures-abris', 'Gestion des clôtures & abris', 'agri', 'Identifier, réparer, sécuriser parcs et abris.', 120, ARRAY['securite', 'bois'], ARRAY['toutes'], 2, ARRAY['gants']),

-- Transformation
(7, 'fromage', 'Fabrication de fromage', 'transfo', 'Du lait au caillé : hygiène, moulage, affinage (découverte).', 90, ARRAY['hygiene', 'precision'], ARRAY['toutes'], 2, ARRAY['tablier']),
(8, 'conserves', 'Confitures & conserves', 'transfo', 'Préparation, stérilisation, mise en pot, étiquetage.', 90, ARRAY['organisation', 'hygiene'], ARRAY['ete', 'automne'], 1, ARRAY['tablier']),
(9, 'laine', 'Transformation de la laine', 'transfo', 'Lavage, cardage, petite création textile.', 90, ARRAY['patience', 'creativite'], ARRAY['toutes'], 1, ARRAY['tablier', 'gants']),
(10, 'jus', 'Fabrication de jus', 'transfo', 'Du verger à la bouteille : tri, pressage, filtration.', 90, ARRAY['hygiene', 'securite'], ARRAY['automne'], 2, ARRAY['tablier', 'gants']),
(11, 'aromatiques-sechage', 'Séchage d''herbes aromatiques', 'transfo', 'Cueillette, séchage, conditionnement doux.', 60, ARRAY['douceur', 'organisation'], ARRAY['ete'], 1, ARRAY['tablier']),
(12, 'pain-four-bois', 'Pain au four à bois', 'transfo', 'Pétrissage, façonnage, cuisson : respect des temps.', 120, ARRAY['precision', 'rythme'], ARRAY['toutes'], 2, ARRAY['tablier']),

-- Artisanat
(13, 'construction-simple', 'Construction simple', 'artisanat', 'Assemblage, vissage, mesures : réaliser un petit ouvrage.', 120, ARRAY['precision', 'bois'], ARRAY['toutes'], 2, ARRAY['gants', 'lunettes']),
(14, 'reparation-outils', 'Réparation & entretien des outils', 'artisanat', 'Affûtage, graissage, petites réparations.', 60, ARRAY['autonomie', 'responsabilite'], ARRAY['toutes'], 1, ARRAY['gants']),
(15, 'menuiserie-simple', 'Menuiserie simple', 'artisanat', 'Mesure, coupe, ponçage, finitions d''un objet.', 120, ARRAY['precision', 'creativite'], ARRAY['toutes'], 2, ARRAY['gants', 'lunettes']),
(16, 'vannerie', 'Vannerie', 'artisanat', 'Tressage d''osier : panier, corbeille, objet décoratif.', 90, ARRAY['patience', 'creativite'], ARRAY['automne', 'hiver'], 1, ARRAY[]::TEXT[]),
(17, 'couture', 'Couture & retouches', 'artisanat', 'Réparer, adapter, créer de petits objets textiles.', 90, ARRAY['precision', 'creativite'], ARRAY['toutes'], 1, ARRAY[]::TEXT[]),
(18, 'poterie', 'Poterie artisanale', 'artisanat', 'Modelage terre : bol, vase, objets utilitaires simples.', 120, ARRAY['creativite', 'patience'], ARRAY['toutes'], 1, ARRAY['tablier']),

-- Nature/Environnement
(19, 'plantation-arbres', 'Plantation d''arbres', 'nature', 'Choix emplacement, creusage, mise en terre, arrosage.', 90, ARRAY['ecologie', 'endurance'], ARRAY['automne', 'printemps'], 1, ARRAY['gants', 'bottes']),
(20, 'compostage', 'Compostage & recyclage', 'nature', 'Tri, mélange, surveillance du compost collectif.', 60, ARRAY['ecologie', 'organisation'], ARRAY['toutes'], 1, ARRAY['gants']),
(21, 'observation-nature', 'Observation de la nature', 'nature', 'Reconnaissance faune/flore, carnet de bord, respect.', 90, ARRAY['curiosite', 'respect'], ARRAY['toutes'], 1, ARRAY[]::TEXT[]),
(22, 'entretien-espaces-verts', 'Entretien des espaces verts', 'nature', 'Taille, désherbage doux, embellissement.', 120, ARRAY['organisation', 'endurance'], ARRAY['printemps', 'ete', 'automne'], 1, ARRAY['gants', 'bottes']),
(23, 'ruche-observation', 'Observation de la ruche', 'nature', 'Découverte apiculture : observer, comprendre (encadré).', 60, ARRAY['respect', 'curiosite'], ARRAY['printemps', 'ete'], 2, ARRAY['combinaison']),
(24, 'gestion-dechets', 'Gestion éco-responsable des déchets', 'nature', 'Tri, valorisation, sensibilisation environnementale.', 60, ARRAY['ecologie', 'responsabilite'], ARRAY['toutes'], 1, ARRAY['gants']),

-- Social/Animation
(25, 'accueil-visiteurs', 'Accueil des visiteurs', 'social', 'Présentation lieu, écoute, orientation simple.', 60, ARRAY['accueil', 'expression'], ARRAY['toutes'], 1, ARRAY[]::TEXT[]),
(26, 'visites-guidees', 'Visites guidées de la ferme', 'social', 'Présenter la ferme, répondre simplement.', 60, ARRAY['expression', 'pedagogie'], ARRAY['toutes'], 1, ARRAY[]::TEXT[]),
(27, 'ateliers-enfants', 'Ateliers pour enfants', 'social', 'Jeux, découvertes nature, mini-gestes encadrés.', 90, ARRAY['patience', 'creativite', 'securite'], ARRAY['toutes'], 2, ARRAY[]::TEXT[]),
(28, 'communication-reseaux', 'Communication & réseaux', 'social', 'Photos, témoignages, petites vidéos valorisantes.', 90, ARRAY['expression', 'creativite'], ARRAY['toutes'], 1, ARRAY[]::TEXT[]),
(29, 'organisation-evenements', 'Organisation d''événements', 'social', 'Préparation, logistique, accueil lors de manifestations.', 180, ARRAY['organisation', 'equipe'], ARRAY['toutes'], 1, ARRAY[]::TEXT[]),
(30, 'marche-local', 'Participation à un marché local', 'social', 'Stand, présentation, caisse symbolique (simulation).', 180, ARRAY['contact', 'compter_simple', 'equipe'], ARRAY['toutes'], 1, ARRAY[]::TEXT[]);

-- Reset sequence to match the inserted IDs
SELECT setval('activities_id_seq', 30, true);

-- Insert sample users (for testing - remove in production)
INSERT INTO users (username, email, hashed_password, full_name, is_mfr_student, skills, availability, preferences) VALUES
('demo_student', 'student@mfr.example', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFCLl1MQjSWpNoi', 'Élève MFR Demo', true, ARRAY['elevage', 'sol', 'creativite'], ARRAY['weekend', 'matin'], ARRAY['agri', 'nature']),
('demo_admin', 'admin@lavidaluca.example', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFCLl1MQjSWpNoi', 'Administrateur Demo', false, ARRAY['organisation', 'pedagogie', 'expression'], ARRAY['semaine', 'matin', 'apres-midi'], ARRAY['social', 'transfo']);

-- Note: The hashed password above is for "demopassword123" - DO NOT use in production!

-- Insert some sample bookings (for testing)
INSERT INTO bookings (user_id, activity_id, scheduled_date, status, notes) VALUES
(1, 1, NOW() + INTERVAL '1 day', 'confirmed', 'Première activité avec les moutons'),
(1, 4, NOW() + INTERVAL '3 days', 'pending', 'Plantation de légumes de saison'),
(2, 25, NOW() + INTERVAL '1 week', 'confirmed', 'Formation accueil des visiteurs');

-- Insert sample analytics events
INSERT INTO analytics_events (user_id, event_type, event_data) VALUES
(1, 'page_view', '{"page": "activities", "category": "agri"}'),
(1, 'activity_view', '{"activity_id": 1, "activity_slug": "nourrir-soigner-moutons"}'),
(2, 'booking_created', '{"activity_id": 25, "scheduled_date": "2024-01-15T10:00:00Z"}');