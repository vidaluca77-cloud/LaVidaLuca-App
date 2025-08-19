-- Seed data for La Vida Luca
-- This file populates the database with initial activities and sample data

-- Insert sample activities based on the catalog from the application
INSERT INTO public.activities (slug, title, category, summary, description, duration_min, skill_tags, seasonality, safety_level, materials, max_participants, min_age) VALUES

-- Agriculture activities
('nourrissage-moutons', 'Nourrissage des moutons', 'agri', 'Foin, granulés, eau : apprendre les besoins nutritionnels.', 'Activité d''introduction aux soins des animaux de ferme. Les participants apprennent à identifier les besoins nutritionnels des moutons selon les saisons et à distribuer la nourriture de manière appropriée.', 45, ARRAY['soin_animaux'], ARRAY['toutes'], 1, ARRAY['bottes', 'gants'], 8, 14),

('tonte-entretien-troupeau', 'Tonte & entretien du troupeau', 'agri', 'Hygiène, tonte (démo), soins courants.', 'Activité de démonstration de la tonte des moutons et apprentissage des soins d''hygiène du troupeau. Comprend l''observation des techniques et la participation aux soins de base.', 90, ARRAY['elevage', 'hygiene'], ARRAY['printemps'], 2, ARRAY['bottes', 'gants'], 6, 16),

('basse-cour-soins', 'Soins basse-cour', 'agri', 'Poules/canards/lapins : alimentation, abris, propreté.', 'Apprentissage des soins quotidiens des animaux de basse-cour. Nettoyage des espaces, alimentation adaptée et observation du comportement animal.', 60, ARRAY['soins_animaux'], ARRAY['toutes'], 1, ARRAY['bottes', 'gants'], 10, 14),

('plantation-cultures', 'Plantation de cultures', 'agri', 'Semis, arrosage, paillage, suivi de plants.', 'Initiation aux techniques de plantation et de culture. Préparation du sol, semis, techniques d''arrosage et mise en place du paillage.', 90, ARRAY['sol', 'plantes'], ARRAY['printemps', 'ete'], 1, ARRAY['gants'], 12, 14),

('init-maraichage', 'Initiation maraîchage', 'agri', 'Plan de culture, entretien, récolte respectueuse.', 'Formation complète aux bases du maraîchage. Planification des cultures, techniques d''entretien et méthodes de récolte respectueuses de l''environnement.', 120, ARRAY['sol', 'organisation'], ARRAY['printemps', 'ete', 'automne'], 1, ARRAY['gants', 'bottes'], 8, 16),

('clotures-abris', 'Gestion des clôtures & abris', 'agri', 'Identifier, réparer, sécuriser parcs et abris.', 'Maintenance et sécurisation des installations agricoles. Inspection, réparation et amélioration des clôtures et abris pour animaux.', 120, ARRAY['securite', 'bois'], ARRAY['toutes'], 2, ARRAY['gants'], 6, 16),

-- Transformation activities
('fromage', 'Fabrication de fromage', 'transfo', 'Du lait au caillé : hygiène, moulage, affinage (découverte).', 'Découverte des techniques traditionnelles de fabrication fromagère. Respect des règles d''hygiène, processus de transformation et initiation à l''affinage.', 90, ARRAY['hygiene', 'precision'], ARRAY['toutes'], 2, ARRAY['tablier'], 6, 16),

('conserves', 'Confitures & conserves', 'transfo', 'Préparation, stérilisation, mise en pot, étiquetage.', 'Apprentissage des techniques de conservation alimentaire. Préparation des fruits, stérilisation, conditionnement et étiquetage selon les normes.', 90, ARRAY['organisation', 'hygiene'], ARRAY['ete', 'automne'], 1, ARRAY['tablier'], 8, 14),

('laine', 'Transformation de la laine', 'transfo', 'Lavage, cardage, petite création textile.', 'Découverte de la filière laine depuis la tonte jusqu''au produit fini. Techniques de lavage, cardage et réalisation de petites créations textiles.', 90, ARRAY['patience', 'creativite'], ARRAY['toutes'], 1, ARRAY['tablier', 'gants'], 8, 14),

-- Artisanat activities
('menuiserie-base', 'Menuiserie de base', 'artisanat', 'Mesurer, scier, poncer, assembler simple.', 'Initiation aux techniques de base de la menuiserie. Utilisation des outils de mesure, techniques de découpe et assemblage de pièces simples.', 120, ARRAY['precision', 'securite'], ARRAY['toutes'], 2, ARRAY['gants', 'lunettes'], 6, 16),

