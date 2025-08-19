import { Middleware } from '@reduxjs/toolkit';
import { showErrorToast, setError } from '../slices/uiSlice';

// Define action type with type property
interface ActionWithType {
  type: string;
  payload?: any;
  error?: any;
}

// Middleware to handle API errors globally
export const errorHandlingMiddleware: Middleware = (store) => (next) => (action: ActionWithType) => {
  // Handle rejected async thunks
  if (action.type && action.type.endsWith('/rejected')) {
    const errorMessage = action.payload || action.error?.message || 'An error occurred';
    const actionType = action.type.replace('/rejected', '');
    
    // Set error in UI state
    store.dispatch(setError({ 
      key: actionType, 
      error: errorMessage 
    }));
    
    // Show error toast
    store.dispatch(showErrorToast({
      title: 'Erreur',
      message: errorMessage,
    }));
  }
  
  return next(action);
};

// Middleware to handle loading states
export const loadingMiddleware: Middleware = (store) => (next) => (action: ActionWithType) => {
  // Auto-manage loading states for async thunks
  if (action.type && action.type.endsWith('/pending')) {
    // Could dispatch loading actions here if needed
  } else if (action.type && (action.type.endsWith('/fulfilled') || action.type.endsWith('/rejected'))) {
    // Loading is handled in slice extraReducers
  }
  
  return next(action);
};

// Middleware for API request logging
export const apiLoggingMiddleware: Middleware = (store) => (next) => (action: ActionWithType) => {
  // Log API requests in development
  if (process.env.NODE_ENV === 'development') {
    if (action.type && (action.type.includes('fetch') || action.type.includes('update') || action.type.includes('create'))) {
      console.log('API Action:', {
        type: action.type,
        payload: action.payload,
        timestamp: new Date().toISOString(),
      });
    }
  }
  
  return next(action);
};