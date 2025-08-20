/**
 * Periodic Sync Manager for La Vida Luca App
 * Handles periodic background synchronization using the Periodic Background Sync API
 */

import { logger } from './logger';

export interface PeriodicSyncConfig {
  enabled: boolean;
  defaultInterval: number; // in milliseconds
  minInterval: number;
  maxInterval: number;
}

export interface PeriodicSyncTask {
  tag: string;
  description: string;
  interval: number;
  lastRun?: number;
  nextRun?: number;
  enabled: boolean;
  handler: () => Promise<void>;
}

class PeriodicSyncManager {
  private static instance: PeriodicSyncManager;
  private config: PeriodicSyncConfig;
  private registration: ServiceWorkerRegistration | null = null;
  private tasks: Map<string, PeriodicSyncTask> = new Map();
  private isSupported = false;

  static getInstance(config?: PeriodicSyncConfig): PeriodicSyncManager {
    if (!PeriodicSyncManager.instance) {
      if (!config) {
        throw new Error('Periodic sync configuration required for first initialization');
      }
      PeriodicSyncManager.instance = new PeriodicSyncManager(config);
    }
    return PeriodicSyncManager.instance;
  }

  private constructor(config: PeriodicSyncConfig) {
    this.config = {
      enabled: true,
      defaultInterval: 1000 * 60 * 60 * 24, // 24 hours
      minInterval: 1000 * 60 * 60, // 1 hour
      maxInterval: 1000 * 60 * 60 * 24 * 7, // 7 days
      ...config,
    };

    this.initPeriodicSync();
  }

  /**
   * Initialize periodic sync functionality
   */
  private async initPeriodicSync(): Promise<void> {
    if (!('serviceWorker' in navigator)) {
      logger.warn('Service Worker not supported');
      return;
    }

    try {
      this.registration = await navigator.serviceWorker.ready;
      
      // Check if periodic background sync is supported
      if ('periodicSync' in this.registration) {
        this.isSupported = true;
        logger.info('Periodic Background Sync initialized successfully');
        this.setupDefaultTasks();
      } else {
        logger.warn('Periodic Background Sync not supported, using fallback');
        this.setupFallbackSync();
      }
    } catch (error) {
      logger.error('Error initializing periodic sync', { error });
      this.setupFallbackSync();
    }
  }

  /**
   * Register a periodic sync task
   */
  async registerTask(task: Omit<PeriodicSyncTask, 'lastRun' | 'nextRun'>): Promise<boolean> {
    if (!this.config.enabled) {
      logger.info('Periodic sync disabled, skipping task registration', { tag: task.tag });
      return false;
    }

    // Validate interval
    const interval = Math.max(
      this.config.minInterval,
      Math.min(this.config.maxInterval, task.interval)
    );

    const periodicTask: PeriodicSyncTask = {
      ...task,
      interval,
      nextRun: Date.now() + interval,
    };

    this.tasks.set(task.tag, periodicTask);

    if (this.isSupported && this.registration) {
      try {
        // Register with browser periodic sync API
        await (this.registration as any).periodicSync.register(task.tag, {
          minInterval: interval,
        });
        
        logger.info('Periodic sync task registered', { tag: task.tag, interval });
        return true;
      } catch (error) {
        logger.error('Error registering periodic sync task', { error, tag: task.tag });
        return false;
      }
    } else {
      // Use fallback timer-based sync
      this.scheduleTaskFallback(periodicTask);
      logger.info('Periodic sync task scheduled with fallback', { tag: task.tag, interval });
      return true;
    }
  }

  /**
   * Unregister a periodic sync task
   */
  async unregisterTask(tag: string): Promise<boolean> {
    this.tasks.delete(tag);

    if (this.isSupported && this.registration) {
      try {
        await (this.registration as any).periodicSync.unregister(tag);
        logger.info('Periodic sync task unregistered', { tag });
        return true;
      } catch (error) {
        logger.error('Error unregistering periodic sync task', { error, tag });
        return false;
      }
    }

    return true;
  }

  /**
   * Get all registered tasks
   */
  getTasks(): PeriodicSyncTask[] {
    return Array.from(this.tasks.values());
  }

  /**
   * Get task by tag
   */
  getTask(tag: string): PeriodicSyncTask | undefined {
    return this.tasks.get(tag);
  }

  /**
   * Enable/disable a specific task
   */
  async toggleTask(tag: string, enabled: boolean): Promise<boolean> {
    const task = this.tasks.get(tag);
    if (!task) {
      return false;
    }

    task.enabled = enabled;

    if (enabled) {
      return await this.registerTask(task);
    } else {
      return await this.unregisterTask(tag);
    }
  }

