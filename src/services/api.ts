import { ApiResponse, ApiError, User, Activity, Booking, AuthTokens, LoginCredentials, RegisterData, UserProfile } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_IA_API_URL || 'http://localhost:8000/api';

class ApiClient {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
    // Try to get token from localStorage on initialization
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('access_token');
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(this.token && { Authorization: `Bearer ${this.token}` }),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return {
        data,
        success: true,
        message: data.message
      };
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  // Authentication methods
  async login(credentials: LoginCredentials): Promise<ApiResponse<AuthTokens>> {
    const response = await this.request<AuthTokens>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    if (response.success && response.data.access_token) {
      this.setToken(response.data.access_token);
    }

    return response;
  }

  async register(userData: RegisterData): Promise<ApiResponse<User>> {
    return this.request<User>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async logout(): Promise<void> {
    try {
      await this.request('/auth/logout', { method: 'POST' });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      this.clearToken();
    }
  }

  async refreshToken(): Promise<ApiResponse<AuthTokens>> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await this.request<AuthTokens>('/auth/refresh', {
      method: 'POST',
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (response.success && response.data.access_token) {
      this.setToken(response.data.access_token);
    }

    return response;
  }

  // User methods
  async getCurrentUser(): Promise<ApiResponse<User>> {
    return this.request<User>('/users/me');
  }

  async updateProfile(profileData: Partial<UserProfile>): Promise<ApiResponse<UserProfile>> {
    return this.request<UserProfile>('/users/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData),
    });
  }

  // Activity methods
  async getActivities(): Promise<ApiResponse<Activity[]>> {
    return this.request<Activity[]>('/activities');
  }

  async getActivity(id: string): Promise<ApiResponse<Activity>> {
    return this.request<Activity>(`/activities/${id}`);
  }

  async getActivitySuggestions(userProfile: UserProfile): Promise<ApiResponse<Activity[]>> {
    return this.request<Activity[]>('/activities/suggestions', {
      method: 'POST',
      body: JSON.stringify(userProfile),
    });
  }

  // Booking methods
  async createBooking(activityId: string, scheduledDate: string, notes?: string): Promise<ApiResponse<Booking>> {
    return this.request<Booking>('/bookings', {
      method: 'POST',
      body: JSON.stringify({
        activity_id: activityId,
        scheduled_date: scheduledDate,
        notes,
      }),
    });
  }

  async getUserBookings(): Promise<ApiResponse<Booking[]>> {
    return this.request<Booking[]>('/bookings/me');
  }

  async updateBooking(bookingId: string, updates: Partial<Booking>): Promise<ApiResponse<Booking>> {
    return this.request<Booking>(`/bookings/${bookingId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  async cancelBooking(bookingId: string): Promise<ApiResponse<void>> {
    return this.request<void>(`/bookings/${bookingId}`, {
      method: 'DELETE',
    });
  }

  // Token management
  setToken(token: string): void {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
    }
  }

  clearToken(): void {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  }

  getToken(): string | null {
    return this.token;
  }

  isAuthenticated(): boolean {
    return !!this.token;
  }
}

// Create and export a singleton instance
export const apiClient = new ApiClient();

// Export the class for testing or custom instances
export { ApiClient };