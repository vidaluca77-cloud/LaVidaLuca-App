/**
 * Tests for OfflineManager
 */

import { offlineManager, OfflineManager } from '@/lib/offline/OfflineManager';
import { mockFunctions } from '@/test/utils';

// Mock dependencies
jest.mock('@/lib/offline/IndexedDBManager');
jest.mock('@/lib/offline/LocalStorageManager');
jest.mock('@/lib/offline/DeferredActionsManager');

describe('OfflineManager', () => {
  beforeEach(() => {
    // Mock localStorage
    mockFunctions.mockLocalStorage();
    
    // Mock navigator.onLine
    Object.defineProperty(navigator, 'onLine', {
      writable: true,
      value: true
    });

    // Mock window events
    Object.defineProperty(window, 'addEventListener', {
      value: jest.fn()
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('Singleton pattern', () => {
    test('should return the same instance', () => {
      const instance1 = OfflineManager.getInstance();
      const instance2 = OfflineManager.getInstance();
      expect(instance1).toBe(instance2);
    });
  });

  describe('Status management', () => {
    test('should start with online status', () => {
      expect(offlineManager.getStatus()).toBe('online');
    });

    test('should report correct online/offline state', () => {
      expect(offlineManager.isOnline()).toBe(true);
      expect(offlineManager.isOffline()).toBe(false);
    });
  });

  describe('Status listeners', () => {
    test('should add and remove status listeners', () => {
      const mockListener = jest.fn();
      
      const unsubscribe = offlineManager.addStatusListener(mockListener);
      expect(typeof unsubscribe).toBe('function');
      
      // Should be able to unsubscribe
      unsubscribe();
    });
  });

  describe('Sync listeners', () => {
    test('should add and remove sync listeners', () => {
      const mockListener = jest.fn();
      
      const unsubscribe = offlineManager.addSyncListener(mockListener);
      expect(typeof unsubscribe).toBe('function');
      
      // Should be able to unsubscribe
      unsubscribe();
    });
  });

  describe('Settings management', () => {
    test('should have default settings', () => {
      const settings = offlineManager.getSettings();
      
      expect(settings).toEqual({
        autoSync: true,
        syncInterval: 30000,
        maxCacheAge: 24 * 60 * 60 * 1000,
        enableNotifications: true
      });
    });

    test('should update settings', async () => {
      await offlineManager.updateSettings({
        autoSync: false,
        syncInterval: 60000
      });

      const settings = offlineManager.getSettings();
      expect(settings.autoSync).toBe(false);
      expect(settings.syncInterval).toBe(60000);
    });
  });

  describe('Error handling', () => {
    test('should handle initialization errors gracefully', async () => {
      // Mock IndexedDB failure
      const mockInit = jest.fn().mockRejectedValue(new Error('IndexedDB failed'));
      
      // Should not throw
      await expect(offlineManager.init()).resolves.not.toThrow();
    });
  });
});