-- Données de test et d'amorçage pour La Vida Luca
-- À exécuter après le schéma principal

-- =====================================
-- Insertion des 30 activités MFR
-- =====================================

INSERT INTO public.activities (slug, title, category, summary, description, duration_min, skill_tags, seasonality, safety_level, materials) VALUES

-- Agriculture (6 activités)
('soins-animaux', 'Soins aux animaux', 'agri', 'Nourrir, observer, nettoyer les espaces de vie.', 'Apprentissage des soins quotidiens aux animaux de la ferme : alimentation, abreuvement, observation comportementale et nettoyage des espaces.', 120, ARRAY['douceur', 'observation', 'responsabilite'], ARRAY['toutes'], 1, ARRAY['bottes', 'gants']),

('cultures-maraicheres', 'Cultures maraîchères', 'agri', 'Préparer, semer, entretenir selon saison.', 'Initiation aux techniques de maraîchage : préparation du sol, semis, repiquage, entretien et récolte des légumes de saison.', 150, ARRAY['patience', 'observation', 'force'], ARRAY['printemps', 'ete', 'automne'], 1, ARRAY['gants', 'bottes', 'outils']),

('verger-entretien', 'Entretien du verger', 'agri', 'Taille douce, observation, cueillette respectueuse.', 'Soins aux arbres fruitiers : taille de formation, observation sanitaire, récolte et conservation des fruits.', 120, ARRAY['precision', 'hauteur', 'patience'], ARRAY['printemps', 'ete', 'automne'], 2, ARRAY['secateur', 'echelle', 'gants']),

('compost-dechets', 'Compost & gestion des déchets', 'agri', 'Tri, retournement, utilisation du compost.', 'Gestion écologique des déchets organiques : tri, constitution et entretien du compost, utilisation au jardin.', 90, ARRAY['organisation', 'ecologie', 'force'], ARRAY['toutes'], 1, ARRAY['gants', 'bottes']),

('prairie-paturage', 'Gestion prairie & pâturage', 'agri', 'Rotation, clôtures mobiles, observation.', 'Principes de gestion durable des prairies : rotation des animaux, entretien des clôtures, observation de la pousse.', 120, ARRAY['observation', 'planification', 'effort'], ARRAY['printemps', 'ete', 'automne'], 2, ARRAY['gants', 'outils']),

('clotures-abris', 'Gestion des clôtures & abris', 'agri', 'Identifier, réparer, sécuriser parcs et abris.', 'Maintenance des infrastructures : inspection, réparation des clôtures, entretien des abris à animaux.', 120, ARRAY['securite', 'bois', 'reparation'], ARRAY['toutes'], 2, ARRAY['gants', 'outils']),

-- Transformation (5 activités)
('fromage', 'Fabrication de fromage', 'transfo', 'Du lait au caillé : hygiène, moulage, affinage (découverte).', 'Initiation à la transformation laitière : pasteurisation, emprésurage, égouttage et bases de l''affinage.', 90, ARRAY['hygiene', 'precision', 'patience'], ARRAY['toutes'], 2, ARRAY['tablier', 'gants']),

('conserves', 'Confitures & conserves', 'transfo', 'Préparation, stérilisation, mise en pot, étiquetage.', 'Transformation des fruits et légumes : préparation, cuisson, stérilisation et conditionnement.', 90, ARRAY['organisation', 'hygiene', 'precision'], ARRAY['ete', 'automne'], 1, ARRAY['tablier', 'gants']),

('laine', 'Transformation de la laine', 'transfo', 'Lavage, cardage, petite création textile.', 'Découverte du travail de la laine : lavage, cardage, filage simple et petites créations textiles.', 90, ARRAY['patience', 'creativite', 'douceur'], ARRAY['toutes'], 1, ARRAY['tablier', 'gants']),

('jus', 'Fabrication de jus', 'transfo', 'Du verger à la bouteille : tri, pressage, filtration.', 'Transformation des fruits en jus : tri, lavage, pressage, filtration et conditionnement.', 90, ARRAY['hygiene', 'securite', 'organisation'], ARRAY['automne'], 2, ARRAY['tablier', 'gants']),

('aromatiques-sechage', 'Séchage d''herbes aromatiques', 'transfo', 'Cueillette, séchage, conditionnement doux.', 'Récolte et conservation des plantes aromatiques : cueillette, séchage naturel, conditionnement.', 60, ARRAY['douceur', 'organisation', 'patience'], ARRAY['ete'], 1, ARRAY['tablier']),

