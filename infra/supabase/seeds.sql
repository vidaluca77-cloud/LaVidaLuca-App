-- Initial seed data for La Vida Luca application

-- Insert sample activities from the application
INSERT INTO activities (id, title, slug, description, category, duration_min, skill_tags, seasonality, safety_level, materials) VALUES
('e8f7e3b0-8f5e-4a8e-9c3e-1f2d3e4f5678', 'Soins aux animaux (base)', 'soins-animaux-base', 'Observation, approche, gestes de base pour poules, lapins, chèvres.', 'agri', 60, '{"elevage", "hygiene", "soins_animaux"}', '{"toutes"}', 1, '{"gants"}'),
('f9e8d7c6-9f6e-5b9e-0d4e-2f3d4e5f6789', 'Nettoyage des espaces animaux', 'nettoyage-espaces-animaux', 'Litière, abreuvoirs, mangeoires : hygiène et bien-être.', 'agri', 90, '{"hygiene", "endurance", "soins_animaux"}', '{"toutes"}', 1, '{"gants", "bottes"}'),
('a1b2c3d4-af7e-6c0e-1e5e-3f4d5e6f7890', 'Alimentation des animaux', 'alimentation-animaux', 'Préparation et distribution équilibrée selon espèces.', 'agri', 60, '{"soins_animaux", "precision", "organisation"}', '{"toutes"}', 1, '{"gants"}'),
('b2c3d4e5-bf8e-7d1e-2f6e-4f5d6e7f8901', 'Plantation de cultures', 'plantation-cultures', 'Semis, arrosage, paillage, suivi de plants.', 'agri', 90, '{"sol", "plantes"}', '{"printemps", "ete"}', 1, '{"gants"}'),
('c3d4e5f6-cf9e-8e2e-3f7e-5f6d7e8f9012', 'Initiation maraîchage', 'init-maraichage', 'Plan de culture, entretien, récolte respectueuse.', 'agri', 120, '{"sol", "organisation"}', '{"printemps", "ete", "automne"}', 1, '{"gants", "bottes"}'),
('d4e5f6g7-dfae-9f3e-4f8e-6f7d8e9f0123', 'Gestion des clôtures & abris', 'clotures-abris', 'Identifier, réparer, sécuriser parcs et abris.', 'agri', 120, '{"securite", "bois"}', '{"toutes"}', 2, '{"gants"}'),

-- Transformation
('e5f6g7h8-efbe-af4e-5f9e-7f8d9e0f1234', 'Fabrication de fromage', 'fromage', 'Du lait au caillé : hygiène, moulage, affinage (découverte).', 'transfo', 90, '{"hygiene", "precision"}', '{"toutes"}', 2, '{"tablier"}'),
('f6g7h8i9-fgce-bf5e-6fae-8f9d0e1f2345', 'Confitures & conserves', 'conserves', 'Préparation, stérilisation, mise en pot, étiquetage.', 'transfo', 90, '{"organisation", "hygiene"}', '{"ete", "automne"}', 1, '{"tablier"}'),
('g7h8i9j0-ghde-cf6e-7fbe-9f0d1e2f3456', 'Transformation de la laine', 'laine', 'Lavage, cardage, petite création textile.', 'transfo', 90, '{"patience", "creativite"}', '{"toutes"}', 1, '{"tablier", "gants"}'),
('h8i9j0k1-hiee-df7e-8fce-0f1d2e3f4567', 'Fabrication de jus', 'jus', 'Du verger à la bouteille : tri, pressage, filtration.', 'transfo', 90, '{"hygiene", "securite"}', '{"automne"}', 2, '{"tablier", "gants"}'),

-- Artisanat
('i9j0k1l2-ijfe-ef8e-9fde-1f2d3e4f5678', 'Construction d''abris', 'abris-bois', 'Petites structures bois : plan, coupe, assemblage.', 'artisanat', 120, '{"bois", "precision", "securite"}', '{"toutes"}', 2, '{"gants"}'),
('j0k1l2m3-jkge-ff9e-afee-2f3d4e5f6789', 'Vannerie simple', 'vannerie', 'Osier, rotin : corbeilles et objets utiles.', 'artisanat', 90, '{"patience", "creativite", "precision"}', '{"toutes"}', 1, '{}'),
('k1l2m3n4-klhe-gfae-bffe-3f4d5e6f7890', 'Couture & réparation textile', 'couture-textile', 'Repriser, coudre, créer : savoir-faire durable.', 'artisanat', 90, '{"patience", "precision", "creativite"}', '{"toutes"}', 1, '{}'),

-- Nature
('l2m3n4o5-lmie-hfbe-cffe-4f5d6e7f8901', 'Jardinage écologique', 'jardinage-ecologique', 'Compost, rotation, associations : équilibre naturel.', 'nature', 120, '{"ecologie", "sol", "plantes"}', '{"printemps", "ete", "automne"}', 1, '{"gants", "bottes"}'),
('m3n4o5p6-mnje-ifce-dffe-5f6d7e8f9012', 'Compostage', 'compostage', 'Tri, compost, valorisation des déchets verts.', 'nature', 60, '{"geste_utile", "hygiene"}', '{"toutes"}', 1, '{"gants"}'),
('n4o5p6q7-noke-jfde-effe-6f7d8e9f0123', 'Observation de la faune locale', 'faune-locale', 'Discrétion, repérage, traces/indices.', 'nature', 60, '{"patience", "respect"}', '{"toutes"}', 1, '{}'),

