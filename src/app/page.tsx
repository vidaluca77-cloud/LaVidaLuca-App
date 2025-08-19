'use client'

import React, { useState, useEffect } from 'react';
import { HeartIcon, AcademicCapIcon, GlobeAltIcon, MapPinIcon, ClockIcon, ShieldCheckIcon, UserGroupIcon, StarIcon } from '@heroicons/react/24/outline';

// Types
interface Activity {
  id: string;
  slug: string;
  title: string;
  category: 'agri' | 'transfo' | 'artisanat' | 'nature' | 'social';
  summary: string;
  duration_min: number;
  skill_tags: string[];
  seasonality: string[];
  safety_level: number;
  materials: string[];
}

interface UserProfile {
  skills: string[];
  availability: string[];
  location: string;
  preferences: string[];
}

interface Suggestion {
  activity: Activity;
  score: number;
  reasons: string[];
}

// Données des 30 activités
const ACTIVITIES: Activity[] = [
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
  { id: '13', slug: 'abris-bois', title: 'Construction d\'abris', category: 'artisanat', summary: 'Petites structures bois : plan, coupe, assemblage.', duration_min: 120, skill_tags: ['bois', 'precision', 'securite'], seasonality: ['toutes'], safety_level: 2, materials: ['gants'] },
  { id: '14', slug: 'reparation-outils', title: 'Réparation & entretien des outils', category: 'artisanat', summary: 'Affûtage, graissage, petites réparations.', duration_min: 60, skill_tags: ['autonomie', 'responsabilite'], seasonality: ['toutes'], safety_level: 1, materials: ['gants'] },
  { id: '15', slug: 'menuiserie-simple', title: 'Menuiserie simple', category: 'artisanat', summary: 'Mesure, coupe, ponçage, finitions d\'un objet.', duration_min: 120, skill_tags: ['precision', 'creativite'], seasonality: ['toutes'], safety_level: 2, materials: ['gants', 'lunettes'] },
  { id: '16', slug: 'peinture-deco', title: 'Peinture & décoration d\'espaces', category: 'artisanat', summary: 'Préparer, protéger, peindre proprement.', duration_min: 90, skill_tags: ['proprete', 'finitions'], seasonality: ['toutes'], safety_level: 1, materials: ['tablier', 'gants'] },
  { id: '17', slug: 'amenagement-verts', title: 'Aménagement d\'espaces verts', category: 'artisanat', summary: 'Désherbage doux, paillage, plantations.', duration_min: 90, skill_tags: ['endurance', 'esthetique'], seasonality: ['printemps', 'ete'], safety_level: 1, materials: ['gants', 'bottes'] },
  { id: '18', slug: 'panneaux-orientation', title: 'Panneaux & orientation', category: 'artisanat', summary: 'Concevoir/poser une signalétique claire.', duration_min: 90, skill_tags: ['clarte', 'precision'], seasonality: ['toutes'], safety_level: 1, materials: ['gants'] },

  // Nature
  { id: '19', slug: 'entretien-riviere', title: 'Entretien de la rivière', category: 'nature', summary: 'Nettoyage doux, observation des berges.', duration_min: 90, skill_tags: ['prudence', 'ecologie'], seasonality: ['printemps', 'ete'], safety_level: 2, materials: ['bottes', 'gants'] },
  { id: '20', slug: 'plantation-arbres', title: 'Plantation d\'arbres', category: 'nature', summary: 'Choix d\'essences, tuteurage, paillage, suivi.', duration_min: 120, skill_tags: ['geste_juste', 'endurance'], seasonality: ['automne', 'hiver'], safety_level: 1, materials: ['gants', 'bottes'] },
  { id: '21', slug: 'potager-eco', title: 'Potager écologique', category: 'nature', summary: 'Associations, paillis, rotation des cultures.', duration_min: 90, skill_tags: ['observation', 'sobriete'], seasonality: ['printemps', 'ete', 'automne'], safety_level: 1, materials: ['gants'] },
  { id: '22', slug: 'compostage', title: 'Compostage', category: 'nature', summary: 'Tri, compost, valorisation des déchets verts.', duration_min: 60, skill_tags: ['geste_utile', 'hygiene'], seasonality: ['toutes'], safety_level: 1, materials: ['gants'] },
  { id: '23', slug: 'faune-locale', title: 'Observation de la faune locale', category: 'nature', summary: 'Discrétion, repérage, traces/indices.', duration_min: 60, skill_tags: ['patience', 'respect'], seasonality: ['toutes'], safety_level: 1, materials: [] },
  { id: '24', slug: 'nichoirs-hotels', title: 'Nichoirs & hôtels à insectes', category: 'nature', summary: 'Concevoir, fabriquer, installer des abris.', duration_min: 120, skill_tags: ['precision', 'pedagogie'], seasonality: ['toutes'], safety_level: 1, materials: ['gants'] },

  // Social
  { id: '25', slug: 'portes-ouvertes', title: 'Journée portes ouvertes', category: 'social', summary: 'Préparer, accueillir, guider un public.', duration_min: 180, skill_tags: ['accueil', 'organisation'], seasonality: ['toutes'], safety_level: 1, materials: [] },
  { id: '26', slug: 'visites-guidees', title: 'Visites guidées de la ferme', category: 'social', summary: 'Présenter la ferme, répondre simplement.', duration_min: 60, skill_tags: ['expression', 'pedagogie'], seasonality: ['toutes'], safety_level: 1, materials: [] },
  { id: '27', slug: 'ateliers-enfants', title: 'Ateliers pour enfants', category: 'social', summary: 'Jeux, découvertes nature, mini-gestes encadrés.', duration_min: 90, skill_tags: ['patience', 'creativite', 'securite'], seasonality: ['toutes'], safety_level: 2, materials: [] },
  { id: '28', slug: 'cuisine-collective', title: 'Cuisine collective (équipe)', category: 'social', summary: 'Préparer un repas simple et bon.', duration_min: 90, skill_tags: ['hygiene', 'equipe', 'temps'], seasonality: ['toutes'], safety_level: 1, materials: ['tablier'] },
  { id: '29', slug: 'gouter-fermier', title: 'Goûter fermier', category: 'social', summary: 'Organisation, service, convivialité, propreté.', duration_min: 60, skill_tags: ['rigueur', 'relationnel'], seasonality: ['toutes'], safety_level: 1, materials: ['tablier'] },
  { id: '30', slug: 'marche-local', title: 'Participation à un marché local', category: 'social', summary: 'Stand, présentation, caisse symbolique (simulation).', duration_min: 180, skill_tags: ['contact', 'compter_simple', 'equipe'], seasonality: ['toutes'], safety_level: 1, materials: [] },
];

