// Activity data for the LaVidaLuca application
import { Activity } from './types';

export const ACTIVITIES: Activity[] = [
  // Agriculture
  { id: '1', slug: 'nourrir-soigner-moutons', title: 'Nourrir et soigner les moutons', category: 'agri', summary: 'Gestes quotidiens : alimentation, eau, observation.', duration_min: 60, skill_tags: ['elevage', 'responsabilite'], seasonality: ['toutes'], safety_level: 1, materials: ['bottes', 'gants'] },
  { id: '2', slug: 'tonte-entretien-troupeau', title: 'Tonte & entretien du troupeau', category: 'agri', summary: 'Hygiène, tonte (démo), soins courants.', duration_min: 90, skill_tags: ['elevage', 'hygiene'], seasonality: ['printemps'], safety_level: 2, materials: ['bottes', 'gants'] },
  { id: '3', slug: 'basse-cour-soins', title: 'Soins basse-cour', category: 'agri', summary: 'Poules/canards/lapins : alimentation, abris, propreté.', duration_min: 60, skill_tags: ['soins_animaux'], seasonality: ['toutes'], safety_level: 1, materials: ['bottes', 'gants'] },
  { id: '4', slug: 'plantation-cultures', title: 'Plantation de cultures', category: 'agri', summary: 'Semis, arrosage, paillage, suivi de plants.', duration_min: 90, skill_tags: ['sol', 'plantes'], seasonality: ['printemps', 'ete'], safety_level: 1, materials: ['gants'] },
  { id: '5', slug: 'init-maraichage', title: 'Initiation maraîchage', category: 'agri', summary: 'Plan de culture, entretien, récolte respectueuse.', duration_min: 120, skill_tags: ['sol', 'organisation'], seasonality: ['printemps', 'ete', 'automne'], safety_level: 1, materials: ['gants', 'bottes'] },
  { id: '6', slug: 'clotures-abris', title: 'Gestion des clôtures & abris', category: 'agri', summary: 'Identifier, réparer, sécuriser parcs et abris.', duration_min: 120, skill_tags: ['securite', 'bois'], seasonality: ['toutes'], safety_level: 2, materials: ['gants'] },

  // Transformation
  { id: '7', slug: 'fromage', title: 'Fabrication de fromage', category: 'transfo', summary: 'Du lait au caillé : hygiène, moulage, affinage (découverte).', duration_min: 90, skill_tags: ['hygiene', 'precision'], seasonality: ['toutes'], safety_level: 2, materials: ['tablier'] },
  { id: '8', slug: 'conserves', title: 'Confitures & conserves', category: 'transfo', summary: 'Préparation, stérilisation, mise en pot, étiquetage.', duration_min: 90, skill_tags: ['organisation', 'hygiene'], seasonality: ['ete', 'automne'], safety_level: 1, materials: ['tablier'] },
  { id: '9', slug: 'laine', title: 'Transformation de la laine', category: 'transfo', summary: 'Lavage, cardage, petite création textile.', duration_min: 90, skill_tags: ['patience', 'creativite'], seasonality: ['toutes'], safety_level: 1, materials: ['tablier', 'gants'] },
  { id: '10', slug: 'jus', title: 'Fabrication de jus', category: 'transfo', summary: 'Du verger à la bouteille : tri, pressage, filtration.', duration_min: 90, skill_tags: ['hygiene', 'securite'], seasonality: ['automne'], safety_level: 2, materials: ['tablier', 'gants'] },
  { id: '11', slug: 'aromatiques-sechage', title: 'Séchage d\'herbes aromatiques', category: 'transfo', summary: 'Cueillette, séchage, conditionnement doux.', duration_min: 60, skill_tags: ['douceur', 'organisation'], seasonality: ['ete'], safety_level: 1, materials: ['tablier'] },
  { id: '12', slug: 'pain-four-bois', title: 'Pain au four à bois', category: 'transfo', summary: 'Pétrissage, façonnage, cuisson : respect des temps.', duration_min: 120, skill_tags: ['precision', 'rythme'], seasonality: ['toutes'], safety_level: 2, materials: ['tablier'] },

  // Artisanat
  { id: '13', slug: 'poterie-argile', title: 'Poterie (terre locale)', category: 'artisanat', summary: 'Façonnage, décoration, séchage (initiation).', duration_min: 90, skill_tags: ['creativite', 'precision'], seasonality: ['toutes'], safety_level: 1, materials: ['tablier'] },
  { id: '14', slug: 'tissage-simple', title: 'Tissage simple', category: 'artisanat', summary: 'Métier à tisser : base, matières naturelles.', duration_min: 90, skill_tags: ['patience', 'concentration'], seasonality: ['toutes'], safety_level: 1, materials: [] },
  { id: '15', slug: 'vannerie', title: 'Vannerie', category: 'artisanat', summary: 'Osier, ronce : corbeilles et objets utiles.', duration_min: 120, skill_tags: ['dexterite', 'patience'], seasonality: ['automne', 'hiver'], safety_level: 1, materials: ['gants'] },
  { id: '16', slug: 'savon-maison', title: 'Fabrication de savon', category: 'artisanat', summary: 'Méthode froide, plantes locales, sécurité.', duration_min: 90, skill_tags: ['precision', 'securite'], seasonality: ['toutes'], safety_level: 3, materials: ['gants', 'lunettes'] },
  { id: '17', slug: 'menuiserie-simple', title: 'Menuiserie simple', category: 'artisanat', summary: 'Petit mobilier : mesure, découpe, assemblage.', duration_min: 120, skill_tags: ['precision', 'securite'], seasonality: ['toutes'], safety_level: 3, materials: ['gants', 'lunettes'] },
  { id: '18', slug: 'teinture-naturelle', title: 'Teinture naturelle', category: 'artisanat', summary: 'Plantes tinctoriales : extraction, mordancage, teinture.', duration_min: 120, skill_tags: ['chimie_naturelle', 'patience'], seasonality: ['ete', 'automne'], safety_level: 2, materials: ['gants', 'tablier'] },

  // Nature
  { id: '19', slug: 'reconnaissance-plantes', title: 'Reconnaissance des plantes', category: 'nature', summary: 'Botanique de terrain : familles, usages, respect.', duration_min: 90, skill_tags: ['observation', 'memoire'], seasonality: ['printemps', 'ete'], safety_level: 1, materials: [] },
  { id: '20', slug: 'compost-permaculture', title: 'Compost & permaculture', category: 'nature', summary: 'Cycles, déchets organiques, équilibre, patience.', duration_min: 90, skill_tags: ['ecologie', 'observation'], seasonality: ['toutes'], safety_level: 1, materials: ['gants'] },
  { id: '21', slug: 'apiculture-decouverte', title: 'Apiculture (découverte)', category: 'nature', summary: 'Observer, comprendre, premiers gestes (accompagné).', duration_min: 90, skill_tags: ['calme', 'respect'], seasonality: ['printemps', 'ete'], safety_level: 2, materials: ['combinaison'] },
  { id: '22', slug: 'eau-gestion', title: 'Gestion de l\'eau', category: 'nature', summary: 'Récupération, filtration, économie, irrigation.', duration_min: 90, skill_tags: ['ecologie', 'ingenierie'], seasonality: ['toutes'], safety_level: 1, materials: [] },
  { id: '23', slug: 'graines-semences', title: 'Graines & semences', category: 'nature', summary: 'Récolte, séchage, conservation, échange.', duration_min: 60, skill_tags: ['organisation', 'precision'], seasonality: ['automne'], safety_level: 1, materials: [] },
  { id: '24', slug: 'foret-gestion', title: 'Gestion forestière', category: 'nature', summary: 'Identifier, nettoyer, planter, protéger.', duration_min: 120, skill_tags: ['endurance', 'observation'], seasonality: ['automne', 'hiver'], safety_level: 2, materials: ['bottes', 'gants'] },

  // Social
  { id: '25', slug: 'accueil-visiteurs', title: 'Accueil de visiteurs', category: 'social', summary: 'Présentation, tour guidé, partage d\'expérience.', duration_min: 60, skill_tags: ['relationnel', 'presentation'], seasonality: ['toutes'], safety_level: 1, materials: [] },
  { id: '26', slug: 'pedagogie-enfants', title: 'Pédagogie avec les enfants', category: 'social', summary: 'Expliquer, montrer, sécuriser, s\'adapter.', duration_min: 90, skill_tags: ['pedagogie', 'patience'], seasonality: ['toutes'], safety_level: 1, materials: [] },
  { id: '27', slug: 'organisation-evenement', title: 'Organisation d\'un événement', category: 'social', summary: 'Planification, logistique, communication.', duration_min: 180, skill_tags: ['organisation', 'communication'], seasonality: ['toutes'], safety_level: 1, materials: [] },
  { id: '28', slug: 'cuisine-collective', title: 'Cuisine collective (équipe)', category: 'social', summary: 'Préparer un repas simple et bon.', duration_min: 90, skill_tags: ['hygiene', 'equipe', 'temps'], seasonality: ['toutes'], safety_level: 1, materials: ['tablier'] },
  { id: '29', slug: 'gouter-fermier', title: 'Goûter fermier', category: 'social', summary: 'Organisation, service, convivialité, propreté.', duration_min: 60, skill_tags: ['rigueur', 'relationnel'], seasonality: ['toutes'], safety_level: 1, materials: ['tablier'] },
  { id: '30', slug: 'marche-local', title: 'Participation à un marché local', category: 'social', summary: 'Stand, présentation, caisse symbolique (simulation).', duration_min: 180, skill_tags: ['contact', 'compter_simple', 'equipe'], seasonality: ['toutes'], safety_level: 1, materials: [] },
];

export const CATEGORY_LABELS = {
  agri: { name: 'Agriculture', desc: 'Élevage, cultures, soins aux animaux' },
  transfo: { name: 'Transformation', desc: 'Produits fermiers, conservation, artisanat alimentaire' },
  artisanat: { name: 'Artisanat', desc: 'Créations manuelles, savoir-faire traditionnels' },
  nature: { name: 'Nature', desc: 'Écologie, environnement, permaculture' },
  social: { name: 'Social', desc: 'Échanges, pédagogie, événements' }
};

export const SKILLS_LIST = [
  'elevage', 'hygiene', 'soins_animaux', 'sol', 'plantes', 'organisation',
  'securite', 'bois', 'precision', 'creativite', 'patience', 'endurance',
  'ecologie', 'accueil', 'pedagogie', 'expression', 'equipe', 'responsabilite',
  'douceur', 'rythme', 'concentration', 'dexterite', 'chimie_naturelle',
  'observation', 'memoire', 'calme', 'respect', 'ingenierie', 'relationnel',
  'presentation', 'communication', 'temps', 'rigueur', 'contact', 'compter_simple'
];

export const AVAILABILITY_OPTIONS = [
  'weekend', 'semaine', 'matin', 'apres-midi', 'vacances'
];