-- Social  
('o5p6q7r8-ople-kfee-fffe-7f8d9e0f1234', 'Accueil et orientation', 'accueil-orientation', 'Recevoir visiteurs, expliquer, accompagner.', 'social', 60, '{"accueil", "pedagogie", "expression"}', '{"toutes"}', 1, '{}'),
('p6q7r8s9-pqme-lffe-gffe-8f9d0e1f2345', 'Cuisine collective (équipe)', 'cuisine-collective', 'Préparer un repas simple et bon.', 'social', 90, '{"hygiene", "equipe", "temps"}', '{"toutes"}', 1, '{"tablier"}'),
('q7r8s9t0-qrne-mffe-hffe-9f0d1e2f3456', 'Goûter fermier', 'gouter-fermier', 'Organisation, service, convivialité, propreté.', 'social', 60, '{"rigueur", "relationnel"}', '{"toutes"}', 1, '{"tablier"}'),
('r8s9t0u1-rsoe-nffe-iffe-0f1d2e3f4567', 'Animation nature pour enfants', 'animation-nature-enfants', 'Jeux, découverte, éveil à la nature.', 'social', 90, '{"pedagogie", "expression", "patience"}', '{"toutes"}', 1, '{}');

-- Insert sample locations
INSERT INTO locations (id, name, address, city, department, region, contact_person, contact_email, description, facilities, capacity, active) VALUES
('loc1-1234-5678-9abc-def123456789', 'MFR de Caen - Site Principal', '12 Route de la Ferme', 'Caen', '14', 'Normandie', 'Jean Dupont', 'contact@mfr-caen.fr', 'Site principal avec ferme pédagogique, ateliers et salles de cours.', '{"ferme", "ateliers", "salles_cours", "cantine"}', 50, true),
('loc2-2345-6789-0bcd-ef123456789a', 'Ferme Partenaire - Les Chênes', '45 Chemin des Chênes', 'Bayeux', '14', 'Normandie', 'Marie Martin', 'contact@ferme-chenes.fr', 'Ferme partenaire spécialisée en élevage et transformation laitière.', '{"ferme", "fromagerie", "etable"}', 20, true),
('loc3-3456-7890-1cde-f123456789ab', 'Atelier Artisanal - Bois & Nature', '8 Rue de l''Artisanat', 'Vire', '14', 'Normandie', 'Pierre Leroy', 'contact@bois-nature.fr', 'Atelier spécialisé dans le travail du bois et l''artisanat traditionnel.', '{"atelier_bois", "outils", "materiel"}', 15, true);

-- Insert a default admin user (will be created when someone signs up with this email)
INSERT INTO users (id, email, full_name, role, skills, availability, location, preferences) VALUES
('admin-1234-5678-9abc-def123456789', 'admin@la-vida-luca.com', 'Administrateur La Vida Luca', 'admin', '{"administration", "pedagogie", "gestion"}', '{"semaine", "weekend"}', 'Caen, Calvados', '{"toutes_categories"}');

-- Insert sample activity sessions
INSERT INTO activity_sessions (id, activity_id, location_id, instructor_id, title, description, start_time, end_time, max_participants, status) VALUES
('sess1-1234-5678-9abc-def123456789', 'e8f7e3b0-8f5e-4a8e-9c3e-1f2d3e4f5678', 'loc1-1234-5678-9abc-def123456789', 'admin-1234-5678-9abc-def123456789', 'Atelier Soins aux Animaux - Initiation', 'Découverte des gestes de base pour prendre soin des animaux de la ferme.', '2024-09-15 09:00:00+02', '2024-09-15 10:00:00+02', 8, 'scheduled'),
('sess2-2345-6789-0bcd-ef123456789a', 'c3d4e5f6-cf9e-8e2e-3f7e-5f6d7e8f9012', 'loc1-1234-5678-9abc-def123456789', 'admin-1234-5678-9abc-def123456789', 'Formation Maraîchage Bio', 'Apprentissage des techniques de maraîchage biologique et durable.', '2024-09-20 14:00:00+02', '2024-09-20 16:00:00+02', 12, 'scheduled'),
('sess3-3456-7890-1cde-f123456789ab', 'e5f6g7h8-efbe-af4e-5f9e-7f8d9e0f1234', 'loc2-2345-6789-0bcd-ef123456789a', 'admin-1234-5678-9abc-def123456789', 'Atelier Fabrication de Fromage', 'Découverte de la transformation du lait en fromage traditionnel.', '2024-09-25 10:00:00+02', '2024-09-25 11:30:00+02', 6, 'scheduled');