('reparation-outils', 'Réparation d''outils', 'artisanat', 'Entretenir, réparer, affûter outils agricoles.', 'Maintenance et réparation des outils agricoles. Techniques d''affûtage, réparation des manches et entretien préventif.', 90, ARRAY['mecanique', 'precision'], ARRAY['toutes'], 2, ARRAY['gants'], 8, 16),

-- Nature activities
('entretien-riviere', 'Entretien de la rivière', 'nature', 'Nettoyage doux, observation des berges.', 'Activité de préservation de l''environnement aquatique. Nettoyage respectueux des berges et observation de la biodiversité.', 90, ARRAY['prudence', 'ecologie'], ARRAY['printemps', 'ete'], 2, ARRAY['bottes', 'gants'], 10, 14),

('plantations-haies', 'Plantations de haies', 'nature', 'Biodiversité locale, plantation, arrosage.', 'Création et entretien de haies bocagères. Sélection d''essences locales, techniques de plantation et suivi de croissance.', 120, ARRAY['ecologie', 'endurance'], ARRAY['automne', 'hiver'], 1, ARRAY['gants', 'bottes'], 10, 14),

-- Social activities
('accueil-visiteurs', 'Accueil de visiteurs', 'social', 'Présenter le lieu, expliquer le projet.', 'Formation à l''accueil et à la communication. Présentation du projet La Vida Luca et animation de visites pédagogiques.', 60, ARRAY['communication', 'pedagogie'], ARRAY['toutes'], 1, ARRAY[], 12, 16),

('organisation-evenements', 'Organisation d''événements', 'social', 'Planifier, coordonner fêtes ou marchés.', 'Apprentissage de l''organisation d''événements agricoles et pédagogiques. Planification, coordination et animation d''activités collectives.', 120, ARRAY['organisation', 'communication'], ARRAY['toutes'], 1, ARRAY[], 8, 16);

-- Insert sample locations
INSERT INTO public.locations (name, address, description, contact_person, contact_email, contact_phone, is_active) VALUES
('Ferme pédagogique La Vida Luca - Site principal', '1 Chemin des Champs, 12345 Campagne-sur-Mer', 'Site principal du projet La Vida Luca, dédié à la formation des jeunes en MFR et au développement d''une agriculture nouvelle.', 'Jean Dupont', 'contact@lavidaluca.fr', '+33 1 23 45 67 89', true),

('Annexe La Vida Luca - Maraîchage', '5 Route des Jardins, 12346 Terre-Verte', 'Site spécialisé dans les activités de maraîchage et de transformation végétale.', 'Marie Martin', 'maraichage@lavidaluca.fr', '+33 1 23 45 67 90', true),

('Atelier La Vida Luca - Artisanat', '10 Rue de l''Artisan, 12347 Bois-Joli', 'Espace dédié aux activités d''artisanat et de menuiserie traditionnelle.', 'Pierre Bois', 'artisanat@lavidaluca.fr', '+33 1 23 45 67 91', true);

-- Insert sample activity sessions (upcoming sessions)
INSERT INTO public.activity_sessions (activity_id, scheduled_date, scheduled_time, max_participants, location, notes) VALUES
((SELECT id FROM public.activities WHERE slug = 'nourrissage-moutons'), CURRENT_DATE + INTERVAL '7 days', '09:00:00', 8, 'Ferme principale - Bergerie', 'Session d''introduction pour nouveaux élèves'),
((SELECT id FROM public.activities WHERE slug = 'plantation-cultures'), CURRENT_DATE + INTERVAL '10 days', '14:00:00', 12, 'Annexe maraîchage - Serres', 'Plantation de légumes de saison'),
((SELECT id FROM public.activities WHERE slug = 'fromage'), CURRENT_DATE + INTERVAL '14 days', '10:00:00', 6, 'Ferme principale - Fromagerie', 'Fabrication de fromage de chèvre'),
((SELECT id FROM public.activities WHERE slug = 'menuiserie-base'), CURRENT_DATE + INTERVAL '21 days', '13:30:00', 6, 'Atelier artisanat - Menuiserie', 'Construction de nichoirs');

-- Note: User profiles and bookings will be created when users register and interact with the system
-- This is just the initial data structure and sample activities