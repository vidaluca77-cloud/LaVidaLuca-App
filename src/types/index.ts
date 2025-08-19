// Core types for the application
export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: 'student' | 'instructor' | 'admin';
  profile?: UserProfile;
}

export interface UserProfile {
  skills: string[];
  availability: string[];
  location: string;
  preferences: string[];
  bio?: string;
  phone?: string;
}

export interface Activity {
  id: string;
  slug: string;
  title: string;
  category: 'agri' | 'transfo' | 'artisanat' | 'nature' | 'social';
  summary: string;
  description?: string;
  duration_min: number;
  skill_tags: string[];
  seasonality: string[];
  safety_level: number;
  materials: string[];
  instructor?: string;
  location?: string;
  maxParticipants?: number;
  currentParticipants?: number;
  images?: string[];
}

export interface Booking {
  id: string;
  userId: string;
  activityId: string;
  date: string;
  status: 'pending' | 'confirmed' | 'cancelled' | 'completed';
  notes?: string;
  createdAt: string;
  updatedAt: string;
}

export interface Suggestion {
  activity: Activity;
  score: number;
  reasons: string[];
}

export interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  token: string | null;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface NotificationState {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}