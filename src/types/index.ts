// Activity type definitions
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