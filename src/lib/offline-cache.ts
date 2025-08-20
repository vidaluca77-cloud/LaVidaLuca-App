/**
 * Offline Cache Manager
 * Handles caching with IndexedDB and LocalStorage fallback
 */

interface CacheItem {
  id: string;
  data: any;
  timestamp: number;
  expiresAt?: number;
  version: number;
}

interface CacheConfig {
  name: string;
  version: number;
  maxAge?: number; // in milliseconds
  maxItems?: number;
}

class OfflineCacheManager {
  private dbName = 'la-vida-luca-cache';
  private dbVersion = 1;
  private db: IDBDatabase | null = null;

  async init(): Promise<void> {
    if (typeof window === 'undefined' || !window.indexedDB) {
      console.warn('IndexedDB not available, falling back to localStorage');
      return;
    }

    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.dbVersion);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        
        // Create cache store
        if (!db.objectStoreNames.contains('cache')) {
          const store = db.createObjectStore('cache', { keyPath: 'id' });
          store.createIndex('timestamp', 'timestamp', { unique: false });
          store.createIndex('expiresAt', 'expiresAt', { unique: false });
        }

        // Create offline queue store
        if (!db.objectStoreNames.contains('offline-queue')) {
          const queueStore = db.createObjectStore('offline-queue', { keyPath: 'id' });
          queueStore.createIndex('timestamp', 'timestamp', { unique: false });
        }

