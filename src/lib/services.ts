import apiClient from './api';
import {
  User,
  UserProfile,
  Activity,
  Recommendation,
  LoginCredentials,
  RegisterData,
  ProfileFormData,
} from '../types';

// Services d'authentification
export const authService = {
  async login(credentials: LoginCredentials): Promise<{ access_token: string; token_type: string }> {
    const response = await apiClient.post('/auth/login', credentials);
    return response.data;
  },

  async register(userData: RegisterData): Promise<User> {
    const response = await apiClient.post('/users/', userData);
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get('/users/me');
    return response.data;
  },

  async updateUser(userData: Partial<RegisterData>): Promise<User> {
    const response = await apiClient.put('/users/me', userData);
    return response.data;
  },
};

// Services de profil utilisateur
export const profileService = {
  async getProfile(): Promise<UserProfile> {
    const response = await apiClient.get('/profiles/');
    return response.data;
  },

  async createOrUpdateProfile(profileData: ProfileFormData): Promise<UserProfile> {
    const response = await apiClient.post('/profiles/', profileData);
    return response.data;
  },

  async updateProfile(profileData: Partial<ProfileFormData>): Promise<UserProfile> {
    const response = await apiClient.put('/profiles/', profileData);
    return response.data;
  },
};

// Services d'activités
export const activityService = {
  async getActivities(params?: {
    skip?: number;
    limit?: number;
    category?: string;
    search?: string;
  }): Promise<Activity[]> {
    const response = await apiClient.get('/activities/', { params });
    return response.data;
  },

  async getActivity(id: number): Promise<Activity> {
    const response = await apiClient.get(`/activities/${id}`);
    return response.data;
  },

  async getActivityBySlug(slug: string): Promise<Activity> {
    const response = await apiClient.get(`/activities/slug/${slug}`);
    return response.data;
  },

  async getCategories(): Promise<string[]> {
    const response = await apiClient.get('/activities/categories');
    return response.data;
  },

  async getSkills(): Promise<string[]> {
    const response = await apiClient.get('/activities/skills');
    return response.data;
  },
};

// Services de recommandations
export const recommendationService = {
  async getRecommendations(params?: {
    limit?: number;
    regenerate?: boolean;
  }): Promise<{ recommendations: Recommendation[]; total_count: number }> {
    const response = await apiClient.get('/recommendations/', { params });
    return response.data;
  },

  async regenerateRecommendations(limit: number = 10): Promise<{ recommendations: Recommendation[]; total_count: number }> {
    const response = await apiClient.post('/recommendations/regenerate', { limit });
    return response.data;
  },
};