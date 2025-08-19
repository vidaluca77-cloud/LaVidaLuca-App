import { Activity, UserProfile, Suggestion } from '@/types';

/**
 * Calculate matching score between user profile and activities
 */
export const calculateMatching = (profile: UserProfile): Suggestion[] => {
  const suggestions = ACTIVITIES.map(activity => {
    let score = 0;
    const reasons: string[] = [];

    // Compétences communes
    const commonSkills = activity.skill_tags.filter(skill =>
      profile.skills.includes(skill)
    );
    if (commonSkills.length > 0) {
      score += commonSkills.length * 15;
      reasons.push(`Compétences correspondantes : ${commonSkills.join(', ')}`);
    }

    // Préférences de catégories
    if (profile.preferences.includes(activity.category)) {
      score += 25;
      const categoryNames = {
        agri: 'Agriculture',
        transfo: 'Transformation',
        artisanat: 'Artisanat',
        nature: 'Environnement',
        social: 'Animation',
      };
      reasons.push(`Catégorie préférée : ${categoryNames[activity.category]}`);
    }

    // Durée adaptée
    if (activity.duration_min <= 90) {
      score += 10;
      reasons.push('Durée adaptée pour débuter');
    }

    // Sécurité
    if (activity.safety_level <= 2) {
      score += 10;
      if (activity.safety_level === 1) {
        reasons.push('Activité sans risque particulier');
      }
    }

    // Disponibilité (simulation)
    if (
      profile.availability.includes('weekend') ||
      profile.availability.includes('semaine')
    ) {
      score += 15;
      reasons.push('Compatible avec vos disponibilités');
    }

    return { activity, score, reasons };
  });

  return suggestions.sort((a, b) => b.score - a.score).slice(0, 3);
};

/**
 * Format duration from minutes to human readable format
 */
export const formatDuration = (minutes: number): string => {
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  if (hours > 0) {
    return `${hours}h${mins > 0 ? mins.toString().padStart(2, '0') : ''}`;
  }
  return `${mins}min`;
};

/**
 * Get safety level color classes
 */
