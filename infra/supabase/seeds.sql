-- Données de test pour La Vida Luca
-- Seeds pour développement et tests

-- Insérer des lieux d'action
INSERT INTO locations (id, name, address, coordinates, department, region, type, contact_email, contact_phone, description, facilities) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'MFR de Calvados', '123 Route de la Ferme, 14000 Caen', ST_GeogFromText('POINT(-0.3781 49.1829)'), '14', 'Normandie', 'mfr', 'contact@mfr-calvados.fr', '02.31.00.00.00', 'Maison Familiale Rurale du Calvados spécialisée dans l''agriculture durable', '["salle_de_classe", "atelier", "ferme_pedagogique", "hebergement"]'),
('550e8400-e29b-41d4-a716-446655440002', 'Ferme La Vida Luca', '456 Chemin des Champs, 14200 Hérouville-Saint-Clair', ST_GeogFromText('POINT(-0.3333 49.2000)'), '14', 'Normandie', 'ferme', 'contact@lavidaluca.fr', '02.31.11.11.11', 'Ferme principale du projet La Vida Luca', '["elevage", "maraichage", "transformation", "accueil_public"]'),
('550e8400-e29b-41d4-a716-446655440003', 'Ferme Partenaire Bio', '789 Avenue Verte, 14100 Lisieux', ST_GeogFromText('POINT(0.2333 49.1500)'), '14', 'Normandie', 'partenaire', 'bio@fermepartenaire.fr', '02.31.22.22.22', 'Ferme partenaire certifiée agriculture biologique', '["certification_bio", "vente_directe", "visites"]');

-- Insérer des activités basées sur le catalogue existant
INSERT INTO activities (id, slug, title, category, summary, description, duration_min, skill_tags, seasonality, safety_level, materials, location_id) VALUES
('660e8400-e29b-41d4-a716-446655440001', 'soins-animaux', 'Soins aux animaux', 'agri', 'Nourrir, observer, soigner selon les besoins.', 'Apprendre les gestes de base pour prendre soin des animaux de la ferme : alimentation, observation du comportement, soins élémentaires.', 90, '["patience", "observation", "douceur"]', '["toutes"]', 1, '["bottes", "gants"]', '550e8400-e29b-41d4-a716-446655440002'),
('660e8400-e29b-41d4-a716-446655440002', 'tonte-entretien-troupeau', 'Tonte & entretien du troupeau', 'agri', 'Hygiène, tonte (démo), soins courants.', 'Découverte des techniques de tonte et d''entretien du troupeau. Apprentissage des gestes d''hygiène et de soins.', 90, '["elevage", "hygiene"]', '["printemps"]', 2, '["bottes", "gants"]', '550e8400-e29b-41d4-a716-446655440002'),
('660e8400-e29b-41d4-a716-446655440003', 'plantation-cultures', 'Plantation de cultures', 'agri', 'Semis, arrosage, paillage, suivi de plants.', 'Initiation aux techniques de plantation : préparation du sol, semis, arrosage, paillage et suivi des cultures.', 90, '["sol", "plantes"]', '["printemps", "ete"]', 1, '["gants"]', '550e8400-e29b-41d4-a716-446655440001'),
('660e8400-e29b-41d4-a716-446655440004', 'fromage', 'Fabrication de fromage', 'transfo', 'Du lait au caillé : hygiène, moulage, affinage (découverte).', 'Découverte de la transformation du lait en fromage : techniques d''hygiène, processus de caillage, moulage et initiation à l''affinage.', 90, '["hygiene", "precision"]', '["toutes"]', 2, '["tablier"]', '550e8400-e29b-41d4-a716-446655440002'),
('660e8400-e29b-41d4-a716-446655440005', 'conserves', 'Confitures & conserves', 'transfo', 'Préparation, stérilisation, mise en pot, étiquetage.', 'Apprentissage des techniques de conservation : préparation des fruits, stérilisation, mise en pot et étiquetage.', 90, '["organisation", "hygiene"]', '["ete", "automne"]', 1, '["tablier"]', '550e8400-e29b-41d4-a716-446655440003'),
('660e8400-e29b-41d4-a716-446655440006', 'menuiserie-simple', 'Menuiserie simple', 'artisanat', 'Mesurer, scier, poncer, assembler (projet défini).', 'Initiation à la menuiserie : apprentissage des mesures, techniques de sciage, ponçage et assemblage pour réaliser un projet simple.', 120, '["precision", "patience"]', '["toutes"]', 2, '["gants", "lunettes"]', '550e8400-e29b-41d4-a716-446655440001'),
('660e8400-e29b-41d4-a716-446655440007', 'potager-eco', 'Potager écologique', 'nature', 'Associations, paillis, rotation des cultures.', 'Découverte du jardinage écologique : associations de plantes, utilisation du paillis, rotation des cultures et respect de la biodiversité.', 90, '["observation", "sobriete"]', '["printemps", "ete", "automne"]', 1, '["gants"]', '550e8400-e29b-41d4-a716-446655440002'),
('660e8400-e29b-41d4-a716-446655440008', 'cuisine-collective', 'Cuisine collective (équipe)', 'social', 'Préparer un repas simple et bon.', 'Apprentissage du travail en équipe pour préparer un repas collectif : organisation, répartition des tâches, cuisine simple et conviviale.', 90, '["hygiene", "equipe", "temps"]', '["toutes"]', 1, '["tablier"]', '550e8400-e29b-41d4-a716-446655440001');

