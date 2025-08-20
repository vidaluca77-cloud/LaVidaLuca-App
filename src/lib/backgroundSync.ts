/**
 * Background Sync Manager for La Vida Luca App
 * Handles background synchronization when the app is not active
 */

import { logger } from './logger';

export interface BackgroundSyncConfig {
  enabled: boolean;
  syncInterval: number;
  maxRetries: number;
  minConnectivity: 'slow-2g' | '2g' | '3g' | '4g';
}

export interface BackgroundTask {
  id: string;
  type: string;
  data: any;
  createdAt: number;
  lastAttempt?: number;
  retryCount: number;
  maxRetries: number;
  priority: 'low' | 'normal' | 'high';
}

class BackgroundSyncManager {
  private static instance: BackgroundSyncManager;
  private config: BackgroundSyncConfig;
  private registration: ServiceWorkerRegistration | null = null;
  private tasks: Map<string, BackgroundTask> = new Map();

  static getInstance(config?: BackgroundSyncConfig): BackgroundSyncManager {
    if (!BackgroundSyncManager.instance) {
      if (!config) {
        throw new Error('Background sync configuration required for first initialization');
      }
      BackgroundSyncManager.instance = new BackgroundSyncManager(config);
    }
    return BackgroundSyncManager.instance;
  }

  private constructor(config: BackgroundSyncConfig) {
    this.config = {
      enabled: true,
      syncInterval: 30000,
      maxRetries: 5,
      minConnectivity: '2g',
      ...config,
    };

    this.initServiceWorker();
  }

  /**
   * Initialize service worker for background sync
   */
  private async initServiceWorker(): Promise<void> {
    if (!('serviceWorker' in navigator)) {
      logger.warn('Service Worker not supported');
      return;
    }

    try {
      this.registration = await navigator.serviceWorker.ready;
      
      // Check if background sync is supported
      if ('sync' in this.registration) {
        logger.info('Background Sync initialized successfully');
        this.setupMessageHandler();
      } else {
        logger.warn('Background Sync not supported');
      }
    } catch (error) {
      logger.error('Error initializing service worker for background sync', { error });
    }
  }

  /**
   * Setup message handler for communication with service worker
   */
  private setupMessageHandler(): void {
    navigator.serviceWorker.addEventListener('message', (event) => {
      const { type, payload } = event.data;

      switch (type) {
        case 'background-sync-complete':
          this.handleSyncComplete(payload);
          break;
        case 'background-sync-failed':
          this.handleSyncFailed(payload);
          break;
        default:
          break;
      }
    });
  }

  /**
   * Schedule a task for background synchronization
   */
  async scheduleTask(task: Omit<BackgroundTask, 'id' | 'createdAt' | 'retryCount'>): Promise<string> {
    const taskId = crypto.randomUUID();
    const backgroundTask: BackgroundTask = {
      id: taskId,
      createdAt: Date.now(),
      retryCount: 0,
      ...task,
    };

    this.tasks.set(taskId, backgroundTask);

    if (this.config.enabled && this.registration) {
      try {
        // Register background sync with service worker
        await (this.registration as any).sync.register(`sync-${taskId}`);
        
        // Send task data to service worker
        this.sendToServiceWorker({
          type: 'schedule-background-task',
          payload: backgroundTask,
        });

        logger.info('Background task scheduled', { taskId, type: task.type });
      } catch (error) {
        logger.error('Error scheduling background task', { error, taskId });
      }
    }

    return taskId;
  }

  /**
   * Cancel a scheduled background task
   */
  async cancelTask(taskId: string): Promise<boolean> {
    try {
      this.tasks.delete(taskId);
      
      this.sendToServiceWorker({
        type: 'cancel-background-task',
        payload: { taskId },
      });

      logger.info('Background task cancelled', { taskId });
      return true;
    } catch (error) {
      logger.error('Error cancelling background task', { error, taskId });
      return false;
    }
  }

  /**
   * Get all pending tasks
   */
  getPendingTasks(): BackgroundTask[] {
    return Array.from(this.tasks.values());
  }

  /**
   * Get task by ID
   */
  getTask(taskId: string): BackgroundTask | undefined {
    return this.tasks.get(taskId);
  }

  /**
   * Clear all completed/failed tasks
   */
  clearCompletedTasks(): void {
    const completedTasks = Array.from(this.tasks.entries()).filter(
      ([_, task]) => task.retryCount >= task.maxRetries
    );

    completedTasks.forEach(([taskId]) => {
      this.tasks.delete(taskId);
    });

    logger.info('Cleared completed background tasks', { count: completedTasks.length });
  }

