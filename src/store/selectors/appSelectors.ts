// src/store/selectors/appSelectors.ts
import { RootState } from '../types';

// App selectors
export const selectAppState = (state: RootState) => state.app;
export const selectIsLoading = (state: RootState) => state.app.isLoading;
export const selectError = (state: RootState) => state.app.error;
export const selectTheme = (state: RootState) => state.app.theme;
export const selectLanguage = (state: RootState) => state.app.language;