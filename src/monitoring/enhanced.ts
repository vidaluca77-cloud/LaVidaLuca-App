/**
 * Enhanced monitoring system with offline support metrics
 */

import { performanceMonitor } from './performance';
import { offlineDataManager } from '@/lib/offlineData';

export interface OfflineMetrics {
  isOnline: boolean;
  connectionType: string;
  effectiveType: string;
  queuedActions: number;
  cachedDataSize: number;
  lastSyncTime: number | null;
  syncFailures: number;
  offlineDuration: number;
  cacheHitRate: number;
}

export interface EnhancedMetrics {
  performance: {
    avgPageLoad: number;
    webVitals: {
      fcp: number;
      lcp: number;
      fid: number;
      cls: number;
    };
    apiCalls: {
      total: number;
      successful: number;
      failed: number;
      avgLatency: number;
      fromCache: number;
    };
  };
  offline: OfflineMetrics;
  pwa: {
    isInstalled: boolean;
    isStandalone: boolean;
    serviceWorkerActive: boolean;
    notificationsEnabled: boolean;
    installPromptShown: boolean;
  };
  alerts: {
    total: number;
    errors: number;
    warnings: number;
    recent: number;
  };
  health: {
    status: 'healthy' | 'warning' | 'critical';
    issues: string[];
    score: number;
  };
}

class EnhancedMonitoringDashboard {
  private offlineStartTime: number | null = null;
  private totalOfflineTime = 0;
  private syncFailureCount = 0;
  private cacheRequests = 0;
  private cacheHits = 0;
  private lastSyncTime: number | null = null;

  constructor() {
    this.initializeOnlineTracking();
    this.initializeCacheTracking();
  }

  /**
   * Initialize online/offline tracking
   */
  private initializeOnlineTracking(): void {
    if (typeof window === 'undefined') return;

    // Track initial state
    if (!navigator.onLine) {
      this.offlineStartTime = Date.now();
    }

    // Listen for online/offline events
    window.addEventListener('online', () => {
      if (this.offlineStartTime) {
        this.totalOfflineTime += Date.now() - this.offlineStartTime;
        this.offlineStartTime = null;
      }
      this.handleBackOnline();
    });

    window.addEventListener('offline', () => {
      this.offlineStartTime = Date.now();
    });

    // Listen for sync events
    window.addEventListener('offlineActionSynced', () => {
      this.lastSyncTime = Date.now();
    });
  }

  /**
   * Initialize cache tracking
   */
  private initializeCacheTracking(): void {
    if (typeof window === 'undefined') return;

    // Wrap fetch to track cache hits
    const originalFetch = window.fetch;
    window.fetch = async (...args) => {
      this.cacheRequests++;
      
      try {
        const response = await originalFetch(...args);
        
        // Check if response came from cache
        if (response.headers.get('x-cache') === 'HIT' || 
            response.type === 'opaque' || 
            !navigator.onLine) {
          this.cacheHits++;
        }
        
        return response;
      } catch (error) {
        throw error;
      }
    };
  }

  /**
   * Handle back online event
   */
  private async handleBackOnline(): Promise<void> {
    try {
      const result = await offlineDataManager.processOfflineActions();
      this.syncFailureCount += result.failed;
      console.log('[Monitoring] Sync result:', result);
    } catch (error) {
      this.syncFailureCount++;
      console.error('[Monitoring] Sync failed:', error);
    }
  }

  /**
   * Get current offline metrics
   */
  private async getOfflineMetrics(): Promise<OfflineMetrics> {
    const stats = await offlineDataManager.getCacheStats();
    const connection = (navigator as any).connection;
    
    let currentOfflineDuration = 0;
    if (this.offlineStartTime) {
      currentOfflineDuration = Date.now() - this.offlineStartTime;
    }

    return {
      isOnline: navigator.onLine,
      connectionType: connection?.type || 'unknown',
      effectiveType: connection?.effectiveType || 'unknown',
      queuedActions: stats.totalActions,
      cachedDataSize: stats.cacheSize,
      lastSyncTime: this.lastSyncTime,
      syncFailures: this.syncFailureCount,
      offlineDuration: this.totalOfflineTime + currentOfflineDuration,
      cacheHitRate: this.cacheRequests > 0 ? (this.cacheHits / this.cacheRequests) * 100 : 0
    };
  }

  /**
   * Get PWA metrics
   */
  private getPWAMetrics(): EnhancedMetrics['pwa'] {
    if (typeof window === 'undefined') {
      return {
        isInstalled: false,
        isStandalone: false,
        serviceWorkerActive: false,
        notificationsEnabled: false,
        installPromptShown: false
      };
    }

    const isStandalone = window.matchMedia('(display-mode: standalone)').matches ||
                        (window.navigator as any).standalone === true;

    return {
      isInstalled: isStandalone,
      isStandalone,
      serviceWorkerActive: 'serviceWorker' in navigator && !!navigator.serviceWorker.controller,
      notificationsEnabled: 'Notification' in window && Notification.permission === 'granted',
      installPromptShown: !!localStorage.getItem('pwa-prompt-dismissed')
    };
  }

