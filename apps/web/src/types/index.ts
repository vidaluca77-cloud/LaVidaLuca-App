/**
 * Type definitions for La Vida Luca application
 */

// User types
export interface User {
  id: number
  email: string
  username: string
  full_name: string
  is_active: boolean
  is_admin: boolean
  created_at: string
  updated_at?: string
  profile?: UserProfile
}

export interface UserProfile {
  bio?: string
  location?: string
  interests: string[]
  experience_level: 'beginner' | 'intermediate' | 'advanced'
  avatar_url?: string
}

// Authentication types
export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  full_name: string
  username?: string
}

// Activity types
export interface Activity {
  id: number
  title: string
  description: string
  category: string
  difficulty_level: 'beginner' | 'intermediate' | 'advanced'
  duration_minutes: number
  location?: string
  equipment_needed?: string
  learning_objectives?: string
  is_published: boolean
  creator_id: number
  created_at: string
  updated_at?: string
  creator?: User
  completions_count?: number
  average_rating?: number
  is_completed?: boolean
  user_rating?: number
}

export interface ActivityCategory {
  id: string
  name: string
  description?: string
  icon?: string
  color?: string
}

export interface ActivityCompletion {
  id: number
  activity_id: number
  completed_at: string
  rating?: number
  feedback?: string
  points_awarded: number
}

// Gamification types
export interface Achievement {
  id: number
  name: string
  description?: string
  category: string
  points: number
  icon?: string
  criteria?: Record<string, any>
  is_active: boolean
  created_at: string
  progress?: number
  max_progress?: number
  is_completed?: boolean
  completed_at?: string
}

export interface Badge {
  id: number
  name: string
  description?: string
  icon?: string
  rarity: 'common' | 'rare' | 'epic' | 'legendary'
  requirements?: Record<string, any>
  is_active: boolean
  created_at: string
  earned_at?: string
}

export interface UserStats {
  user_id: number
  level: number
  experience_points: number
  total_points: number
  total_achievements: number
  completed_achievements: number
  total_badges: number
  earned_badges: number
  activities_completed: number
  current_streak: number
  rank?: number
}

export interface LeaderboardEntry {
  user_id: number
  username: string
  full_name?: string
  total_points: number
  level: number
  achievements_count: number
  badges_count: number
  rank: number
}

// AI/IA types
export interface GuideRequest {
  question: string
  context?: string
  user_level?: string
}

export interface GuideResponse {
  title: string
  answer: string
  question_echo: string
  confidence?: number
  sources?: string[]
}

export interface SuggestionRequest {
  user_profile: string
  category?: string
  difficulty?: string
}

export interface SuggestionResponse {
  suggestions: ActivitySuggestion[]
  reasoning: string
}

export interface ActivitySuggestion {
  title: string
  description: string
  category: string
  difficulty: string
  estimated_duration?: number
  relevance_score?: number
}

// Contact types
export interface ContactForm {
  name: string
  email: string
  subject: string
  message: string
  type?: 'question' | 'support' | 'feedback' | 'partnership'
}

// UI Component types
export interface TabItem {
  id: string
  label: string
  content: React.ReactNode
  badge?: number
  disabled?: boolean
}

export interface SelectOption {
  value: string
  label: string
  disabled?: boolean
}

export interface ProgressBarProps {
  value: number
  max?: number
  label?: string
  color?: 'blue' | 'green' | 'yellow' | 'red' | 'purple'
  size?: 'sm' | 'md' | 'lg'
  showPercentage?: boolean
}

// Notification types
export interface Notification {
  id: string
  title: string
  message?: string
  type: 'success' | 'error' | 'warning' | 'info'
  duration?: number
  action?: {
    label: string
    onClick: () => void
  }
}

// Search and filtering types
export interface SearchFilters {
  query?: string
  category?: string
  difficulty?: string
  duration?: {
    min?: number
    max?: number
  }
  rating?: {
    min?: number
    max?: number
  }
  tags?: string[]
}

export interface PaginationParams {
  page: number
  limit: number
  total?: number
  hasMore?: boolean
}

export interface SortOption {
  field: string
  direction: 'asc' | 'desc'
  label: string
}

// Dashboard types
export interface DashboardStats {
  activitiesCompleted: number
  currentLevel: number
  totalPoints: number
  achievementsUnlocked: number
  currentStreak: number
  weeklyProgress: number[]
  recentActivities: Activity[]
  upcomingDeadlines: any[]
}

// Theme types
export interface Theme {
  name: string
  colors: {
    primary: string
    secondary: string
    accent: string
    background: string
    surface: string
    text: string
    textSecondary: string
  }
  dark: boolean
}

// Error types
export interface ApiError {
  status: number
  message: string
  details?: any
}

export interface FormError {
  field: string
  message: string
}

// Feature flags
export interface FeatureFlags {
  enableGamification: boolean
  enableAISuggestions: boolean
  enableSocialFeatures: boolean
  enableNotifications: boolean
  enableOfflineMode: boolean
}

// App state types
export interface AppState {
  user: User | null
  isAuthenticated: boolean
  theme: Theme
  notifications: Notification[]
  featureFlags: FeatureFlags
  loading: boolean
  error: string | null
}