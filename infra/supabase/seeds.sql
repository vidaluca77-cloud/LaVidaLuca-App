-- Seeds pour la base de données La Vida Luca
-- Données initiales pour tester et démarrer l'application

-- Insertion des activités du catalogue MFR
INSERT INTO activities (id, slug, title, category, summary, duration_min, skill_tags, seasonality, safety_level, materials) VALUES
-- Agriculture
('1', 'nourrir-animaux', 'Nourrir les animaux', 'agri', 'Distribution alimentation, vérifier abreuvoirs, observer comportements.', 60, '["observation", "douceur"]', '["toutes"]', 1, '["bottes"]'),
('2', 'collecte-oeufs', 'Collecte des œufs', 'agri', 'Ramasser délicatement, nettoyer si besoin, stockage correct.', 30, '["douceur", "organisation"]', '["toutes"]', 1, '[]'),
('3', 'entretien-jardins', 'Entretien des jardins', 'agri', 'Désherbage doux, binage, arrosage selon météo et saison.', 90, '["sol", "endurance"]', '["printemps", "ete"]', 1, '["gants", "bottes"]'),
('4', 'plantation-cultures', 'Plantation de cultures', 'agri', 'Semis, arrosage, paillage, suivi de plants.', 90, '["sol", "plantes"]', '["printemps", "ete"]', 1, '["gants"]'),
('5', 'init-maraichage', 'Initiation maraîchage', 'agri', 'Plan de culture, entretien, récolte respectueuse.', 120, '["sol", "organisation"]', '["printemps", "ete", "automne"]', 1, '["gants", "bottes"]'),

-- Transformation
('7', 'fromage', 'Fabrication de fromage', 'transfo', 'Du lait au caillé : hygiène, moulage, affinage (découverte).', 90, '["hygiene", "precision"]', '["toutes"]', 2, '["tablier"]'),
('8', 'conserves', 'Confitures & conserves', 'transfo', 'Préparation, stérilisation, mise en pot, étiquetage.', 90, '["organisation", "hygiene"]', '["ete", "automne"]', 1, '["tablier"]'),
('9', 'laine', 'Transformation de la laine', 'transfo', 'Lavage, cardage, petite création textile.', 90, '["patience", "creativite"]', '["toutes"]', 1, '["tablier", "gants"]'),

-- Artisanat
('13', 'abris-bois', 'Construction d''abris', 'artisanat', 'Petites structures bois : plan, coupe, assemblage.', 120, '["bois", "precision", "securite"]', '["toutes"]', 2, '["gants"]'),
('14', 'clotures', 'Réparation de clôtures', 'artisanat', 'Identifier défauts, remplacer piquets, retendre fils.', 90, '["bois", "securite"]', '["toutes"]', 2, '["gants"]'),
('15', 'poterie', 'Initiation poterie', 'artisanat', 'Modelage terre, techniques de base, décoration simple.', 90, '["creativite", "patience"]', '["toutes"]', 1, '["tablier"]'),

-- Social
('29', 'accueil-visiteurs', 'Accueil de visiteurs', 'social', 'Présentation lieu, accompagnement, réponse aux questions.', 120, '["contact", "pedagogie"]', '["toutes"]', 1, '[]'),
('30', 'marche-local', 'Participation à un marché local', 'social', 'Stand, présentation, caisse symbolique (simulation).', 180, '["contact", "compter_simple", "equipe"]', '["toutes"]', 1, '[]');

-- Insertion des lieux d'action
INSERT INTO action_sites (name, description, address, city, department, contact_info, active) VALUES
('Ferme pédagogique de Caen', 'Site principal du projet La Vida Luca avec activités complètes', '123 Route de la Ferme', 'Caen', 'Calvados (14)', '{"email": "caen@lavidaluca.fr", "phone": "02.31.XX.XX.XX"}', true),
('Jardin partagé de Bayeux', 'Espace de maraîchage et transformation artisanale', '45 Rue du Jardin', 'Bayeux', 'Calvados (14)', '{"email": "bayeux@lavidaluca.fr"}', true),
('Atelier rural de Vire', 'Focus artisanat et construction durable', '67 Avenue Rurale', 'Vire', 'Calvados (14)', '{"email": "vire@lavidaluca.fr"}', true);

-- Insertion d'exemples de profils utilisateurs pour les tests
INSERT INTO user_profiles (user_id, skills, availability, location, preferences) VALUES
('test_user_1', '["observation", "douceur", "organisation"]', '["toutes"]', 'Calvados', '["agri", "social"]'),
('test_user_2', '["bois", "securite", "precision"]', '["printemps", "ete"]', 'Normandie', '["artisanat"]'),
('test_user_3', '["hygiene", "creativite", "patience"]', '["automne", "hiver"]', 'Caen', '["transfo", "artisanat"]');

-- Insertion d'exemples d'articles pour le blog/actualités
INSERT INTO articles (title, slug, content, excerpt, author, published, published_at) VALUES
('Lancement du projet La Vida Luca', 'lancement-projet', 'Le projet La Vida Luca démarre avec l''objectif de créer un réseau de fermes pédagogiques...', 'Découvrez les objectifs et la vision du projet La Vida Luca', 'Équipe La Vida Luca', true, NOW()),
('Première session de formation en maraîchage', 'premiere-formation-maraichage', 'Retour sur la première session de formation qui s''est déroulée...', 'Retour d''expérience sur notre première formation', 'Jean Dupont', true, NOW() - INTERVAL '1 week'),
('Partenariat avec les MFR normandes', 'partenariat-mfr', 'Nous sommes fiers d''annoncer notre partenariat avec plusieurs MFR...', 'Nouveau partenariat pour étendre notre impact', 'Marie Martin', false, NULL);