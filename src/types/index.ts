// src/types/index.ts
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'student' | 'supervisor' | 'admin';
  profile?: UserProfile;
}

export interface UserProfile {
  id: string;
  user_id: string;
  full_name: string;
  phone?: string;
  location?: string;
  skills: string[];
  availability: string[];
  preferences: string[];
  bio?: string;
  avatar_url?: string;
  created_at: string;
  updated_at: string;
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
  location?: string;
  supervisor_id?: string;
  max_participants?: number;
  status?: 'active' | 'inactive' | 'draft';
  created_at?: string;
  updated_at?: string;
}

export interface Booking {
  id: string;
  activity_id: string;
  student_id: string;
  supervisor_id: string;
  status: 'pending' | 'confirmed' | 'completed' | 'cancelled';
  scheduled_date: string;
  duration_minutes: number;
  notes?: string;
  feedback?: string;
  rating?: number;
  created_at: string;
  updated_at: string;
  activity?: Activity;
  student?: UserProfile;
  supervisor?: UserProfile;
}

export interface Farm {
  id: string;
  name: string;
  description: string;
  location: string;
  address: string;
  contact_email: string;
  contact_phone?: string;
  website?: string;
  specialties: string[];
  capacity: number;
  facilities: string[];
  supervisor_id: string;
  status: 'active' | 'inactive';
  created_at: string;
  updated_at: string;
  supervisor?: UserProfile;
}

export interface Message {
  id: string;
  sender_id: string;
  receiver_id: string;
  subject: string;
  content: string;
  read: boolean;
  created_at: string;
  sender?: UserProfile;
  receiver?: UserProfile;
}

export interface Progress {
  id: string;
  student_id: string;
  activity_id: string;
  status: 'not_started' | 'in_progress' | 'completed';
  progress_percentage: number;
  milestones_completed: string[];
  notes?: string;
  started_at?: string;
  completed_at?: string;
  activity?: Activity;
  student?: UserProfile;
}