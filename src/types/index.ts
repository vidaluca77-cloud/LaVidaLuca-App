// Common types used across the application

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
  description?: string;
  requirements?: string[];
  learning_objectives?: string[];
}

export interface UserProfile {
  id?: string;
  skills: string[];
  availability: string[];
  location: string;
  preferences: string[];
  name?: string;
  email?: string;
  phone?: string;
  experience_level?: 'beginner' | 'intermediate' | 'advanced';
}

export interface Suggestion {
  activity: Activity;
  score: number;
  reasons: string[];
}

export interface User {
  id: string;
  email: string;
  name: string;
  profile?: UserProfile;
  role: 'student' | 'instructor' | 'admin';
  created_at: string;
  updated_at: string;
}

export interface Booking {
  id: string;
  user_id: string;
  activity_id: string;
  scheduled_date: string;
  status: 'pending' | 'confirmed' | 'completed' | 'cancelled';
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface ApiError {
  message: string;
  field?: string;
  code?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  expires_in: number;
  token_type: 'Bearer';
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}