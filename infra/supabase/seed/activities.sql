-- Seed Data: Activities for La Vida Luca
-- Description: Insert all 30 educational agricultural activities
-- Date: 2025-01-19

BEGIN;

-- Clear existing data (for development/reset)
DELETE FROM activity_registrations;
DELETE FROM activities;

-- Insert all 30 activities from the frontend catalogue
INSERT INTO activities (activity_id, slug, title, category, summary, description, duration_min, skill_tags, seasonality, safety_level, materials, max_participants, min_age) VALUES 

-- Agriculture Activities (1-6)
('1', 'nourrir-soigner-moutons', 'Nourrir et soigner les moutons', 'agri', 'Gestes quotidiens : alimentation, eau, observation.', 'Apprentissage des soins quotidiens aux moutons : distribution de foin et granulés, vérification de l''eau, observation comportementale et détection des signes de maladie.', 60, '["elevage", "responsabilite"]', '["toutes"]', 1, '["bottes", "gants"]', 6, 14),

('2', 'tonte-entretien-troupeau', 'Tonte & entretien du troupeau', 'agri', 'Hygiène, tonte (démo), soins courants.', 'Initiation à la tonte des moutons avec démonstration, hygiène du troupeau, parage des onglons et soins vétérinaires de base.', 90, '["elevage", "hygiene"]', '["printemps"]', 2, '["bottes", "gants"]', 4, 16),

('3', 'basse-cour-soins', 'Soins basse-cour', 'agri', 'Poules/canards/lapins : alimentation, abris, propreté.', 'Soins quotidiens aux animaux de basse-cour : alimentation adaptée, nettoyage des abris, collecte des œufs et observation sanitaire.', 60, '["soins_animaux"]', '["toutes"]', 1, '["bottes", "gants"]', 8, 12),

('4', 'plantation-cultures', 'Plantation de cultures', 'agri', 'Semis, arrosage, paillage, suivi de plants.', 'Initiation au maraîchage : préparation du sol, semis en pleine terre, techniques d''arrosage, paillage naturel et suivi de croissance.', 90, '["sol", "plantes"]', '["printemps", "ete"]', 1, '["gants"]', 10, 14),

('5', 'init-maraichage', 'Initiation maraîchage', 'agri', 'Plan de culture, entretien, récolte respectueuse.', 'Découverte complète du maraîchage bio : planification des cultures, rotation, associations de plantes, entretien et récolte respectueuse.', 120, '["sol", "organisation"]', '["printemps", "ete", "automne"]', 1, '["gants", "bottes"]', 8, 16),

('6', 'clotures-abris', 'Gestion des clôtures & abris', 'agri', 'Identifier, réparer, sécuriser parcs et abris.', 'Maintenance des infrastructures d''élevage : inspection des clôtures, réparation des barrières, sécurisation des parcs et entretien des abris.', 120, '["securite", "bois"]', '["toutes"]', 2, '["gants"]', 6, 16),

-- Transformation Activities (7-12)
('7', 'fromage', 'Fabrication de fromage', 'transfo', 'Du lait au caillé : hygiène, moulage, affinage (découverte).', 'Initiation à la fromagerie : pasteurisation du lait, ajout de présure, découpage du caillé, moulage et introduction aux techniques d''affinage.', 90, '["hygiene", "precision"]', '["toutes"]', 2, '["tablier"]', 6, 16),

('8', 'conserves', 'Confitures & conserves', 'transfo', 'Préparation, stérilisation, mise en pot, étiquetage.', 'Transformation des fruits de saison : préparation, cuisson, stérilisation des bocaux, mise en pot et étiquetage selon les normes.', 90, '["organisation", "hygiene"]', '["ete", "automne"]', 1, '["tablier"]', 8, 14),

('9', 'laine', 'Transformation de la laine', 'transfo', 'Lavage, cardage, petite création textile.', 'Valorisation de la laine de mouton : lavage dégraissage, cardage manuel, filage simple et réalisation d''un petit objet textile.', 90, '["patience", "creativite"]', '["toutes"]', 1, '["tablier", "gants"]', 6, 14),

