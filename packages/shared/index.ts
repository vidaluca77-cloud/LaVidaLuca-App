// Shared types and utilities for La Vida Luca applications

export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'farmer' | 'student';
}

export interface Farm {
  id: string;
  name: string;
  location: string;
  description: string;
  ownerId: string;
}

export const API_ENDPOINTS = {
  USERS: '/api/users',
  FARMS: '/api/farms',
  HEALTH: '/health',
} as const;