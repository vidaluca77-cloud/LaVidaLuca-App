-- Données d'exemple pour La Vida Luca
-- À exécuter après schema.sql

-- Insertion des 30 activités du catalogue MFR
INSERT INTO activities (slug, title, category, summary, description, duration_min, skill_tags, seasonality, safety_level, materials, learning_objectives) VALUES 

-- Agriculture (10 activités)
('soins-animaux', 'Soins aux animaux', 'agri', 'Alimentation, observation, manipulation douce des animaux.', 'Apprendre les bases du soin animal : alimentation équilibrée, observation du comportement, manipulation respectueuse et sécurisée des animaux de ferme.', 90, ARRAY['soins_animaux', 'observation'], ARRAY['toutes'], 1, ARRAY['bottes', 'gants'], ARRAY['Comprendre les besoins des animaux', 'Maîtriser les gestes de base', 'Développer le sens de l''observation']),

('tonte-entretien-troupeau', 'Tonte & entretien du troupeau', 'agri', 'Hygiène, tonte (démo), soins courants.', 'Découverte de l''entretien du troupeau : hygiène, techniques de tonte, soins préventifs et curatifs de base.', 90, ARRAY['elevage', 'hygiene'], ARRAY['printemps'], 2, ARRAY['bottes', 'gants'], ARRAY['Comprendre l''hygiène animale', 'Observer les techniques de tonte', 'Apprendre les soins de base']),

('basse-cour-soins', 'Soins basse-cour', 'agri', 'Poules/canards/lapins : alimentation, abris, propreté.', 'Gestion complète de la basse-cour : alimentation adaptée, entretien des abris, maintien de la propreté et de la santé des animaux.', 60, ARRAY['soins_animaux'], ARRAY['toutes'], 1, ARRAY['bottes', 'gants'], ARRAY['Gérer une basse-cour', 'Maintenir l''hygiène', 'Assurer le bien-être animal']),

('plantation-cultures', 'Plantation de cultures', 'agri', 'Semis, arrosage, paillage, suivi de plants.', 'Apprentissage des techniques de plantation : préparation du sol, semis, techniques d''arrosage, paillage et suivi de croissance.', 90, ARRAY['sol', 'plantes'], ARRAY['printemps', 'ete'], 1, ARRAY['gants'], ARRAY['Maîtriser les techniques de semis', 'Comprendre les besoins des plantes', 'Apprendre le suivi cultural']),

('init-maraichage', 'Initiation maraîchage', 'agri', 'Plan de culture, entretien, récolte respectueuse.', 'Introduction au maraîchage : élaboration d''un plan de culture, techniques d''entretien, récolte au bon moment et dans le respect de la plante.', 120, ARRAY['sol', 'organisation'], ARRAY['printemps', 'ete', 'automne'], 1, ARRAY['gants', 'bottes'], ARRAY['Planifier une culture', 'Organiser l''espace', 'Récolter au bon moment']),

('clotures-abris', 'Gestion des clôtures & abris', 'agri', 'Identifier, réparer, sécuriser parcs et abris.', 'Maintenance des infrastructures agricoles : identification des problèmes, réparations simples, sécurisation des parcs et abris.', 120, ARRAY['securite', 'bois'], ARRAY['toutes'], 2, ARRAY['gants'], ARRAY['Identifier les dysfonctionnements', 'Effectuer des réparations simples', 'Assurer la sécurité']),

-- Transformation (5 activités)
('fromage', 'Fabrication de fromage', 'transfo', 'Du lait au caillé : hygiène, moulage, affinage (découverte).', 'Découverte de la fabrication fromagère : processus de transformation du lait, techniques de moulage, principes d''affinage.', 90, ARRAY['hygiene', 'precision'], ARRAY['toutes'], 2, ARRAY['tablier'], ARRAY['Comprendre la transformation laitière', 'Maîtriser l''hygiène alimentaire', 'Découvrir l''affinage']),

('conserves', 'Confitures & conserves', 'transfo', 'Préparation, stérilisation, mise en pot, étiquetage.', 'Techniques de conservation : préparation des fruits et légumes, processus de stérilisation, mise en pot et étiquetage professionnel.', 90, ARRAY['organisation', 'hygiene'], ARRAY['ete', 'automne'], 1, ARRAY['tablier'], ARRAY['Maîtriser la conservation', 'Assurer la stérilisation', 'Organiser la production']),

('laine', 'Transformation de la laine', 'transfo', 'Lavage, cardage, petite création textile.', 'Transformation de la laine brute : techniques de lavage, cardage manuel, initiation aux créations textiles simples.', 90, ARRAY['patience', 'creativite'], ARRAY['toutes'], 1, ARRAY['tablier', 'gants'], ARRAY['Transformer la matière première', 'Développer la patience', 'Créer des objets utiles']),

('jus', 'Fabrication de jus', 'transfo', 'Du verger à la bouteille : tri, pressage, filtration.', 'Circuit complet de production de jus : tri des fruits, techniques de pressage, filtration et mise en bouteille.', 90, ARRAY['hygiene', 'securite'], ARRAY['automne'], 2, ARRAY['tablier', 'gants'], ARRAY['Maîtriser le circuit de production', 'Assurer la qualité', 'Respecter l''hygiène']),

('aromatiques-sechage', 'Séchage d''herbes aromatiques', 'transfo', 'Cueillette, séchage, conditionnement doux.', 'Valorisation des plantes aromatiques : techniques de cueillette, méthodes de séchage, conditionnement respectueux.', 60, ARRAY['douceur', 'organisation'], ARRAY['ete'], 1, ARRAY['tablier'], ARRAY['Cueillir au bon moment', 'Maîtriser le séchage', 'Conditionner proprement']);

-- Insertion des lieux d'action (exemples)
INSERT INTO action_locations (name, description, address, city, postal_code, contact_email, specialties, facilities) VALUES 
('MFR de Bretagne', 'Maison Familiale Rurale spécialisée en agriculture durable', '12 Route de la Ferme', 'Ploemeur', '56270', 'contact@mfr-bretagne.fr', ARRAY['agriculture', 'elevage', 'maraichage'], ARRAY['etables', 'serres', 'atelier_transformation']),

('Ferme Pédagogique du Lot', 'Ferme d''insertion et de formation aux métiers verts', 'Lieu-dit La Bergerie', 'Cahors', '46000', 'contact@ferme-lot.fr', ARRAY['transformation', 'artisanat', 'permaculture'], ARRAY['laboratoire', 'four_pain', 'ruches']),

('MFR des Alpes', 'Formation en milieu montagnard', '5 Chemin des Alpages', 'Annecy', '74000', 'contact@mfr-alpes.fr', ARRAY['agriculture_montagne', 'fromage', 'bois'], ARRAY['fromagerie', 'scierie', 'bergerie']);

-- Insertion d'activités futures (exemples de sessions)
INSERT INTO activity_sessions (activity_id, session_date, start_time, end_time, location, max_participants) 
SELECT 
    a.id,
    CURRENT_DATE + (CASE WHEN a.seasonality && ARRAY['printemps'] THEN 30 ELSE 60 END),
    '09:00'::TIME,
    (('09:00'::TIME + (a.duration_min || ' minutes')::INTERVAL))::TIME,
    'MFR de Bretagne',
    8
FROM activities a 
WHERE a.slug IN ('soins-animaux', 'plantation-cultures', 'fromage', 'conserves')
LIMIT 10;