// IA de matching simulée
const calculateMatching = (profile: UserProfile): Suggestion[] => {
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
        social: 'Animation'
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
    if (profile.availability.includes('weekend') || profile.availability.includes('semaine')) {
      score += 15;
      reasons.push('Compatible avec vos disponibilités');
    }

    return { activity, score, reasons };
  });

  return suggestions
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);
};

// Composants
const HomePage = () => (
  <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-amber-50">
    {/* Header */}
    <header className="bg-white/90 backdrop-blur-sm border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">VL</span>
            </div>
            <span className="font-bold text-xl text-gray-900">La Vida Luca</span>
          </div>
          
          <nav className="hidden md:flex space-x-8">
            <a href="#mission" className="text-gray-700 hover:text-green-500 font-medium">
              Notre mission
            </a>
            <a href="#activites" className="text-gray-700 hover:text-green-500 font-medium">
              Activités
            </a>
            <a href="#contact" className="text-gray-700 hover:text-green-500 font-medium">
              Contact
            </a>
          </nav>
        </div>
      </div>
    </header>

    {/* Hero Section */}
    <section className="relative py-20 lg:py-32">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            <span className="text-green-500">Le cœur</span> avant l'argent
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Réseau national de fermes pédagogiques dédiées à la formation des jeunes 
            et au développement d'une agriculture vivante et respectueuse.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a 
              href="/auth"
              className="bg-green-500 text-white px-8 py-4 rounded-lg font-medium hover:bg-green-600 transition-colors text-center"
            >
              Proposer mon aide
            </a>
            <a
              href="/activities"
              className="bg-white text-green-500 border-2 border-green-500 px-8 py-4 rounded-lg font-medium hover:bg-green-50 transition-colors text-center"
            >
              Découvrir nos activités
            </a>
          </div>
        </div>
      </div>
    </section>

    {/* Mission Section */}
    <section id="mission" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Notre mission
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Trois piliers fondamentaux guident notre action quotidienne
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center p-8">
            <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-6">
              <AcademicCapIcon className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Formation des jeunes</h3>
            <p className="text-gray-600">
              Partenariats avec les Maisons Familiales Rurales pour offrir aux élèves 
              une formation pratique et humaine dans un cadre authentique.
            </p>
          </div>

          <div className="text-center p-8">
            <div className="w-16 h-16 bg-amber-600 rounded-full flex items-center justify-center mx-auto mb-6">
              <GlobeAltIcon className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Agriculture vivante</h3>
            <p className="text-gray-600">
              Développement de pratiques agricoles durables respectueuses 
              de l'environnement et du bien-être animal.
            </p>
          </div>

          <div className="text-center p-8">
            <div className="w-16 h-16 bg-amber-400 rounded-full flex items-center justify-center mx-auto mb-6">
              <HeartIcon className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Insertion sociale</h3>
            <p className="text-gray-600">
              Accompagnement personnalisé de chaque jeune vers l'autonomie 
              et l'épanouissement personnel et professionnel.
            </p>
          </div>
        </div>
      </div>
    </section>

    {/* Contact */}
    <section id="contact" className="py-20 bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-8">
          Rejoignez l'aventure La Vida Luca
        </h2>
        <div className="grid md:grid-cols-2 gap-8 max-w-2xl mx-auto">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h3 className="font-semibold text-gray-900 mb-2">Snapchat</h3>
            <p className="text-green-500 font-medium">@lavidaluca77</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h3 className="font-semibold text-gray-900 mb-2">Email</h3>
            <p className="text-green-500 font-medium">vidaluca77@gmail.com</p>
          </div>
        </div>
      </div>
    </section>
  </div>
);

