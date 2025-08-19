export interface Activity {
  id: string;
  slug: string;
  title: string;
  category: 'agri' | 'transfo' | 'artisanat' | 'nature' | 'social';
  summary: string;
  description: string;
  duration: string;
  duration_min: number;
  skill_tags: string[];
  seasonality: string[];
  safety_level: number;
  materials: string[];
  image?: string;
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