  /**
   * Update task interval
   */
  async updateTaskInterval(tag: string, interval: number): Promise<boolean> {
    const task = this.tasks.get(tag);
    if (!task) {
      return false;
    }

    // Unregister old task
    await this.unregisterTask(tag);

    // Register with new interval
    task.interval = Math.max(
      this.config.minInterval,
      Math.min(this.config.maxInterval, interval)
    );

    return await this.registerTask(task);
  }

  /**
   * Execute a task immediately (for testing or manual triggering)
   */
  async executeTask(tag: string): Promise<boolean> {
    const task = this.tasks.get(tag);
    if (!task || !task.enabled) {
      return false;
    }

    try {
      logger.info('Executing periodic sync task', { tag });
      await task.handler();
      
      task.lastRun = Date.now();
      task.nextRun = task.lastRun + task.interval;
      
      logger.info('Periodic sync task completed', { tag });
      return true;
    } catch (error) {
      logger.error('Error executing periodic sync task', { error, tag });
      return false;
    }
  }

  /**
   * Get next scheduled run times for all tasks
   */
  getSchedule(): Array<{ tag: string; nextRun: number; description: string }> {
    return Array.from(this.tasks.values())
      .filter(task => task.enabled && task.nextRun)
      .map(task => ({
        tag: task.tag,
        nextRun: task.nextRun!,
        description: task.description,
      }))
      .sort((a, b) => a.nextRun - b.nextRun);
  }

  /**
   * Setup default periodic sync tasks
   */
  private setupDefaultTasks(): void {
    // Data synchronization
    this.registerTask({
      tag: 'data-sync',
      description: 'Synchroniser les données avec le serveur',
      interval: 1000 * 60 * 30, // 30 minutes
      enabled: true,
      handler: async () => {
        // Import sync manager dynamically to avoid circular dependencies
        const { getSyncManager } = await import('./syncManager');
        const syncManager = getSyncManager();
        await syncManager.sync();
      },
    });

    // Cache cleanup
    this.registerTask({
      tag: 'cache-cleanup',
      description: 'Nettoyer le cache expiré',
      interval: 1000 * 60 * 60 * 6, // 6 hours
      enabled: true,
      handler: async () => {
        const { cacheManager } = await import('./cache');
        await cacheManager.cleanExpiredItems();
      },
    });

    // Performance metrics collection
    this.registerTask({
      tag: 'metrics-collection',
      description: 'Collecter les métriques de performance',
      interval: 1000 * 60 * 60, // 1 hour
      enabled: true,
      handler: async () => {
        const { performanceMonitor } = await import('./performance');
        await performanceMonitor.collectMetrics();
      },
    });

    // Analytics sync
    this.registerTask({
      tag: 'analytics-sync',
      description: 'Synchroniser les événements analytiques',
      interval: 1000 * 60 * 60 * 2, // 2 hours
      enabled: true,
      handler: async () => {
        const { analyticsService } = await import('./analytics');
        await analyticsService.syncEvents();
      },
    });
  }

  /**
   * Setup fallback sync using timers (when periodic sync API is not available)
   */
  private setupFallbackSync(): void {
    setInterval(() => {
      this.runFallbackTasks();
    }, 1000 * 60 * 5); // Check every 5 minutes
  }

  /**
   * Run fallback tasks using timer
   */
  private async runFallbackTasks(): Promise<void> {
    const now = Date.now();

    this.tasks.forEach(async (task) => {
      if (task.enabled && task.nextRun && now >= task.nextRun) {
        try {
          await this.executeTask(task.tag);
        } catch (error) {
          logger.error('Error in fallback task execution', { error, tag: task.tag });
        }
      }
    });
  }

  /**
   * Schedule a task using fallback timer method
   */
  private scheduleTaskFallback(task: PeriodicSyncTask): void {
    const scheduleNext = () => {
      setTimeout(async () => {
        if (task.enabled && this.tasks.has(task.tag)) {
          try {
            await this.executeTask(task.tag);
          } catch (error) {
            logger.error('Error in fallback task execution', { error, tag: task.tag });
          }
          
          // Schedule next run
          scheduleNext();
        }
      }, task.interval);
    };

    scheduleNext();
  }

  /**
   * Update configuration
   */
  updateConfig(updates: Partial<PeriodicSyncConfig>): void {
    this.config = { ...this.config, ...updates };
    logger.info('Periodic sync configuration updated', { config: this.config });
  }

  /**
   * Check if periodic sync is supported
   */
  isPeriodicSyncSupported(): boolean {
    return this.isSupported;
  }
}

// Export singleton instance factory
export const createPeriodicSyncManager = (config: PeriodicSyncConfig) => {
  return PeriodicSyncManager.getInstance(config);
};

// Export for getting existing instance
export const getPeriodicSyncManager = () => {
  return PeriodicSyncManager.getInstance();
};