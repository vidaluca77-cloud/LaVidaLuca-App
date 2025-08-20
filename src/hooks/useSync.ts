/**
 * useSync hook for data synchronization state management
 * Provides React integration for sync functionality
 */

import { useEffect, useState, useCallback, useRef } from 'react';
import {
  SyncManager,
  SyncConfig,
  SyncItem,
  SyncStrategy,
  SyncStatus,
  createSyncManager,
  getSyncManager
} from '@/lib/syncManager';
import { logger } from '@/lib/logger';

export interface UseSyncOptions extends Partial<SyncConfig> {
  autoInitialize?: boolean;
  strategies?: SyncStrategy[];
  onSyncComplete?: (item: SyncItem) => void;
  onSyncError?: (item: SyncItem, error: Error) => void;
  onStatusChange?: (status: SyncStatus) => void;
}

export interface UseSyncReturn {
  // Sync state
  status: SyncStatus;
  isOnline: boolean;
  
  // Queue management
  queueSync: (
    id: string,
    type: string,
    data: any,
    priority?: SyncItem['priority'],
    ttl?: number
  ) => void;
  removeFromQueue: (id: string) => boolean;
  clearQueue: () => void;
  forceSync: () => Promise<void>;
  
  // Cache management
  cache: <T>(key: string, data: T, ttl?: number) => void;
  getCached: <T>(key: string) => T | null;
  isCached: (key: string) => boolean;
  invalidateCache: (key: string) => void;
  clearCache: () => void;
  
  // Strategy management
  registerStrategy: (strategy: SyncStrategy) => void;
  
  // Utilities
  refresh: () => void;
}

export const useSync = (options: UseSyncOptions = {}): UseSyncReturn => {
  const {
    autoInitialize = true,
    strategies = [],
    onSyncComplete,
    onSyncError,
    onStatusChange,
    ...config
  } = options;

  // State
  const [status, setStatus] = useState<SyncStatus>({
    pending: 0,
    syncing: 0,
    failed: 0,
    lastSyncTime: null,
    isOnline: navigator.onLine,
    cacheSize: 0,
    queueSize: 0,
  });

  const [isOnline, setIsOnline] = useState(navigator.onLine);

  // Refs
  const managerRef = useRef<SyncManager | null>(null);
  const statusIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Initialize sync manager
  useEffect(() => {
    if (!autoInitialize) return;

    managerRef.current = createSyncManager(config);

    // Register provided strategies
    strategies.forEach(strategy => {
      if (onSyncComplete || onSyncError) {
        const enhancedStrategy: SyncStrategy = {
          ...strategy,
          onSuccess: (item) => {
            strategy.onSuccess?.(item);
            onSyncComplete?.(item);
          },
          onFailure: (item, error) => {
            strategy.onFailure?.(item, error);
            onSyncError?.(item, error);
          },
        };
        managerRef.current!.registerStrategy(enhancedStrategy);
      } else {
        managerRef.current!.registerStrategy(strategy);
      }
    });

    logger.info('Sync manager initialized in hook', {
      strategiesCount: strategies.length
    }, 'sync-hook');

    return () => {
      managerRef.current?.stop();
    };
  }, [autoInitialize]);

  // Update status periodically
  useEffect(() => {
    const updateStatus = () => {
      if (managerRef.current) {
        const newStatus = managerRef.current.getStatus();
        setStatus(newStatus);
        setIsOnline(newStatus.isOnline);
        onStatusChange?.(newStatus);
      }
    };

    // Update immediately
    updateStatus();

    // Update periodically
    statusIntervalRef.current = setInterval(updateStatus, 2000);

    return () => {
      if (statusIntervalRef.current) {
        clearInterval(statusIntervalRef.current);
      }
    };
  }, [onStatusChange]);

  // Listen for online/offline events
  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      logger.info('Network online detected in sync hook', {}, 'sync-hook');
    };

    const handleOffline = () => {
      setIsOnline(false);
      logger.info('Network offline detected in sync hook', {}, 'sync-hook');
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Queue sync function
  const queueSync = useCallback((
    id: string,
    type: string,
    data: any,
    priority: SyncItem['priority'] = 'medium',
    ttl?: number
  ): void => {
    if (!managerRef.current) {
      logger.warn('Attempted to queue sync but manager not initialized', {
        id, type
      }, 'sync-hook');
      return;
    }

    managerRef.current.queueSync(id, type, data, priority, ttl);
    
    logger.debug('Sync queued via hook', {
      id, type, priority
    }, 'sync-hook');
  }, []);

  // Remove from queue function
  const removeFromQueue = useCallback((id: string): boolean => {
    if (!managerRef.current) {
      logger.warn('Attempted to remove from queue but manager not initialized', {
        id
      }, 'sync-hook');
      return false;
    }

    const removed = managerRef.current.removeFromQueue(id);
    
    if (removed) {
      logger.debug('Item removed from queue via hook', { id }, 'sync-hook');
    }
    
    return removed;
  }, []);

  // Clear queue function
  const clearQueue = useCallback((): void => {
    if (!managerRef.current) {
      return;
    }

    managerRef.current.clearQueue();
    logger.info('Sync queue cleared via hook', {}, 'sync-hook');
  }, []);

  // Force sync function
  const forceSync = useCallback(async (): Promise<void> => {
    if (!managerRef.current) {
      throw new Error('Sync manager not initialized');
    }

    logger.info('Force sync triggered via hook', {}, 'sync-hook');
    await managerRef.current.forcSync();
  }, []);

  // Cache function
  const cache = useCallback(<T>(key: string, data: T, ttl?: number): void => {
    if (!managerRef.current) {
      logger.warn('Attempted to cache but manager not initialized', {
        key
      }, 'sync-hook');
      return;
    }

    managerRef.current.cache(key, data, ttl);
    
    logger.debug('Data cached via hook', { key, ttl }, 'sync-hook');
  }, []);

  // Get cached function
  const getCached = useCallback(<T>(key: string): T | null => {
    if (!managerRef.current) {
      logger.warn('Attempted to get cache but manager not initialized', {
        key
      }, 'sync-hook');
      return null;
    }

    const result = managerRef.current.getCached<T>(key);
    
    logger.debug('Cache access via hook', {
      key,
      hit: result !== null
    }, 'sync-hook');
    
    return result;
  }, []);

  // Is cached function
  const isCached = useCallback((key: string): boolean => {
    if (!managerRef.current) {
      return false;
    }

    return managerRef.current.isCached(key);
  }, []);

  // Invalidate cache function
  const invalidateCache = useCallback((key: string): void => {
    if (!managerRef.current) {
      return;
    }

    managerRef.current.invalidateCache(key);
    logger.debug('Cache invalidated via hook', { key }, 'sync-hook');
  }, []);

  // Clear cache function
  const clearCache = useCallback((): void => {
    if (!managerRef.current) {
      return;
    }

    managerRef.current.clearCache();
    logger.info('Cache cleared via hook', {}, 'sync-hook');
  }, []);

  // Register strategy function
  const registerStrategy = useCallback((strategy: SyncStrategy): void => {
    if (!managerRef.current) {
      logger.warn('Attempted to register strategy but manager not initialized', {
        strategyName: strategy.name
      }, 'sync-hook');
      return;
    }

    // Enhance strategy with callback support
    const enhancedStrategy: SyncStrategy = {
      ...strategy,
      onSuccess: (item) => {
        strategy.onSuccess?.(item);
        onSyncComplete?.(item);
      },
      onFailure: (item, error) => {
        strategy.onFailure?.(item, error);
        onSyncError?.(item, error);
      },
    };

    managerRef.current.registerStrategy(enhancedStrategy);
    
    logger.info('Strategy registered via hook', {
      strategyName: strategy.name
    }, 'sync-hook');
  }, [onSyncComplete, onSyncError]);

  // Refresh function
  const refresh = useCallback((): void => {
    if (managerRef.current) {
      const newStatus = managerRef.current.getStatus();
      setStatus(newStatus);
      setIsOnline(newStatus.isOnline);
      onStatusChange?.(newStatus);
    }
  }, [onStatusChange]);

  return {
    // State
    status,
    isOnline,
    
    // Queue management
    queueSync,
    removeFromQueue,
    clearQueue,
    forceSync,
    
    // Cache management
    cache,
    getCached,
    isCached,
    invalidateCache,
    clearCache,
    
    // Strategy management
    registerStrategy,
    
    // Utilities
    refresh,
  };
};