const OnboardingFlow = ({ onComplete }: { onComplete: (profile: UserProfile) => void }) => {
  const [step, setStep] = useState(1);
  const [profile, setProfile] = useState<UserProfile>({
    skills: [],
    availability: [],
    location: '',
    preferences: []
  });

  const skillsList = [
    'elevage', 'hygiene', 'soins_animaux', 'sol', 'plantes', 'organisation',
    'securite', 'bois', 'precision', 'creativite', 'patience', 'endurance',
    'ecologie', 'accueil', 'pedagogie', 'expression', 'equipe'
  ];

  const availabilityOptions = [
    'weekend', 'semaine', 'matin', 'apres-midi', 'vacances'
  ];

  const categoryOptions = [
    { id: 'agri', name: 'Agriculture', desc: 'Élevage, cultures, soins aux animaux' },
    { id: 'transfo', name: 'Transformation', desc: 'Fromage, conserves, pain...' },
    { id: 'artisanat', name: 'Artisanat', desc: 'Menuiserie, construction, réparation' },
    { id: 'nature', name: 'Environnement', desc: 'Plantation, compostage, écologie' },
    { id: 'social', name: 'Animation', desc: 'Accueil, visites, ateliers enfants' }
  ];

  const updateProfile = (key: keyof UserProfile, value: any) => {
    setProfile(prev => ({ ...prev, [key]: value }));
  };

  const handleSkillToggle = (skill: string) => {
    const newSkills = profile.skills.includes(skill)
      ? profile.skills.filter(s => s !== skill)
      : [...profile.skills, skill];
    updateProfile('skills', newSkills);
  };

  const handleAvailabilityToggle = (option: string) => {
    const newAvailability = profile.availability.includes(option)
      ? profile.availability.filter(a => a !== option)
      : [...profile.availability, option];
    updateProfile('availability', newAvailability);
  };

  const handlePreferenceToggle = (category: string) => {
    const newPreferences = profile.preferences.includes(category)
      ? profile.preferences.filter(p => p !== category)
      : [...profile.preferences, category];
    updateProfile('preferences', newPreferences);
  };

  if (step === 1) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Comment souhaitez-vous participer ?
          </h1>
          <p className="text-gray-600">
            Sélectionnez vos compétences actuelles ou celles que vous aimeriez développer
          </p>
        </div>

        <div className="space-y-4 mb-8">
          <h3 className="text-lg font-semibold text-gray-900">Vos compétences :</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {skillsList.map(skill => (
              <button
                key={skill}
                onClick={() => handleSkillToggle(skill)}
                className={`p-3 rounded-lg border text-sm font-medium transition-colors ${
                  profile.skills.includes(skill)
                    ? 'bg-green-500 text-white border-green-500'
                    : 'bg-white text-gray-700 border-gray-300 hover:border-green-500'
                }`}
              >
                {skill.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>

        <div className="flex justify-end">
          <button
            onClick={() => setStep(2)}
            className="bg-green-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-600 transition-colors"
          >
            Suivant
          </button>
        </div>
      </div>
    );
  }

  if (step === 2) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Vos disponibilités
          </h1>
          <p className="text-gray-600">
            Quand pourriez-vous participer aux activités ?
          </p>
        </div>

        <div className="space-y-4 mb-8">
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {availabilityOptions.map(option => (
              <button
                key={option}
                onClick={() => handleAvailabilityToggle(option)}
                className={`p-4 rounded-lg border text-sm font-medium transition-colors ${
                  profile.availability.includes(option)
                    ? 'bg-green-500 text-white border-green-500'
                    : 'bg-white text-gray-700 border-gray-300 hover:border-green-500'
                }`}
              >
                {option.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>

        <div className="flex justify-between">
          <button
            onClick={() => setStep(1)}
            className="bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-400 transition-colors"
          >
            Retour
          </button>
          <button
            onClick={() => setStep(3)}
            className="bg-green-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-600 transition-colors"
          >
            Suivant
          </button>
        </div>
      </div>
    );
  }

  if (step === 3) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Votre région
          </h1>
          <p className="text-gray-600">
            Dans quelle région souhaitez-vous participer ?
          </p>
        </div>

        <div className="space-y-4 mb-8">
          <input
            type="text"
            placeholder="Ex: Ile-de-France, Auvergne-Rhône-Alpes..."
            value={profile.location}
            onChange={(e) => updateProfile('location', e.target.value)}
            className="w-full p-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
        </div>

        <div className="flex justify-between">
          <button
            onClick={() => setStep(2)}
            className="bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-400 transition-colors"
          >
            Retour
          </button>
          <button
            onClick={() => setStep(4)}
            className="bg-green-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-600 transition-colors"
          >
            Suivant
          </button>
        </div>
      </div>
    );
  }

  if (step === 4) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Vos préférences
          </h1>
          <p className="text-gray-600">
            Quels types d'activités vous intéressent le plus ?
          </p>
        </div>

        <div className="space-y-4 mb-8">
          {categoryOptions.map(category => (
            <button
              key={category.id}
              onClick={() => handlePreferenceToggle(category.id)}
              className={`w-full p-4 rounded-lg border text-left transition-colors ${
                profile.preferences.includes(category.id)
                  ? 'bg-green-500 text-white border-green-500'
                  : 'bg-white text-gray-700 border-gray-300 hover:border-green-500'
              }`}
            >
              <div className="font-medium">{category.name}</div>
              <div className="text-sm opacity-90">{category.desc}</div>
            </button>
          ))}
        </div>

        <div className="flex justify-between">
          <button
            onClick={() => setStep(3)}
            className="bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-400 transition-colors"
          >
            Retour
          </button>
          <button
            onClick={() => onComplete(profile)}
            className="bg-green-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-600 transition-colors"
          >
            Voir mes propositions
          </button>
        </div>
      </div>
    );
  }

  return null;
};

