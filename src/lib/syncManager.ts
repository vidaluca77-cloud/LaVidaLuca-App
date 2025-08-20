/**
 * Synchronization Manager for La Vida Luca App
 * Handles data synchronization between local cache and remote server
 */

import { cacheManager } from './cache';
import { logger } from './logger';
import { notificationManager } from './notifications';

export type SyncStatus = 'idle' | 'syncing' | 'success' | 'error' | 'conflict';

export interface SyncItem {
  id: string;
  action: 'create' | 'update' | 'delete';
  data: any;
  timestamp: number;
  retryCount: number;
  maxRetries: number;
  endpoint: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
}

export interface SyncConfig {
  apiBaseUrl: string;
  syncInterval: number;
  maxRetries: number;
  batchSize: number;
  conflictResolution: 'client' | 'server' | 'manual';
}

export interface SyncResult {
  success: boolean;
  synced: number;
  failed: number;
  conflicts: number;
  errors: string[];
}

class SyncManager {
  private static instance: SyncManager;
  private config: SyncConfig;
  private syncTimer: NodeJS.Timeout | null = null;
  private isSyncing = false;
  private listeners: ((status: SyncStatus, result?: SyncResult) => void)[] = [];

  static getInstance(config?: SyncConfig): SyncManager {
    if (!SyncManager.instance) {
      if (!config) {
        throw new Error('Sync configuration required for first initialization');
      }
      SyncManager.instance = new SyncManager(config);
    }
    return SyncManager.instance;
  }

  private constructor(config: SyncConfig) {
    this.config = {
      syncInterval: 30000, // 30 seconds
      maxRetries: 3,
      batchSize: 10,
      conflictResolution: 'manual',
      ...config,
    };
  }

  /**
   * Start automatic synchronization
   */
  startAutoSync(): void {
    if (this.syncTimer) {
      this.stopAutoSync();
    }

    this.syncTimer = setInterval(() => {
      this.sync().catch(error => {
        logger.error('Auto sync error', { error });
      });
    }, this.config.syncInterval);

    logger.info('Auto sync started', { interval: this.config.syncInterval });
  }

  /**
   * Stop automatic synchronization
   */
  stopAutoSync(): void {
    if (this.syncTimer) {
      clearInterval(this.syncTimer);
      this.syncTimer = null;
      logger.info('Auto sync stopped');
    }
  }

  /**
   * Perform synchronization
   */
  async sync(): Promise<SyncResult> {
    if (this.isSyncing) {
      logger.debug('Sync already in progress, skipping');
      return { success: false, synced: 0, failed: 0, conflicts: 0, errors: ['Sync already in progress'] };
    }

    this.isSyncing = true;
    this.notifyListeners('syncing');

    try {
      logger.info('Starting data synchronization');
      
      const result: SyncResult = {
        success: true,
        synced: 0,
        failed: 0,
        conflicts: 0,
        errors: [],
      };

      // 1. Push local changes to server
      const pushResult = await this.pushLocalChanges();
      result.synced += pushResult.synced;
      result.failed += pushResult.failed;
      result.errors.push(...pushResult.errors);

      // 2. Pull remote changes from server
      const pullResult = await this.pullRemoteChanges();
      result.synced += pullResult.synced;
      result.failed += pullResult.failed;
      result.conflicts += pullResult.conflicts;
      result.errors.push(...pullResult.errors);

      // 3. Handle conflicts if any
      if (result.conflicts > 0) {
        await this.handleConflicts();
      }

      result.success = result.failed === 0 && result.conflicts === 0;
      
      this.notifyListeners(result.success ? 'success' : 'error', result);
      
      logger.info('Synchronization completed', { result });
      return result;

    } catch (error) {
      logger.error('Synchronization failed', { error });
      const errorResult: SyncResult = {
        success: false,
        synced: 0,
        failed: 1,
        conflicts: 0,
        errors: [error instanceof Error ? error.message : 'Unknown error'],
      };
      
      this.notifyListeners('error', errorResult);
      return errorResult;
    } finally {
      this.isSyncing = false;
    }
  }

