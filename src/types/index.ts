/**
 * Type definitions for La Vida Luca App
 */

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

export interface CategoryOption {
  id: string;
  name: string;
  desc: string;
}

export interface PerformanceMetric {
  name: string;
  duration_ms: number;
  timestamp?: string;
  metadata?: Record<string, any>;
}

export interface ContactFormData {
  name: string;
  email: string;
  message: string;
  type?: 'contact' | 'join' | 'partnership';
}

export type SafetyLevel = 1 | 2 | 3;

export type ActivityCategory = Activity['category'];

export type SeasonalityPeriod =
  | 'printemps'
  | 'ete'
  | 'automne'
  | 'hiver'
  | 'toutes';
