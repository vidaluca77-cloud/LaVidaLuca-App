/**
 * Offline Manager - Main orchestrator for offline functionality
 * Coordinates IndexedDB, LocalStorage, and deferred actions
 */

import { indexedDBManager } from './IndexedDBManager';
import { localStorageManager } from './LocalStorageManager';
import { deferredActionsManager, DeferredAction, ActionResult } from './DeferredActionsManager';

export type OfflineStatus = 'online' | 'offline' | 'syncing';

export interface OfflineSettings {
  autoSync: boolean;
  syncInterval: number; // milliseconds
  maxCacheAge: number; // milliseconds
  enableNotifications: boolean;
}

export interface SyncResult {
  success: boolean;
  actionsProcessed: number;
  errors: string[];
  timestamp: number;
}

export class OfflineManager {
  private static instance: OfflineManager;
  private status: OfflineStatus = 'online';
  private listeners: Set<(status: OfflineStatus) => void> = new Set();
  private syncListeners: Set<(result: SyncResult) => void> = new Set();
  private syncInterval: NodeJS.Timeout | null = null;
  
  private settings: OfflineSettings = {
    autoSync: true,
    syncInterval: 30000, // 30 seconds
    maxCacheAge: 24 * 60 * 60 * 1000, // 24 hours
    enableNotifications: true
  };

  static getInstance(): OfflineManager {
    if (!OfflineManager.instance) {
      OfflineManager.instance = new OfflineManager();
    }
    return OfflineManager.instance;
  }

  /**
   * Initialize offline manager
   */
  async init(customSettings?: Partial<OfflineSettings>): Promise<void> {
    console.log('Initializing OfflineManager...');

    // Update settings
    if (customSettings) {
      this.settings = { ...this.settings, ...customSettings };
    }

    // Initialize storage managers
    try {
      await indexedDBManager.init();
      console.log('IndexedDB initialized successfully');
    } catch (error) {
      console.warn('IndexedDB initialization failed:', error);
    }

    // Set up network status monitoring
    this.setupNetworkMonitoring();

    // Load offline settings from storage
    await this.loadSettings();

    // Set up auto-sync if enabled
    if (this.settings.autoSync) {
      this.startAutoSync();
    }

    // Clean up expired data
    await this.cleanupExpiredData();

    console.log('OfflineManager initialized with settings:', this.settings);
  }

  /**
   * Set up network status monitoring
   */
  private setupNetworkMonitoring(): void {
    if (typeof window === 'undefined') return;

    // Check initial status
    this.updateStatus(navigator.onLine ? 'online' : 'offline');

    // Listen for network changes
    const handleOnline = () => {
      this.updateStatus('online');
      this.handleOnlineStatusChange(true);
    };

    const handleOffline = () => {
      this.updateStatus('offline');
      this.handleOnlineStatusChange(false);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Store references for cleanup
    (this as any)._handleOnline = handleOnline;
    (this as any)._handleOffline = handleOffline;
  }

  /**
   * Handle online/offline status changes
   */
  private async handleOnlineStatusChange(isOnline: boolean): Promise<void> {
    if (isOnline) {
      console.log('Network connection restored, triggering sync...');
      await this.sync();
    } else {
      console.log('Network connection lost, entering offline mode');
      if (this.settings.enableNotifications) {
        this.showOfflineNotification();
      }
    }
  }

  /**
   * Update offline status and notify listeners
   */
  private updateStatus(newStatus: OfflineStatus): void {
    if (this.status !== newStatus) {
      this.status = newStatus;
      console.log(`Offline status changed to: ${newStatus}`);
      
      // Notify all listeners
      this.listeners.forEach(listener => {
        try {
          listener(newStatus);
        } catch (error) {
          console.error('Error in offline status listener:', error);
        }
      });
    }
  }

  /**
   * Get current offline status
   */
  getStatus(): OfflineStatus {
    return this.status;
  }

  /**
   * Check if currently online
   */
  isOnline(): boolean {
    return this.status === 'online';
  }

  /**
   * Check if currently offline
   */
  isOffline(): boolean {
    return this.status === 'offline';
  }

  /**
   * Add listener for status changes
   */
  addStatusListener(listener: (status: OfflineStatus) => void): () => void {
    this.listeners.add(listener);
    
    // Return unsubscribe function
    return () => {
      this.listeners.delete(listener);
    };
  }

  /**
   * Add listener for sync events
   */
  addSyncListener(listener: (result: SyncResult) => void): () => void {
    this.syncListeners.add(listener);
    
    return () => {
      this.syncListeners.delete(listener);
    };
  }

  /**
   * Start automatic sync
   */
  private startAutoSync(): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
    }

