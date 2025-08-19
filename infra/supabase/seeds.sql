-- Seed data for La Vida Luca platform
-- This script populates the database with the 30 activities mentioned in the README

INSERT INTO activities (id, title, slug, category, summary, duration_min, skill_tags, seasonality, safety_level, materials) VALUES
-- Agriculture (6 activities)
(uuid_generate_v4(), 'Nourrir et soigner les moutons', 'nourrir-soigner-moutons', 'agri', 'Gestes quotidiens : alimentation, eau, observation.', 60, ARRAY['elevage', 'responsabilite'], ARRAY['toutes'], 1, ARRAY['bottes', 'gants']),
(uuid_generate_v4(), 'Traite des chèvres', 'traite-chevres', 'agri', 'Technique de traite manuelle, hygiène, relation animal.', 45, ARRAY['elevage', 'hygiene'], ARRAY['toutes'], 1, ARRAY['seaux', 'gants']),
(uuid_generate_v4(), 'Soins aux animaux', 'soins-animaux', 'agri', 'Observation, petits soins, prévention santé.', 75, ARRAY['soins_animaux', 'observation'], ARRAY['toutes'], 2, ARRAY['trousse_soins']),
(uuid_generate_v4(), 'Plantation de cultures', 'plantation-cultures', 'agri', 'Semis, arrosage, paillage, suivi de plants.', 90, ARRAY['sol', 'plantes'], ARRAY['printemps', 'ete'], 1, ARRAY['gants']),
(uuid_generate_v4(), 'Initiation maraîchage', 'init-maraichage', 'agri', 'Plan de culture, entretien, récolte respectueuse.', 120, ARRAY['sol', 'organisation'], ARRAY['printemps', 'ete', 'automne'], 1, ARRAY['gants', 'bottes']),
(uuid_generate_v4(), 'Récolte et conservation', 'recolte-conservation', 'agri', 'Timing de récolte, stockage, préservation qualité.', 90, ARRAY['observation', 'organisation'], ARRAY['ete', 'automne'], 1, ARRAY['paniers', 'gants']),

-- Transformation (6 activities)
(uuid_generate_v4(), 'Fabrication de fromage', 'fabrication-fromage', 'transfo', 'Caillage, égouttage, affinage : bases fromagères.', 150, ARRAY['hygiene', 'precision'], ARRAY['toutes'], 2, ARRAY['tablier', 'gants']),
(uuid_generate_v4(), 'Conserves de légumes', 'conserves-legumes', 'transfo', 'Stérilisation, mise en bocaux, techniques conservation.', 120, ARRAY['hygiene', 'precision'], ARRAY['ete', 'automne'], 2, ARRAY['bocaux', 'gants']),
(uuid_generate_v4(), 'Confitures artisanales', 'confitures-artisanales', 'transfo', 'Cuisson maîtrisée, dosage sucre, texture parfaite.', 90, ARRAY['precision', 'creativite'], ARRAY['ete', 'automne'], 1, ARRAY['tablier']),
(uuid_generate_v4(), 'Transformation laitière', 'transformation-laitiere', 'transfo', 'Yaourts, beurre, crème : techniques de base.', 120, ARRAY['hygiene', 'precision'], ARRAY['toutes'], 2, ARRAY['ustensiles', 'gants']),
(uuid_generate_v4(), 'Séchage et déshydratation', 'sechage-deshydratation', 'transfo', 'Fruits, légumes, plantes : conservation naturelle.', 60, ARRAY['patience', 'organisation'], ARRAY['ete', 'automne'], 1, ARRAY['clayettes']),
(uuid_generate_v4(), 'Pain au four à bois', 'pain-four-bois', 'transfo', 'Pétrissage, façonnage, cuisson : respect des temps.', 120, ARRAY['precision', 'rythme'], ARRAY['toutes'], 2, ARRAY['tablier']),

