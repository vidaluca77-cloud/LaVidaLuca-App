import { ApiResponse, User, Activity, Booking, UserProfile } from '@/types';

// Base API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// API client class
class ApiClient {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
    // Try to get token from localStorage if available
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('auth_token');
    }
  }

  setToken(token: string | null) {
    this.token = token;
    if (typeof window !== 'undefined') {
      if (token) {
        localStorage.setItem('auth_token', token);
      } else {
        localStorage.removeItem('auth_token');
      }
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          error: data.message || `HTTP error! status: ${response.status}`,
        };
      }

      return { data };
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  }

  // Authentication endpoints
  async login(email: string, password: string): Promise<ApiResponse<{ user: User; token: string }>> {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async register(email: string, password: string, name: string): Promise<ApiResponse<{ user: User; token: string }>> {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    });
  }

  async logout(): Promise<ApiResponse<void>> {
    const result = await this.request<void>('/auth/logout', {
      method: 'POST',
    });
    this.setToken(null);
    return result;
  }

  async getCurrentUser(): Promise<ApiResponse<User>> {
    return this.request('/auth/me');
  }

  // User profile endpoints
  async updateProfile(profile: Partial<UserProfile>): Promise<ApiResponse<User>> {
    return this.request('/profile', {
      method: 'PUT',
      body: JSON.stringify(profile),
    });
  }

  // Activity endpoints
  async getActivities(): Promise<ApiResponse<Activity[]>> {
    return this.request('/activities');
  }

  async getActivity(id: string): Promise<ApiResponse<Activity>> {
    return this.request(`/activities/${id}`);
  }

  async getSuggestions(): Promise<ApiResponse<Activity[]>> {
    return this.request('/activities/suggestions');
  }

  // Booking endpoints
  async createBooking(activityId: string, date: string, notes?: string): Promise<ApiResponse<Booking>> {
    return this.request('/bookings', {
      method: 'POST',
      body: JSON.stringify({ activityId, date, notes }),
    });
  }

  async getBookings(): Promise<ApiResponse<Booking[]>> {
    return this.request('/bookings');
  }

  async updateBooking(id: string, status: Booking['status']): Promise<ApiResponse<Booking>> {
    return this.request(`/bookings/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    });
  }

  async cancelBooking(id: string): Promise<ApiResponse<void>> {
    return this.request(`/bookings/${id}`, {
      method: 'DELETE',
    });
  }
}

// Create and export the API client instance
export const apiClient = new ApiClient(API_BASE_URL);

// Export individual API functions for convenience
export const api = {
  // Auth
  login: (email: string, password: string) => apiClient.login(email, password),
  register: (email: string, password: string, name: string) => apiClient.register(email, password, name),
  logout: () => apiClient.logout(),
  getCurrentUser: () => apiClient.getCurrentUser(),
  
  // Profile
  updateProfile: (profile: Partial<UserProfile>) => apiClient.updateProfile(profile),
  
  // Activities
  getActivities: () => apiClient.getActivities(),
  getActivity: (id: string) => apiClient.getActivity(id),
  getSuggestions: () => apiClient.getSuggestions(),
  
  // Bookings
  createBooking: (activityId: string, date: string, notes?: string) => 
    apiClient.createBooking(activityId, date, notes),
  getBookings: () => apiClient.getBookings(),
  updateBooking: (id: string, status: Booking['status']) => 
    apiClient.updateBooking(id, status),
  cancelBooking: (id: string) => apiClient.cancelBooking(id),
  
  // Set token
  setToken: (token: string | null) => apiClient.setToken(token),
};

export default api;