('10', 'jus', 'Fabrication de jus', 'transfo', 'Du verger à la bouteille : tri, pressage, filtration.', 'Circuit complet du jus de pomme : cueillette, tri des fruits, broyage, pressage, filtration et mise en bouteille artisanale.', 90, '["hygiene", "securite"]', '["automne"]', 2, '["tablier", "gants"]', 6, 16),

('11', 'aromatiques-sechage', 'Séchage d''herbes aromatiques', 'transfo', 'Cueillette, séchage, conditionnement doux.', 'Valorisation des plantes aromatiques : identification, cueillette au bon moment, techniques de séchage naturel et conditionnement.', 60, '["douceur", "organisation"]', '["ete"]', 1, '["tablier"]', 8, 12),

('12', 'pain-four-bois', 'Pain au four à bois', 'transfo', 'Pétrissage, façonnage, cuisson : respect des temps.', 'Boulangerie traditionnelle : préparation de la pâte, pétrissage, façonnage des pains, allumage du four à bois et cuisson.', 120, '["precision", "rythme"]', '["toutes"]', 2, '["tablier"]', 6, 16),

-- Artisanat Activities (13-18)
('13', 'abris-bois', 'Construction d''abris', 'artisanat', 'Petites structures bois : plan, coupe, assemblage.', 'Menuiserie de base : lecture de plans simples, coupe du bois, techniques d''assemblage et construction de petits abris pour animaux.', 120, '["bois", "precision", "securite"]', '["toutes"]', 2, '["gants"]', 4, 16),

('14', 'reparation-outils', 'Réparation & entretien des outils', 'artisanat', 'Affûtage, graissage, petites réparations.', 'Maintenance du matériel agricole : affûtage des outils de coupe, graissage des mécanismes, petites réparations et rangement.', 60, '["autonomie", "responsabilite"]', '["toutes"]', 1, '["gants"]', 6, 14),

('15', 'menuiserie-simple', 'Menuiserie simple', 'artisanat', 'Mesure, coupe, ponçage, finitions d''un objet.', 'Projet de menuiserie : mesures précises, coupe du bois, ponçage, assemblage et finitions pour créer un objet utile à la ferme.', 120, '["precision", "creativite"]', '["toutes"]', 2, '["gants", "lunettes"]', 6, 16),

('16', 'peinture-deco', 'Peinture & décoration d''espaces', 'artisanat', 'Préparer, protéger, peindre proprement.', 'Rénovation d''espaces : préparation des surfaces, protection, application de peinture et décoration des bâtiments de la ferme.', 90, '["proprete", "finitions"]', '["toutes"]', 1, '["tablier", "gants"]', 8, 14),

('17', 'amenagement-verts', 'Aménagement d''espaces verts', 'artisanat', 'Désherbage doux, paillage, plantations.', 'Paysagisme écologique : désherbage manuel, paillage naturel, plantations ornementales et aménagement d''espaces de détente.', 90, '["endurance", "esthetique"]', '["printemps", "ete"]', 1, '["gants", "bottes"]', 8, 14),

('18', 'panneaux-orientation', 'Panneaux & orientation', 'artisanat', 'Concevoir/poser une signalétique claire.', 'Communication visuelle : conception de panneaux informatifs, découpe, peinture et installation d''une signalétique claire pour la ferme.', 90, '["clarte", "precision"]', '["toutes"]', 1, '["gants"]', 6, 14),

-- Nature Activities (19-24)
('19', 'entretien-riviere', 'Entretien de la rivière', 'nature', 'Nettoyage doux, observation des berges.', 'Gestion écologique des cours d''eau : nettoyage respectueux, observation de la faune aquatique, entretien des berges et sensibilisation environnementale.', 90, '["prudence", "ecologie"]', '["printemps", "ete"]', 2, '["bottes", "gants"]', 6, 16),

('20', 'plantation-arbres', 'Plantation d''arbres', 'nature', 'Choix d''essences, tuteurage, paillage, suivi.', 'Agroforesterie : sélection d''espèces locales, techniques de plantation, tuteurage, paillage et planification du suivi à long terme.', 120, '["geste_juste", "endurance"]', '["automne", "hiver"]', 1, '["gants", "bottes"]', 8, 14),

