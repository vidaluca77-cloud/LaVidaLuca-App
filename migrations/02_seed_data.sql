-- migrations/02_seed_data.sql
-- Seed data for La Vida Luca project

-- Insert activity categories
INSERT INTO activity_categories (name, description, color) VALUES
('Agriculture', 'Activités liées à l''agriculture durable et autonome', '#10b981'),
('Artisanat', 'Activités artisanales et création manuelle', '#f59e0b'),
('Environnement', 'Activités environnementales et écologiques', '#22c55e'),
('Formation', 'Modules de formation et apprentissage', '#3b82f6'),
('Insertion', 'Activités d''insertion sociale et professionnelle', '#8b5cf6');

-- Insert sample activities (30 activities as mentioned in the catalog)
INSERT INTO activities (title, description, duration, category) VALUES
-- Agriculture (10 activities)
('Maraîchage biologique', 'Apprentissage des techniques de maraîchage en agriculture biologique', 240, 'Agriculture'),
('Permaculture', 'Initiation aux principes et pratiques de la permaculture', 180, 'Agriculture'),
('Élevage de poules pondeuses', 'Gestion d''un poulailler et production d''œufs', 120, 'Agriculture'),
('Apiculture', 'Introduction à l''élevage d''abeilles et production de miel', 300, 'Agriculture'),
('Compostage et fertilisation', 'Techniques de compostage et création d''engrais naturels', 90, 'Agriculture'),
('Cultures céréalières', 'Production et transformation de céréales anciennes', 360, 'Agriculture'),
('Arboriculture fruitière', 'Plantation et entretien d''arbres fruitiers', 150, 'Agriculture'),
('Viticulture naturelle', 'Production de raisin sans intrants chimiques', 240, 'Agriculture'),
('Aquaculture durable', 'Élevage de poissons en système circulaire', 180, 'Agriculture'),
('Plantes médicinales', 'Culture et transformation de plantes aromatiques et médicinales', 120, 'Agriculture'),

-- Artisanat (8 activities)
('Menuiserie écologique', 'Création de meubles avec du bois local et durable', 360, 'Artisanat'),
('Poterie traditionnelle', 'Façonnage et cuisson d''objets en terre', 180, 'Artisanat'),
('Tissage et filature', 'Transformation de fibres naturelles en textiles', 240, 'Artisanat'),
('Maroquinerie artisanale', 'Confection d''objets en cuir naturel', 150, 'Artisanat'),
('Savonnerie naturelle', 'Fabrication de savons à base d''ingrédients naturels', 90, 'Artisanat'),
('Vannerie traditionnelle', 'Tressage de paniers avec des matériaux locaux', 120, 'Artisanat'),
('Forge et métallurgie', 'Travail du métal pour outils agricoles', 300, 'Artisanat'),
('Boulangerie au levain', 'Fabrication de pain traditionnel au levain naturel', 180, 'Artisanat'),

-- Environnement (7 activities)
('Gestion des déchets', 'Tri, recyclage et valorisation des déchets organiques', 120, 'Environnement'),
('Énergies renouvelables', 'Installation et maintenance de systèmes solaires', 240, 'Environnement'),
('Phytoépuration', 'Traitement naturel des eaux usées par les plantes', 180, 'Environnement'),
('Biodiversité locale', 'Inventaire et protection de la faune et flore locales', 150, 'Environnement'),
('Construction écologique', 'Techniques de construction avec matériaux naturels', 360, 'Environnement'),
('Agroforesterie', 'Intégration d''arbres dans les systèmes agricoles', 240, 'Environnement'),
('Récupération d''eau de pluie', 'Systèmes de collecte et stockage d''eau', 120, 'Environnement'),

-- Formation (3 activities)
('Gestion de projet', 'Méthodologie de conduite de projets agricoles', 120, 'Formation'),
('Communication et vente', 'Techniques de communication et commercialisation', 90, 'Formation'),
('Comptabilité agricole', 'Gestion financière d''une exploitation', 150, 'Formation'),

-- Insertion (2 activities)
('Accompagnement individuel', 'Suivi personnalisé des parcours d''insertion', 60, 'Insertion'),
('Projet professionnel', 'Élaboration d''un projet professionnel personnalisé', 120, 'Insertion');

-- Create a sample admin user (password should be hashed in real implementation)
INSERT INTO users (email, password_hash, full_name) VALUES
('admin@lavidaluca.fr', '$2b$12$sample.hashed.password.here', 'Administrateur La Vida Luca');