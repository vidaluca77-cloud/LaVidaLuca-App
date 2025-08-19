// Core domain types for La Vida Luca application

export interface Activity {
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

export interface UserProfile {
  skills: string[];
  availability: string[];
  location: string;
  preferences: string[];
}

export interface Suggestion {
  activity: Activity;
  score: number;
  reasons: string[];
}

export type PageType = 'home' | 'onboarding' | 'suggestions' | 'catalog';

export interface CategoryOption {
  id: string;
  name: string;
  desc: string;
}

export interface Category {
  id: string;
  name: string;
  count: number;
}

export interface SafetyGuide {
  rules: string[];
  checklist: string[];
}
