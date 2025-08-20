/**
 * Tests for useOffline hook
 */

import { renderHook, act } from '@testing-library/react';
import { mockFunctions } from '@/test/utils';

// Mock dependencies
const mockOfflineManager = {
  init: jest.fn().mockResolvedValue(undefined),
  getStatus: jest.fn().mockReturnValue('online'),
  addStatusListener: jest.fn().mockReturnValue(() => {}),
  addSyncListener: jest.fn().mockReturnValue(() => {}),
  getStats: jest.fn().mockResolvedValue({
    deferredActions: { total: 0 },
    storage: {},
    lastSync: undefined
  }),
  cacheData: jest.fn().mockResolvedValue(true),
  getCachedData: jest.fn().mockResolvedValue(null),
  queueAction: jest.fn().mockResolvedValue('action-id'),
  sync: jest.fn().mockResolvedValue({ success: true, actionsProcessed: 0, errors: [], timestamp: Date.now() })
};

jest.mock('@/lib/offline/OfflineManager', () => ({
  offlineManager: mockOfflineManager
}));

import { useOffline } from '@/hooks/useOffline';

describe('useOffline', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockFunctions.mockLocalStorage();
  });

  describe('Hook initialization', () => {
    test('should initialize with online status', () => {
      const { result } = renderHook(() => useOffline());

      expect(result.current.status).toBe('online');
      expect(result.current.isOnline).toBe(true);
      expect(result.current.isOffline).toBe(false);
      expect(result.current.isSyncing).toBe(false);
    });

    test('should call offline manager init', () => {
      renderHook(() => useOffline());
      expect(mockOfflineManager.init).toHaveBeenCalled();
    });
  });

  describe('Data caching', () => {
    test('should cache data successfully', async () => {
      const { result } = renderHook(() => useOffline());

      await act(async () => {
        const success = await result.current.cacheData('test-key', { data: 'test' });
        expect(success).toBe(true);
      });

      expect(mockOfflineManager.cacheData).toHaveBeenCalledWith('test-key', { data: 'test' }, 'cache', undefined);
    });

    test('should retrieve cached data', async () => {
      mockOfflineManager.getCachedData.mockResolvedValue({ data: 'cached' });

      const { result } = renderHook(() => useOffline());

      await act(async () => {
        const data = await result.current.getCachedData('test-key');
        expect(data).toEqual({ data: 'cached' });
      });

      expect(mockOfflineManager.getCachedData).toHaveBeenCalledWith('test-key', 'cache');
    });
  });

  describe('Action queuing', () => {
    test('should queue actions', async () => {
      const { result } = renderHook(() => useOffline());

      await act(async () => {
        const actionId = await result.current.queueAction(
          'api_call',
          '/api/test',
          'POST',
          { test: 'data' }
        );
        expect(actionId).toBe('action-id');
      });

      expect(mockOfflineManager.queueAction).toHaveBeenCalledWith(
        'api_call',
        '/api/test',
        'POST',
        { test: 'data' },
        undefined
      );
    });
  });

  describe('Sync operations', () => {
    test('should perform sync', async () => {
      const { result } = renderHook(() => useOffline());

      await act(async () => {
        const syncResult = await result.current.sync();
        expect(syncResult.success).toBe(true);
      });

      expect(mockOfflineManager.sync).toHaveBeenCalled();
    });
  });

  describe('Statistics', () => {
    test('should provide stats', () => {
      const { result } = renderHook(() => useOffline());

      expect(result.current.stats).toEqual({
        pendingActions: 0,
        storageUsage: undefined,
        lastSync: undefined
      });
    });
  });

  describe('Error handling', () => {
    test('should handle cache data errors gracefully', async () => {
      mockOfflineManager.cacheData.mockRejectedValue(new Error('Cache failed'));

      const { result } = renderHook(() => useOffline());

      await act(async () => {
        const success = await result.current.cacheData('test-key', { data: 'test' });
        expect(success).toBe(false);
      });
    });

    test('should handle get cached data errors gracefully', async () => {
      mockOfflineManager.getCachedData.mockRejectedValue(new Error('Get failed'));

      const { result } = renderHook(() => useOffline());

      await act(async () => {
        const data = await result.current.getCachedData('test-key');
        expect(data).toBe(null);
      });
    });

    test('should handle queue action errors', async () => {
      mockOfflineManager.queueAction.mockRejectedValue(new Error('Queue failed'));

      const { result } = renderHook(() => useOffline());

      await act(async () => {
        await expect(result.current.queueAction('api_call', '/api/test', 'POST')).rejects.toThrow('Queue failed');
      });
    });

    test('should handle sync errors', async () => {
      mockOfflineManager.sync.mockRejectedValue(new Error('Sync failed'));

      const { result } = renderHook(() => useOffline());

      await act(async () => {
        await expect(result.current.sync()).rejects.toThrow('Sync failed');
      });
    });
  });
});