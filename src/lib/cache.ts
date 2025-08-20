/**
 * Cache management with IndexedDB for La Vida Luca App
 * Provides offline-first data storage and retrieval
 */

import { openDB, IDBPDatabase, IDBPTransaction } from 'idb';
import { logger } from './logger';

export interface CacheItem<T = any> {
  id: string;
  data: T;
  timestamp: number;
  expiresAt?: number;
  version: number;
  metadata?: Record<string, any>;
}

export interface CacheOptions {
  ttl?: number; // Time to live in milliseconds
  version?: number;
  metadata?: Record<string, any>;
}

export interface CacheQuery {
  limit?: number;
  offset?: number;
  orderBy?: string;
  orderDirection?: 'asc' | 'desc';
  filter?: (item: CacheItem) => boolean;
}

class CacheManager {
  private static instance: CacheManager;
  private db: IDBPDatabase | null = null;
  private dbName = 'LaVidaLucaCache';
  private dbVersion = 1;
  private stores: string[] = [
    'activities',
    'users',
    'notifications',
    'sync_queue',
    'app_data',
  ];

  static getInstance(): CacheManager {
    if (!CacheManager.instance) {
      CacheManager.instance = new CacheManager();
    }
    return CacheManager.instance;
  }

  private constructor() {
    this.initDB();
  }

  /**
   * Initialize IndexedDB database
   */
  private async initDB(): Promise<void> {
    try {
      this.db = await openDB(this.dbName, this.dbVersion, {
        upgrade(db) {
          // Create stores if they don't exist
          for (const storeName of this.stores) {
            if (!db.objectStoreNames.contains(storeName)) {
              const store = db.createObjectStore(storeName, { keyPath: 'id' });
              store.createIndex('timestamp', 'timestamp');
              store.createIndex('expiresAt', 'expiresAt');
              store.createIndex('version', 'version');
            }
          }
        },
      });

      logger.info('Cache database initialized successfully');
      
      // Clean expired items on startup
      this.cleanExpiredItems();
    } catch (error) {
      logger.error('Error initializing cache database', { error });
    }
  }

  /**
   * Store item in cache
   */
  async set<T>(
    storeName: string,
    id: string,
    data: T,
    options: CacheOptions = {}
  ): Promise<boolean> {
    try {
      await this.ensureDB();
      
      const now = Date.now();
      const item: CacheItem<T> = {
        id,
        data,
        timestamp: now,
        expiresAt: options.ttl ? now + options.ttl : undefined,
        version: options.version || 1,
        metadata: options.metadata,
      };

      const tx = this.db!.transaction(storeName, 'readwrite');
      await tx.objectStore(storeName).put(item);
      await tx.done;

      logger.debug('Item cached successfully', { storeName, id });
      return true;
    } catch (error) {
      logger.error('Error caching item', { error, storeName, id });
      return false;
    }
  }

  /**
   * Get item from cache
   */
  async get<T>(storeName: string, id: string): Promise<T | null> {
    try {
      await this.ensureDB();
      
      const item: CacheItem<T> | undefined = await this.db!
        .transaction(storeName, 'readonly')
        .objectStore(storeName)
        .get(id);

      if (!item) {
        return null;
      }

      // Check if item is expired
      if (item.expiresAt && Date.now() > item.expiresAt) {
        await this.delete(storeName, id);
        return null;
      }

      logger.debug('Item retrieved from cache', { storeName, id });
      return item.data;
    } catch (error) {
      logger.error('Error retrieving item from cache', { error, storeName, id });
      return null;
    }
  }

  /**
   * Get multiple items from cache
   */
  async getAll<T>(storeName: string, query: CacheQuery = {}): Promise<T[]> {
    try {
      await this.ensureDB();
      
      const tx = this.db!.transaction(storeName, 'readonly');
      const store = tx.objectStore(storeName);
      let items: CacheItem<T>[] = await store.getAll();

      // Filter expired items
      const now = Date.now();
      items = items.filter(item => !item.expiresAt || now <= item.expiresAt);

      // Apply custom filter
      if (query.filter) {
        items = items.filter(query.filter);
      }

      // Sort items
      if (query.orderBy) {
        items.sort((a, b) => {
          const aVal = (a as any)[query.orderBy!];
          const bVal = (b as any)[query.orderBy!];
          const comparison = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
          return query.orderDirection === 'desc' ? -comparison : comparison;
        });
      }

      // Apply pagination
      const startIndex = query.offset || 0;
      const endIndex = query.limit ? startIndex + query.limit : undefined;
      items = items.slice(startIndex, endIndex);

      return items.map(item => item.data);
    } catch (error) {
      logger.error('Error retrieving items from cache', { error, storeName });
      return [];
    }
  }

  /**
   * Delete item from cache
   */
  async delete(storeName: string, id: string): Promise<boolean> {
    try {
      await this.ensureDB();
      
      const tx = this.db!.transaction(storeName, 'readwrite');
      await tx.objectStore(storeName).delete(id);
      await tx.done;

      logger.debug('Item deleted from cache', { storeName, id });
      return true;
    } catch (error) {
      logger.error('Error deleting item from cache', { error, storeName, id });
      return false;
    }
  }