/**
 * Hook for using cached data with automatic sync
 */
export const useSyncedData = <T>(
  key: string,
  fetcher: () => Promise<T>,
  options: {
    ttl?: number;
    priority?: SyncItem['priority'];
    syncOnMount?: boolean;
    syncOnFocus?: boolean;
  } = {}
): {
  data: T | null;
  isLoading: boolean;
  error: Error | null;
  refresh: () => Promise<void>;
  lastUpdated: Date | null;
} => {
  const { ttl, priority = 'medium', syncOnMount = true, syncOnFocus = false } = options;
  const { cache, getCached, queueSync } = useSync();
  
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  // Load cached data on mount
  useEffect(() => {
    const cached = getCached<{ data: T; timestamp: Date }>(key);
    
    if (cached) {
      setData(cached.data);
      setLastUpdated(cached.timestamp);
      
      logger.debug('Cached data loaded in useSyncedData', { key }, 'sync-hook');
    } else if (syncOnMount) {
      // Queue sync if no cached data
      queueSync(key, 'fetch', { fetcher: fetcher.toString() }, priority, ttl);
    }
  }, [key, syncOnMount]);

  // Refresh function
  const refresh = useCallback(async (): Promise<void> => {
    setIsLoading(true);
    setError(null);

    try {
      logger.info('Refreshing synced data', { key }, 'sync-hook');
      
      const freshData = await fetcher();
      const timestamp = new Date();
      
      // Cache the fresh data
      cache(key, { data: freshData, timestamp }, ttl);
      
      setData(freshData);
      setLastUpdated(timestamp);
      
      logger.info('Synced data refreshed successfully', { key }, 'sync-hook');
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      setError(error);
      
      logger.error('Error refreshing synced data', {
        key,
        error: error.message
      }, 'sync-hook');
    } finally {
      setIsLoading(false);
    }
  }, [key, fetcher, cache, ttl]);

  // Sync on window focus
  useEffect(() => {
    if (!syncOnFocus) return;

    const handleFocus = () => {
      // Only refresh if data is older than 5 minutes
      if (lastUpdated && Date.now() - lastUpdated.getTime() > 5 * 60 * 1000) {
        refresh();
      }
    };

    window.addEventListener('focus', handleFocus);
    return () => window.removeEventListener('focus', handleFocus);
  }, [syncOnFocus, lastUpdated, refresh]);

  return {
    data,
    isLoading,
    error,
    refresh,
    lastUpdated,
  };
};

/**
 * Hook for managing sync queue operations
 */
export const useSyncQueue = (): {
  queueSize: number;
  pendingItems: number;
  failedItems: number;
  isProcessing: boolean;
  clearQueue: () => void;
  forceSync: () => Promise<void>;
} => {
  const { status, clearQueue, forceSync } = useSync({ autoInitialize: false });

  return {
    queueSize: status.queueSize,
    pendingItems: status.pending,
    failedItems: status.failed,
    isProcessing: status.syncing > 0,
    clearQueue,
    forceSync,
  };
};