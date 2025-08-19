import { configureStore, combineReducers } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import authReducer from './slices/authSlice';
import activitiesReducer from './slices/activitiesSlice';
import uiReducer from './slices/uiSlice';
import { errorHandlingMiddleware, loadingMiddleware, apiLoggingMiddleware } from './middleware';

// Redux Persist configuration
const persistConfig = {
  key: 'root',
  storage,
  whitelist: ['auth'], // Only persist auth state
  blacklist: ['ui'], // Don't persist UI state (loading, errors, toasts)
};

// Auth persist configuration (more granular)
const authPersistConfig = {
  key: 'auth',
  storage,
  whitelist: ['user'], // Only persist user data
  blacklist: ['isLoading', 'error'], // Don't persist loading/error states
};

// Combine reducers
const rootReducer = combineReducers({
  auth: persistReducer(authPersistConfig, authReducer),
  activities: activitiesReducer,
  ui: uiReducer,
});

// Create persisted reducer
const persistedReducer = persistReducer(persistConfig, rootReducer);

// Configure store
export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }).concat(
      errorHandlingMiddleware,
      loadingMiddleware,
      apiLoggingMiddleware
    ),
  devTools: process.env.NODE_ENV !== 'production',
});

// Create persistor
export const persistor = persistStore(store);

// Export types
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Type-safe hooks
export { useAppDispatch, useAppSelector } from './hooks';