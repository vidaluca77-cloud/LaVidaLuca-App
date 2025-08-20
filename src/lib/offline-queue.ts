/**
 * Offline Queue Manager
 * Handles queuing actions when offline and processing them when back online
 */

import { offlineCacheManager } from './offline-cache';
import { logger } from './logger';

export interface OfflineAction {
  id: string;
  type: string;
  data: any;
  timestamp: number;
  retries: number;
  maxRetries: number;
  priority: 'low' | 'normal' | 'high';
  metadata?: Record<string, any>;
}

export interface OfflineQueueConfig {
  maxRetries?: number;
  retryDelay?: number;
  maxQueueSize?: number;
  autoSync?: boolean;
}

class OfflineQueueManager {
  private queue: OfflineAction[] = [];
  private isProcessing = false;
  private config: Required<OfflineQueueConfig>;
  private syncCallbacks: Array<(action: OfflineAction, success: boolean) => void> = [];

  constructor(config: OfflineQueueConfig = {}) {
    this.config = {
      maxRetries: config.maxRetries || 3,
      retryDelay: config.retryDelay || 1000,
      maxQueueSize: config.maxQueueSize || 100,
      autoSync: config.autoSync !== false,
    };

    this.init();
  }

  private async init() {
    // Only run in browser environment
    if (typeof window === 'undefined') return;
    
    // Load persisted queue
    await this.loadQueue();

    // Set up online/offline listeners
    window.addEventListener('online', () => this.handleOnline());
    window.addEventListener('offline', () => this.handleOffline());

    // Auto-sync if online and enabled
    if (this.config.autoSync && navigator.onLine) {
      this.processQueue();
    }
  }

  /**
   * Add an action to the offline queue
   */
  async enqueue(
    type: string,
    data: any,
    options: {
      priority?: 'low' | 'normal' | 'high';
      maxRetries?: number;
      metadata?: Record<string, any>;
    } = {}
  ): Promise<string> {
    const action: OfflineAction = {
      id: crypto.randomUUID(),
      type,
      data,
      timestamp: Date.now(),
      retries: 0,
      maxRetries: options.maxRetries || this.config.maxRetries,
      priority: options.priority || 'normal',
      metadata: options.metadata,
    };

    // Add to queue (with priority ordering)
    this.insertByPriority(action);

    // Enforce max queue size
    if (this.queue.length > this.config.maxQueueSize) {
      this.queue = this.queue.slice(-this.config.maxQueueSize);
    }

    // Persist queue
    await this.saveQueue();

    // Try to process immediately if online
    if (navigator.onLine && this.config.autoSync) {
      this.processQueue();
    }

    // Send to service worker for background sync
    this.sendToServiceWorker(action);

    logger.info('Action queued for offline processing', {
      actionId: action.id,
      type: action.type,
      queueLength: this.queue.length,
    });

    return action.id;
  }

  /**
   * Remove an action from the queue
   */
  async dequeue(actionId: string): Promise<boolean> {
    const index = this.queue.findIndex(action => action.id === actionId);
    if (index >= 0) {
      this.queue.splice(index, 1);
      await this.saveQueue();
      return true;
    }
    return false;
  }

  /**
   * Get current queue status
   */
  getQueueStatus() {
    const isOnline = typeof window !== 'undefined' && navigator.onLine;
    
    return {
      length: this.queue.length,
      isProcessing: this.isProcessing,
      isOnline,
      actions: this.queue.map(action => ({
        id: action.id,
        type: action.type,
        timestamp: action.timestamp,
        retries: action.retries,
        priority: action.priority,
      })),
    };
  }

  /**
   * Manually trigger queue processing
   */
  async processQueue(): Promise<void> {
    if (this.isProcessing || this.queue.length === 0) {
      return;
    }

    this.isProcessing = true;

    try {
      // Sort by priority and timestamp
      this.queue.sort((a, b) => {
        const priorityOrder = { high: 3, normal: 2, low: 1 };
        const priorityDiff = priorityOrder[b.priority] - priorityOrder[a.priority];
        if (priorityDiff !== 0) return priorityDiff;
        return a.timestamp - b.timestamp;
      });

      const actionsToProcess = [...this.queue];
      
      for (const action of actionsToProcess) {
        try {
          await this.processAction(action);
          await this.dequeue(action.id);
          this.notifyCallbacks(action, true);
        } catch (error) {
          action.retries++;
          
          if (action.retries >= action.maxRetries) {
            logger.error('Action exceeded max retries, removing from queue', {
              actionId: action.id,
              type: action.type,
              retries: action.retries,
              error: error instanceof Error ? error.message : 'Unknown error',
            });
            
            await this.dequeue(action.id);
            this.notifyCallbacks(action, false);
          } else {
            logger.warn('Action processing failed, will retry', {
              actionId: action.id,
              type: action.type,
              retries: action.retries,
              maxRetries: action.maxRetries,
              error: error instanceof Error ? error.message : 'Unknown error',
            });
            
            // Wait before next retry
            await new Promise(resolve => setTimeout(resolve, this.config.retryDelay * action.retries));
          }
        }
      }

      await this.saveQueue();
    } finally {
      this.isProcessing = false;
    }
  }