('21', 'potager-eco', 'Potager écologique', 'nature', 'Associations, paillis, rotation des cultures.', 'Permaculture appliquée : associations de légumes, techniques de paillage, rotation des cultures et création d''un écosystème équilibré.', 90, '["observation", "sobriete"]', '["printemps", "ete", "automne"]', 1, '["gants"]', 8, 14),

('22', 'compostage', 'Compostage', 'nature', 'Tri, compost, valorisation des déchets verts.', 'Cycle des matières organiques : tri des déchets, techniques de compostage, retournement et utilisation du compost mûr au jardin.', 60, '["geste_utile", "hygiene"]', '["toutes"]', 1, '["gants"]', 10, 12),

('23', 'faune-locale', 'Observation de la faune locale', 'nature', 'Discrétion, repérage, traces/indices.', 'Découverte naturaliste : techniques d''observation discrète, identification des espèces locales, relevé de traces et indices de présence.', 60, '["patience", "respect"]', '["toutes"]', 1, '[]', 12, 10),

('24', 'nichoirs-hotels', 'Nichoirs & hôtels à insectes', 'nature', 'Concevoir, fabriquer, installer des abris.', 'Biodiversité pratique : conception de nichoirs adaptés, fabrication d''hôtels à insectes, installation stratégique et suivi des occupants.', 120, '["precision", "pedagogie"]', '["toutes"]', 1, '["gants"]', 8, 14),

-- Social Activities (25-30)
('25', 'portes-ouvertes', 'Journée portes ouvertes', 'social', 'Préparer, accueillir, guider un public.', 'Animation événementielle : préparation logistique, accueil du public, visites guidées et présentation des activités de la ferme.', 180, '["accueil", "organisation"]', '["toutes"]', 1, '[]', 15, 16),

('26', 'visites-guidees', 'Visites guidées de la ferme', 'social', 'Présenter la ferme, répondre simplement.', 'Médiation culturelle : préparation d''un parcours de visite, techniques de présentation orale et interaction avec différents publics.', 60, '["expression", "pedagogie"]', '["toutes"]', 1, '[]', 12, 16),

('27', 'ateliers-enfants', 'Ateliers pour enfants', 'social', 'Jeux, découvertes nature, mini-gestes encadrés.', 'Pédagogie active : animation d''ateliers ludiques, activités sensorielles nature, gestes agricoles adaptés et sécurité enfants.', 90, '["patience", "creativite", "securite"]', '["toutes"]', 2, '[]', 8, 18),

('28', 'cuisine-collective', 'Cuisine collective (équipe)', 'social', 'Préparer un repas simple et bon.', 'Restauration collective : planification des menus, préparation en équipe, cuisson de produits de la ferme et service.', 90, '["hygiene", "equipe", "temps"]', '["toutes"]', 1, '["tablier"]', 10, 16),

('29', 'gouter-fermier', 'Goûter fermier', 'social', 'Organisation, service, convivialité, propreté.', 'Accueil gourmand : préparation de collations avec les produits de la ferme, mise en place, service et animation conviviale.', 60, '["rigueur", "relationnel"]', '["toutes"]', 1, '["tablier"]', 12, 14),

('30', 'marche-local', 'Participation à un marché local', 'social', 'Stand, présentation, caisse symbolique (simulation).', 'Vente directe simulée : préparation du stand, présentation des produits, interaction commerciale et gestion de caisse en situation réelle.', 180, '["contact", "compter_simple", "equipe"]', '["toutes"]', 1, '[]', 6, 16);

-- Verification
SELECT 
    COUNT(*) as total_activities,
    COUNT(CASE WHEN category = 'agri' THEN 1 END) as agriculture,
    COUNT(CASE WHEN category = 'transfo' THEN 1 END) as transformation,
    COUNT(CASE WHEN category = 'artisanat' THEN 1 END) as artisanat,
    COUNT(CASE WHEN category = 'nature' THEN 1 END) as nature,
    COUNT(CASE WHEN category = 'social' THEN 1 END) as social
FROM activities;

COMMIT;