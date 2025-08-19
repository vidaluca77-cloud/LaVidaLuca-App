-- Seed data for La Vida Luca

-- Insert sample activities (30 activities as mentioned in the README)
INSERT INTO activities (slug, title, category, summary, duration_min, skill_tags, seasonality, safety_level, materials) VALUES 
-- Agriculture
('soins-animaux', 'Soins aux animaux', 'agri', 'Nourrir, observer, nettoyer les espaces des animaux de la ferme.', 60, ARRAY['bienveillance', 'observation'], ARRAY['toutes'], 1, ARRAY['gants']),
('preparation-sols', 'Préparation des sols', 'agri', 'Bêcher, aérer, amender un sol pour les futures cultures.', 90, ARRAY['force', 'sol'], ARRAY['printemps', 'automne'], 2, ARRAY['gants', 'bottes']),
('semis-potager', 'Semis en potager', 'agri', 'Tracer, semer, arroser selon les besoins de chaque légume.', 60, ARRAY['precision', 'plantes'], ARRAY['printemps'], 1, ARRAY['gants']),
('plantation-cultures', 'Plantation de cultures', 'agri', 'Semis, arrosage, paillage, suivi de plants.', 90, ARRAY['sol', 'plantes'], ARRAY['printemps', 'ete'], 1, ARRAY['gants']),
('init-maraichage', 'Initiation maraîchage', 'agri', 'Plan de culture, entretien, récolte respectueuse.', 120, ARRAY['sol', 'organisation'], ARRAY['printemps', 'ete', 'automne'], 1, ARRAY['gants', 'bottes']),
('clotures-abris', 'Gestion des clôtures & abris', 'agri', 'Identifier, réparer, sécuriser parcs et abris.', 120, ARRAY['securite', 'bois'], ARRAY['toutes'], 2, ARRAY['gants']),

-- Transformation
('fromage', 'Fabrication de fromage', 'transfo', 'Du lait au caillé : hygiène, moulage, affinage (découverte).', 90, ARRAY['hygiene', 'precision'], ARRAY['toutes'], 2, ARRAY['tablier']),
('conserves', 'Confitures & conserves', 'transfo', 'Préparation, stérilisation, mise en pot, étiquetage.', 90, ARRAY['organisation', 'hygiene'], ARRAY['ete', 'automne'], 1, ARRAY['tablier']),
('laine', 'Transformation de la laine', 'transfo', 'Lavage, cardage, petite création textile.', 90, ARRAY['patience', 'creativite'], ARRAY['toutes'], 1, ARRAY['tablier', 'gants']),
('jus', 'Fabrication de jus', 'transfo', 'Du verger à la bouteille : tri, pressage, filtration.', 90, ARRAY['hygiene', 'securite'], ARRAY['automne'], 2, ARRAY['tablier', 'gants']),
('aromatiques-sechage', 'Séchage d''herbes aromatiques', 'transfo', 'Cueillette, séchage, conditionnement doux.', 60, ARRAY['douceur', 'organisation'], ARRAY['ete'], 1, ARRAY['tablier']),
('pain-traditionnel', 'Pain traditionnel', 'transfo', 'Pétrissage, fermentation, cuisson au four traditionnel.', 180, ARRAY['patience', 'rythme'], ARRAY['toutes'], 1, ARRAY['tablier']),

-- Artisanat
('menuiserie-simple', 'Menuiserie simple', 'artisanat', 'Mesurer, scier, assembler : petit mobilier utile.', 120, ARRAY['precision', 'bois'], ARRAY['toutes'], 2, ARRAY['gants']),
('poterie-terre', 'Poterie & terre cuite', 'artisanat', 'Façonner l''argile, créer des objets du quotidien.', 120, ARRAY['creativite', 'patience'], ARRAY['toutes'], 1, ARRAY['tablier']),
('reparation-outils', 'Réparation d''outils', 'artisanat', 'Affûter, réparer, entretenir les outils de la ferme.', 90, ARRAY['technique', 'securite'], ARRAY['toutes'], 2, ARRAY['gants']),
('peinture-deco', 'Peinture & décoration d''espaces', 'artisanat', 'Préparer, protéger, peindre proprement.', 90, ARRAY['proprete', 'finitions'], ARRAY['toutes'], 1, ARRAY['tablier', 'gants']),
('amenagement-verts', 'Aménagement d''espaces verts', 'artisanat', 'Désherbage doux, paillage, plantations.', 90, ARRAY['endurance', 'esthetique'], ARRAY['printemps', 'ete'], 1, ARRAY['gants', 'bottes']),
('panneaux-orientation', 'Panneaux & orientation', 'artisanat', 'Concevoir/poser une signalétique claire.', 90, ARRAY['clarte', 'precision'], ARRAY['toutes'], 1, ARRAY['gants']),

