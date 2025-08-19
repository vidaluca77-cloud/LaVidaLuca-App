// API utilities for communicating with the backend
const API_BASE_URL = process.env.NEXT_PUBLIC_IA_API_URL || 'http://localhost:8000';

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

// Get auth token from localStorage
const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('auth_token');
  }
  return null;
};

// Set auth token in localStorage
const setAuthToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth_token', token);
  }
};

// Remove auth token from localStorage
const removeAuthToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth_token');
  }
};

// Base fetch wrapper with error handling
const apiFetch = async (endpoint: string, options: RequestInit = {}): Promise<any> => {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = getAuthToken();
  
  const config: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new ApiError(response.status, errorData.detail || `HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(0, 'Network error or server unavailable');
  }
};

// Auth API
export const authAPI = {
  async login(email: string, password: string) {
    const response = await apiFetch('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    
    if (response.access_token) {
      setAuthToken(response.access_token);
    }
    
    return response;
  },

  async register(userData: {
    email: string;
    password: string;
    full_name: string;
    location?: string;
    availability?: string[];
    preferences?: string[];
    is_student?: boolean;
  }) {
    return await apiFetch('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },

  logout() {
    removeAuthToken();
  },
};

// User API
export const userAPI = {
  async getCurrentUser() {
    return await apiFetch('/api/users/me');
  },

  async updateCurrentUser(userData: {
    full_name?: string;
    location?: string;
    availability?: string[];
    preferences?: string[];
  }) {
    return await apiFetch('/api/users/me', {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  },
};

// Activities API
export const activitiesAPI = {
  async getActivities(params: {
    skip?: number;
    limit?: number;
    category?: string;
    is_student_only?: boolean;
  } = {}) {
    const queryParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        queryParams.append(key, value.toString());
      }
    });
    
    const endpoint = `/api/activities/${queryParams.toString() ? `?${queryParams}` : ''}`;
    return await apiFetch(endpoint);
  },

  async getActivity(activityId: number) {
    return await apiFetch(`/api/activities/${activityId}`);
  },

  async getActivityBySlug(slug: string) {
    return await apiFetch(`/api/activities/slug/${slug}`);
  },

  async getRecommendations(userId: number, categoryFilter?: string, limit: number = 10) {
    const params = new URLSearchParams({ limit: limit.toString() });
    if (categoryFilter) {
      params.append('category_filter', categoryFilter);
    }
    
    return await apiFetch(`/api/activities/recommendations/${userId}?${params}`);
  },

  async markActivityComplete(activityId: number) {
    return await apiFetch(`/api/activities/${activityId}/complete`, {
      method: 'POST',
    });
  },

  async getCategories() {
    return await apiFetch('/api/activities/categories/list');
  },
};

// Helper function to check if user is authenticated
export const isAuthenticated = (): boolean => {
  return getAuthToken() !== null;
};

// Helper function to handle API errors in components
export const handleApiError = (error: unknown): string => {
  if (error instanceof ApiError) {
    if (error.status === 401) {
      removeAuthToken();
      return 'Session expirée. Veuillez vous reconnecter.';
    }
    return error.message;
  }
  return 'Une erreur inattendue est survenue.';
};

export { ApiError };