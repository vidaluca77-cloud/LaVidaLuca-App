import axios, { AxiosInstance, AxiosResponse } from 'axios';
import Cookies from 'js-cookie';

// Configuration de l'API
const API_BASE_URL = process.env.NEXT_PUBLIC_IA_API_URL || 'http://localhost:8000';

// Instance Axios avec configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token d'authentification
apiClient.interceptors.request.use((config) => {
  const token = Cookies.get('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Intercepteur pour gérer les erreurs de réponse
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expiré ou invalide, rediriger vers la connexion
      if (typeof window !== 'undefined') {
        window.location.href = '/auth/login';
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;