        // Create sync status store
        if (!db.objectStoreNames.contains('sync-status')) {
          db.createObjectStore('sync-status', { keyPath: 'key' });
        }
      };
    });
  }

  async set(key: string, data: any, config?: Partial<CacheConfig>): Promise<void> {
    const item: CacheItem = {
      id: key,
      data,
      timestamp: Date.now(),
      version: config?.version || 1,
    };

    if (config?.maxAge) {
      item.expiresAt = Date.now() + config.maxAge;
    }

    // Try IndexedDB first
    if (this.db) {
      try {
        await this.setIndexedDB(item);
        return;
      } catch (error) {
        console.warn('IndexedDB write failed, falling back to localStorage:', error);
      }
    }

    // Fallback to localStorage
    this.setLocalStorage(key, item);
  }

  async get(key: string): Promise<any | null> {
    // Try IndexedDB first
    if (this.db) {
      try {
        const item = await this.getIndexedDB(key);
        if (item && this.isValidItem(item)) {
          return item.data;
        }
      } catch (error) {
        console.warn('IndexedDB read failed, falling back to localStorage:', error);
      }
    }

    // Fallback to localStorage
    const item = this.getLocalStorage(key);
    if (item && this.isValidItem(item)) {
      return item.data;
    }

    return null;
  }

  async remove(key: string): Promise<void> {
    // Remove from IndexedDB
    if (this.db) {
      try {
        await this.removeIndexedDB(key);
      } catch (error) {
        console.warn('IndexedDB remove failed:', error);
      }
    }

    // Remove from localStorage
    this.removeLocalStorage(key);
  }

  async clear(): Promise<void> {
    // Clear IndexedDB
    if (this.db) {
      try {
        await this.clearIndexedDB();
      } catch (error) {
        console.warn('IndexedDB clear failed:', error);
      }
    }

    // Clear localStorage (only our keys)
    this.clearLocalStorage();
  }

  async getCacheSize(): Promise<{ indexedDB: number; localStorage: number }> {
    let indexedDBSize = 0;
    let localStorageSize = 0;

    // Calculate IndexedDB size
    if (this.db) {
      try {
        const transaction = this.db.transaction(['cache'], 'readonly');
        const store = transaction.objectStore('cache');
        const request = store.getAll();
        
        const items = await new Promise<CacheItem[]>((resolve, reject) => {
          request.onsuccess = () => resolve(request.result);
          request.onerror = () => reject(request.error);
        });

        indexedDBSize = items.reduce((size, item) => {
          return size + JSON.stringify(item).length;
        }, 0);
      } catch (error) {
        console.warn('Failed to calculate IndexedDB size:', error);
      }
    }

    // Calculate localStorage size
    try {
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key?.startsWith('lvc-')) {
          const value = localStorage.getItem(key);
          if (value) {
            localStorageSize += key.length + value.length;
          }
        }
      }
    } catch (error) {
      console.warn('Failed to calculate localStorage size:', error);
    }

    return { indexedDB: indexedDBSize, localStorage: localStorageSize };
  }

  async cleanupExpired(): Promise<void> {
    const now = Date.now();

    // Cleanup IndexedDB
    if (this.db) {
      try {
        const transaction = this.db.transaction(['cache'], 'readwrite');
        const store = transaction.objectStore('cache');
        const index = store.index('expiresAt');
        const range = IDBKeyRange.upperBound(now);
        
        const request = index.openCursor(range);
        request.onsuccess = (event) => {
          const cursor = (event.target as IDBRequest).result;
          if (cursor) {
            cursor.delete();
            cursor.continue();
          }
        };
      } catch (error) {
        console.warn('Failed to cleanup expired IndexedDB items:', error);
      }
    }

    // Cleanup localStorage
    try {
      for (let i = localStorage.length - 1; i >= 0; i--) {
        const key = localStorage.key(i);
        if (key?.startsWith('lvc-')) {
          const item = this.getLocalStorage(key.substring(4)); // Remove 'lvc-' prefix
          if (item && item.expiresAt && item.expiresAt < now) {
            localStorage.removeItem(key);
          }
        }
      }
    } catch (error) {
      console.warn('Failed to cleanup expired localStorage items:', error);
    }
  }

  // Private IndexedDB methods
  private async setIndexedDB(item: CacheItem): Promise<void> {
    if (!this.db) throw new Error('IndexedDB not initialized');

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['cache'], 'readwrite');
      const store = transaction.objectStore('cache');
      const request = store.put(item);

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  private async getIndexedDB(key: string): Promise<CacheItem | null> {
    if (!this.db) throw new Error('IndexedDB not initialized');

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['cache'], 'readonly');
      const store = transaction.objectStore('cache');
      const request = store.get(key);

      request.onsuccess = () => resolve(request.result || null);
      request.onerror = () => reject(request.error);
    });
  }

  private async removeIndexedDB(key: string): Promise<void> {
    if (!this.db) throw new Error('IndexedDB not initialized');

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['cache'], 'readwrite');
      const store = transaction.objectStore('cache');
      const request = store.delete(key);

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  private async clearIndexedDB(): Promise<void> {
    if (!this.db) throw new Error('IndexedDB not initialized');

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['cache'], 'readwrite');
      const store = transaction.objectStore('cache');
      const request = store.clear();

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  // Private localStorage methods
  private setLocalStorage(key: string, item: CacheItem): void {
    try {
      localStorage.setItem(`lvc-${key}`, JSON.stringify(item));
    } catch (error) {
      console.warn('Failed to write to localStorage:', error);
    }
  }

  private getLocalStorage(key: string): CacheItem | null {
    try {
      const value = localStorage.getItem(`lvc-${key}`);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.warn('Failed to read from localStorage:', error);
      return null;
    }
  }

  private removeLocalStorage(key: string): void {
    try {
      localStorage.removeItem(`lvc-${key}`);
    } catch (error) {
      console.warn('Failed to remove from localStorage:', error);
    }
  }

  private clearLocalStorage(): void {
    try {
      const keysToRemove: string[] = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key?.startsWith('lvc-')) {
          keysToRemove.push(key);
        }
      }
      keysToRemove.forEach(key => localStorage.removeItem(key));
    } catch (error) {
      console.warn('Failed to clear localStorage:', error);
    }
  }

  private isValidItem(item: CacheItem): boolean {
    if (!item) return false;
    
    // Check if expired
    if (item.expiresAt && item.expiresAt < Date.now()) {
      return false;
    }

    return true;
  }
}

export const offlineCacheManager = new OfflineCacheManager();

// Auto-initialize
if (typeof window !== 'undefined') {
  offlineCacheManager.init().catch(console.error);
  
  // Cleanup expired items periodically
  setInterval(() => {
    offlineCacheManager.cleanupExpired().catch(console.error);
  }, 5 * 60 * 1000); // Every 5 minutes
}