-- Artisanat (7 activités)
('bois-creation', 'Petite création bois', 'artisanat', 'Mesurer, découper, assembler des objets simples.', 'Initiation au travail du bois : mesure, découpe, assemblage de petits objets utilitaires.', 120, ARRAY['precision', 'securite', 'creativite'], ARRAY['toutes'], 2, ARRAY['lunettes', 'gants']),

('metal-forge', 'Initiation forge', 'artisanat', 'Chauffer, former, refroidir (sécurité maximale).', 'Découverte de la forge : chauffage, formage simple et refroidissement du métal sous supervision.', 90, ARRAY['securite', 'force', 'concentration'], ARRAY['toutes'], 3, ARRAY['tablier-cuir', 'lunettes', 'gants-cuir']),

('poterie-terre', 'Poterie & travail de la terre', 'artisanat', 'Modeler, tourner, sécher, comprendre l''argile.', 'Découverte de la céramique : modelage, initiation au tour, séchage et cuisson des pièces.', 120, ARRAY['creativite', 'patience', 'douceur'], ARRAY['toutes'], 1, ARRAY['tablier']),

('couture-textile', 'Couture & textile', 'artisanat', 'Réparer, créer, personnaliser avec les aiguilles.', 'Techniques de couture : réparation de vêtements, création de petits objets textiles.', 90, ARRAY['precision', 'patience', 'creativite'], ARRAY['toutes'], 1, ARRAY['des-a-coudre']),

('vannerie', 'Vannerie simple', 'artisanat', 'Tresser osier, rotin pour des objets pratiques.', 'Initiation à la vannerie : préparation de l''osier, techniques de tressage, création d''objets utiles.', 120, ARRAY['patience', 'dexterite', 'creativite'], ARRAY['automne', 'hiver'], 1, ARRAY['gants']),

('peinture-deco', 'Peinture & décoration d''espaces', 'artisanat', 'Préparer, protéger, peindre proprement.', 'Techniques de peinture et décoration : préparation des supports, application soignée.', 90, ARRAY['proprete', 'finitions', 'esthetique'], ARRAY['toutes'], 1, ARRAY['tablier', 'gants']),

('amenagement-verts', 'Aménagement d''espaces verts', 'artisanat', 'Désherbage doux, paillage, plantations.', 'Création et entretien d''espaces verts : désherbage écologique, paillage, plantations.', 90, ARRAY['endurance', 'esthetique', 'ecologie'], ARRAY['printemps', 'ete'], 1, ARRAY['gants', 'bottes']),

('panneaux-orientation', 'Panneaux & orientation', 'artisanat', 'Concevoir/poser une signalétique claire.', 'Conception et installation de signalétique : design, fabrication et pose de panneaux.', 90, ARRAY['clarte', 'precision', 'esthetique'], ARRAY['toutes'], 1, ARRAY['gants']),

-- Nature (7 activités)
('entretien-riviere', 'Entretien de la rivière', 'nature', 'Nettoyage doux, observation des berges.', 'Préservation des milieux aquatiques : nettoyage respectueux, observation de la biodiversité.', 90, ARRAY['prudence', 'ecologie', 'observation'], ARRAY['printemps', 'ete'], 2, ARRAY['bottes', 'gants']),

('foret-entretien', 'Entretien forestier', 'nature', 'Débroussaillage, sentiers, observation faune.', 'Gestion douce des espaces forestiers : entretien des sentiers, observation de la faune et flore.', 120, ARRAY['endurance', 'observation', 'prudence'], ARRAY['automne', 'hiver'], 2, ARRAY['bottes', 'gants']),

('haies-biodiversite', 'Plantation de haies & biodiversité', 'nature', 'Essences locales, technique, arrosage.', 'Création de corridors écologiques : sélection d''essences, plantation et entretien des haies.', 120, ARRAY['ecologie', 'patience', 'planification'], ARRAY['automne', 'hiver'], 1, ARRAY['gants', 'bottes']),

('mare-ecosystem', 'Création d''une mare', 'nature', 'Creuser, étanchéifier, planter, observer.', 'Aménagement d''un écosystème aquatique : conception, creusement, plantation d''espèces adaptées.', 180, ARRAY['effort', 'ecologie', 'patience'], ARRAY['printemps'], 2, ARRAY['bottes', 'gants']),