  /**
   * Update configuration
   */
  updateConfig(updates: Partial<BackgroundSyncConfig>): void {
    this.config = { ...this.config, ...updates };
    
    this.sendToServiceWorker({
      type: 'update-background-sync-config',
      payload: this.config,
    });

    logger.info('Background sync configuration updated', { config: this.config });
  }

  /**
   * Force sync all pending tasks (when coming back online)
   */
  async forceSyncAll(): Promise<void> {
    if (!this.registration) {
      logger.warn('Service worker not available for force sync');
      return;
    }

    try {
      await (this.registration as any).sync.register('force-sync-all');
      logger.info('Force sync all tasks triggered');
    } catch (error) {
      logger.error('Error triggering force sync', { error });
    }
  }

  /**
   * Check network connectivity and decide if sync should proceed
   */
  private async checkConnectivity(): Promise<boolean> {
    const connection = (navigator as any).connection;
    if (!connection) {
      return navigator.onLine;
    }

    const effectiveType = connection.effectiveType;
    
    const connectivityLevels = {
      'slow-2g': 1,
      '2g': 2,
      '3g': 3,
      '4g': 4,
    };

    const currentLevel = connectivityLevels[effectiveType as keyof typeof connectivityLevels] || 0;
    const requiredLevel = connectivityLevels[this.config.minConnectivity];

    return currentLevel >= requiredLevel;
  }

  /**
   * Handle sync completion from service worker
   */
  private handleSyncComplete(payload: { taskId: string; result: any }): void {
    const task = this.tasks.get(payload.taskId);
    if (task) {
      this.tasks.delete(payload.taskId);
      logger.info('Background task completed successfully', { 
        taskId: payload.taskId, 
        type: task.type 
      });
    }
  }

  /**
   * Handle sync failure from service worker
   */
  private handleSyncFailed(payload: { taskId: string; error: string }): void {
    const task = this.tasks.get(payload.taskId);
    if (task) {
      task.retryCount++;
      task.lastAttempt = Date.now();

      if (task.retryCount < task.maxRetries) {
        // Schedule retry
        this.scheduleRetry(task);
      } else {
        logger.error('Background task failed permanently', { 
          taskId: payload.taskId, 
          type: task.type,
          error: payload.error 
        });
      }
    }
  }

  /**
   * Schedule retry for failed task
   */
  private async scheduleRetry(task: BackgroundTask): Promise<void> {
    const delay = Math.min(1000 * Math.pow(2, task.retryCount), 30000); // Exponential backoff, max 30s
    
    setTimeout(async () => {
      if (this.registration) {
        try {
          await (this.registration as any).sync.register(`retry-${task.id}`);
          logger.info('Background task retry scheduled', { 
            taskId: task.id, 
            attempt: task.retryCount + 1 
          });
        } catch (error) {
          logger.error('Error scheduling task retry', { error, taskId: task.id });
        }
      }
    }, delay);
  }

  /**
   * Send message to service worker
   */
  private sendToServiceWorker(message: { type: string; payload: any }): void {
    if (this.registration && this.registration.active) {
      this.registration.active.postMessage(message);
    }
  }
}

// Export singleton instance factory
export const createBackgroundSyncManager = (config: BackgroundSyncConfig) => {
  return BackgroundSyncManager.getInstance(config);
};

// Export for getting existing instance
export const getBackgroundSyncManager = () => {
  return BackgroundSyncManager.getInstance();
};

// Convenience functions for common background tasks
export const backgroundSync = {
  // Schedule data sync
  scheduleDataSync: async (data: any, endpoint: string, method: string = 'POST') => {
    const manager = getBackgroundSyncManager();
    return await manager.scheduleTask({
      type: 'data-sync',
      data: { data, endpoint, method },
      priority: 'normal',
      maxRetries: 3,
    });
  },

  // Schedule file upload
  scheduleFileUpload: async (file: File, endpoint: string) => {
    const manager = getBackgroundSyncManager();
    
    // Convert file to base64 for storage
    const fileData = await new Promise<string>((resolve) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as string);
      reader.readAsDataURL(file);
    });

    return await manager.scheduleTask({
      type: 'file-upload',
      data: {
        fileName: file.name,
        fileType: file.type,
        fileData,
        endpoint,
      },
      priority: 'low',
      maxRetries: 5,
    });
  },

  // Schedule analytics event
  scheduleAnalytics: async (event: string, properties: any) => {
    const manager = getBackgroundSyncManager();
    return await manager.scheduleTask({
      type: 'analytics',
      data: { event, properties, timestamp: Date.now() },
      priority: 'low',
      maxRetries: 2,
    });
  },

  // Schedule notification
  scheduleNotification: async (notification: any) => {
    const manager = getBackgroundSyncManager();
    return await manager.scheduleTask({
      type: 'notification',
      data: notification,
      priority: 'high',
      maxRetries: 3,
    });
  },
};