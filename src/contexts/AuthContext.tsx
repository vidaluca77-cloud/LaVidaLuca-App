'use client';

import React, { createContext, useContext, useReducer, useEffect, ReactNode } from 'react';
import { apiClient } from '@/services/api';
import { User, LoginCredentials, RegisterData } from '@/types';

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: string | null;
}

type AuthAction =
  | { type: 'AUTH_START' }
  | { type: 'AUTH_SUCCESS'; payload: User }
  | { type: 'AUTH_ERROR'; payload: string }
  | { type: 'AUTH_LOGOUT' }
  | { type: 'CLEAR_ERROR' };

interface AuthContextType extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  clearError: () => void;
}

const initialState: AuthState = {
  user: null,
  isLoading: false,
  isAuthenticated: false,
  error: null,
};

function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'AUTH_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case 'AUTH_SUCCESS':
      return {
        ...state,
        user: action.payload,
        isLoading: false,
        isAuthenticated: true,
        error: null,
      };
    case 'AUTH_ERROR':
      return {
        ...state,
        user: null,
        isLoading: false,
        isAuthenticated: false,
        error: action.payload,
      };
    case 'AUTH_LOGOUT':
      return {
        ...state,
        user: null,
        isLoading: false,
        isAuthenticated: false,
        error: null,
      };
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    default:
      return state;
  }
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Check for existing authentication on mount
  useEffect(() => {
    const checkAuth = async () => {
      if (apiClient.isAuthenticated()) {
        try {
          dispatch({ type: 'AUTH_START' });
          const response = await apiClient.getCurrentUser();
          if (response.success) {
            dispatch({ type: 'AUTH_SUCCESS', payload: response.data });
          } else {
            // Token is invalid, clear it
            apiClient.clearToken();
            dispatch({ type: 'AUTH_LOGOUT' });
          }
        } catch (error) {
          // Token is invalid, clear it
          apiClient.clearToken();
          dispatch({ type: 'AUTH_LOGOUT' });
        }
      }
    };

    checkAuth();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    try {
      dispatch({ type: 'AUTH_START' });
      const response = await apiClient.login(credentials);
      
      if (response.success) {
        // Store refresh token if provided
        if ('refresh_token' in response.data) {
          localStorage.setItem('refresh_token', response.data.refresh_token);
        }
        
        // Get user profile
        const userResponse = await apiClient.getCurrentUser();
        if (userResponse.success) {
          dispatch({ type: 'AUTH_SUCCESS', payload: userResponse.data });
        } else {
          throw new Error('Failed to get user profile');
        }
      } else {
        throw new Error(response.message || 'Login failed');
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Login failed';
      dispatch({ type: 'AUTH_ERROR', payload: message });
      throw error;
    }
  };

  const register = async (userData: RegisterData) => {
    try {
      dispatch({ type: 'AUTH_START' });
      const response = await apiClient.register(userData);
      
      if (response.success) {
        // Auto-login after successful registration
        await login({ email: userData.email, password: userData.password });
      } else {
        throw new Error(response.message || 'Registration failed');
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Registration failed';
      dispatch({ type: 'AUTH_ERROR', payload: message });
      throw error;
    }
  };

  const logout = async () => {
    try {
      await apiClient.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      dispatch({ type: 'AUTH_LOGOUT' });
    }
  };

  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  const value: AuthContextType = {
    ...state,
    login,
    register,
    logout,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}