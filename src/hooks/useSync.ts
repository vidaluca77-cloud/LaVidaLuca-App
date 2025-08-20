'use client';

import { useState, useEffect, useCallback } from 'react';
import { 
  createSyncManager, 
  getSyncManager,
  type SyncStatus, 
  type SyncResult, 
  type SyncConfig 
} from '@/lib/syncManager';
import { logger } from '@/lib/logger';

export interface UseSyncReturn {
  status: SyncStatus;
  isOnline: boolean;
  lastSync: Date | null;
  pendingChanges: number;
  failedChanges: number;
  error: string | null;
  
  // Actions
  sync: () => Promise<SyncResult>;
  queueChange: (change: any) => Promise<string>;
  clearQueue: () => Promise<void>;
  
  // Settings
  enableAutoSync: (enabled: boolean) => void;
  updateSyncConfig: (config: Partial<SyncConfig>) => void;
}

interface UseSyncOptions {
  autoSync?: boolean;
  syncConfig?: SyncConfig;
}

/**
 * Hook for managing data synchronization and offline capabilities
 */
export const useSync = (options: UseSyncOptions = {}): UseSyncReturn => {
  const {
    autoSync = true,
    syncConfig = {
      apiBaseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      syncInterval: 30000,
      maxRetries: 3,
      batchSize: 10,
      conflictResolution: 'manual',
    },
  } = options;

  const [status, setStatus] = useState<SyncStatus>('idle');
  const [isOnline, setIsOnline] = useState(true);
  const [lastSync, setLastSync] = useState<Date | null>(null);
  const [pendingChanges, setPendingChanges] = useState(0);
  const [failedChanges, setFailedChanges] = useState(0);
  const [error, setError] = useState<string | null>(null);

  // Initialize sync manager
  useEffect(() => {
    try {
      const syncManager = createSyncManager(syncConfig);
      
      // Subscribe to sync status changes
      const unsubscribe = syncManager.subscribe((newStatus, result) => {
        setStatus(newStatus);
        
        if (result) {
          if (result.success) {
            setLastSync(new Date());
            setError(null);
          } else {
            setError(result.errors.join(', '));
          }
        }
      });

      // Start auto sync if enabled
      if (autoSync) {
        syncManager.startAutoSync();
      }

      // Update queue status
      updateQueueStatus();

      return () => {
        unsubscribe();
        if (autoSync) {
          syncManager.stopAutoSync();
        }
      };
    } catch (err) {
      logger.error('Error initializing sync hook', { error: err });
      setError('Erreur d\'initialisation de la synchronisation');
    }
  }, [autoSync, syncConfig]);

  // Monitor online status
  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      // Trigger sync when coming back online
      if (autoSync) {
        sync().catch(error => {
          logger.error('Error syncing after coming online', { error });
        });
      }
    };

    const handleOffline = () => {
      setIsOnline(false);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Set initial online status
    setIsOnline(navigator.onLine);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [autoSync]);

  // Update queue status periodically
  const updateQueueStatus = useCallback(async () => {
    try {
      const syncManager = getSyncManager();
      const queueStatus = await syncManager.getSyncQueueStatus();
      setPendingChanges(queueStatus.pending);
      setFailedChanges(queueStatus.failed);
    } catch (err) {
      logger.error('Error updating queue status', { error: err });
    }
  }, []);

  // Update queue status periodically
  useEffect(() => {
    const interval = setInterval(updateQueueStatus, 5000);
    return () => clearInterval(interval);
  }, [updateQueueStatus]);

  // Manual sync function
  const sync = useCallback(async (): Promise<SyncResult> => {
    try {
      const syncManager = getSyncManager();
      const result = await syncManager.sync();
      
      // Update queue status after sync
      await updateQueueStatus();
      
      return result;
    } catch (err) {
      logger.error('Error during manual sync', { error: err });
      const errorResult: SyncResult = {
        success: false,
        synced: 0,
        failed: 1,
        conflicts: 0,
        errors: [err instanceof Error ? err.message : 'Unknown error'],
      };
      setError(errorResult.errors.join(', '));
      return errorResult;
    }
  }, [updateQueueStatus]);

  // Queue change for sync
  const queueChange = useCallback(async (change: any): Promise<string> => {
    try {
      const syncManager = getSyncManager();
      const changeId = await syncManager.queueSync(change);
      
      // Update queue status
      await updateQueueStatus();
      
      return changeId;
    } catch (err) {
      logger.error('Error queuing change for sync', { error: err });
      setError('Erreur lors de la mise en file d\'attente');
      throw err;
    }
  }, [updateQueueStatus]);

  // Clear sync queue
  const clearQueue = useCallback(async (): Promise<void> => {
    try {
      const syncManager = getSyncManager();
      await syncManager.clearSyncQueue();
      await updateQueueStatus();
    } catch (err) {
      logger.error('Error clearing sync queue', { error: err });
      setError('Erreur lors de la suppression de la file d\'attente');
    }
  }, [updateQueueStatus]);

  // Enable/disable auto sync
  const enableAutoSync = useCallback((enabled: boolean) => {
    try {
      const syncManager = getSyncManager();
      if (enabled) {
        syncManager.startAutoSync();
      } else {
        syncManager.stopAutoSync();
      }
    } catch (err) {
      logger.error('Error toggling auto sync', { error: err });
      setError('Erreur lors de la configuration de la synchronisation automatique');
    }
  }, []);

  // Update sync configuration
  const updateSyncConfig = useCallback((config: Partial<SyncConfig>) => {
    try {
      const syncManager = getSyncManager();
      syncManager.updateConfig(config);
    } catch (err) {
      logger.error('Error updating sync config', { error: err });
      setError('Erreur lors de la mise à jour de la configuration');
    }
  }, []);

  return {
    status,
    isOnline,
    lastSync,
    pendingChanges,
    failedChanges,
    error,
    
    // Actions
    sync,
    queueChange,
    clearQueue,
    
    // Settings
    enableAutoSync,
    updateSyncConfig,
  };
};

/**
 * Hook for offline state management
 */
export const useOffline = () => {
  const [isOffline, setIsOffline] = useState(false);
  const [wasOffline, setWasOffline] = useState(false);

  useEffect(() => {
    const handleOnline = () => {
      setWasOffline(isOffline);
      setIsOffline(false);
    };

    const handleOffline = () => {
      setIsOffline(true);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Set initial state
    setIsOffline(!navigator.onLine);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [isOffline]);

  return {
    isOffline,
    wasOffline,
    isOnline: !isOffline,
  };
};