  /**
   * Queue item for synchronization
   */
  async queueSync(item: Omit<SyncItem, 'id' | 'timestamp' | 'retryCount'>): Promise<string> {
    const syncItem: SyncItem = {
      id: crypto.randomUUID(),
      timestamp: Date.now(),
      retryCount: 0,
      maxRetries: this.config.maxRetries,
      ...item,
    };

    try {
      await cacheManager.set('sync_queue', syncItem.id, syncItem);
      logger.debug('Item queued for sync', { syncItem });
      return syncItem.id;
    } catch (error) {
      logger.error('Error queuing sync item', { error, syncItem });
      throw error;
    }
  }

  /**
   * Get sync queue status
   */
  async getSyncQueueStatus(): Promise<{ pending: number; failed: number }> {
    try {
      const queueItems = await cacheManager.getAll<SyncItem>('sync_queue');
      const pending = queueItems.filter(item => item.retryCount < item.maxRetries).length;
      const failed = queueItems.filter(item => item.retryCount >= item.maxRetries).length;
      
      return { pending, failed };
    } catch (error) {
      logger.error('Error getting sync queue status', { error });
      return { pending: 0, failed: 0 };
    }
  }

  /**
   * Clear sync queue
   */
  async clearSyncQueue(): Promise<void> {
    try {
      await cacheManager.clear('sync_queue');
      logger.info('Sync queue cleared');
    } catch (error) {
      logger.error('Error clearing sync queue', { error });
    }
  }

