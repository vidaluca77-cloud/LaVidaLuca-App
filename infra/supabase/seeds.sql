-- =====================================================
-- SEEDS SQL POUR LA VIDA LUCA  
-- =====================================================
-- Données initiales pour la plateforme La Vida Luca
-- À exécuter APRÈS schema.sql

-- =====================================================
-- DONNÉES: Locations (Lieux d'action)
-- =====================================================

INSERT INTO public.locations (id, name, slug, address, city, department, region, description, contact_email, contact_phone, facilities, activities_offered, status) VALUES
(uuid_generate_v4(), 'Ferme pédagogique de Normandie', 'ferme-normandie', '123 Route des Champs', 'Caen', 'Calvados (14)', 'Normandie', 'Ferme pédagogique dédiée à la formation des jeunes en agriculture durable et élevage responsable.', 'contact@ferme-normandie.fr', '02.31.XX.XX.XX', ARRAY['étables', 'fromagerie', 'potager', 'salle de cours', 'parking'], ARRAY['agri', 'transfo', 'nature'], 'active'),

(uuid_generate_v4(), 'Atelier artisanal du Bocage', 'atelier-bocage', '45 Rue de l''Artisan', 'Vire', 'Calvados (14)', 'Normandie', 'Atelier spécialisé dans l''artisanat traditionnel et la menuiserie écologique.', 'atelier@bocage-artisan.fr', '02.31.XX.XX.XX', ARRAY['atelier bois', 'forge', 'salle polyvalente'], ARRAY['artisanat', 'social'], 'active'),

(uuid_generate_v4(), 'Espace Nature Rivière', 'espace-nature-riviere', 'Lieu-dit La Rivière', 'Bayeux', 'Calvados (14)', 'Normandie', 'Site naturel pour les activités d''environnement et de préservation de la biodiversité.', 'nature@riviere-bayeux.fr', '02.31.XX.XX.XX', ARRAY['sentiers', 'observatoire', 'point d''eau'], ARRAY['nature', 'social'], 'active');

-- =====================================================
-- DONNÉES: Activities (Catalogue des 30 activités)
-- =====================================================

-- Agriculture (6 activités)
INSERT INTO public.activities (id, slug, title, category, summary, description, duration_min, skill_tags, seasonality, safety_level, materials, max_participants, min_age) VALUES

(uuid_generate_v4(), 'traite-soins-bovins', 'Traite & soins aux bovins', 'agri', 'Apprendre la traite manuelle/mécanique et les soins de base.', 'Formation complète à la traite des vaches laitières, incluant l''hygiène, les techniques de traite manuelle et mécanique, ainsi que les soins quotidiens aux bovins. Apprentissage de l''observation animale et des gestes de base.', 120, ARRAY['elevage', 'hygiene', 'observation'], ARRAY['toutes'], 2, ARRAY['bottes', 'gants', 'tablier'], 8, 14),

(uuid_generate_v4(), 'tonte-entretien-troupeau', 'Tonte & entretien du troupeau', 'agri', 'Hygiène, tonte (démo), soins courants.', 'Démonstration de tonte ovine et apprentissage des soins d''hygiène pour le troupeau. Observation du comportement animal et gestes de contention douce.', 90, ARRAY['elevage', 'hygiene'], ARRAY['printemps'], 2, ARRAY['bottes', 'gants'], 6, 15),

(uuid_generate_v4(), 'basse-cour-soins', 'Soins basse-cour', 'agri', 'Poules/canards/lapins : alimentation, abris, propreté.', 'Gestion quotidienne de la basse-cour : alimentation adaptée, nettoyage des habitats, observation sanitaire des volailles et lapins.', 60, ARRAY['soins_animaux'], ARRAY['toutes'], 1, ARRAY['bottes', 'gants'], 10, 12),

(uuid_generate_v4(), 'cultures-legumes', 'Cultures de légumes', 'agri', 'Semis, repiquage, entretien, récolte selon saison.', 'Cycle complet de production légumière : préparation du sol, semis, repiquage, entretien cultural, lutte naturelle contre les parasites, récolte et conservation.', 150, ARRAY['jardinage', 'patience'], ARRAY['printemps', 'ete', 'automne'], 1, ARRAY['gants', 'outils jardin'], 12, 13),

(uuid_generate_v4(), 'prairie-fourrage', 'Gestion prairie & fourrage', 'agri', 'Fauche, stockage, analyse qualité des fourrages.', 'Techniques de fauche, de séchage et de stockage des fourrages. Évaluation de la qualité nutritive et gestion des prairies pour l''alimentation animale.', 120, ARRAY['mecanique', 'plein_air'], ARRAY['ete'], 2, ARRAY['bottes', 'gants'], 8, 16),

(uuid_generate_v4(), 'clotures-abris', 'Gestion des clôtures & abris', 'agri', 'Identifier, réparer, sécuriser parcs et abris.', 'Maintenance et réparation des infrastructures d''élevage : clôtures, barrières, abris. Techniques de base en bricolage rural et sécurisation.', 120, ARRAY['securite', 'bois'], ARRAY['toutes'], 2, ARRAY['gants'], 6, 15);

-- Transformation (5 activités)  
INSERT INTO public.activities (slug, title, category, summary, description, duration_min, skill_tags, seasonality, safety_level, materials, max_participants, min_age) VALUES

('fromage', 'Fabrication de fromage', 'transfo', 'Du lait au caillé : hygiène, moulage, affinage (découverte).', 'Initiation à la transformation fromagère : pasteurisation, emprésurage, moulage et découverte de l''affinage. Respect strict des règles d''hygiène alimentaire.', 90, ARRAY['hygiene', 'precision'], ARRAY['toutes'], 2, ARRAY['tablier'], 6, 14),

('conserves', 'Confitures & conserves', 'transfo', 'Préparation, stérilisation, mise en pot, étiquetage.', 'Techniques de conservation des fruits et légumes : préparation, cuisson, stérilisation et conditionnement. Respect des normes d''hygiène et étiquetage.', 90, ARRAY['organisation', 'hygiene'], ARRAY['ete', 'automne'], 1, ARRAY['tablier'], 8, 13),

('laine', 'Transformation de la laine', 'transfo', 'Lavage, cardage, petite création textile.', 'Processus de transformation de la laine brute : lavage, cardage, peignage et initiation au filage. Création de petits objets textiles.', 90, ARRAY['patience', 'creativite'], ARRAY['toutes'], 1, ARRAY['tablier', 'gants'], 8, 12),

('jus', 'Fabrication de jus', 'transfo', 'Du verger à la bouteille : tri, pressage, filtration.', 'Production de jus de fruits : tri des fruits, pressage, filtration et mise en bouteille. Hygiène alimentaire et conservation naturelle.', 90, ARRAY['hygiene', 'securite'], ARRAY['automne'], 2, ARRAY['tablier', 'gants'], 8, 14),

('aromatiques-sechage', 'Séchage d''herbes aromatiques', 'transfo', 'Cueillette, séchage, conditionnement doux.', 'Cueillette raisonnée d''herbes aromatiques, techniques de séchage traditionnel et conditionnement pour la conservation.', 60, ARRAY['douceur', 'organisation'], ARRAY['ete'], 1, ARRAY['tablier'], 10, 12);

-- Artisanat (6 activités)
INSERT INTO public.activities (slug, title, category, summary, description, duration_min, skill_tags, seasonality, safety_level, materials, max_participants, min_age) VALUES

('menuiserie-base', 'Menuiserie de base', 'artisanat', 'Mesures, découpe, assemblage de petits objets.', 'Initiation aux techniques de menuiserie : utilisation des outils de base, mesures précises, découpe et assemblage de petits objets utilitaires.', 120, ARRAY['precision', 'outils'], ARRAY['toutes'], 3, ARRAY['gants', 'lunettes'], 6, 15),

('poterie', 'Poterie & céramique', 'artisanat', 'Modelage, tournage (découverte), cuisson.', 'Découverte de l''art de la poterie : préparation de l''argile, techniques de modelage, initiation au tournage et processus de cuisson.', 120, ARRAY['creativite', 'patience'], ARRAY['toutes'], 2, ARRAY['tablier'], 8, 12),

('vannerie', 'Vannerie traditionnelle', 'artisanat', 'Osier, rotin : techniques de tressage ancestrales.', 'Apprentissage des techniques traditionnelles de vannerie : préparation de l''osier, tressages de base et création de paniers utilitaires.', 150, ARRAY['patience', 'dexterite'], ARRAY['automne', 'hiver'], 1, ARRAY['gants'], 8, 13),

('forge', 'Initiation à la forge', 'artisanat', 'Sécurité, feu, façonnage métal (démo/simple).', 'Découverte de la forge traditionnelle : allumage du feu, sécurité, démonstration de façonnage et réalisation d''objets simples.', 90, ARRAY['securite', 'force'], ARRAY['toutes'], 3, ARRAY['gants', 'lunettes'], 4, 16),

('couture-reparation', 'Couture & réparation textile', 'artisanat', 'Points de base, reprise, création d''accessoires.', 'Techniques de couture de base : points essentiels, réparation de vêtements et création de petits accessoires utiles.', 90, ARRAY['precision', 'patience'], ARRAY['toutes'], 1, ARRAY[], 10, 12),

('panneaux-orientation', 'Panneaux & orientation', 'artisanat', 'Concevoir/poser une signalétique claire.', 'Création de panneaux de signalisation : conception graphique, découpe, peinture et installation pour l''orientation sur site.', 90, ARRAY['clarte', 'precision'], ARRAY['toutes'], 1, ARRAY['gants'], 8, 14);

-- Nature/Environnement (6 activités)
INSERT INTO public.activities (slug, title, category, summary, description, duration_min, skill_tags, seasonality, safety_level, materials, max_participants, min_age) VALUES

('entretien-riviere', 'Entretien de la rivière', 'nature', 'Nettoyage doux, observation des berges.', 'Entretien écologique des cours d''eau : nettoyage respectueux, observation de la faune et flore aquatique, préservation des berges.', 90, ARRAY['prudence', 'ecologie'], ARRAY['printemps', 'ete'], 2, ARRAY['bottes', 'gants'], 10, 14),

('compostage', 'Compostage & sols', 'nature', 'Déchets verts, retournement, amendement terre.', 'Techniques de compostage : tri des déchets organiques, gestion des tas de compost, utilisation pour l''amendement des sols.', 60, ARRAY['ecologie', 'organisation'], ARRAY['toutes'], 1, ARRAY['gants'], 12, 12),

('plantation-arbres', 'Plantation d''arbres', 'nature', 'Choix essence, techniques, suivi croissance.', 'Plantation raisonnée d''arbres : choix des essences adaptées, techniques de plantation, protection et suivi de croissance.', 120, ARRAY['ecologie', 'planification'], ARRAY['automne', 'hiver'], 1, ARRAY['gants', 'bêche'], 10, 13),

('observation-faune', 'Observation de la faune', 'nature', 'Discrétion, reconnaissance, carnet naturaliste.', 'Apprentissage de l''observation naturaliste : techniques discrètes, reconnaissance des espèces, tenue d''un carnet de terrain.', 90, ARRAY['patience', 'observation'], ARRAY['toutes'], 1, ARRAY[], 8, 12),

('ruches-abeilles', 'Ruches & abeilles (observation)', 'nature', 'Sécurité, cycle abeille, rôle pollinisation.', 'Découverte de l''apiculture : observation sécurisée des ruches, cycle de vie des abeilles, importance de la pollinisation.', 60, ARRAY['prudence', 'observation'], ARRAY['printemps', 'ete'], 2, ARRAY['combinaison'], 6, 14),

('nichoirs-hotels', 'Nichoirs & hôtels à insectes', 'nature', 'Concevoir, fabriquer, installer des abris.', 'Construction d''abris pour la faune : conception de nichoirs et hôtels à insectes, choix des matériaux, installation et suivi.', 120, ARRAY['precision', 'pedagogie'], ARRAY['toutes'], 1, ARRAY['gants'], 8, 12);

-- Social/Animation (7 activités)
INSERT INTO public.activities (slug, title, category, summary, description, duration_min, skill_tags, seasonality, safety_level, materials, max_participants, min_age) VALUES

('portes-ouvertes', 'Journée portes ouvertes', 'social', 'Préparer, accueillir, guider un public.', 'Organisation d''événements d''accueil : préparation des espaces, techniques d''accueil, guidage de groupes et présentation pédagogique.', 180, ARRAY['accueil', 'organisation'], ARRAY['toutes'], 1, ARRAY[], 15, 14),

('visite-guidee', 'Visite guidée éducative', 'social', 'Parcours thématique, explications, interaction.', 'Animation de visites thématiques : élaboration de parcours, techniques d''explication et d''interaction avec différents publics.', 90, ARRAY['pedagogie', 'expression'], ARRAY['toutes'], 1, ARRAY[], 12, 15),

('atelier-enfants', 'Animation enfants', 'social', 'Activités ludiques, sécurité, patience.', 'Animation d''ateliers adaptés aux jeunes enfants : conception d''activités ludiques et éducatives, gestion de groupe et sécurité.', 120, ARRAY['patience', 'ludique'], ARRAY['toutes'], 1, ARRAY[], 20, 16),

('cuisine-collective', 'Cuisine collective', 'social', 'Préparer un repas pour le groupe, partage.', 'Organisation de repas collectifs : planification des menus, préparation en équipe, partage convivial et nettoyage.', 150, ARRAY['organisation', 'equipe'], ARRAY['toutes'], 2, ARRAY['tablier'], 15, 13),

('reportage-photo', 'Reportage photo/vidéo', 'social', 'Documenter les activités, montage simple.', 'Documentation visuelle des activités : prise de vues, techniques de base en photographie et montage simple pour valorisation.', 120, ARRAY['creativite', 'technique'], ARRAY['toutes'], 1, ARRAY[], 8, 15),

('marche-local', 'Participation à un marché local', 'social', 'Stand, présentation, caisse symbolique (simulation).', 'Simulation de participation à un marché local : installation d''un stand, présentation des produits, interaction avec le public.', 180, ARRAY['contact', 'compter_simple', 'equipe'], ARRAY['toutes'], 1, ARRAY[], 12, 14),

('evenement-ferme', 'Organisation d''événement à la ferme', 'social', 'Planifier, coordonner, animer une manifestation.', 'Gestion complète d''événement : planification, coordination logistique, animation et évaluation d''une manifestation à la ferme.', 240, ARRAY['organisation', 'leadership', 'equipe'], ARRAY['toutes'], 1, ARRAY[], 20, 16);

-- =====================================================
-- DONNÉES: Catalog Items (Catalogue produits/services)
-- =====================================================

INSERT INTO public.catalog_items (slug, title, description, price, category, department, tags, status) VALUES

-- Produits vivants
('agneau-broutard', 'Agneau broutard (vivant)', 'Réservation locale, qualité élevée.', '299 € TTC', 'Produits vivants', 'Calvados (14)', ARRAY['local', 'réservation'], 'available'),
('plants-arbres', 'Plants & arbres (saison)', 'Variétés locales selon stock.', 'Selon stock', 'Produits vivants', 'Calvados (14)', ARRAY['pépinière'], 'seasonal'),

-- Activités terrain  
('journee-decouverte', 'Journée découverte ferme', 'Publics jeunes, familles, structures.', 'Prix libre', 'Activités terrain', 'Calvados (14)', ARRAY['groupes'], 'available'),
('stage-weekend', 'Stage week-end agriculture', 'Formation pratique sur 2 jours.', '150 € par personne', 'Activités terrain', 'Calvados (14)', ARRAY['formation'], 'available'),

-- Services
('visite-pedagogique', 'Visite pédagogique MFR/lycées', 'Accueil encadré, objectifs pédagogiques.', 'Sur devis', 'Services', 'Calvados (14)', ARRAY['éducation'], 'available'),
('conseil-installation', 'Conseil installation agricole', 'Accompagnement projet jeune agriculteur.', 'Sur devis', 'Services', 'National', ARRAY['conseil'], 'available'),

-- Dons en nature
('dons-nature', 'Dons en nature', 'Matériel agricole, plants, clôtures, caméras…', '—', 'Dons en nature', 'National', ARRAY['partenariat'], 'available'),
('benevola-competences', 'Bénévolat de compétences', 'Expertise technique, administrative, pédagogique.', '—', 'Dons en nature', 'National', ARRAY['bénévolat'], 'available');

-- =====================================================
-- PROFIL ADMIN PAR DÉFAUT (à adapter)
-- =====================================================
-- Note: Ces données ne peuvent être insérées qu'après création d'un utilisateur via auth
-- Exemple de profil admin - à adapter selon l'authentification mise en place

-- INSERT INTO public.profiles (id, email, full_name, role, bio, skills, location, status) VALUES
-- ('xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', 'admin@lavidaluca.fr', 'Administrateur La Vida Luca', 'admin', 'Coordinateur du projet La Vida Luca', ARRAY['gestion', 'pedagogie', 'agriculture'], 'Calvados (14)', 'active');

-- =====================================================
-- COMMENTAIRES ET INSTRUCTIONS
-- =====================================================

-- Après exécution de ce script :
-- 1. Créer un utilisateur admin via l'interface Supabase Auth
-- 2. Mettre à jour la table profiles avec les bonnes informations
-- 3. Configurer les variables d'environnement dans l'application
-- 4. Tester les policies RLS avec différents profils utilisateur

-- Variables d'environnement recommandées :
-- NEXT_PUBLIC_SUPABASE_URL=votre_url_supabase  
-- NEXT_PUBLIC_SUPABASE_ANON_KEY=votre_clé_anonyme
-- NEXT_PUBLIC_IA_API_URL=url_de_votre_api_ia_render
-- NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
-- NEXT_PUBLIC_CONTACT_PHONE=+33.XX.XX.XX.XX