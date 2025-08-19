// Integration helper for LaVidaLuca FastAPI backend
// This file can be used in the Next.js frontend to interact with the FastAPI backend

const API_BASE_URL = process.env.NEXT_PUBLIC_IA_API_URL || 'http://localhost:8000';

interface UserProfile {
  skills: string[];
  availability: string[];
  location: string;
  preferences: string[];
}

interface Activity {
  id: number;
  slug: string;
  title: string;
  category: string;
  summary: string;
  duration_min: number;
  skill_tags: string[];
  seasonality: string[];
  safety_level: number;
  materials: string[];
}

interface Suggestion {
  activity: Activity;
  score: number;
  reasons: string[];
}

class LaVidaLucaAPI {
  private baseURL: string;
  private authToken?: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  setAuthToken(token: string) {
    this.authToken = token;
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.authToken) {
      headers.Authorization = `Bearer ${this.authToken}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'Network error' }));
      throw new Error(error.message || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Auth endpoints
  async register(userData: {
    email: string;
    username: string;
    password: string;
    full_name?: string;
    skills?: string[];
    availability?: string[];
    location?: string;
    preferences?: string[];
  }) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(username: string, password: string) {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    
    if (response.access_token) {
      this.setAuthToken(response.access_token);
    }
    
    return response;
  }

  // Activity endpoints
  async getActivities(category?: string): Promise<Activity[]> {
    const params = category ? `?category=${category}` : '';
    return this.request(`/activities/${params}`);
  }

  async getActivity(id: number): Promise<Activity> {
    return this.request(`/activities/${id}`);
  }

  async getActivityBySlug(slug: string): Promise<Activity> {
    return this.request(`/activities/slug/${slug}`);
  }

  async getCategories() {
    return this.request('/activities/categories/list');
  }

  // Recommendation endpoints
  async getRecommendations(userProfile: UserProfile, limit: number = 5): Promise<Suggestion[]> {
    return this.request('/recommendations/suggest', {
      method: 'POST',
      body: JSON.stringify({
        user_profile: userProfile,
        limit,
      }),
    });
  }

  async generateRecommendationsForUser(limit: number = 5): Promise<Suggestion[]> {
    return this.request(`/recommendations/generate?limit=${limit}`, {
      method: 'POST',
    });
  }

  async getMyRecommendations() {
    return this.request('/recommendations/me');
  }

  // User endpoints
  async getProfile() {
    return this.request('/users/me');
  }

  async updateProfile(updates: {
    email?: string;
    username?: string;
    full_name?: string;
    skills?: string[];
    availability?: string[];
    location?: string;
    preferences?: string[];
  }) {
    return this.request('/users/me', {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  async getUserProfile(): Promise<UserProfile> {
    return this.request('/users/me/profile');
  }

  async updateUserProfile(profile: UserProfile): Promise<UserProfile> {
    return this.request('/users/me/profile', {
      method: 'PUT',
      body: JSON.stringify(profile),
    });
  }

  // Health check
  async healthCheck() {
    return this.request('/health');
  }
}

// Export singleton instance
export const api = new LaVidaLucaAPI();

// Export types for use in frontend
export type { UserProfile, Activity, Suggestion };

// Example usage:
/*
// In your React component:
import { api, UserProfile } from './api/lavidaluca';

// Get activities
const activities = await api.getActivities();

// Get recommendations
const userProfile: UserProfile = {
  skills: ['agriculture', 'elevage'],
  availability: ['weekend'],
  location: 'France',
  preferences: ['agri']
};

const suggestions = await api.getRecommendations(userProfile, 5);

// Auth flow
await api.login('username', 'password');
const profile = await api.getProfile();
*/