  /**
   * Subscribe to sync status changes
   */
  subscribe(listener: (status: SyncStatus, result?: SyncResult) => void): () => void {
    this.listeners.push(listener);
    return () => {
      const index = this.listeners.indexOf(listener);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }

  /**
   * Update sync configuration
   */
  updateConfig(updates: Partial<SyncConfig>): void {
    this.config = { ...this.config, ...updates };
    
    // Restart auto sync if it was running
    if (this.syncTimer) {
      this.stopAutoSync();
      this.startAutoSync();
    }
    
    logger.info('Sync configuration updated', { config: this.config });
  }

  /**
   * Push local changes to server
   */
  private async pushLocalChanges(): Promise<SyncResult> {
    const result: SyncResult = {
      success: true,
      synced: 0,
      failed: 0,
      conflicts: 0,
      errors: [],
    };

    try {
      const queueItemsData = await cacheManager.getAll<SyncItem>('sync_queue', {
        limit: this.config.batchSize,
        orderBy: 'timestamp',
        orderDirection: 'asc',
      });

      // Filter out items that have exceeded retry count
      const queueItems = queueItemsData.filter(item => item.retryCount < item.maxRetries);

      for (const item of queueItems) {
        try {
          const response = await fetch(`${this.config.apiBaseUrl}${item.endpoint}`, {
            method: item.method,
            headers: {
              'Content-Type': 'application/json',
            },
            body: item.method !== 'GET' ? JSON.stringify(item.data) : undefined,
          });

          if (response.ok) {
            // Remove from sync queue on success
            await cacheManager.delete('sync_queue', item.id);
            result.synced++;
            
            logger.debug('Sync item pushed successfully', { itemId: item.id });
          } else if (response.status === 409) {
            // Conflict detected
            result.conflicts++;
            await this.handleSyncConflict(item, await response.json());
          } else {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
          }

        } catch (error) {
          logger.error('Error pushing sync item', { error, itemId: item.id });
          
          // Increment retry count
          item.retryCount++;
          if (item.retryCount < item.maxRetries) {
            await cacheManager.set('sync_queue', item.id, item);
          } else {
            result.failed++;
            result.errors.push(`Failed to sync item ${item.id}: ${error instanceof Error ? error.message : 'Unknown error'}`);
          }
        }
      }

    } catch (error) {
      logger.error('Error in push sync operation', { error });
      result.errors.push(error instanceof Error ? error.message : 'Unknown error');
    }

    return result;
  }

  /**
   * Pull remote changes from server
   */
  private async pullRemoteChanges(): Promise<SyncResult> {
    const result: SyncResult = {
      success: true,
      synced: 0,
      failed: 0,
      conflicts: 0,
      errors: [],
    };

    try {
      // Get last sync timestamp
      const lastSync = await cacheManager.get<number>('app_data', 'last_sync_timestamp') || 0;
      
      const response = await fetch(`${this.config.apiBaseUrl}/sync/changes?since=${lastSync}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const changes = await response.json();
      
      // Process each change
      for (const change of changes.data || []) {
        try {
          const localItem = await this.getLocalItem(change.type, change.id);
          
          if (localItem && localItem.version > change.version) {
            // Local version is newer - conflict
            result.conflicts++;
            await this.handleDataConflict(change, localItem);
          } else {
            // Apply remote change
            await this.applyRemoteChange(change);
            result.synced++;
          }
        } catch (error) {
          logger.error('Error processing remote change', { error, change });
          result.failed++;
          result.errors.push(`Failed to process change for ${change.id}`);
        }
      }

      // Update last sync timestamp
      await cacheManager.set('app_data', 'last_sync_timestamp', Date.now());

    } catch (error) {
      logger.error('Error in pull sync operation', { error });
      result.errors.push(error instanceof Error ? error.message : 'Unknown error');
    }

    return result;
  }

  /**
   * Handle sync conflicts
   */
  private async handleConflicts(): Promise<void> {
    // Implementation depends on conflict resolution strategy
    switch (this.config.conflictResolution) {
      case 'client':
        // Client wins - do nothing, keep local changes
        break;
      case 'server':
        // Server wins - already handled in pullRemoteChanges
        break;
      case 'manual':
        // Notify user of conflicts
        notificationManager.addNotification(
          'warning',
          'Conflits de synchronisation',
          'Certaines données ont été modifiées simultanément. Vérifiez vos données.',
          { showBrowser: true }
        );
        break;
    }
  }

  /**
   * Handle sync conflict for specific item
   */
  private async handleSyncConflict(item: SyncItem, serverData: any): Promise<void> {
    // Store conflict information for manual resolution
    await cacheManager.set('sync_conflicts', item.id, {
      item,
      serverData,
      timestamp: Date.now(),
    });
  }

  /**
   * Handle data conflict between local and remote
   */
  private async handleDataConflict(remoteChange: any, localItem: any): Promise<void> {
    // Store conflict for resolution
    await cacheManager.set('data_conflicts', remoteChange.id, {
      remote: remoteChange,
      local: localItem,
      timestamp: Date.now(),
    });
  }

  /**
   * Apply remote change to local cache
   */
  private async applyRemoteChange(change: any): Promise<void> {
    const storeName = this.getStoreNameForType(change.type);
    
    if (change.action === 'delete') {
      await cacheManager.delete(storeName, change.id);
    } else {
      await cacheManager.set(storeName, change.id, change.data, {
        version: change.version,
      });
    }
  }

  /**
   * Get local item for comparison
   */
  private async getLocalItem(type: string, id: string): Promise<any> {
    const storeName = this.getStoreNameForType(type);
    return await cacheManager.get(storeName, id);
  }

  /**
   * Get store name for data type
   */
  private getStoreNameForType(type: string): string {
    const typeToStore: Record<string, string> = {
      'activity': 'activities',
      'user': 'users',
      'notification': 'notifications',
    };
    
    return typeToStore[type] || 'app_data';
  }

  /**
   * Notify all listeners of status change
   */
  private notifyListeners(status: SyncStatus, result?: SyncResult): void {
    this.listeners.forEach(listener => {
      try {
        listener(status, result);
      } catch (error) {
        logger.error('Error in sync status listener', { error });
      }
    });
  }
}

// Export singleton instance factory
export const createSyncManager = (config: SyncConfig) => {
  return SyncManager.getInstance(config);
};

// Export for getting existing instance
export const getSyncManager = () => {
  return SyncManager.getInstance();
};