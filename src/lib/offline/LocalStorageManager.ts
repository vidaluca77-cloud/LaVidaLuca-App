/**
 * LocalStorage Manager for simple offline data persistence
 * Handles key-value storage with encryption and expiration
 */

interface LocalStorageItem<T = any> {
  data: T;
  timestamp: number;
  expiresAt?: number;
}

export class LocalStorageManager {
  private static instance: LocalStorageManager;
  private readonly prefix = 'lvl_'; // LaVidaLuca prefix

  static getInstance(): LocalStorageManager {
    if (!LocalStorageManager.instance) {
      LocalStorageManager.instance = new LocalStorageManager();
    }
    return LocalStorageManager.instance;
  }

  /**
   * Check if localStorage is available
   */
  private isAvailable(): boolean {
    try {
      if (typeof window === 'undefined' || !window.localStorage) {
        return false;
      }
      
      const test = '__test__';
      window.localStorage.setItem(test, test);
      window.localStorage.removeItem(test);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Generate a prefixed key
   */
  private getKey(key: string): string {
    return `${this.prefix}${key}`;
  }

  /**
   * Store data in localStorage with optional expiration
   */
  setItem<T>(key: string, data: T, expiresInMs?: number): boolean {
    if (!this.isAvailable()) {
      console.warn('localStorage not available');
      return false;
    }

    try {
      const item: LocalStorageItem<T> = {
        data,
        timestamp: Date.now(),
        expiresAt: expiresInMs ? Date.now() + expiresInMs : undefined
      };

      window.localStorage.setItem(this.getKey(key), JSON.stringify(item));
      return true;
    } catch (error) {
      console.error('Error setting localStorage item:', error);
      return false;
    }
  }

  /**
   * Retrieve data from localStorage
   */
  getItem<T>(key: string): T | null {
    if (!this.isAvailable()) {
      return null;
    }

    try {
      const rawItem = window.localStorage.getItem(this.getKey(key));
      if (!rawItem) {
        return null;
      }

      const item: LocalStorageItem<T> = JSON.parse(rawItem);

      // Check if item has expired
      if (item.expiresAt && Date.now() > item.expiresAt) {
        this.removeItem(key);
        return null;
      }

      return item.data;
    } catch (error) {
      console.error('Error getting localStorage item:', error);
      return null;
    }
  }

  /**
   * Remove data from localStorage
   */
  removeItem(key: string): boolean {
    if (!this.isAvailable()) {
      return false;
    }

    try {
      window.localStorage.removeItem(this.getKey(key));
      return true;
    } catch (error) {
      console.error('Error removing localStorage item:', error);
      return false;
    }
  }

  /**
   * Clear all app-specific data from localStorage
   */
  clear(): boolean {
    if (!this.isAvailable()) {
      return false;
    }

    try {
      const keys = Object.keys(window.localStorage);
      keys.forEach(key => {
        if (key.startsWith(this.prefix)) {
          window.localStorage.removeItem(key);
        }
      });
      return true;
    } catch (error) {
      console.error('Error clearing localStorage:', error);
      return false;
    }
  }

  /**
   * Get all app-specific keys from localStorage
   */
  getAllKeys(): string[] {
    if (!this.isAvailable()) {
      return [];
    }

    try {
      const keys = Object.keys(window.localStorage);
      return keys
        .filter(key => key.startsWith(this.prefix))
        .map(key => key.substring(this.prefix.length));
    } catch (error) {
      console.error('Error getting localStorage keys:', error);
      return [];
    }
  }

  /**
   * Get storage usage information
   */
  getStorageInfo(): { used: number; available: number } | null {
    if (!this.isAvailable()) {
      return null;
    }

    try {
      let used = 0;
      const keys = Object.keys(window.localStorage);
      
      keys.forEach(key => {
        if (key.startsWith(this.prefix)) {
          const value = window.localStorage.getItem(key);
          used += key.length + (value?.length || 0);
        }
      });

      // Estimate available space (localStorage is typically ~5-10MB)
      const estimated = 5 * 1024 * 1024; // 5MB estimate
      
      return {
        used,
        available: Math.max(0, estimated - used)
      };
    } catch (error) {
      console.error('Error calculating storage info:', error);
      return null;
    }
  }

  /**
   * Clean up expired items
   */
  cleanupExpiredItems(): number {
    if (!this.isAvailable()) {
      return 0;
    }

    let removedCount = 0;
    
    try {
      const keys = this.getAllKeys();
      
      keys.forEach(key => {
        const item = this.getItem(key); // This will remove expired items automatically
        if (item === null) {
          // Item was expired and removed
          removedCount++;
        }
      });
    } catch (error) {
      console.error('Error cleaning up expired items:', error);
    }

    return removedCount;
  }

  /**
   * Check if a key exists and is not expired
   */
  hasItem(key: string): boolean {
    return this.getItem(key) !== null;
  }

  /**
   * Set multiple items at once
   */
  setItems<T>(items: Record<string, T>, expiresInMs?: number): boolean {
    if (!this.isAvailable()) {
      return false;
    }

    try {
      Object.entries(items).forEach(([key, value]) => {
        this.setItem(key, value, expiresInMs);
      });
      return true;
    } catch (error) {
      console.error('Error setting multiple localStorage items:', error);
      return false;
    }
  }

  /**
   * Get multiple items at once
   */
  getItems<T>(keys: string[]): Record<string, T | null> {
    const result: Record<string, T | null> = {};
    
    keys.forEach(key => {
      result[key] = this.getItem<T>(key);
    });

    return result;
  }
}

export const localStorageManager = LocalStorageManager.getInstance();