-- Nature
('entretien-riviere', 'Entretien de la rivière', 'nature', 'Nettoyage doux, observation des berges.', 90, ARRAY['prudence', 'ecologie'], ARRAY['printemps', 'ete'], 2, ARRAY['bottes', 'gants']),
('creation-sentiers', 'Création de sentiers', 'nature', 'Baliser, débroussailler, créer des chemins sûrs.', 120, ARRAY['orientation', 'endurance'], ARRAY['printemps', 'ete'], 2, ARRAY['gants', 'bottes']),
('plantation-arbres', 'Plantation d''arbres', 'nature', 'Choisir l''emplacement, creuser, planter, arroser.', 90, ARRAY['ecologie', 'force'], ARRAY['printemps', 'automne'], 1, ARRAY['gants', 'bottes']),
('compostage', 'Compostage', 'nature', 'Tri, compost, valorisation des déchets verts.', 60, ARRAY['geste_utile', 'hygiene'], ARRAY['toutes'], 1, ARRAY['gants']),
('faune-locale', 'Observation de la faune locale', 'nature', 'Discrétion, repérage, traces/indices.', 60, ARRAY['patience', 'respect'], ARRAY['toutes'], 1, ARRAY[]),
('mare-biodiversite', 'Création d''une mare', 'nature', 'Creuser, étanchéifier, planter pour la biodiversité.', 150, ARRAY['ecologie', 'conception'], ARRAY['printemps'], 2, ARRAY['bottes', 'gants']),
('refuges-insectes', 'Refuges à insectes', 'nature', 'Construire des abris pour les auxiliaires du jardin.', 90, ARRAY['creativity', 'ecologie'], ARRAY['toutes'], 1, ARRAY['gants']),

-- Social
('accueil-visiteurs', 'Accueil de visiteurs', 'social', 'Présenter le lieu, guider, répondre aux questions.', 90, ARRAY['communication', 'bienveillance'], ARRAY['toutes'], 1, ARRAY[]),
('organisation-evenements', 'Organisation d''événements', 'social', 'Planifier, coordonner, gérer une manifestation.', 120, ARRAY['organisation', 'creativite'], ARRAY['toutes'], 1, ARRAY[]),
('cuisine-collective', 'Cuisine collective (équipe)', 'social', 'Préparer un repas simple et bon.', 90, ARRAY['hygiene', 'equipe', 'temps'], ARRAY['toutes'], 1, ARRAY['tablier']),
('gouter-fermier', 'Goûter fermier', 'social', 'Organisation, service, convivialité, propreté.', 60, ARRAY['rigueur', 'relationnel'], ARRAY['toutes'], 1, ARRAY['tablier']),
('nettoyage-collectif', 'Nettoyage collectif d''espaces', 'social', 'Organiser/mener un nettoyage en groupe.', 90, ARRAY['organisation', 'equipe'], ARRAY['toutes'], 1, ARRAY['gants']);

-- Insert sample instructor profile
INSERT INTO profiles (id, email, full_name, role, location, skills, preferences, availability)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'instructor@lavidaluca.fr', 
    'Marie Dupont',
    'instructor',
    'Ferme de la Vallée Verte',
    ARRAY['agriculture', 'transformation', 'animation'],
    ARRAY['bio', 'permaculture', 'formation'],
    ARRAY['matin', 'apres-midi']
);

-- Insert sample student profile
INSERT INTO profiles (id, email, full_name, role, location, skills, preferences, availability)
VALUES (
    '00000000-0000-0000-0000-000000000002',
    'student@example.com',
    'Lucas Martin', 
    'student',
    'MFR du Limousin',
    ARRAY['motivation', 'curiosite'],
    ARRAY['agriculture', 'nature'],
    ARRAY['apres-midi', 'weekend']
);

-- Insert sample activity sessions
INSERT INTO activity_sessions (activity_id, instructor_id, title, description, start_time, end_time, location, max_participants)
VALUES 
(
    (SELECT id FROM activities WHERE slug = 'soins-animaux'),
    '00000000-0000-0000-0000-000000000001',
    'Soins aux animaux - Session découverte',
    'Première approche des soins aux animaux de la ferme',
    NOW() + INTERVAL '1 day',
    NOW() + INTERVAL '1 day' + INTERVAL '1 hour',
    'Étable principale',
    8
),
(
    (SELECT id FROM activities WHERE slug = 'semis-potager'),
    '00000000-0000-0000-0000-000000000001',
    'Atelier semis de printemps',
    'Apprentissage des techniques de semis pour le potager',
    NOW() + INTERVAL '3 days',
    NOW() + INTERVAL '3 days' + INTERVAL '90 minutes',
    'Jardin pédagogique',
    10
);

-- Insert sample participation
INSERT INTO session_participants (session_id, user_id, status, notes)
VALUES 
(
    (SELECT id FROM activity_sessions WHERE title = 'Soins aux animaux - Session découverte'),
    '00000000-0000-0000-0000-000000000002',
    'registered',
    'Première participation, très motivé'
);

-- Insert sample user progress
INSERT INTO user_activity_progress (user_id, activity_id, completion_count, total_duration_minutes, skill_level)
VALUES 
(
    '00000000-0000-0000-0000-000000000002',
    (SELECT id FROM activities WHERE slug = 'soins-animaux'),
    2,
    120,
    1
);

-- Insert sample contact message
INSERT INTO contact_messages (name, email, subject, message, status)
VALUES 
(
    'Jean Dubois',
    'jean.dubois@example.com',
    'Inscription MFR',
    'Bonjour, je souhaiterais inscrire mon fils dans votre programme. Pouvez-vous me donner plus d''informations ?',
    'new'
);

-- Insert sample system log
INSERT INTO system_logs (level, source, message, context)
VALUES 
(
    'INFO',
    'DATABASE',
    'Database seeded successfully',
    '{"tables": ["activities", "profiles", "activity_sessions", "session_participants", "user_activity_progress", "contact_messages"], "timestamp": "' || NOW()::text || '"}'
);