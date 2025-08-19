// Types for the application
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

export interface User {
  id: number;
  email: string;
  full_name: string;
  location?: string;
  availability: string[];
  preferences: string[];
  is_active: boolean;
  is_student: boolean;
  created_at: string;
}

export interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<boolean>;
  register: (userData: any) => Promise<boolean>;
  logout: () => void;
  isLoading: boolean;
}