export const getSafetyColor = (level: number): string => {
  switch (level) {
    case 1:
      return 'bg-green-100 text-green-800';
    case 2:
      return 'bg-yellow-100 text-yellow-800';
    case 3:
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

/**
 * Get safety level text
 */
export const getSafetyText = (level: number): string => {
  switch (level) {
    case 1:
      return 'Facile';
    case 2:
      return 'Attention';
    case 3:
      return 'Expert';
    default:
      return 'Non défini';
  }
};

/**
 * Generate safety guide for an activity
 */
export const generateSafetyGuide = (activity: Activity) => {
  const rules = [
    "Respecter les consignes de l'encadrant en permanence",
    'Porter les équipements de protection indiqués',
    'Signaler immédiatement tout problème ou incident',
  ];

  const checklist = [
    "Vérifier la présence de l'encadrant",
    "S'assurer d'avoir tous les matériels nécessaires",
    'Prendre connaissance des consignes de sécurité',
  ];

  if (activity.safety_level >= 2) {
    rules.push(
      'Ne jamais agir seul, toujours en binôme minimum',
      "Vérifier deux fois avant d'utiliser un outil"
    );
    checklist.push(
      "Vérifier l'état des outils avant utilisation",
      "S'assurer de la présence d'une trousse de premiers secours"
    );
  }

  return { rules, checklist };
};

// Activity data - should ideally come from API
export const ACTIVITIES: Activity[] = [
  // Agriculture
  {
    id: '1',
    slug: 'nourrir-soigner-moutons',
    title: 'Nourrir et soigner les moutons',
    category: 'agri',
    summary: 'Gestes quotidiens : alimentation, eau, observation.',
    duration_min: 60,
    skill_tags: ['elevage', 'responsabilite'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: ['bottes', 'gants'],
  },
  {
    id: '2',
    slug: 'tonte-entretien-troupeau',
    title: 'Tonte & entretien du troupeau',
    category: 'agri',
    summary: 'Hygiène, tonte (démo), soins courants.',
    duration_min: 90,
    skill_tags: ['elevage', 'hygiene'],
    seasonality: ['printemps'],
    safety_level: 2,
    materials: ['bottes', 'gants'],
  },
  {
    id: '3',
    slug: 'basse-cour-soins',
    title: 'Soins basse-cour',
    category: 'agri',
    summary: 'Poules/canards/lapins : alimentation, abris, propreté.',
    duration_min: 60,
    skill_tags: ['soins_animaux'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: ['bottes', 'gants'],
  },
  {
    id: '4',
    slug: 'plantation-cultures',
    title: 'Plantation de cultures',
    category: 'agri',
    summary: 'Semis, arrosage, paillage, suivi de plants.',
    duration_min: 90,
    skill_tags: ['sol', 'plantes'],
    seasonality: ['printemps', 'ete'],
    safety_level: 1,
    materials: ['gants'],
  },
  {
    id: '5',
    slug: 'init-maraichage',
    title: 'Initiation maraîchage',
    category: 'agri',
    summary: 'Plan de culture, entretien, récolte respectueuse.',
    duration_min: 120,
    skill_tags: ['sol', 'organisation'],
    seasonality: ['printemps', 'ete', 'automne'],
    safety_level: 1,
    materials: ['gants', 'bottes'],
  },
  {
    id: '6',
    slug: 'clotures-abris',
    title: 'Gestion des clôtures & abris',
    category: 'agri',
    summary: 'Identifier, réparer, sécuriser parcs et abris.',
    duration_min: 120,
    skill_tags: ['securite', 'bois'],
    seasonality: ['toutes'],
    safety_level: 2,
    materials: ['gants'],
  },

  // Transformation
  {
    id: '7',
    slug: 'fromage',
    title: 'Fabrication de fromage',
    category: 'transfo',
    summary: 'Du lait au caillé : hygiène, moulage, affinage (découverte).',
    duration_min: 90,
    skill_tags: ['hygiene', 'precision'],
    seasonality: ['toutes'],
    safety_level: 2,
    materials: ['tablier'],
  },
  {
    id: '8',
    slug: 'conserves',
    title: 'Confitures & conserves',
    category: 'transfo',
    summary: 'Préparation, stérilisation, mise en pot, étiquetage.',
    duration_min: 90,
    skill_tags: ['organisation', 'hygiene'],
    seasonality: ['ete', 'automne'],
    safety_level: 1,
    materials: ['tablier'],
  },
  {
    id: '9',
    slug: 'laine',
    title: 'Transformation de la laine',
    category: 'transfo',
    summary: 'Lavage, cardage, petite création textile.',
    duration_min: 90,
    skill_tags: ['patience', 'creativite'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: ['tablier', 'gants'],
  },
  {
    id: '10',
    slug: 'jus',
    title: 'Fabrication de jus',
    category: 'transfo',
    summary: 'Du verger à la bouteille : tri, pressage, filtration.',
    duration_min: 90,
    skill_tags: ['hygiene', 'securite'],
    seasonality: ['automne'],
    safety_level: 2,
    materials: ['tablier', 'gants'],
  },
  {
    id: '11',
    slug: 'aromatiques-sechage',
    title: "Séchage d'herbes aromatiques",
    category: 'transfo',
    summary: 'Cueillette, séchage, conditionnement doux.',
    duration_min: 60,
    skill_tags: ['douceur', 'organisation'],
    seasonality: ['ete'],
    safety_level: 1,
    materials: ['tablier'],
  },
  {
    id: '12',
    slug: 'pain-four-bois',
    title: 'Pain au four à bois',
    category: 'transfo',
    summary: 'Pétrissage, façonnage, cuisson : respect des temps.',
    duration_min: 120,
    skill_tags: ['precision', 'rythme'],
    seasonality: ['toutes'],
    safety_level: 2,
    materials: ['tablier'],
  },

  // Artisanat
  {
    id: '13',
    slug: 'abris-bois',
    title: "Construction d'abris",
    category: 'artisanat',
    summary: 'Petites structures bois : plan, coupe, assemblage.',
    duration_min: 120,
    skill_tags: ['bois', 'precision', 'securite'],
    seasonality: ['toutes'],
    safety_level: 2,
    materials: ['gants'],
  },
  {
    id: '14',
    slug: 'reparation-outils',
    title: 'Réparation & entretien des outils',
    category: 'artisanat',
    summary: 'Affûtage, graissage, petites réparations.',
    duration_min: 60,
    skill_tags: ['autonomie', 'responsabilite'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: ['gants'],
  },
  {
    id: '15',
    slug: 'menuiserie-simple',
    title: 'Menuiserie simple',
    category: 'artisanat',
    summary: "Mesure, coupe, ponçage, finitions d'un objet.",
    duration_min: 120,
    skill_tags: ['precision', 'creativite'],
    seasonality: ['toutes'],
    safety_level: 2,
    materials: ['gants', 'lunettes'],
  },
  {
    id: '16',
    slug: 'peinture-deco',
    title: "Peinture & décoration d'espaces",
    category: 'artisanat',
    summary: 'Préparer, protéger, peindre proprement.',
    duration_min: 90,
    skill_tags: ['proprete', 'finitions'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: ['tablier', 'gants'],
  },
  {
    id: '17',
    slug: 'amenagement-verts',
    title: "Aménagement d'espaces verts",
    category: 'artisanat',
    summary: 'Désherbage doux, paillage, plantations.',
    duration_min: 90,
    skill_tags: ['endurance', 'esthetique'],
    seasonality: ['printemps', 'ete'],
    safety_level: 1,
    materials: ['gants', 'bottes'],
  },
  {
    id: '18',
    slug: 'panneaux-orientation',
    title: 'Panneaux & orientation',
    category: 'artisanat',
    summary: 'Concevoir/poser une signalétique claire.',
    duration_min: 90,
    skill_tags: ['clarte', 'precision'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: ['gants'],
  },

  // Nature
  {
    id: '19',
    slug: 'entretien-riviere',
    title: 'Entretien de la rivière',
    category: 'nature',
    summary: 'Nettoyage doux, observation des berges.',
    duration_min: 90,
    skill_tags: ['prudence', 'ecologie'],
    seasonality: ['printemps', 'ete'],
    safety_level: 2,
    materials: ['bottes', 'gants'],
  },
  {
    id: '20',
    slug: 'plantation-arbres',
    title: "Plantation d'arbres",
    category: 'nature',
    summary: "Choix d'essences, tuteurage, paillage, suivi.",
    duration_min: 120,
    skill_tags: ['geste_juste', 'endurance'],
    seasonality: ['automne', 'hiver'],
    safety_level: 1,
    materials: ['gants', 'bottes'],
  },
  {
    id: '21',
    slug: 'potager-eco',
    title: 'Potager écologique',
    category: 'nature',
    summary: 'Associations, paillis, rotation des cultures.',
    duration_min: 90,
    skill_tags: ['observation', 'sobriete'],
    seasonality: ['printemps', 'ete', 'automne'],
    safety_level: 1,
    materials: ['gants'],
  },
  {
    id: '22',
    slug: 'compostage',
    title: 'Compostage',
    category: 'nature',
    summary: 'Tri, compost, valorisation des déchets verts.',
    duration_min: 60,
    skill_tags: ['geste_utile', 'hygiene'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: ['gants'],
  },
  {
    id: '23',
    slug: 'faune-locale',
    title: 'Observation de la faune locale',
    category: 'nature',
    summary: 'Discrétion, repérage, traces/indices.',
    duration_min: 60,
    skill_tags: ['patience', 'respect'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: [],
  },
  {
    id: '24',
    slug: 'nichoirs-hotels',
    title: 'Nichoirs & hôtels à insectes',
    category: 'nature',
    summary: 'Concevoir, fabriquer, installer des abris.',
    duration_min: 120,
    skill_tags: ['precision', 'pedagogie'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: ['gants'],
  },

  // Social
  {
    id: '25',
    slug: 'portes-ouvertes',
    title: 'Journée portes ouvertes',
    category: 'social',
    summary: 'Préparer, accueillir, guider un public.',
    duration_min: 180,
    skill_tags: ['accueil', 'organisation'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: [],
  },
  {
    id: '26',
    slug: 'visites-guidees',
    title: 'Visites guidées de la ferme',
    category: 'social',
    summary: 'Présenter la ferme, répondre simplement.',
    duration_min: 60,
    skill_tags: ['expression', 'pedagogie'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: [],
  },
  {
    id: '27',
    slug: 'ateliers-enfants',
    title: 'Ateliers pour enfants',
    category: 'social',
    summary: 'Jeux, découvertes nature, mini-gestes encadrés.',
    duration_min: 90,
    skill_tags: ['patience', 'creativite', 'securite'],
    seasonality: ['toutes'],
    safety_level: 2,
    materials: [],
  },
  {
    id: '28',
    slug: 'cuisine-collective',
    title: 'Cuisine collective (équipe)',
    category: 'social',
    summary: 'Préparer un repas simple et bon.',
    duration_min: 90,
    skill_tags: ['hygiene', 'equipe', 'temps'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: ['tablier'],
  },
  {
    id: '29',
    slug: 'gouter-fermier',
    title: 'Goûter fermier',
    category: 'social',
    summary: 'Organisation, service, convivialité, propreté.',
    duration_min: 60,
    skill_tags: ['rigueur', 'relationnel'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: ['tablier'],
  },
  {
    id: '30',
    slug: 'marche-local',
    title: 'Participation à un marché local',
    category: 'social',
    summary: 'Stand, présentation, caisse symbolique (simulation).',
    duration_min: 180,
    skill_tags: ['contact', 'compter_simple', 'equipe'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: [],
  },
];
