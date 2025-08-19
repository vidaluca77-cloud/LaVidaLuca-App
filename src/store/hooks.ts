// src/store/hooks.ts
// Re-export the typed hooks for easier imports
export { useAppDispatch, useAppSelector } from './index';

// Export app slice actions
export {
  setLoading,
  setError,
  clearError as clearAppError,
  setTheme,
  setLanguage,
  resetApp
} from './slices/appSlice';

// Export UI slice actions
export {
  toggleSidebar,
  setSidebarOpen,
  openModal,
  closeModal,
  addNotification,
  removeNotification,
  clearNotifications
} from './slices/uiSlice';

// Export contact slice actions with prefixed names
export {
  updateFormData as updateContactFormData,
  resetForm as resetContactForm,
  clearError as clearContactError
} from './slices/contactSlice';

// Export join slice actions with prefixed names
export {
  updateFormData as updateJoinFormData,
  resetForm as resetJoinForm,
  clearError as clearJoinError
} from './slices/joinSlice';

// Export all thunks
export * from './thunks/contactThunks';
export * from './thunks/joinThunks';

// Export all selectors
export * from './selectors';