  /**
   * Clear the entire queue
   */
  async clearQueue(): Promise<void> {
    this.queue = [];
    await this.saveQueue();
    
    logger.info('Offline queue cleared');
  }

  /**
   * Add callback for queue processing events
   */
  onSync(callback: (action: OfflineAction, success: boolean) => void): void {
    this.syncCallbacks.push(callback);
  }

  /**
   * Remove sync callback
   */
  offSync(callback: (action: OfflineAction, success: boolean) => void): void {
    const index = this.syncCallbacks.indexOf(callback);
    if (index >= 0) {
      this.syncCallbacks.splice(index, 1);
    }
  }

  private insertByPriority(action: OfflineAction): void {
    const priorityOrder = { high: 3, normal: 2, low: 1 };
    const actionPriority = priorityOrder[action.priority];

    let insertIndex = this.queue.length;
    for (let i = 0; i < this.queue.length; i++) {
      const queuePriority = priorityOrder[this.queue[i].priority];
      if (actionPriority > queuePriority) {
        insertIndex = i;
        break;
      }
    }

    this.queue.splice(insertIndex, 0, action);
  }

  private async processAction(action: OfflineAction): Promise<void> {
    switch (action.type) {
      case 'CONTACT_FORM_SUBMIT':
        return this.processContactForm(action);
      
      case 'USER_PREFERENCE_UPDATE':
        return this.processUserPreference(action);
      
      case 'ACTIVITY_INTERACTION':
        return this.processActivityInteraction(action);
      
      default:
        throw new Error(`Unknown action type: ${action.type}`);
    }
  }

  private async processContactForm(action: OfflineAction): Promise<void> {
    const response = await fetch('/api/contact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(action.data),
    });

    if (!response.ok) {
      throw new Error(`Contact form submission failed: ${response.status}`);
    }

    logger.info('Contact form submitted successfully from offline queue', {
      actionId: action.id,
    });
  }

  private async processUserPreference(action: OfflineAction): Promise<void> {
    // Store preference locally and sync with backend
    await offlineCacheManager.set(`user-preference-${action.data.key}`, action.data.value);
    
    // If we have an API endpoint for preferences, sync with backend
    // This would be implemented based on the actual backend API
    
    logger.info('User preference synced from offline queue', {
      actionId: action.id,
      key: action.data.key,
    });
  }

  private async processActivityInteraction(action: OfflineAction): Promise<void> {
    // Log activity interaction (view, like, etc.)
    logger.info('Activity interaction processed from offline queue', {
      actionId: action.id,
      activityId: action.data.activityId,
      interactionType: action.data.type,
    });
  }

  private async saveQueue(): Promise<void> {
    try {
      await offlineCacheManager.set('offline-queue', this.queue, {
        maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
      });
    } catch (error) {
      logger.error('Failed to save offline queue', { error });
    }
  }

  private async loadQueue(): Promise<void> {
    // Only run in browser environment
    if (typeof window === 'undefined') return;
    
    try {
      const savedQueue = await offlineCacheManager.get('offline-queue');
      if (Array.isArray(savedQueue)) {
        this.queue = savedQueue;
        logger.info('Loaded offline queue from storage', {
          queueLength: this.queue.length,
        });
      }
    } catch (error) {
      logger.error('Failed to load offline queue', { error });
    }
  }

  private sendToServiceWorker(action: OfflineAction): void {
    if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
      navigator.serviceWorker.controller.postMessage({
        type: 'QUEUE_OFFLINE_ACTION',
        actionType: action.type,
        data: action.data,
      });
    }
  }

  private handleOnline(): void {
    logger.info('Device came back online, processing offline queue');
    if (this.config.autoSync) {
      this.processQueue();
    }
  }

  private handleOffline(): void {
    logger.info('Device went offline, offline queue activated');
  }

  private notifyCallbacks(action: OfflineAction, success: boolean): void {
    this.syncCallbacks.forEach(callback => {
      try {
        callback(action, success);
      } catch (error) {
        logger.error('Error in sync callback', { error });
      }
    });
  }
}

export const offlineQueue = new OfflineQueueManager();