-- Programmer des sessions d'activités
INSERT INTO activity_sessions (id, activity_id, location_id, scheduled_date, duration_min, max_participants, status) VALUES
('770e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440002', '2024-08-25 09:00:00+02', 90, 8, 'scheduled'),
('770e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440001', '2024-08-26 14:00:00+02', 90, 10, 'scheduled'),
('770e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440002', '2024-08-27 10:00:00+02', 90, 6, 'scheduled'),
('770e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440001', '2024-08-28 09:00:00+02', 120, 4, 'scheduled'),
('770e8400-e29b-41d4-a716-446655440005', '660e8400-e29b-41d4-a716-446655440008', '550e8400-e29b-41d4-a716-446655440001', '2024-08-29 11:30:00+02', 90, 12, 'scheduled');

-- Insérer des utilisateurs de test (les mots de passe devront être hachés en production)
INSERT INTO users (id, email, first_name, last_name, phone, location, location_name, bio, skills, interests, role, status) VALUES
('880e8400-e29b-41d4-a716-446655440001', 'admin@lavidaluca.fr', 'Admin', 'LaVidaLuca', '06.01.02.03.04', ST_GeogFromText('POINT(-0.3781 49.1829)'), 'Caen, Calvados', 'Administrateur de la plateforme La Vida Luca', '["gestion", "coordination", "communication"]', '["agriculture", "formation", "environnement"]', 'admin', 'active'),
('880e8400-e29b-41d4-a716-446655440002', 'marie.durand@email.fr', 'Marie', 'Durand', '06.11.22.33.44', ST_GeogFromText('POINT(-0.3500 49.1800)'), 'Hérouville-Saint-Clair', 'Instructrice spécialisée en agriculture biologique', '["agriculture_bio", "elevage", "fromage"]', '["animaux", "transformation", "transmission"]', 'instructor', 'active'),
('880e8400-e29b-41d4-a716-446655440003', 'pierre.martin@email.fr', 'Pierre', 'Martin', '06.55.66.77.88', ST_GeogFromText('POINT(-0.4000 49.2000)'), 'Caen', 'Coordinator des activités artisanales', '["menuiserie", "bricolage", "formation"]', '["artisanat", "creation", "pedagogie"]', 'coordinator', 'active'),
('880e8400-e29b-41d4-a716-446655440004', 'sophie.lefevre@email.fr', 'Sophie', 'Lefevre', '06.99.88.77.66', ST_GeogFromText('POINT(-0.3200 49.1900)'), 'Calvados', 'Étudiante MFR passionnée de nature', '["observation", "patience"]', '["jardinage", "nature", "animaux"]', 'participant', 'active'),
('880e8400-e29b-41d4-a716-446655440005', 'julien.moreau@email.fr', 'Julien', 'Moreau', '06.12.34.56.78', ST_GeogFromText('POINT(-0.3600 49.1700)'), 'Lisieux', 'Jeune intéressé par l''agriculture durable', '["motivation", "apprentissage"]', '["agriculture", "environnement", "social"]', 'participant', 'active');

-- Insérer quelques inscriptions d'exemple
INSERT INTO activity_registrations (user_id, activity_id, session_date, status) VALUES
('880e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440001', '2024-08-25 09:00:00+02', 'confirmed'),
('880e8400-e29b-41d4-a716-446655440005', '660e8400-e29b-41d4-a716-446655440001', '2024-08-25 09:00:00+02', 'confirmed'),
('880e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440003', '2024-08-26 14:00:00+02', 'pending'),
('880e8400-e29b-41d4-a716-446655440005', '660e8400-e29b-41d4-a716-446655440006', '2024-08-28 09:00:00+02', 'confirmed');

-- Insérer des suggestions IA d'exemple
INSERT INTO ai_suggestions (user_id, activity_id, score, reasons, context) VALUES
('880e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440007', 0.95, '["Correspond à vos intérêts pour le jardinage", "Activité disponible près de chez vous", "Niveau débutant adapté"]', '{"recommendation_type": "interest_based", "location_proximity": true}'),
('880e8400-e29b-41d4-a716-446655440005', '660e8400-e29b-41d4-a716-446655440004', 0.88, '["Découverte de la transformation alimentaire", "Complète bien vos activités agricoles", "Instructeur expérimenté"]', '{"recommendation_type": "skill_progression", "difficulty_progression": true}');

-- Insérer des notifications d'exemple
INSERT INTO notifications (user_id, title, content, type, action_url) VALUES
('880e8400-e29b-41d4-a716-446655440004', 'Rappel : Soins aux animaux demain', 'N''oubliez pas votre session "Soins aux animaux" prévue demain à 9h à la Ferme La Vida Luca.', 'activity_reminder', '/activites/soins-animaux'),
('880e8400-e29b-41d4-a716-446655440005', 'Nouvelle activité disponible', 'Une nouvelle session de "Potager écologique" vient d''être programmée. Inscrivez-vous dès maintenant !', 'new_activity', '/activites/potager-eco'),
('880e8400-e29b-41d4-a716-446655440004', 'Bienvenue sur La Vida Luca !', 'Bienvenue dans la communauté La Vida Luca ! Découvrez toutes nos activités et commencez votre parcours.', 'system', '/catalogue'),
('880e8400-e29b-41d4-a716-446655440005', 'Inscription confirmée', 'Votre inscription à l''activité "Menuiserie simple" a été confirmée. Rendez-vous le 28 août à 9h.', 'activity_confirmation', '/mes-activites');

-- Mettre à jour les comptes de participants pour les sessions
UPDATE activity_sessions SET current_participants = 2 WHERE id = '770e8400-e29b-41d4-a716-446655440001';
UPDATE activity_sessions SET current_participants = 1 WHERE id = '770e8400-e29b-41d4-a716-446655440004';