const SuggestionsPage = ({ suggestions, profile }: { suggestions: Suggestion[], profile: UserProfile }) => {
  const [selectedActivity, setSelectedActivity] = useState<Activity | null>(null);
  const [showGuide, setShowGuide] = useState(false);

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h${mins > 0 ? mins.toString().padStart(2, '0') : ''}`;
    }
    return `${mins}min`;
  };

  const getSafetyColor = (level: number) => {
    switch (level) {
      case 1: return 'bg-green-100 text-green-800';
      case 2: return 'bg-yellow-100 text-yellow-800';
      case 3: return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getSafetyText = (level: number) => {
    switch (level) {
      case 1: return 'Facile';
      case 2: return 'Attention';
      case 3: return 'Expert';
      default: return 'Non défini';
    }
  };

  const generateSafetyGuide = (activity: Activity) => {
    const rules = [
      "Respecter les consignes de l'encadrant en permanence",
      "Porter les équipements de protection indiqués",
      "Signaler immédiatement tout problème ou incident"
    ];

    const checklist = [
      "Vérifier la présence de l'encadrant",
      "S'assurer d'avoir tous les matériels nécessaires",
      "Prendre connaissance des consignes de sécurité"
    ];

    if (activity.safety_level >= 2) {
      rules.push(
        "Ne jamais agir seul, toujours en binôme minimum",
        "Vérifier deux fois avant d'utiliser un outil"
      );
      checklist.push(
        "Vérifier l'état des outils avant utilisation",
        "S'assurer de la présence d'une trousse de premiers secours"
      );
    }

    return { rules, checklist };
  };

  if (showGuide && selectedActivity) {
    const guide = generateSafetyGuide(selectedActivity);
    
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Guide sécurité : {selectedActivity.title}
          </h2>
          
          <div className="mb-6">
            <div className="flex items-center space-x-4 text-sm text-gray-600 mb-4">
              <div className="flex items-center">
                <ClockIcon className="w-4 h-4 mr-1" />
                {formatDuration(selectedActivity.duration_min)}
              </div>
              <div className={`px-2 py-1 rounded-full text-xs font-medium ${getSafetyColor(selectedActivity.safety_level)}`}>
                {getSafetyText(selectedActivity.safety_level)}
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Règles de sécurité
              </h3>
              <ul className="space-y-2">
                {guide.rules.map((rule, index) => (
                  <li key={index} className="flex items-start">
                    <ShieldCheckIcon className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700">{rule}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Checklist avant de commencer
              </h3>
              <ul className="space-y-2">
                {guide.checklist.map((item, index) => (
                  <li key={index} className="flex items-start">
                    <input 
                      type="checkbox" 
                      className="w-4 h-4 text-green-500 mr-3 mt-1"
                      onChange={() => {}}
                    />
                    <span className="text-gray-700">{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {selectedActivity.materials.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  Matériel requis
                </h3>
                <div className="flex flex-wrap gap-2">
                  {selectedActivity.materials.map((material, index) => (
                    <span 
                      key={index}
                      className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium"
                    >
                      {material}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="flex justify-between mt-8">
            <button
              onClick={() => setShowGuide(false)}
              className="bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-400 transition-colors"
            >
              Retour
            </button>
            <button
              onClick={() => {
                alert('Inscription enregistrée ! Un encadrant vous contactera bientôt.');
                setShowGuide(false);
              }}
              className="bg-green-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-600 transition-colors"
            >
              Je m'inscris
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Vos propositions personnalisées
        </h1>
        <p className="text-gray-600">
          Notre IA a sélectionné ces activités spécialement pour vous
        </p>
      </div>

      <div className="space-y-6">
        {suggestions.map((suggestion, index) => (
          <div key={suggestion.activity.id} className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <div className="flex items-center mb-2">
                  <span className="bg-green-500 text-white px-3 py-1 rounded-full text-xs font-medium mr-3">
                    #{index + 1}
                  </span>
                  <h3 className="text-xl font-bold text-gray-900">
                    {suggestion.activity.title}
                  </h3>
                </div>
                <p className="text-gray-600 mb-4">
                  {suggestion.activity.summary}
                </p>
              </div>
              <div className="text-right ml-4">
                <div className="flex items-center text-yellow-500 mb-2">
                  <StarIcon className="w-5 h-5 mr-1" />
                  <span className="font-bold">{Math.round(suggestion.score)}%</span>
                </div>
                <span className="text-xs text-gray-500">compatibilité</span>
              </div>
            </div>

            <div className="flex items-center space-x-4 text-sm text-gray-600 mb-4">
              <div className="flex items-center">
                <ClockIcon className="w-4 h-4 mr-1" />
                {formatDuration(suggestion.activity.duration_min)}
              </div>
              <div className={`px-2 py-1 rounded-full text-xs font-medium ${getSafetyColor(suggestion.activity.safety_level)}`}>
                {getSafetyText(suggestion.activity.safety_level)}
              </div>
              <div className="flex items-center">
                <UserGroupIcon className="w-4 h-4 mr-1" />
                {suggestion.activity.category}
              </div>
            </div>

            <div className="mb-4">
              <h4 className="font-medium text-gray-900 mb-2">Pourquoi cette activité vous correspond :</h4>
              <ul className="space-y-1">
                {suggestion.reasons.map((reason, reasonIndex) => (
                  <li key={reasonIndex} className="flex items-start text-sm text-gray-700">
                    <span className="text-green-500 mr-2">•</span>
                    {reason}
                  </li>
                ))}
              </ul>
            </div>

            <div className="flex space-x-3">
              <button
                onClick={() => {
                  setSelectedActivity(suggestion.activity);
                  setShowGuide(true);
                }}
                className="bg-green-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-600 transition-colors flex-1"
              >
                Voir le guide & m'inscrire
              </button>
              <button
                onClick={() => setSelectedActivity(suggestion.activity)}
                className="bg-white text-green-500 border-2 border-green-500 px-4 py-3 rounded-lg font-medium hover:bg-green-50 transition-colors"
              >
                Détails
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="text-center mt-8">
        <p className="text-gray-600 mb-4">
          Ces propositions ne vous conviennent pas ?
        </p>
        <button
          onClick={() => window.location.reload()}
          className="bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-400 transition-colors"
        >
          Refaire le questionnaire
        </button>
      </div>
    </div>
  );
};

const ActivityCatalog = () => {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  
  const categories = [
    { id: 'all', name: 'Toutes', count: 30 },
    { id: 'agri', name: 'Agriculture', count: 6 },
    { id: 'transfo', name: 'Transformation', count: 6 },
    { id: 'artisanat', name: 'Artisanat', count: 6 },
    { id: 'nature', name: 'Environnement', count: 6 },
    { id: 'social', name: 'Animation', count: 6 }
  ];

  const filteredActivities = selectedCategory === 'all' 
    ? ACTIVITIES 
    : ACTIVITIES.filter(activity => activity.category === selectedCategory);

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h${mins > 0 ? mins.toString().padStart(2, '0') : ''}`;
    }
    return `${mins}min`;
  };

  const getSafetyColor = (level: number) => {
    switch (level) {
      case 1: return 'bg-green-100 text-green-800';
      case 2: return 'bg-yellow-100 text-yellow-800';
      case 3: return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getSafetyText = (level: number) => {
    switch (level) {
      case 1: return 'Facile';
      case 2: return 'Attention';
      case 3: return 'Expert';
      default: return 'Non défini';
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Catalogue des activités
        </h1>
        <p className="text-gray-600">
          30 activités pour apprendre et découvrir l'agriculture vivante
        </p>
      </div>

      {/* Filtres par catégorie */}
      <div className="flex flex-wrap justify-center gap-3 mb-8">
        {categories.map(category => (
          <button
            key={category.id}
            onClick={() => setSelectedCategory(category.id)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              selectedCategory === category.id
                ? 'bg-green-500 text-white'
                : 'bg-white text-gray-700 border border-gray-300 hover:border-green-500'
            }`}
          >
            {category.name} ({category.count})
          </button>
        ))}
      </div>

      {/* Grille des activités */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredActivities.map(activity => (
          <div key={activity.id} className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow">
            <div className="mb-4">
              <h3 className="text-lg font-bold text-gray-900 mb-2">
                {activity.title}
              </h3>
              <p className="text-gray-600 text-sm mb-3">
                {activity.summary}
              </p>
            </div>

            <div className="flex items-center justify-between text-sm text-gray-600 mb-4">
              <div className="flex items-center">
                <ClockIcon className="w-4 h-4 mr-1" />
                {formatDuration(activity.duration_min)}
              </div>
              <div className={`px-2 py-1 rounded-full text-xs font-medium ${getSafetyColor(activity.safety_level)}`}>
                {getSafetyText(activity.safety_level)}
              </div>
            </div>

            {activity.skill_tags.length > 0 && (
              <div className="mb-4">
                <div className="flex flex-wrap gap-1">
                  {activity.skill_tags.slice(0, 3).map((skill, index) => (
                    <span 
                      key={index}
                      className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs"
                    >
                      {skill}
                    </span>
                  ))}
                  {activity.skill_tags.length > 3 && (
                    <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">
                      +{activity.skill_tags.length - 3}
                    </span>
                  )}
                </div>
              </div>
            )}

            {activity.materials.length > 0 && (
              <div className="mb-4">
                <h4 className="text-xs font-medium text-gray-500 mb-1">Matériel :</h4>
                <p className="text-xs text-gray-600">
                  {activity.materials.join(', ')}
                </p>
              </div>
            )}

            <button className="w-full bg-green-500 text-white py-2 rounded-lg font-medium hover:bg-green-600 transition-colors">
              En savoir plus
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

// App principale
const App = () => {
  const [currentPage, setCurrentPage] = useState<'home' | 'onboarding' | 'suggestions' | 'catalog'>('home');
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);

  const handleOnboardingComplete = (profile: UserProfile) => {
    setUserProfile(profile);
    const calculatedSuggestions = calculateMatching(profile);
    setSuggestions(calculatedSuggestions);
    setCurrentPage('suggestions');
  };

  const navigateToOnboarding = () => {
    setCurrentPage('onboarding');
  };

  const navigateToCatalog = () => {
    setCurrentPage('catalog');
  };

  const navigateToHome = () => {
    setCurrentPage('home');
  };

  if (currentPage === 'onboarding') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-amber-50">
        <div className="py-8">
          <div className="text-center mb-8">
            <button 
              onClick={navigateToHome}
              className="inline-flex items-center space-x-2 text-green-500 hover:text-green-600 mb-4"
            >
              <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">VL</span>
              </div>
              <span className="font-bold text-xl">La Vida Luca</span>
            </button>
          </div>
          <OnboardingFlow onComplete={handleOnboardingComplete} />
        </div>
      </div>
    );
  }

  if (currentPage === 'suggestions' && userProfile) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-amber-50">
        <div className="py-8">
          <div className="text-center mb-8">
            <button 
              onClick={navigateToHome}
              className="inline-flex items-center space-x-2 text-green-500 hover:text-green-600 mb-4"
            >
              <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">VL</span>
              </div>
              <span className="font-bold text-xl">La Vida Luca</span>
            </button>
          </div>
          <SuggestionsPage suggestions={suggestions} profile={userProfile} />
        </div>
      </div>
    );
  }

  if (currentPage === 'catalog') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-amber-50">
        <div className="py-8">
          <div className="text-center mb-8">
            <button 
              onClick={navigateToHome}
              className="inline-flex items-center space-x-2 text-green-500 hover:text-green-600 mb-4"
            >
              <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">VL</span>
              </div>
              <span className="font-bold text-xl">La Vida Luca</span>
            </button>
          </div>
          <ActivityCatalog />
        </div>
      </div>
    );
  }

  return (
    <div onClick={(e) => {
      const target = e.target as HTMLElement;
      if (target.textContent === 'Proposer mon aide') {
        e.preventDefault();
        navigateToOnboarding();
      } else if (target.textContent === 'Découvrir nos activités') {
        e.preventDefault();
        navigateToCatalog();
      }
    }}>
      <HomePage />
    </div>
  );
};

export default App;
