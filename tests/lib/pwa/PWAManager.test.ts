/**
 * Tests for PWAManager
 */

import { pwaManager, PWAManager } from '@/lib/pwa/PWAManager';

// Mock service worker
const mockServiceWorker = {
  register: jest.fn(),
  addEventListener: jest.fn(),
  getRegistration: jest.fn()
};

// Mock navigator
Object.defineProperty(navigator, 'serviceWorker', {
  value: mockServiceWorker,
  writable: true
});

describe('PWAManager', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Mock window events
    Object.defineProperty(window, 'addEventListener', {
      value: jest.fn()
    });
  });

  describe('Singleton pattern', () => {
    test('should return the same instance', () => {
      const instance1 = PWAManager.getInstance();
      const instance2 = PWAManager.getInstance();
      expect(instance1).toBe(instance2);
    });
  });

  describe('Service Worker support detection', () => {
    test('should detect service worker support', async () => {
      mockServiceWorker.register.mockResolvedValue({
        scope: '/',
        addEventListener: jest.fn()
      });

      await pwaManager.init();
      
      expect(mockServiceWorker.register).toHaveBeenCalledWith('/sw.js', {
        scope: '/'
      });
    });

    test('should handle service worker registration failure', async () => {
      mockServiceWorker.register.mockRejectedValue(new Error('Registration failed'));

      // Should not throw
      await expect(pwaManager.init()).resolves.not.toThrow();
    });
  });

  describe('PWA detection', () => {
    test('should detect standalone mode', () => {
      // Mock standalone display mode
      window.matchMedia = jest.fn().mockReturnValue({
        matches: true
      });

      expect(pwaManager.isPWA()).toBe(true);
    });

    test('should detect non-PWA mode', () => {
      // Mock browser mode
      window.matchMedia = jest.fn().mockReturnValue({
        matches: false
      });

      // Mock iOS standalone
      (window.navigator as any).standalone = false;

      expect(pwaManager.isPWA()).toBe(false);
    });
  });

  describe('Install prompt', () => {
    test('should handle install prompt unavailable', async () => {
      const result = await pwaManager.showInstallPrompt();
      expect(result).toBe('unavailable');
    });
  });

  describe('Push notifications', () => {
    test('should handle push notification setup', async () => {
      // Mock Notification API
      Object.defineProperty(window, 'Notification', {
        value: {
          requestPermission: jest.fn().mockResolvedValue('granted')
        },
        writable: true
      });

      // Mock PushManager
      Object.defineProperty(window, 'PushManager', {
        value: {},
        writable: true
      });

      const mockRegistration = {
        pushManager: {
          subscribe: jest.fn()
        }
      };

      // Mock getting registration
      jest.spyOn(pwaManager, 'getRegistration').mockReturnValue(mockRegistration as any);

      const result = await pwaManager.setupPushNotifications();
      expect(result).toBe(true);
    });

    test('should handle notification permission denied', async () => {
      // Mock Notification API
      Object.defineProperty(window, 'Notification', {
        value: {
          requestPermission: jest.fn().mockResolvedValue('denied')
        },
        writable: true
      });

      Object.defineProperty(window, 'PushManager', {
        value: {},
        writable: true
      });

      const mockRegistration = {
        pushManager: {
          subscribe: jest.fn()
        }
      };

      jest.spyOn(pwaManager, 'getRegistration').mockReturnValue(mockRegistration as any);

      const result = await pwaManager.setupPushNotifications();
      expect(result).toBe(false);
    });
  });

  describe('Update detection', () => {
    test('should initially have no updates available', () => {
      expect(pwaManager.isUpdateAvailable()).toBe(false);
    });
  });
});