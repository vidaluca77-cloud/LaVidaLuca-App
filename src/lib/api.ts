import { Activity } from '@/types'

// Mock data for activities - in real app this would come from an API
const ACTIVITIES: Activity[] = [
  // Agriculture
  {
    id: '1',
    slug: 'nourrir-soigner-moutons',
    title: 'Nourrir et soigner les moutons',
    category: 'agri',
    summary: 'Gestes quotidiens : alimentation, eau, observation.',
    description: 'Apprendre les gestes quotidiens pour prendre soin des moutons : distribution de nourriture, vérification de l\'eau, observation du comportement des animaux.',
    duration: '1h',
    duration_min: 60,
    skill_tags: ['elevage', 'responsabilite'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: ['bottes', 'gants'],
    image: '/placeholder.svg'
  },
  {
    id: '2',
    slug: 'tonte-entretien-troupeau',
    title: 'Tonte & entretien du troupeau',
    category: 'agri',
    summary: 'Hygiène, tonte (démo), soins courants.',
    description: 'Découverte de la tonte des moutons, hygiène du troupeau et soins vétérinaires de base.',
    duration: '1h30',
    duration_min: 90,
    skill_tags: ['elevage', 'hygiene'],
    seasonality: ['printemps'],
    safety_level: 2,
    materials: ['bottes', 'gants'],
    image: '/placeholder.svg'
  },
  {
    id: '3',
    slug: 'plantation-cultures',
    title: 'Plantation de cultures',
    category: 'agri',
    summary: 'Semis, arrosage, paillage, suivi de plants.',
    description: 'Initiation au maraîchage : préparation du sol, semis, plantation, arrosage et suivi des cultures.',
    duration: '1h30',
    duration_min: 90,
    skill_tags: ['sol', 'plantes'],
    seasonality: ['printemps', 'ete'],
    safety_level: 1,
    materials: ['gants'],
    image: '/placeholder.svg'
  }
];

export async function getActivities(): Promise<Activity[]> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 100));
  return ACTIVITIES;
}

export async function getActivity(id: string): Promise<Activity | null> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 100));
  return ACTIVITIES.find(activity => activity.id === id) || null;
}

export async function login(email: string, password: string): Promise<{ token: string }> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // Mock validation
  if (email && password) {
    return { token: 'mock-jwt-token' };
  }
  
  throw new Error('Invalid credentials');
}