  /**
   * Calculate health score
   */
  private calculateHealthScore(metrics: EnhancedMetrics): number {
    let score = 100;
    const issues: string[] = [];

    // Performance penalties
    if (metrics.performance.webVitals.fcp > 1500) {
      score -= 10;
      issues.push('FCP trop élevé');
    }
    if (metrics.performance.webVitals.lcp > 2500) {
      score -= 15;
      issues.push('LCP trop élevé');
    }
    if (metrics.performance.webVitals.cls > 0.1) {
      score -= 10;
      issues.push('CLS trop élevé');
    }
    if (metrics.performance.webVitals.fid > 100) {
      score -= 10;
      issues.push('FID trop élevé');
    }

    // API failure penalties
    const apiFailureRate = metrics.performance.apiCalls.total > 0 
      ? (metrics.performance.apiCalls.failed / metrics.performance.apiCalls.total) * 100 
      : 0;
    
    if (apiFailureRate > 10) {
      score -= 20;
      issues.push(`${apiFailureRate.toFixed(1)}% d'échecs API`);
    }

    // Offline penalties
    if (metrics.offline.syncFailures > 5) {
      score -= 15;
      issues.push('Échecs de synchronisation fréquents');
    }

    if (metrics.offline.queuedActions > 10) {
      score -= 10;
      issues.push('Beaucoup d\'actions en attente');
    }

    // PWA bonuses
    if (metrics.pwa.serviceWorkerActive) score += 5;
    if (metrics.pwa.notificationsEnabled) score += 5;
    if (metrics.offline.cacheHitRate > 80) score += 10;

    metrics.health.issues = issues;
    return Math.max(0, Math.min(100, score));
  }

  /**
   * Get enhanced dashboard metrics
   */
  async getEnhancedMetrics(): Promise<EnhancedMetrics> {
    const performanceMetrics = performanceMonitor.getMetrics();
    const offlineMetrics = await this.getOfflineMetrics();
    const pwaMetrics = this.getPWAMetrics();

    // Calculate API metrics
    const apiMetrics = {
      total: 0,
      successful: 0,
      failed: 0,
      avgLatency: 0,
      fromCache: 0
    };

    const apiCalls = performanceMetrics.filter(m => m.name.startsWith('api-'));
    apiMetrics.total = apiCalls.length;

    if (apiCalls.length > 0) {
      apiMetrics.successful = apiCalls.filter(m => m.metadata?.success).length;
      apiMetrics.failed = apiCalls.filter(m => m.metadata?.error).length;
      apiMetrics.fromCache = apiCalls.filter(m => m.metadata?.fromCache).length;
      apiMetrics.avgLatency = apiCalls.reduce((sum, m) => sum + m.value, 0) / apiCalls.length;
    }

    // Calculate Web Vitals
    const webVitals = {
      fcp: performanceMetrics.find(m => m.name === 'fcp')?.value || 0,
      lcp: performanceMetrics.find(m => m.name === 'lcp')?.value || 0,
      fid: performanceMetrics.find(m => m.name === 'fid')?.value || 0,
      cls: performanceMetrics.find(m => m.name === 'cls')?.value || 0
    };

    const metrics: EnhancedMetrics = {
      performance: {
        avgPageLoad: performanceMetrics
          .filter(m => m.name === 'page-load')
          .reduce((sum, m, _, arr) => sum + m.value / arr.length, 0),
        webVitals,
        apiCalls: apiMetrics
      },
      offline: offlineMetrics,
      pwa: pwaMetrics,
      alerts: {
        total: 0,
        errors: 0,
        warnings: 0,
        recent: 0
      },
      health: {
        status: 'healthy',
        issues: [],
        score: 0
      }
    };

    // Calculate health score and status
    metrics.health.score = this.calculateHealthScore(metrics);
    
    if (metrics.health.score >= 80) {
      metrics.health.status = 'healthy';
    } else if (metrics.health.score >= 60) {
      metrics.health.status = 'warning';
    } else {
      metrics.health.status = 'critical';
    }

    return metrics;
  }

  /**
   * Export enhanced metrics
   */
  async exportEnhancedMetrics(): Promise<string> {
    try {
      const metrics = await this.getEnhancedMetrics();
      return JSON.stringify(metrics, null, 2);
    } catch (error) {
      return JSON.stringify({ error: (error as Error).message }, null, 2);
    }
  }

  /**
   * Start real-time monitoring with enhanced metrics
   */
  startEnhancedRealTimeMonitoring(
    callback: (metrics: EnhancedMetrics) => void,
    interval: number = 30000
  ): number {
    const updateMetrics = async () => {
      try {
        const metrics = await this.getEnhancedMetrics();
        callback(metrics);
      } catch (error) {
        console.error('[Monitoring] Failed to get enhanced metrics:', error);
      }
    };

    // Initial update
    updateMetrics();

    // Set up interval
    return window.setInterval(updateMetrics, interval);
  }

  /**
   * Stop real-time monitoring
   */
  stopRealTimeMonitoring(intervalId: number): void {
    clearInterval(intervalId);
  }

  /**
   * Reset offline metrics
   */
  resetOfflineMetrics(): void {
    this.offlineStartTime = null;
    this.totalOfflineTime = 0;
    this.syncFailureCount = 0;
    this.cacheRequests = 0;
    this.cacheHits = 0;
    this.lastSyncTime = null;
  }

  /**
   * Get cache performance report
   */
  async getCacheReport(): Promise<{
    hitRate: number;
    totalRequests: number;
    totalHits: number;
    queuedActions: number;
    cacheSize: string;
  }> {
    const stats = await offlineDataManager.getCacheStats();
    
    return {
      hitRate: this.cacheRequests > 0 ? (this.cacheHits / this.cacheRequests) * 100 : 0,
      totalRequests: this.cacheRequests,
      totalHits: this.cacheHits,
      queuedActions: stats.totalActions,
      cacheSize: (stats.cacheSize / 1024).toFixed(2) + ' KB'
    };
  }
}

// Singleton instance
export const enhancedMonitoringDashboard = new EnhancedMonitoringDashboard();