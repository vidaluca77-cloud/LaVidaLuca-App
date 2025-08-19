// src/store/types.ts
/**
 * Redux store type definitions
 */

// App state types
export interface AppState {
  isLoading: boolean;
  error: string | null;
  theme: 'light' | 'dark';
  language: 'fr' | 'en';
}

// UI state types
export interface UIState {
  sidebarOpen: boolean;
  modalOpen: boolean;
  notifications: Notification[];
}

export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  timestamp: number;
}

// API state types
export interface ApiState {
  isLoading: boolean;
  error: string | null;
  lastFetch: number | null;
}

// Contact form state
export interface ContactState extends ApiState {
  formData: ContactFormData;
  submitted: boolean;
}

export interface ContactFormData {
  name: string;
  email: string;
  message: string;
}

// Join form state
export interface JoinState extends ApiState {
  formData: JoinFormData;
  submitted: boolean;
}

export interface JoinFormData {
  name: string;
  email: string;
  phone: string;
  motivation: string;
}

// Root state type
export interface RootState {
  app: AppState;
  ui: UIState;
  contact: ContactState;
  join: JoinState;
}

// Async thunk types
export interface AsyncThunkConfig {
  state: RootState;
  rejectValue: string;
}