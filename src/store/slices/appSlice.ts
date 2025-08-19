// src/store/slices/appSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AppState } from '../types';

const initialState: AppState = {
  isLoading: false,
  error: null,
  theme: 'light',
  language: 'fr'
};

const appSlice = createSlice({
  name: 'app',
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    setTheme: (state, action: PayloadAction<'light' | 'dark'>) => {
      state.theme = action.payload;
    },
    setLanguage: (state, action: PayloadAction<'fr' | 'en'>) => {
      state.language = action.payload;
    },
    resetApp: () => initialState
  }
});

export const {
  setLoading,
  setError,
  clearError,
  setTheme,
  setLanguage,
  resetApp
} = appSlice.actions;

export default appSlice.reducer;