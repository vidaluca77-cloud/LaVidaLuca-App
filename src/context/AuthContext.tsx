'use client';

import React, { createContext, useContext, useReducer, useEffect, ReactNode } from 'react';
import Cookies from 'js-cookie';
import toast from 'react-hot-toast';
import { AuthState, User, UserProfile, LoginCredentials, RegisterData } from '../types';
import { authService, profileService } from '../lib/services';

// Types pour les actions
type AuthAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_USER'; payload: User | null }
  | { type: 'SET_TOKEN'; payload: string | null }
  | { type: 'SET_PROFILE'; payload: UserProfile | null }
  | { type: 'LOGOUT' };

// État initial
const initialState: AuthState & { profile: UserProfile | null } = {
  user: null,
  profile: null,
  token: null,
  isLoading: false,
  isAuthenticated: false,
};

// Reducer
function authReducer(state: typeof initialState, action: AuthAction): typeof initialState {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_USER':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: !!action.payload,
      };
    case 'SET_TOKEN':
      return { ...state, token: action.payload };
    case 'SET_PROFILE':
      return { ...state, profile: action.payload };
    case 'LOGOUT':
      return {
        ...initialState,
        isLoading: false,
      };
    default:
      return state;
  }
}

// Context
type AuthContextType = typeof initialState & {
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  updateProfile: (profileData: any) => Promise<void>;
  loadProfile: () => Promise<void>;
  refreshUser: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider
export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Initialisation au chargement
  useEffect(() => {
    const initAuth = async () => {
      const token = Cookies.get('auth_token');
      if (token) {
        dispatch({ type: 'SET_TOKEN', payload: token });
        try {
          dispatch({ type: 'SET_LOADING', payload: true });
          const user = await authService.getCurrentUser();
          dispatch({ type: 'SET_USER', payload: user });
          
          // Charger le profil si l'utilisateur existe
          try {
            const profile = await profileService.getProfile();
            dispatch({ type: 'SET_PROFILE', payload: profile });
          } catch (error) {
            // Profil n'existe pas encore, ce n'est pas grave
            console.log('Aucun profil trouvé');
          }
        } catch (error) {
          console.error('Erreur lors de l\'initialisation:', error);
          Cookies.remove('auth_token');
          dispatch({ type: 'LOGOUT' });
        } finally {
          dispatch({ type: 'SET_LOADING', payload: false });
        }
      }
    };

    initAuth();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const { access_token } = await authService.login(credentials);
      
      Cookies.set('auth_token', access_token, { expires: 1 }); // 1 jour
      dispatch({ type: 'SET_TOKEN', payload: access_token });
      
      const user = await authService.getCurrentUser();
      dispatch({ type: 'SET_USER', payload: user });
      
      // Tenter de charger le profil
      try {
        const profile = await profileService.getProfile();
        dispatch({ type: 'SET_PROFILE', payload: profile });
      } catch (error) {
        // Profil n'existe pas
        console.log('Aucun profil trouvé');
      }
      
      toast.success('Connexion réussie !');
    } catch (error: any) {
      console.error('Erreur de connexion:', error);
      toast.error(error.response?.data?.detail || 'Erreur de connexion');
      throw error;
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const register = async (userData: RegisterData) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      await authService.register(userData);
      
      // Connexion automatique après inscription
      await login({ email: userData.email, password: userData.password });
      
      toast.success('Inscription réussie !');
    } catch (error: any) {
      console.error('Erreur d\'inscription:', error);
      toast.error(error.response?.data?.detail || 'Erreur d\'inscription');
      throw error;
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const logout = () => {
    Cookies.remove('auth_token');
    dispatch({ type: 'LOGOUT' });
    toast.success('Déconnexion réussie !');
  };

  const updateProfile = async (profileData: any) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const profile = await profileService.createOrUpdateProfile(profileData);
      dispatch({ type: 'SET_PROFILE', payload: profile });
      toast.success('Profil mis à jour !');
    } catch (error: any) {
      console.error('Erreur de mise à jour du profil:', error);
      toast.error(error.response?.data?.detail || 'Erreur de mise à jour');
      throw error;
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const loadProfile = async () => {
    try {
      const profile = await profileService.getProfile();
      dispatch({ type: 'SET_PROFILE', payload: profile });
    } catch (error) {
      console.log('Aucun profil trouvé');
    }
  };

  const refreshUser = async () => {
    try {
      const user = await authService.getCurrentUser();
      dispatch({ type: 'SET_USER', payload: user });
    } catch (error) {
      console.error('Erreur lors du rafraîchissement utilisateur:', error);
    }
  };

  const value: AuthContextType = {
    ...state,
    login,
    register,
    logout,
    updateProfile,
    loadProfile,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Hook pour utiliser le contexte
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}