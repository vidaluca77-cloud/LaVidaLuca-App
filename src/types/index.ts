export interface User {
  id: number;
  email: string;
  full_name?: string;
  is_active: boolean;
  is_mfr_student: boolean;
  created_at: string;
}

export interface UserProfile {
  id: number;
  user_id: number;
  location?: string;
  availability: string[];
  experience_level: string;
  skills: string[];
  preferences: string[];
  created_at: string;
}

export interface Activity {
  id: number;
  slug: string;
  title: string;
  category: 'agri' | 'transfo' | 'artisanat' | 'nature' | 'social';
  summary?: string;
  description?: string;
  duration_min: number;
  skill_tags: string[];
  seasonality: string[];
  safety_level: number;
  materials: string[];
  is_active: boolean;
  created_at: string;
}

export interface Recommendation {
  id: number;
  user_id: number;
  activity_id: number;
  activity: Activity;
  score: number;
  reasons: string[];
  ai_explanation?: string;
  created_at: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name?: string;
  is_mfr_student?: boolean;
}

export interface ApiError {
  message: string;
  detail?: string;
  status?: number;
}

export interface ProfileFormData {
  location?: string;
  availability: string[];
  experience_level: string;
  skills: string[];
  preferences: string[];
}