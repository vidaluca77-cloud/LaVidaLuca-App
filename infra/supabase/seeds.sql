-- Données initiales pour la base de données La Vida Luca
-- À exécuter après schema.sql dans Supabase SQL Editor

-- Insertion des 30 activités du catalogue MFR
INSERT INTO activities (id, slug, title, category, summary, duration_min, skill_tags, seasonality, safety_level, materials) VALUES

-- Agriculture
('a1000000-0000-0000-0000-000000000001', 'soins-animaux', 'Soins aux animaux', 'agri', 'Contact, alimentation, observation du troupeau.', 60, ARRAY['relationnel', 'observation'], ARRAY['toutes'], 1, ARRAY['gants']),
('a1000000-0000-0000-0000-000000000002', 'traite-vaches', 'Traite des vaches', 'agri', 'Hygiène, gestes techniques, respect des animaux.', 90, ARRAY['precision', 'hygiene'], ARRAY['toutes'], 2, ARRAY['blouse', 'gants']),
('a1000000-0000-0000-0000-000000000003', 'entretien-pature', 'Entretien des pâtures', 'agri', 'Clôtures, points d''eau, rotation des parcelles.', 120, ARRAY['effort', 'autonomie'], ARRAY['printemps', 'ete', 'automne'], 2, ARRAY['gants', 'bottes']),
('a1000000-0000-0000-0000-000000000004', 'plantation-cultures', 'Plantation de cultures', 'agri', 'Semis, arrosage, paillage, suivi de plants.', 90, ARRAY['sol', 'plantes'], ARRAY['printemps', 'ete'], 1, ARRAY['gants']),
('a1000000-0000-0000-0000-000000000005', 'init-maraichage', 'Initiation maraîchage', 'agri', 'Plan de culture, entretien, récolte respectueuse.', 120, ARRAY['sol', 'organisation'], ARRAY['printemps', 'ete', 'automne'], 1, ARRAY['gants', 'bottes']),
('a1000000-0000-0000-0000-000000000006', 'clotures-abris', 'Gestion des clôtures & abris', 'agri', 'Identifier, réparer, sécuriser parcs et abris.', 120, ARRAY['securite', 'bois'], ARRAY['toutes'], 2, ARRAY['gants']),

-- Transformation
('a2000000-0000-0000-0000-000000000007', 'fromage', 'Fabrication de fromage', 'transfo', 'Du lait au caillé : hygiène, moulage, affinage (découverte).', 90, ARRAY['hygiene', 'precision'], ARRAY['toutes'], 2, ARRAY['tablier']),
('a2000000-0000-0000-0000-000000000008', 'conserves', 'Confitures & conserves', 'transfo', 'Préparation, stérilisation, mise en pot, étiquetage.', 90, ARRAY['organisation', 'hygiene'], ARRAY['ete', 'automne'], 1, ARRAY['tablier']),
('a2000000-0000-0000-0000-000000000009', 'laine', 'Transformation de la laine', 'transfo', 'Lavage, cardage, petite création textile.', 90, ARRAY['patience', 'creativite'], ARRAY['toutes'], 1, ARRAY['tablier', 'gants']),
('a2000000-0000-0000-0000-000000000010', 'boulangerie', 'Boulangerie fermière', 'transfo', 'Pétrissage, façonnage, cuisson au feu de bois.', 180, ARRAY['force', 'temps'], ARRAY['toutes'], 2, ARRAY['tablier']),
('a2000000-0000-0000-0000-000000000011', 'charcuterie', 'Charcuterie artisanale', 'transfo', 'Découpe, préparation, conservation traditionnelle.', 120, ARRAY['precision', 'hygiene'], ARRAY['automne', 'hiver'], 3, ARRAY['tablier', 'gants']),
('a2000000-0000-0000-0000-000000000012', 'brassage', 'Brassage de bière', 'transfo', 'Maltage, brassage, fermentation, mise en bouteille.', 240, ARRAY['chimie', 'patience'], ARRAY['toutes'], 2, ARRAY['tablier']),