  /**
   * Clear all items from a store
   */
  async clear(storeName: string): Promise<boolean> {
    try {
      await this.ensureDB();
      
      const tx = this.db!.transaction(storeName, 'readwrite');
      await tx.objectStore(storeName).clear();
      await tx.done;

      logger.info('Cache store cleared', { storeName });
      return true;
    } catch (error) {
      logger.error('Error clearing cache store', { error, storeName });
      return false;
    }
  }

  /**
   * Get cache statistics
   */
  async getStats(): Promise<Record<string, { count: number; size: number }>> {
    const stats: Record<string, { count: number; size: number }> = {};

    try {
      await this.ensureDB();
      
      for (const storeName of this.stores) {
        const tx = this.db!.transaction(storeName, 'readonly');
        const store = tx.objectStore(storeName);
        const items = await store.getAll();
        
        stats[storeName] = {
          count: items.length,
          size: JSON.stringify(items).length, // Approximate size in bytes
        };
      }
    } catch (error) {
      logger.error('Error getting cache statistics', { error });
    }

    return stats;
  }

  /**
   * Clean expired items from all stores
   */
  async cleanExpiredItems(): Promise<void> {
    try {
      await this.ensureDB();
      
      const now = Date.now();
      let totalCleaned = 0;

      for (const storeName of this.stores) {
        const tx = this.db!.transaction(storeName, 'readwrite');
        const store = tx.objectStore(storeName);
        const index = store.index('expiresAt');
        
        // Get all expired items
        const expiredItems = await index.getAll(IDBKeyRange.upperBound(now));
        
        // Delete expired items
        for (const item of expiredItems) {
          await store.delete(item.id);
          totalCleaned++;
        }
        
        await tx.done;
      }

      if (totalCleaned > 0) {
        logger.info('Cleaned expired cache items', { count: totalCleaned });
      }
    } catch (error) {
      logger.error('Error cleaning expired cache items', { error });
    }
  }

  /**
   * Export cache data for backup/sync
   */
  async exportData(): Promise<Record<string, CacheItem[]>> {
    const data: Record<string, CacheItem[]> = {};

    try {
      await this.ensureDB();
      
      for (const storeName of this.stores) {
        const tx = this.db!.transaction(storeName, 'readonly');
        const items = await tx.objectStore(storeName).getAll();
        data[storeName] = items;
      }
    } catch (error) {
      logger.error('Error exporting cache data', { error });
    }

    return data;
  }

  /**
   * Import cache data from backup/sync
   */
  async importData(data: Record<string, CacheItem[]>): Promise<boolean> {
    try {
      await this.ensureDB();
      
      for (const [storeName, items] of Object.entries(data)) {
        if (this.stores.includes(storeName)) {
          const tx = this.db!.transaction(storeName, 'readwrite');
          const store = tx.objectStore(storeName);
          
          for (const item of items) {
            await store.put(item);
          }
          
          await tx.done;
        }
      }

      logger.info('Cache data imported successfully');
      return true;
    } catch (error) {
      logger.error('Error importing cache data', { error });
      return false;
    }
  }

  /**
   * Ensure database is initialized
   */
  private async ensureDB(): Promise<void> {
    if (!this.db) {
      await this.initDB();
    }
  }
}

// Export singleton instance
export const cacheManager = CacheManager.getInstance();

// Convenience functions for common cache operations
export const cache = {
  // Activities cache
  activities: {
    set: (id: string, data: any, options?: CacheOptions) => 
      cacheManager.set('activities', id, data, options),
    get: (id: string) => 
      cacheManager.get('activities', id),
    getAll: (query?: CacheQuery) => 
      cacheManager.getAll('activities', query),
    delete: (id: string) => 
      cacheManager.delete('activities', id),
  },
  
  // Users cache
  users: {
    set: (id: string, data: any, options?: CacheOptions) => 
      cacheManager.set('users', id, data, options),
    get: (id: string) => 
      cacheManager.get('users', id),
    getAll: (query?: CacheQuery) => 
      cacheManager.getAll('users', query),
    delete: (id: string) => 
      cacheManager.delete('users', id),
  },
  
  // Notifications cache
  notifications: {
    set: (id: string, data: any, options?: CacheOptions) => 
      cacheManager.set('notifications', id, data, options),
    get: (id: string) => 
      cacheManager.get('notifications', id),
    getAll: (query?: CacheQuery) => 
      cacheManager.getAll('notifications', query),
    delete: (id: string) => 
      cacheManager.delete('notifications', id),
  },
  
  // App data cache
  appData: {
    set: (id: string, data: any, options?: CacheOptions) => 
      cacheManager.set('app_data', id, data, options),
    get: (id: string) => 
      cacheManager.get('app_data', id),
    getAll: (query?: CacheQuery) => 
      cacheManager.getAll('app_data', query),
    delete: (id: string) => 
      cacheManager.delete('app_data', id),
  },
};