    this.syncInterval = setInterval(async () => {
      if (this.isOnline()) {
        await this.sync();
      }
    }, this.settings.syncInterval);
  }

  /**
   * Stop automatic sync
   */
  private stopAutoSync(): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
    }
  }

  /**
   * Perform sync operation
   */
  async sync(): Promise<SyncResult> {
    if (!this.isOnline()) {
      const result: SyncResult = {
        success: false,
        actionsProcessed: 0,
        errors: ['Cannot sync while offline'],
        timestamp: Date.now()
      };
      return result;
    }

    this.updateStatus('syncing');
    
    try {
      console.log('Starting sync operation...');
      
      const syncResult = await deferredActionsManager.processActions();
      
      const result: SyncResult = {
        success: syncResult.failed === 0,
        actionsProcessed: syncResult.processed,
        errors: syncResult.failed > 0 ? [`${syncResult.failed} actions failed`] : [],
        timestamp: Date.now()
      };

      console.log('Sync completed:', result);

      // Notify sync listeners
      this.syncListeners.forEach(listener => {
        try {
          listener(result);
        } catch (error) {
          console.error('Error in sync listener:', error);
        }
      });

      return result;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown sync error';
      console.error('Sync failed:', errorMessage);

      const result: SyncResult = {
        success: false,
        actionsProcessed: 0,
        errors: [errorMessage],
        timestamp: Date.now()
      };

      this.syncListeners.forEach(listener => {
        try {
          listener(result);
        } catch (listenerError) {
          console.error('Error in sync listener:', listenerError);
        }
      });

      return result;
    } finally {
      this.updateStatus(navigator.onLine ? 'online' : 'offline');
    }
  }

  /**
   * Cache data for offline use
   */
  async cacheData<T>(key: string, data: T, category: string = 'cache', expiresInMs?: number): Promise<boolean> {
    try {
      await indexedDBManager.setItem(category, key, data, expiresInMs || this.settings.maxCacheAge);
      return true;
    } catch (error) {
      console.warn('Failed to cache data in IndexedDB, trying localStorage:', error);
      return localStorageManager.setItem(`cache_${key}`, data, expiresInMs || this.settings.maxCacheAge);
    }
  }

  /**
   * Retrieve cached data
   */
  async getCachedData<T>(key: string, category: string = 'cache'): Promise<T | null> {
    try {
      return await indexedDBManager.getItem<T>(category, key);
    } catch (error) {
      console.warn('Failed to get data from IndexedDB, trying localStorage:', error);
      return localStorageManager.getItem<T>(`cache_${key}`);
    }
  }

  /**
   * Queue an action for later execution
   */
  async queueAction(
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
  ): Promise<string> {
    // Convert callback signatures to match DeferredActionsManager
    const convertedOptions = options ? {
      headers: options.headers,
      priority: options.priority,
      onSuccess: options.onSuccess ? (result: ActionResult) => options.onSuccess!(result.response) : undefined,
      onError: options.onError ? (result: ActionResult) => options.onError!(result.error || 'Unknown error') : undefined
    } : undefined;

    return await deferredActionsManager.addAction(type, endpoint, method, data, convertedOptions);
  }

  /**
   * Get offline statistics
   */
  async getStats(): Promise<{
    status: OfflineStatus;
    storage: {
      indexedDB?: { usage: number; quota: number } | null;
      localStorage?: { used: number; available: number } | null;
    };
    deferredActions: Awaited<ReturnType<typeof deferredActionsManager.getStats>>;
    lastSync?: Date;
  }> {
    const deferredStats = await deferredActionsManager.getStats();
    const lastSyncTimestamp = localStorageManager.getItem<number>('lastSyncTimestamp');

    return {
      status: this.status,
      storage: {
        indexedDB: await indexedDBManager.getStorageInfo(),
        localStorage: localStorageManager.getStorageInfo()
      },
      deferredActions: deferredStats,
      lastSync: lastSyncTimestamp ? new Date(lastSyncTimestamp) : undefined
    };
  }

  /**
   * Update settings
   */
  async updateSettings(newSettings: Partial<OfflineSettings>): Promise<void> {
    this.settings = { ...this.settings, ...newSettings };
    await this.saveSettings();

    // Restart auto-sync if interval changed
    if (newSettings.autoSync !== undefined || newSettings.syncInterval !== undefined) {
      this.stopAutoSync();
      if (this.settings.autoSync) {
        this.startAutoSync();
      }
    }
  }

  /**
   * Get current settings
   */
  getSettings(): OfflineSettings {
    return { ...this.settings };
  }

  /**
   * Save settings to storage
   */
  private async saveSettings(): Promise<void> {
    localStorageManager.setItem('offlineSettings', this.settings);
  }

  /**
   * Load settings from storage
   */
  private async loadSettings(): Promise<void> {
    const savedSettings = localStorageManager.getItem<OfflineSettings>('offlineSettings');
    if (savedSettings) {
      this.settings = { ...this.settings, ...savedSettings };
    }
  }

  /**
   * Clean up expired data across all storage systems
   */
  private async cleanupExpiredData(): Promise<void> {
    try {
      await indexedDBManager.cleanupExpiredItems();
      localStorageManager.cleanupExpiredItems();
      console.log('Cleanup of expired data completed');
    } catch (error) {
      console.error('Error during cleanup:', error);
    }
  }

  /**
   * Show offline notification (if supported)
   */
  private showOfflineNotification(): void {
    if (typeof window === 'undefined' || !window.Notification) return;

    if (Notification.permission === 'granted') {
      new Notification('You\'re now offline', {
        body: 'Don\'t worry, your actions will be saved and synced when you\'re back online.',
        icon: '/icons/icon-192.png'
      });
    }
  }

  /**
   * Request notification permission
   */
  async requestNotificationPermission(): Promise<boolean> {
    if (typeof window === 'undefined' || !window.Notification) return false;

    if (Notification.permission === 'granted') return true;
    if (Notification.permission === 'denied') return false;

    const permission = await Notification.requestPermission();
    return permission === 'granted';
  }

  /**
   * Clear all offline data
   */
  async clearAllData(): Promise<void> {
    try {
      await deferredActionsManager.clearActions();
      await indexedDBManager.clearStore('cache');
      await indexedDBManager.clearStore('activities');
      await indexedDBManager.clearStore('userProfile');
      await indexedDBManager.clearStore('suggestions');
      localStorageManager.clear();
      console.log('All offline data cleared');
    } catch (error) {
      console.error('Error clearing offline data:', error);
      throw error;
    }
  }

  /**
   * Cleanup when manager is destroyed
   */
  destroy(): void {
    this.stopAutoSync();
    this.listeners.clear();
    this.syncListeners.clear();
    
    if (typeof window !== 'undefined') {
      window.removeEventListener('online', (this as any)._handleOnline);
      window.removeEventListener('offline', (this as any)._handleOffline);
    }
  }
}

export const offlineManager = OfflineManager.getInstance();