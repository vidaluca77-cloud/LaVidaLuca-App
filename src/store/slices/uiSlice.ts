import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { UIState, ToastMessage } from '../../lib/types';

const initialState: UIState = {
  loading: {},
  errors: {},
  currentPage: 'home',
  sidebarOpen: false,
  toasts: [],
};

let toastIdCounter = 0;

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    // Loading state management
    setLoading: (state, action: PayloadAction<{ key: string; isLoading: boolean }>) => {
      state.loading[action.payload.key] = action.payload.isLoading;
    },
    clearLoading: (state, action: PayloadAction<string>) => {
      delete state.loading[action.payload];
    },
    clearAllLoading: (state) => {
      state.loading = {};
    },

    // Error state management
    setError: (state, action: PayloadAction<{ key: string; error: string | null }>) => {
      state.errors[action.payload.key] = action.payload.error;
    },
    clearError: (state, action: PayloadAction<string>) => {
      delete state.errors[action.payload];
    },
    clearAllErrors: (state) => {
      state.errors = {};
    },

    // Page navigation
    setCurrentPage: (state, action: PayloadAction<UIState['currentPage']>) => {
      state.currentPage = action.payload;
    },

    // Sidebar management
    setSidebarOpen: (state, action: PayloadAction<boolean>) => {
      state.sidebarOpen = action.payload;
    },
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },

    // Toast notifications
    addToast: (state, action: PayloadAction<Omit<ToastMessage, 'id'>>) => {
      const toast: ToastMessage = {
        ...action.payload,
        id: `toast-${++toastIdCounter}`,
        duration: action.payload.duration || 5000,
      };
      state.toasts.push(toast);
    },
    removeToast: (state, action: PayloadAction<string>) => {
      state.toasts = state.toasts.filter(toast => toast.id !== action.payload);
    },
    clearToasts: (state) => {
      state.toasts = [];
    },

    // Utility actions
    showSuccessToast: (state, action: PayloadAction<{ title: string; message?: string }>) => {
      const toast: ToastMessage = {
        id: `toast-${++toastIdCounter}`,
        type: 'success',
        title: action.payload.title,
        message: action.payload.message,
        duration: 4000,
      };
      state.toasts.push(toast);
    },
    showErrorToast: (state, action: PayloadAction<{ title: string; message?: string }>) => {
      const toast: ToastMessage = {
        id: `toast-${++toastIdCounter}`,
        type: 'error',
        title: action.payload.title,
        message: action.payload.message,
        duration: 6000,
      };
      state.toasts.push(toast);
    },
    showWarningToast: (state, action: PayloadAction<{ title: string; message?: string }>) => {
      const toast: ToastMessage = {
        id: `toast-${++toastIdCounter}`,
        type: 'warning',
        title: action.payload.title,
        message: action.payload.message,
        duration: 5000,
      };
      state.toasts.push(toast);
    },
    showInfoToast: (state, action: PayloadAction<{ title: string; message?: string }>) => {
      const toast: ToastMessage = {
        id: `toast-${++toastIdCounter}`,
        type: 'info',
        title: action.payload.title,
        message: action.payload.message,
        duration: 4000,
      };
      state.toasts.push(toast);
    },
  },
});

export const {
  setLoading,
  clearLoading,
  clearAllLoading,
  setError,
  clearError,
  clearAllErrors,
  setCurrentPage,
  setSidebarOpen,
  toggleSidebar,
  addToast,
  removeToast,
  clearToasts,
  showSuccessToast,
  showErrorToast,
  showWarningToast,
  showInfoToast,
} = uiSlice.actions;

export default uiSlice.reducer;