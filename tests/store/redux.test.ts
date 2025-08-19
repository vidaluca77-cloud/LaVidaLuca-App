// tests/store/redux.test.ts
import { configureStore } from '@reduxjs/toolkit';
import { describe, it, expect } from '@jest/globals';

// Import our slices
import appReducer, { setLoading, setError, setTheme } from '../../src/store/slices/appSlice';
import uiReducer, { addNotification, removeNotification } from '../../src/store/slices/uiSlice';
import contactReducer, { updateFormData, resetForm } from '../../src/store/slices/contactSlice';

describe('Redux Store', () => {
  describe('App Slice', () => {
    it('should handle setLoading action', () => {
      const initialState = {
        isLoading: false,
        error: null,
        theme: 'light' as const,
        language: 'fr' as const
      };

      const action = setLoading(true);
      const newState = appReducer(initialState, action);

      expect(newState.isLoading).toBe(true);
    });

    it('should handle setError action', () => {
      const initialState = {
        isLoading: false,
        error: null,
        theme: 'light' as const,
        language: 'fr' as const
      };

      const errorMessage = 'Test error';
      const action = setError(errorMessage);
      const newState = appReducer(initialState, action);

      expect(newState.error).toBe(errorMessage);
    });

    it('should handle setTheme action', () => {
      const initialState = {
        isLoading: false,
        error: null,
        theme: 'light' as const,
        language: 'fr' as const
      };

      const action = setTheme('dark');
      const newState = appReducer(initialState, action);

      expect(newState.theme).toBe('dark');
    });
  });

  describe('UI Slice', () => {
    it('should handle addNotification action', () => {
      const initialState = {
        sidebarOpen: false,
        modalOpen: false,
        notifications: []
      };

      const notification = {
        type: 'success' as const,
        message: 'Test notification'
      };

      const action = addNotification(notification);
      const newState = uiReducer(initialState, action);

      expect(newState.notifications).toHaveLength(1);
      expect(newState.notifications[0].message).toBe('Test notification');
      expect(newState.notifications[0].type).toBe('success');
      expect(newState.notifications[0].id).toBeDefined();
      expect(newState.notifications[0].timestamp).toBeDefined();
    });

    it('should handle removeNotification action', () => {
      const notificationId = 'test-id';
      const initialState = {
        sidebarOpen: false,
        modalOpen: false,
        notifications: [{
          id: notificationId,
          type: 'info' as const,
          message: 'Test',
          timestamp: Date.now()
        }]
      };

      const action = removeNotification(notificationId);
      const newState = uiReducer(initialState, action);

      expect(newState.notifications).toHaveLength(0);
    });
  });

  describe('Contact Slice', () => {
    it('should handle updateFormData action', () => {
      const initialState = {
        isLoading: false,
        error: null,
        lastFetch: null,
        formData: {
          name: '',
          email: '',
          message: ''
        },
        submitted: false
      };

      const updateData = { name: 'John Doe', email: 'john@example.com' };
      const action = updateFormData(updateData);
      const newState = contactReducer(initialState, action);

      expect(newState.formData.name).toBe('John Doe');
      expect(newState.formData.email).toBe('john@example.com');
      expect(newState.formData.message).toBe(''); // Should remain unchanged
    });

    it('should handle resetForm action', () => {
      const initialState = {
        isLoading: false,
        error: 'Some error',
        lastFetch: null,
        formData: {
          name: 'John Doe',
          email: 'john@example.com',
          message: 'Test message'
        },
        submitted: true
      };

      const action = resetForm();
      const newState = contactReducer(initialState, action);

      expect(newState.formData.name).toBe('');
      expect(newState.formData.email).toBe('');
      expect(newState.formData.message).toBe('');
      expect(newState.submitted).toBe(false);
      expect(newState.error).toBe(null);
    });
  });

  describe('Store Integration', () => {
    it('should create store with all reducers', () => {
      const store = configureStore({
        reducer: {
          app: appReducer,
          ui: uiReducer,
          contact: contactReducer,
        },
      });

      const state = store.getState();

      expect(state.app).toBeDefined();
      expect(state.ui).toBeDefined();
      expect(state.contact).toBeDefined();

      expect(state.app.isLoading).toBe(false);
      expect(state.ui.notifications).toEqual([]);
      expect(state.contact.formData.name).toBe('');
    });

    it('should handle dispatched actions correctly', () => {
      const store = configureStore({
        reducer: {
          app: appReducer,
          ui: uiReducer,
          contact: contactReducer,
        },
      });

      // Dispatch actions
      store.dispatch(setLoading(true));
      store.dispatch(addNotification({ type: 'success', message: 'Test' }));
      store.dispatch(updateFormData({ name: 'Test User' }));

      const state = store.getState();

      expect(state.app.isLoading).toBe(true);
      expect(state.ui.notifications).toHaveLength(1);
      expect(state.contact.formData.name).toBe('Test User');
    });
  });
});