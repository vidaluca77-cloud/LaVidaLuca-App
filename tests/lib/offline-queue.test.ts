/**
 * @jest-environment jsdom
 */

import { offlineQueue } from '../../src/lib/offline-queue';

// Mock dependencies
jest.mock('../../src/lib/offline-cache', () => ({
  offlineCacheManager: {
    set: jest.fn(),
    get: jest.fn(),
  },
}));

jest.mock('../../src/lib/logger', () => ({
  logger: {
    info: jest.fn(),
    warn: jest.fn(),
    error: jest.fn(),
  },
}));

// Mock fetch
global.fetch = jest.fn();

// Mock crypto.randomUUID
Object.defineProperty(global, 'crypto', {
  value: {
    randomUUID: jest.fn(() => 'mock-uuid-' + Date.now()),
  },
});

describe('OfflineQueueManager', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Mock navigator.onLine
    Object.defineProperty(navigator, 'onLine', {
      writable: true,
      value: true,
    });

    // Clear queue
    offlineQueue.clearQueue();
  });

  describe('Queue management', () => {
    it('should enqueue actions correctly', async () => {
      const actionId = await offlineQueue.enqueue('TEST_ACTION', { test: 'data' });
      
      expect(actionId).toBeDefined();
      expect(typeof actionId).toBe('string');
      
      const status = offlineQueue.getQueueStatus();
      expect(status.length).toBe(1);
      expect(status.actions[0].type).toBe('TEST_ACTION');
    });

    it('should respect priority ordering', async () => {
      await offlineQueue.enqueue('LOW_PRIORITY', { data: 'low' }, { priority: 'low' });
      await offlineQueue.enqueue('HIGH_PRIORITY', { data: 'high' }, { priority: 'high' });
      await offlineQueue.enqueue('NORMAL_PRIORITY', { data: 'normal' }, { priority: 'normal' });

      const status = offlineQueue.getQueueStatus();
      expect(status.actions[0].type).toBe('HIGH_PRIORITY');
      expect(status.actions[1].type).toBe('NORMAL_PRIORITY');
      expect(status.actions[2].type).toBe('LOW_PRIORITY');
    });

    it('should dequeue actions correctly', async () => {
      const actionId = await offlineQueue.enqueue('DEQUEUE_TEST', { test: 'data' });
      
      let status = offlineQueue.getQueueStatus();
      expect(status.length).toBe(1);

      const dequeued = await offlineQueue.dequeue(actionId);
      expect(dequeued).toBe(true);

      status = offlineQueue.getQueueStatus();
      expect(status.length).toBe(0);
    });

    it('should handle dequeuing non-existent actions', async () => {
      const dequeued = await offlineQueue.dequeue('non-existent-id');
      expect(dequeued).toBe(false);
    });

    it('should enforce max queue size', async () => {
      // Create a new instance with small max size for testing
      const smallQueueManager = new (require('../../src/lib/offline-queue').OfflineQueueManager)({
        maxQueueSize: 3,
        autoSync: false,
      });

      await smallQueueManager.enqueue('ACTION_1', {});
      await smallQueueManager.enqueue('ACTION_2', {});
      await smallQueueManager.enqueue('ACTION_3', {});
      await smallQueueManager.enqueue('ACTION_4', {}); // Should remove oldest

      const status = smallQueueManager.getQueueStatus();
      expect(status.length).toBe(3);
      expect(status.actions.find(a => a.type === 'ACTION_1')).toBeUndefined();
    });
  });

  describe('Queue processing', () => {
    it('should process contact form actions', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        status: 200,
      });

      await offlineQueue.enqueue('CONTACT_FORM_SUBMIT', {
        name: 'Test User',
        email: 'test@example.com',
        message: 'Test message',
      });

      await offlineQueue.processQueue();

      expect(global.fetch).toHaveBeenCalledWith('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: 'Test User',
          email: 'test@example.com',
          message: 'Test message',
        }),
      });

      const status = offlineQueue.getQueueStatus();
      expect(status.length).toBe(0); // Should be removed after successful processing
    });

    it('should retry failed actions', async () => {
      (global.fetch as jest.Mock)
        .mockRejectedValueOnce(new Error('Network error'))
        .mockResolvedValueOnce({ ok: true, status: 200 });

      await offlineQueue.enqueue('CONTACT_FORM_SUBMIT', { test: 'data' });

      // First processing should fail and retry
      await offlineQueue.processQueue();
      
      let status = offlineQueue.getQueueStatus();
      expect(status.length).toBe(1);
      expect(status.actions[0].retries).toBe(1);

      // Second processing should succeed
      await offlineQueue.processQueue();
      
      status = offlineQueue.getQueueStatus();
      expect(status.length).toBe(0);
    });

    it('should remove actions after max retries', async () => {
      (global.fetch as jest.Mock).mockRejectedValue(new Error('Persistent error'));

      await offlineQueue.enqueue('CONTACT_FORM_SUBMIT', { test: 'data' }, { maxRetries: 2 });

      // Process multiple times to exceed max retries
      await offlineQueue.processQueue();
      await offlineQueue.processQueue();
      await offlineQueue.processQueue();

      const status = offlineQueue.getQueueStatus();
      expect(status.length).toBe(0); // Should be removed after exceeding max retries
    });

    it('should handle unknown action types', async () => {
      await offlineQueue.enqueue('UNKNOWN_ACTION_TYPE', { test: 'data' });

      await offlineQueue.processQueue();

      const status = offlineQueue.getQueueStatus();
      expect(status.length).toBe(0); // Should be removed even if unknown
    });
  });

  describe('Online/offline handling', () => {
    it('should detect online status correctly', () => {
      const status = offlineQueue.getQueueStatus();
      expect(status.isOnline).toBe(true);

      // Mock offline
      Object.defineProperty(navigator, 'onLine', {
        writable: true,
        value: false,
      });

      const offlineStatus = offlineQueue.getQueueStatus();
      expect(offlineStatus.isOnline).toBe(false);
    });

    it('should not auto-process when offline', async () => {
      Object.defineProperty(navigator, 'onLine', {
        writable: true,
        value: false,
      });

      const processSpy = jest.spyOn(offlineQueue, 'processQueue');

      await offlineQueue.enqueue('TEST_ACTION', { test: 'data' });

      // Should not call processQueue when offline
      expect(processSpy).not.toHaveBeenCalled();

      processSpy.mockRestore();
    });
  });

  describe('Sync callbacks', () => {
    it('should call sync callbacks on success', async () => {
      const callback = jest.fn();
      offlineQueue.onSync(callback);

      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        status: 200,
      });

      await offlineQueue.enqueue('CONTACT_FORM_SUBMIT', { test: 'data' });
      await offlineQueue.processQueue();

      expect(callback).toHaveBeenCalledWith(
        expect.objectContaining({ type: 'CONTACT_FORM_SUBMIT' }),
        true
      );

      offlineQueue.offSync(callback);
    });

    it('should call sync callbacks on failure after max retries', async () => {
      const callback = jest.fn();
      offlineQueue.onSync(callback);

      (global.fetch as jest.Mock).mockRejectedValue(new Error('Persistent error'));

      await offlineQueue.enqueue('CONTACT_FORM_SUBMIT', { test: 'data' }, { maxRetries: 1 });
      await offlineQueue.processQueue();
      await offlineQueue.processQueue();

      expect(callback).toHaveBeenCalledWith(
        expect.objectContaining({ type: 'CONTACT_FORM_SUBMIT' }),
        false
      );

      offlineQueue.offSync(callback);
    });

    it('should remove sync callbacks correctly', () => {
      const callback = jest.fn();
      offlineQueue.onSync(callback);
      offlineQueue.offSync(callback);

      // Callback should not be called after removal
      offlineQueue.processQueue();
      expect(callback).not.toHaveBeenCalled();
    });
  });

  describe('Clear queue', () => {
    it('should clear all actions from queue', async () => {
      await offlineQueue.enqueue('ACTION_1', { test: 'data1' });
      await offlineQueue.enqueue('ACTION_2', { test: 'data2' });

      let status = offlineQueue.getQueueStatus();
      expect(status.length).toBe(2);

      await offlineQueue.clearQueue();

      status = offlineQueue.getQueueStatus();
      expect(status.length).toBe(0);
    });
  });
});