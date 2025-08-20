/**
 * useOffline Hook
 * React hook for managing offline state and functionality
 */

'use client';

import { useState, useEffect, useCallback } from 'react';
import { offlineManager, OfflineStatus, SyncResult } from '@/lib/offline/OfflineManager';
import { DeferredAction } from '@/lib/offline/DeferredActionsManager';

export interface OfflineHookReturn {
  // Status
  status: OfflineStatus;
  isOnline: boolean;
  isOffline: boolean;
  isSyncing: boolean;

  // Actions
  cacheData: <T>(key: string, data: T, expiresInMs?: number) => Promise<boolean>;
  getCachedData: <T>(key: string) => Promise<T | null>;
  queueAction: (
    type: DeferredAction['type'],
    endpoint: string,
    method: DeferredAction['method'],
    data?: any,
    options?: {
      headers?: Record<string, string>;
      priority?: DeferredAction['priority'];
      onSuccess?: (result: any) => void;
      onError?: (error: string) => void;
    }
  ) => Promise<string>;
  sync: () => Promise<SyncResult>;

  // Statistics
  stats: {
    pendingActions: number;
    storageUsage?: {
      indexedDB?: { usage: number; quota: number } | null;
      localStorage?: { used: number; available: number } | null;
    };
    lastSync?: Date;
  };

  // Events
  lastSyncResult: SyncResult | null;
}

export const useOffline = (): OfflineHookReturn => {
  const [status, setStatus] = useState<OfflineStatus>('online');
  const [stats, setStats] = useState({
    pendingActions: 0,
    storageUsage: undefined,
    lastSync: undefined
  });
  const [lastSyncResult, setLastSyncResult] = useState<SyncResult | null>(null);

  // Initialize offline manager
  useEffect(() => {
    const initOfflineManager = async () => {
      try {
        await offlineManager.init();
        setStatus(offlineManager.getStatus());
        
        // Load initial stats
        const offlineStats = await offlineManager.getStats();
        setStats({
          pendingActions: offlineStats.deferredActions.total,
          storageUsage: offlineStats.storage,
          lastSync: offlineStats.lastSync
        });
      } catch (error) {
        console.error('Failed to initialize offline manager:', error);
      }
    };

    initOfflineManager();
  }, []);

  // Listen for status changes
  useEffect(() => {
    const unsubscribeStatus = offlineManager.addStatusListener((newStatus) => {
      setStatus(newStatus);
    });

    const unsubscribeSync = offlineManager.addSyncListener((result) => {
      setLastSyncResult(result);
      
      // Refresh stats after sync
      offlineManager.getStats().then((offlineStats) => {
        setStats({
          pendingActions: offlineStats.deferredActions.total,
          storageUsage: offlineStats.storage,
          lastSync: offlineStats.lastSync
        });
      });
    });

    return () => {
      unsubscribeStatus();
      unsubscribeSync();
    };
  }, []);

  // Cache data function
  const cacheData = useCallback(async <T>(
    key: string, 
    data: T, 
    expiresInMs?: number
  ): Promise<boolean> => {
    try {
      return await offlineManager.cacheData(key, data, 'cache', expiresInMs);
    } catch (error) {
      console.error('Failed to cache data:', error);
      return false;
    }
  }, []);

  // Get cached data function
  const getCachedData = useCallback(async <T>(key: string): Promise<T | null> => {
    try {
      return await offlineManager.getCachedData<T>(key, 'cache');
    } catch (error) {
      console.error('Failed to get cached data:', error);
      return null;
    }
  }, []);

  // Queue action function
  const queueAction = useCallback(async (
    type: DeferredAction['type'],
    endpoint: string,
    method: DeferredAction['method'],
    data?: any,
    options?: {
      headers?: Record<string, string>;
      priority?: DeferredAction['priority'];
      onSuccess?: (result: any) => void;
      onError?: (error: string) => void;
    }
  ): Promise<string> => {
    try {
      const actionId = await offlineManager.queueAction(type, endpoint, method, data, options);
      
      // Refresh stats
      const offlineStats = await offlineManager.getStats();
      setStats(prev => ({
        ...prev,
        pendingActions: offlineStats.deferredActions.total
      }));

      return actionId;
    } catch (error) {
      console.error('Failed to queue action:', error);
      throw error;
    }
  }, []);

  // Sync function
  const sync = useCallback(async (): Promise<SyncResult> => {
    try {
      return await offlineManager.sync();
    } catch (error) {
      console.error('Sync failed:', error);
      throw error;
    }
  }, []);

  return {
    // Status
    status,
    isOnline: status === 'online',
    isOffline: status === 'offline',
    isSyncing: status === 'syncing',

    // Actions
    cacheData,
    getCachedData,
    queueAction,
    sync,

    // Statistics
    stats,

    // Events
    lastSyncResult
  };
};