-- Artisanat
('a3000000-0000-0000-0000-000000000013', 'poterie', 'Poterie & céramique', 'artisanat', 'Modelage, tournage, émaillage, cuisson.', 120, ARRAY['creativite', 'patience'], ARRAY['toutes'], 1, ARRAY['tablier']),
('a3000000-0000-0000-0000-000000000014', 'reparation-outils', 'Réparation & entretien des outils', 'artisanat', 'Affûtage, graissage, petites réparations.', 60, ARRAY['autonomie', 'responsabilite'], ARRAY['toutes'], 1, ARRAY['gants']),
('a3000000-0000-0000-0000-000000000015', 'menuiserie-simple', 'Menuiserie simple', 'artisanat', 'Mesure, coupe, ponçage, finitions d''un objet.', 120, ARRAY['precision', 'creativite'], ARRAY['toutes'], 2, ARRAY['gants', 'lunettes']),
('a3000000-0000-0000-0000-000000000016', 'peinture-deco', 'Peinture & décoration d''espaces', 'artisanat', 'Préparer, protéger, peindre proprement.', 90, ARRAY['proprete', 'finitions'], ARRAY['toutes'], 1, ARRAY['tablier', 'gants']),
('a3000000-0000-0000-0000-000000000017', 'amenagement-verts', 'Aménagement d''espaces verts', 'artisanat', 'Désherbage doux, paillage, plantations.', 90, ARRAY['endurance', 'esthetique'], ARRAY['printemps', 'ete'], 1, ARRAY['gants', 'bottes']),
('a3000000-0000-0000-0000-000000000018', 'panneaux-orientation', 'Panneaux & orientation', 'artisanat', 'Concevoir/poser une signalétique claire.', 90, ARRAY['clarte', 'precision'], ARRAY['toutes'], 1, ARRAY['gants']),

-- Nature
('a4000000-0000-0000-0000-000000000019', 'entretien-riviere', 'Entretien de la rivière', 'nature', 'Nettoyage doux, observation des berges.', 90, ARRAY['prudence', 'ecologie'], ARRAY['printemps', 'ete'], 2, ARRAY['bottes', 'gants']),
('a4000000-0000-0000-0000-000000000020', 'haies-bocage', 'Plantation de haies & bocage', 'nature', 'Choix d''essences, plantation, protection.', 120, ARRAY['ecologie', 'effort'], ARRAY['automne', 'hiver'], 1, ARRAY['gants', 'bottes']),
('a4000000-0000-0000-0000-000000000021', 'foret-pedagogique', 'Gestion de la forêt pédagogique', 'nature', 'Débroussaillage, marquage, sentiers.', 120, ARRAY['nature', 'securite'], ARRAY['automne', 'hiver'], 2, ARRAY['gants', 'casque']),
('a4000000-0000-0000-0000-000000000022', 'compostage', 'Compostage', 'nature', 'Tri, compost, valorisation des déchets verts.', 60, ARRAY['geste_utile', 'hygiene'], ARRAY['toutes'], 1, ARRAY['gants']),
('a4000000-0000-0000-0000-000000000023', 'faune-locale', 'Observation de la faune locale', 'nature', 'Discrétion, repérage, traces/indices.', 60, ARRAY['patience', 'respect'], ARRAY['toutes'], 1, ARRAY[]),
('a4000000-0000-0000-0000-000000000024', 'nichoirs-hotels', 'Nichoirs & hôtels à insectes', 'nature', 'Concevoir, fabriquer, installer des abris.', 120, ARRAY['precision', 'pedagogie'], ARRAY['toutes'], 1, ARRAY['gants']),

-- Social
('a5000000-0000-0000-0000-000000000025', 'portes-ouvertes', 'Journée portes ouvertes', 'social', 'Préparer, accueillir, guider un public.', 180, ARRAY['accueil', 'organisation'], ARRAY['toutes'], 1, ARRAY[]),
('a5000000-0000-0000-0000-000000000026', 'visites-guidees', 'Visites guidées de la ferme', 'social', 'Présenter la ferme, répondre simplement.', 60, ARRAY['expression', 'pedagogie'], ARRAY['toutes'], 1, ARRAY[]),
('a5000000-0000-0000-0000-000000000027', 'ateliers-enfants', 'Ateliers pour enfants', 'social', 'Jeux, découvertes nature, mini-gestes encadrés.', 90, ARRAY['patience', 'creativite', 'securite'], ARRAY['toutes'], 2, ARRAY[]),
('a5000000-0000-0000-0000-000000000028', 'cuisine-collective', 'Cuisine collective (équipe)', 'social', 'Préparer un repas simple et bon.', 90, ARRAY['hygiene', 'equipe', 'temps'], ARRAY['toutes'], 1, ARRAY['tablier']),
('a5000000-0000-0000-0000-000000000029', 'gouter-fermier', 'Goûter fermier', 'social', 'Organisation, service, convivialité, propreté.', 60, ARRAY['rigueur', 'relationnel'], ARRAY['toutes'], 1, ARRAY['tablier']),
('a5000000-0000-0000-0000-000000000030', 'marche-local', 'Participation au marché local', 'social', 'Présentation produits, vente, échange avec les clients.', 240, ARRAY['commercial', 'relationnel'], ARRAY['toutes'], 1, ARRAY[]);