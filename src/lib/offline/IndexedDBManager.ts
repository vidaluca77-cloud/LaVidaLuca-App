/**
 * IndexedDB Manager for offline data persistence
 * Handles structured data storage for offline functionality
 */

interface StoredItem<T = any> {
  id: string;
  data: T;
  timestamp: number;
  expiresAt?: number;
}

export class IndexedDBManager {
  private static instance: IndexedDBManager;
  private db: IDBDatabase | null = null;
  private readonly dbName = 'LaVidaLucaOfflineDB';
  private readonly dbVersion = 1;

  static getInstance(): IndexedDBManager {
    if (!IndexedDBManager.instance) {
      IndexedDBManager.instance = new IndexedDBManager();
    }
    return IndexedDBManager.instance;
  }

  /**
   * Initialize the IndexedDB database
   */
  async init(): Promise<void> {
    if (typeof window === 'undefined' || !window.indexedDB) {
      throw new Error('IndexedDB not supported');
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

        // Create object stores for different data types
        if (!db.objectStoreNames.contains('activities')) {
          const activitiesStore = db.createObjectStore('activities', { keyPath: 'id' });
          activitiesStore.createIndex('category', 'data.category', { unique: false });
          activitiesStore.createIndex('timestamp', 'timestamp', { unique: false });
        }

        if (!db.objectStoreNames.contains('userProfile')) {
          db.createObjectStore('userProfile', { keyPath: 'id' });
        }

        if (!db.objectStoreNames.contains('suggestions')) {
          const suggestionsStore = db.createObjectStore('suggestions', { keyPath: 'id' });
          suggestionsStore.createIndex('timestamp', 'timestamp', { unique: false });
        }

        if (!db.objectStoreNames.contains('deferredActions')) {
          const actionsStore = db.createObjectStore('deferredActions', { keyPath: 'id' });
          actionsStore.createIndex('type', 'data.type', { unique: false });
          actionsStore.createIndex('timestamp', 'timestamp', { unique: false });
        }

        if (!db.objectStoreNames.contains('cache')) {
          const cacheStore = db.createObjectStore('cache', { keyPath: 'id' });
          cacheStore.createIndex('expiresAt', 'expiresAt', { unique: false });
        }
      };
    });
  }

  /**
   * Store data in a specific object store
   */
  async setItem<T>(storeName: string, id: string, data: T, expiresInMs?: number): Promise<void> {
    if (!this.db) {
      await this.init();
    }

    const item: StoredItem<T> = {
      id,
      data,
      timestamp: Date.now(),
      expiresAt: expiresInMs ? Date.now() + expiresInMs : undefined
    };

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([storeName], 'readwrite');
      const store = transaction.objectStore(storeName);
      const request = store.put(item);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }

  /**
   * Retrieve data from a specific object store
   */
  async getItem<T>(storeName: string, id: string): Promise<T | null> {
    if (!this.db) {
      await this.init();
    }

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([storeName], 'readonly');
      const store = transaction.objectStore(storeName);
      const request = store.get(id);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        const item: StoredItem<T> | undefined = request.result;
        
        if (!item) {
          resolve(null);
          return;
        }

        // Check if item has expired
        if (item.expiresAt && Date.now() > item.expiresAt) {
          this.removeItem(storeName, id);
          resolve(null);
          return;
        }

        resolve(item.data);
      };
    });
  }

  /**
   * Remove data from a specific object store
   */
  async removeItem(storeName: string, id: string): Promise<void> {
    if (!this.db) {
      await this.init();
    }

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([storeName], 'readwrite');
      const store = transaction.objectStore(storeName);
      const request = store.delete(id);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }

  /**
   * Get all items from a specific object store
   */
  async getAllItems<T>(storeName: string): Promise<StoredItem<T>[]> {
    if (!this.db) {
      await this.init();
    }

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([storeName], 'readonly');
      const store = transaction.objectStore(storeName);
      const request = store.getAll();

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        const items: StoredItem<T>[] = request.result || [];
        
        // Filter out expired items
        const validItems = items.filter(item => {
          if (item.expiresAt && Date.now() > item.expiresAt) {
            this.removeItem(storeName, item.id);
            return false;
          }
          return true;
        });

        resolve(validItems);
      };
    });
  }

  /**
   * Clear all data from a specific object store
   */
  async clearStore(storeName: string): Promise<void> {
    if (!this.db) {
      await this.init();
    }

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([storeName], 'readwrite');
      const store = transaction.objectStore(storeName);
      const request = store.clear();

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }

  /**
   * Get storage quota information
   */
  async getStorageInfo(): Promise<{ usage: number; quota: number } | null> {
    if (typeof navigator === 'undefined' || !navigator.storage || !navigator.storage.estimate) {
      return null;
    }

    try {
      const estimate = await navigator.storage.estimate();
      return {
        usage: estimate.usage || 0,
        quota: estimate.quota || 0
      };
    } catch (error) {
      console.warn('Could not estimate storage:', error);
      return null;
    }
  }

  /**
   * Clean up expired items across all stores
   */
  async cleanupExpiredItems(): Promise<void> {
    if (!this.db) {
      await this.init();
    }

    const storeNames = ['activities', 'userProfile', 'suggestions', 'deferredActions', 'cache'];
    
    for (const storeName of storeNames) {
      try {
        await this.getAllItems(storeName); // This will automatically remove expired items
      } catch (error) {
        console.warn(`Error cleaning up store ${storeName}:`, error);
      }
    }
  }
}

export const indexedDBManager = IndexedDBManager.getInstance();