('ruches-apiculture', 'Initiation apiculture', 'nature', 'Observer, enfumer, récolter avec protection.', 'Découverte de l''apiculture : observation des ruches, manipulation douce, récolte du miel.', 90, ARRAY['calme', 'douceur', 'observation'], ARRAY['printemps', 'ete'], 3, ARRAY['combinaison', 'enfumoir']),

('plantes-medicinales', 'Reconnaissance plantes médicinales', 'nature', 'Identifier, cueillir, sécher selon règles.', 'Botanique appliquée : identification, cueillette raisonnée et conservation des plantes médicinales.', 90, ARRAY['observation', 'memoire', 'respect'], ARRAY['printemps', 'ete'], 1, ARRAY['carnet', 'loupe']),

('meteo-observation', 'Observation météo & climat', 'nature', 'Mesurer, noter, comprendre les cycles.', 'Météorologie pratique : observation, mesure et compréhension des phénomènes climatiques.', 60, ARRAY['observation', 'rigueur', 'patience'], ARRAY['toutes'], 1, ARRAY['carnet']),

-- Social (5 activités)
('accueil-groupes', 'Accueil de groupes', 'social', 'Présenter, guider, faire participer.', 'Animation et accueil : présentation du projet, guidage de visites, animation d''ateliers.', 120, ARRAY['communication', 'pedagogie', 'enthousiasme'], ARRAY['toutes'], 1, ARRAY[]),

('marche-local', 'Participation marché local', 'social', 'Vendre, expliquer, créer du lien.', 'Commercialisation et lien social : vente de produits, explication des méthodes, création de liens.', 180, ARRAY['communication', 'commercial', 'sourire'], ARRAY['toutes'], 1, ARRAY[]),

('cuisine-collective', 'Cuisine collective', 'social', 'Préparer, partager, nettoyer ensemble.', 'Préparation de repas en groupe : planification, cuisson, service et nettoyage collaboratif.', 150, ARRAY['cooperation', 'hygiene', 'organisation'], ARRAY['toutes'], 1, ARRAY['tablier']),

('documentation-photos', 'Documentation & photos', 'social', 'Photographier, écrire, témoigner.', 'Communication du projet : prise de photos, rédaction de témoignages, documentation des activités.', 90, ARRAY['creativite', 'communication', 'technique'], ARRAY['toutes'], 1, ARRAY['appareil-photo']),

('planification-collective', 'Planification collective', 'social', 'Organiser, programmer, répartir les tâches.', 'Organisation participative : planification des activités, répartition des tâches, suivi collectif.', 120, ARRAY['organisation', 'communication', 'leadership'], ARRAY['toutes'], 1, ARRAY['tableau', 'marqueurs']);

-- =====================================
-- Lieux d'action par défaut
-- =====================================

INSERT INTO public.locations (name, address, departement, region, type, description, capacity, active) VALUES

('Ferme pédagogique La Vida Luca - Site principal', '14 Route de la Ferme, 14000 Caen', 'Calvados (14)', 'Normandie', 'ferme', 'Site principal du projet La Vida Luca. Formation, hébergement et coordination générale.', 30, true),

('MFR Partenaire Calvados', 'Route de l''Education, 14100 Lisieux', 'Calvados (14)', 'Normandie', 'mfr', 'Maison Familiale Rurale partenaire pour l''accueil des jeunes en formation.', 25, true),

('Relais Bretagne - Finistère', 'Lieu-dit Kerguelen, 29000 Quimper', 'Finistère (29)', 'Bretagne', 'relais', 'Relais régional pour les activités marines et l''agriculture littorale.', 15, true),

('Ferme bio partenaire - Orne', 'La Grande Ferme, 61000 Alençon', 'Orne (61)', 'Normandie', 'partenaire', 'Ferme biologique partenaire spécialisée en maraîchage et élevage.', 20, true);

-- =====================================
-- Données de test pour le développement
-- =====================================

-- Contact de test (sera visible côté admin)
INSERT INTO public.contact_requests (full_name, email, phone, message, type) VALUES
('Jean Dupont', 'jean.dupont@example.com', '0123456789', 'Bonjour, je souhaite en savoir plus sur le projet La Vida Luca et les possibilités de formation pour mon fils.', 'general'),
('Marie Martin', 'marie.martin@example.com', '0654321098', 'Je représente une MFR et nous aimerions devenir partenaires de votre projet.', 'partenariat'),
('Pierre Durand', 'pierre.durand@example.com', null, 'Comment puis-je devenir relais La Vida Luca dans ma région ?', 'rejoindre');