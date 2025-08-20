/**
 * @jest-environment jsdom
 */

import { renderHook, act } from '@testing-library/react';
import { useConnectionStatus } from '../../src/hooks/useConnectionStatus';

// Mock dependencies
jest.mock('../../src/lib/offline-queue', () => ({
  offlineQueue: {
    getQueueStatus: jest.fn(() => ({
      length: 0,
      isProcessing: false,
      isOnline: true,
      actions: [],
    })),
    onSync: jest.fn(),
    offSync: jest.fn(),
  },
}));

const { offlineQueue } = require('../../src/lib/offline-queue');

describe('useConnectionStatus', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Reset navigator.onLine
    Object.defineProperty(navigator, 'onLine', {
      writable: true,
      value: true,
    });

    // Reset queue status
    offlineQueue.getQueueStatus.mockReturnValue({
      length: 0,
      isProcessing: false,
      isOnline: true,
      actions: [],
    });
  });

  it('should return initial connection status', () => {
    const { result } = renderHook(() => useConnectionStatus());

    expect(result.current.isOnline).toBe(true);
    expect(result.current.isOfflineMode).toBe(false);
    expect(result.current.queueLength).toBe(0);
    expect(result.current.isProcessing).toBe(false);
    expect(result.current.lastOnline).toBeNull();
    expect(result.current.lastOffline).toBeNull();
  });

  it('should update status when going offline', () => {
    const { result } = renderHook(() => useConnectionStatus());

    act(() => {
      Object.defineProperty(navigator, 'onLine', {
        writable: true,
        value: false,
      });

      offlineQueue.getQueueStatus.mockReturnValue({
        length: 0,
        isProcessing: false,
        isOnline: false,
        actions: [],
      });

      // Simulate offline event
      window.dispatchEvent(new Event('offline'));
    });

    expect(result.current.isOnline).toBe(false);
    expect(result.current.isOfflineMode).toBe(true);
    expect(result.current.lastOffline).toBeInstanceOf(Date);
  });

  it('should update status when coming back online', () => {
    // Start offline
    Object.defineProperty(navigator, 'onLine', {
      writable: true,
      value: false,
    });

    offlineQueue.getQueueStatus.mockReturnValue({
      length: 0,
      isProcessing: false,
      isOnline: false,
      actions: [],
    });

    const { result } = renderHook(() => useConnectionStatus());

    act(() => {
      // Go online
      Object.defineProperty(navigator, 'onLine', {
        writable: true,
        value: true,
      });

      offlineQueue.getQueueStatus.mockReturnValue({
        length: 0,
        isProcessing: false,
        isOnline: true,
        actions: [],
      });

      // Simulate online event
      window.dispatchEvent(new Event('online'));
    });

    expect(result.current.isOnline).toBe(true);
    expect(result.current.isOfflineMode).toBe(false);
    expect(result.current.lastOnline).toBeInstanceOf(Date);
  });

  it('should show offline mode when queue has items', () => {
    offlineQueue.getQueueStatus.mockReturnValue({
      length: 3,
      isProcessing: false,
      isOnline: true,
      actions: [],
    });

    const { result } = renderHook(() => useConnectionStatus());

    expect(result.current.isOnline).toBe(true);
    expect(result.current.isOfflineMode).toBe(true); // True because queue has items
    expect(result.current.queueLength).toBe(3);
  });

  it('should update processing status', () => {
    offlineQueue.getQueueStatus.mockReturnValue({
      length: 2,
      isProcessing: true,
      isOnline: true,
      actions: [],
    });

    const { result } = renderHook(() => useConnectionStatus());

    expect(result.current.isProcessing).toBe(true);
    expect(result.current.queueLength).toBe(2);
  });

  it('should register and cleanup sync callbacks', () => {
    const { unmount } = renderHook(() => useConnectionStatus());

    expect(offlineQueue.onSync).toHaveBeenCalled();

    unmount();

    expect(offlineQueue.offSync).toHaveBeenCalled();
  });

  it('should handle sync callbacks correctly', () => {
    let syncCallback: Function;
    
    offlineQueue.onSync.mockImplementation((callback) => {
      syncCallback = callback;
    });

    const { result } = renderHook(() => useConnectionStatus());

    // Simulate sync callback
    act(() => {
      if (syncCallback) {
        syncCallback();
      }
    });

    // Should trigger status update
    expect(offlineQueue.getQueueStatus).toHaveBeenCalled();
  });

  it('should periodically update status', async () => {
    jest.useFakeTimers();

    const { result } = renderHook(() => useConnectionStatus());

    const initialCalls = offlineQueue.getQueueStatus.mock.calls.length;

    // Fast-forward 5 seconds
    act(() => {
      jest.advanceTimersByTime(5000);
    });

    expect(offlineQueue.getQueueStatus.mock.calls.length).toBeGreaterThan(initialCalls);

    jest.useRealTimers();
  });

  it('should cleanup intervals on unmount', () => {
    jest.useFakeTimers();
    const clearIntervalSpy = jest.spyOn(global, 'clearInterval');

    const { unmount } = renderHook(() => useConnectionStatus());

    unmount();

    expect(clearIntervalSpy).toHaveBeenCalled();

    clearIntervalSpy.mockRestore();
    jest.useRealTimers();
  });

  it('should handle SSR environment gracefully', () => {
    // Mock window as undefined to simulate SSR
    const originalWindow = global.window;
    delete (global as any).window;

    const { result } = renderHook(() => useConnectionStatus());

    // Should return default values without errors
    expect(result.current.isOnline).toBe(true);
    expect(result.current.isOfflineMode).toBe(false);

    // Restore window
    global.window = originalWindow;
  });
});