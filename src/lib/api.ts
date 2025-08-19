const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  message?: string;
}

export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  is_admin: boolean;
  bio?: string;
  location?: string;
  phone?: string;
  skills: string[];
  preferences: string[];
  availability: string[];
  created_at: string;
}

export interface Activity {
  id: number;
  slug: string;
  title: string;
  category: string;
  summary: string;
  description?: string;
  duration_min: number;
  skill_tags: string[];
  seasonality: string[];
  safety_level: number;
  materials: string[];
  max_participants: number;
  min_age: number;
  location?: string;
  difficulty_level: number;
  is_active: boolean;
  is_featured: boolean;
  created_at: string;
  participant_count?: number;
  average_rating?: number;
  completion_rate?: number;
}

export interface Participation {
  id: number;
  user_id: number;
  activity_id: number;
  status: string;
  scheduled_date?: string;
  completion_date?: string;
  rating?: number;
  comment?: string;
  feedback?: any;
  skills_acquired: string[];
  completion_percentage: number;
  created_at: string;
  activity?: Activity;
}

export interface Recommendation {
  activity: Activity;
  score: number;
  reasons: string[];
  confidence?: number;
}

class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
    // Load token from localStorage if available
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('token');
    }
  }

  setToken(token: string | null) {
    this.token = token;
    if (typeof window !== 'undefined') {
      if (token) {
        localStorage.setItem('token', token);
      } else {
        localStorage.removeItem('token');
      }
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}/api${endpoint}`;
    
    const defaultHeaders: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      defaultHeaders.Authorization = `Bearer ${this.token}`;
    }

    const config: RequestInit = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        return {
          error: errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
        };
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  }

  // Authentication
  async login(username: string, password: string): Promise<ApiResponse<{ access_token: string; token_type: string }>> {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    return this.request('/auth/login', {
      method: 'POST',
      headers: {}, // Remove Content-Type to let browser set it for FormData
      body: formData,
    });
  }

  async register(userData: {
    email: string;
    username: string;
    password: string;
    first_name: string;
    last_name: string;
    bio?: string;
    location?: string;
    phone?: string;
    skills?: string[];
    preferences?: string[];
    availability?: string[];
  }): Promise<ApiResponse<User>> {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async getCurrentUser(): Promise<ApiResponse<User>> {
    return this.request('/auth/me');
  }

  logout() {
    this.setToken(null);
  }

  // Activities
  async getActivities(params?: {
    skip?: number;
    limit?: number;
    category?: string;
    search?: string;
    active_only?: boolean;
  }): Promise<ApiResponse<Activity[]>> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, value.toString());
        }
      });
    }
    
    const queryString = queryParams.toString();
    const endpoint = `/activities${queryString ? `?${queryString}` : ''}`;
    
    return this.request(endpoint);
  }

  async getActivity(activityId: number): Promise<ApiResponse<Activity>> {
    return this.request(`/activities/${activityId}`);
  }

  // Participations
  async getParticipations(): Promise<ApiResponse<Participation[]>> {
    return this.request('/participations/');
  }

  async createParticipation(activityId: number, scheduledDate?: string): Promise<ApiResponse<Participation>> {
    return this.request('/participations/', {
      method: 'POST',
      body: JSON.stringify({
        activity_id: activityId,
        scheduled_date: scheduledDate,
      }),
    });
  }

  async updateParticipation(participationId: number, data: {
    status?: string;
    rating?: number;
    comment?: string;
    completion_percentage?: number;
  }): Promise<ApiResponse<Participation>> {
    return this.request(`/participations/${participationId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async cancelParticipation(participationId: number): Promise<ApiResponse<{ message: string }>> {
    return this.request(`/participations/${participationId}`, {
      method: 'DELETE',
    });
  }

  // Recommendations
  async getRecommendations(limit: number = 5): Promise<ApiResponse<{
    recommendations: Recommendation[];
    total_activities: number;
    user_profile_completeness?: number;
  }>> {
    return this.request(`/recommendations/?limit=${limit}`);
  }

  async getRecommendationsByPreferences(data: {
    user_skills?: string[];
    user_preferences?: string[];
    user_availability?: string[];
    limit?: number;
  }): Promise<ApiResponse<{
    recommendations: Recommendation[];
    total_activities: number;
  }>> {
    return this.request('/recommendations/by-preferences', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getCategories(): Promise<ApiResponse<{
    categories: Array<{
      id: string;
      name: string;
      description: string;
      skills?: string[];
    }>;
  }>> {
    return this.request('/recommendations/categories');
  }

  async getSkills(): Promise<ApiResponse<{
    skills: Array<{
      id: string;
      name: string;
      category: string;
    }>;
  }>> {
    return this.request('/recommendations/skills');
  }
}

export const apiClient = new ApiClient();
export default apiClient;