-- Artisanat (6 activities)
(uuid_generate_v4(), 'Construction d''abris', 'abris-bois', 'artisanat', 'Petites structures bois : plan, coupe, assemblage.', 120, ARRAY['bois', 'precision', 'securite'], ARRAY['toutes'], 2, ARRAY['gants']),
(uuid_generate_v4(), 'Réparation d''outils', 'reparation-outils', 'artisanat', 'Maintenance, affûtage, remise en état matériel.', 90, ARRAY['precision', 'securite'], ARRAY['toutes'], 3, ARRAY['outils', 'gants']),
(uuid_generate_v4(), 'Menuiserie simple', 'menuiserie-simple', 'artisanat', 'Objets usuels bois : mesure, découpe, assemblage.', 150, ARRAY['bois', 'precision'], ARRAY['toutes'], 2, ARRAY['outils', 'lunettes']),
(uuid_generate_v4(), 'Travail du métal', 'travail-metal', 'artisanat', 'Soudure légère, pliage, création d''objets simples.', 120, ARRAY['precision', 'securite'], ARRAY['toutes'], 4, ARRAY['protection', 'gants']),
(uuid_generate_v4(), 'Vannerie naturelle', 'vannerie-naturelle', 'artisanat', 'Tressage osier, création paniers, objets déco.', 180, ARRAY['creativite', 'patience'], ARRAY['toutes'], 1, ARRAY['osier']),
(uuid_generate_v4(), 'Couture et textile', 'couture-textile', 'artisanat', 'Réparations, créations simples, upcycling tissus.', 120, ARRAY['precision', 'creativite'], ARRAY['toutes'], 1, ARRAY['fil', 'aiguilles']),

-- Nature/Environnement (6 activities)
(uuid_generate_v4(), 'Plantation d''arbres', 'plantation-arbres', 'nature', 'Choix essences, préparation sol, plantation correcte.', 120, ARRAY['sol', 'ecologie'], ARRAY['automne', 'hiver'], 1, ARRAY['beche', 'gants']),
(uuid_generate_v4(), 'Compostage avancé', 'compostage-avance', 'nature', 'Techniques, équilibre matières, gestion température.', 90, ARRAY['ecologie', 'organisation'], ARRAY['toutes'], 1, ARRAY['fourche']),
(uuid_generate_v4(), 'Jardins en permaculture', 'jardins-permaculture', 'nature', 'Conception, associations plantes, cycles naturels.', 150, ARRAY['ecologie', 'observation'], ARRAY['printemps', 'ete'], 1, ARRAY['gants', 'outils']),
(uuid_generate_v4(), 'Gestion de l''eau', 'gestion-eau', 'nature', 'Récupération, stockage, irrigation économe.', 120, ARRAY['ecologie', 'organisation'], ARRAY['toutes'], 2, ARRAY['outils']),
(uuid_generate_v4(), 'Biodiversité locale', 'biodiversite-locale', 'nature', 'Observation, recensement, protection espèces.', 90, ARRAY['observation', 'ecologie'], ARRAY['printemps', 'ete'], 1, ARRAY['carnets']),
(uuid_generate_v4(), 'Nichoirs & hôtels à insectes', 'nichoirs-hotels', 'nature', 'Concevoir, fabriquer, installer des abris.', 120, ARRAY['precision', 'pedagogie'], ARRAY['toutes'], 1, ARRAY['gants']),

-- Social/Animation (6 activities)
(uuid_generate_v4(), 'Journée portes ouvertes', 'portes-ouvertes', 'social', 'Préparer, accueillir, guider un public.', 180, ARRAY['accueil', 'organisation'], ARRAY['toutes'], 1, ARRAY[]),
(uuid_generate_v4(), 'Ateliers enfants nature', 'ateliers-enfants', 'social', 'Animation découverte, jeux éducatifs, sécurité.', 120, ARRAY['pedagogie', 'patience'], ARRAY['toutes'], 1, ARRAY['materiel_jeux']),
(uuid_generate_v4(), 'Visites guidées ferme', 'visites-guidees', 'social', 'Présentation lieux, explications, interaction.', 90, ARRAY['expression', 'accueil'], ARRAY['toutes'], 1, ARRAY[]),
(uuid_generate_v4(), 'Communication digitale', 'communication-digitale', 'social', 'Photos, réseaux, valorisation activités.', 120, ARRAY['creativite', 'expression'], ARRAY['toutes'], 1, ARRAY['appareil_photo']),
(uuid_generate_v4(), 'Coordination d''équipes', 'coordination-equipes', 'social', 'Organisation, planification, suivi groupe.', 150, ARRAY['organisation', 'equipe'], ARRAY['toutes'], 1, ARRAY[]),
(uuid_generate_v4(), 'Participation à un marché local', 'marche-local', 'social', 'Stand, présentation, caisse symbolique (simulation).', 180, ARRAY['contact', 'compter_simple', 'equipe'], ARRAY['toutes'], 1, ARRAY[]);

-- Create a sample user for testing
INSERT INTO users (id, email, full_name, profile, is_active) VALUES
(uuid_generate_v4(), 'test@lavidaluca.fr', 'Utilisateur Test', 
 '{"skills": ["elevage", "hygiene"], "availability": ["weekend", "matin"], "location": "France", "preferences": ["agri", "nature"]}', 
 true);