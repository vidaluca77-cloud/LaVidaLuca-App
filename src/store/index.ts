// src/store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
import type { RootState } from './types';

// Import reducers
import appReducer from './slices/appSlice';
import uiReducer from './slices/uiSlice';
import contactReducer from './slices/contactSlice';
import joinReducer from './slices/joinSlice';

export const store = configureStore({
  reducer: {
    app: appReducer,
    ui: uiReducer,
    contact: contactReducer,
    join: joinReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore these action types
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
  devTools: process.env.NODE_ENV !== 'production',
});

export type AppDispatch = typeof store.dispatch;

// Typed hooks for use throughout the app
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// Export store type for use in other files
export type { RootState } from './types';