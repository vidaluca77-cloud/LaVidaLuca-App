/**
 * Performance Monitor for La Vida Luca App
 * Extends existing monitoring with advanced metrics collection and reporting
 */

import { logger } from './logger';
import { performanceMonitor as existingMonitor } from '../monitoring/performance';

export interface PerformanceMetrics {
  // Web Vitals
  fcp?: number; // First Contentful Paint
  lcp?: number; // Largest Contentful Paint
  fid?: number; // First Input Delay
  cls?: number; // Cumulative Layout Shift
  ttfb?: number; // Time to First Byte
  
  // Navigation timing
  domContentLoaded?: number;
  loadComplete?: number;
  
  // Resource timing
  totalResourceSize?: number;
  resourceCount?: number;
  averageResourceTime?: number;
  
  // Memory usage
  usedJSHeapSize?: number;
  totalJSHeapSize?: number;
  jsHeapSizeLimit?: number;
  
  // Connection info
  connectionType?: string;
  connectionSpeed?: string;
  
  // Custom metrics
  apiResponseTimes?: Record<string, number>;
  componentRenderTimes?: Record<string, number>;
  userInteractions?: number;
  
  // Timestamp
  timestamp: number;
  sessionId: string;
  userId?: string;
}

export interface PerformanceThresholds {
  fcp: { good: number; needsImprovement: number };
  lcp: { good: number; needsImprovement: number };
  fid: { good: number; needsImprovement: number };
  cls: { good: number; needsImprovement: number };
}

class PerformanceMonitorAdvanced {
  private static instance: PerformanceMonitorAdvanced;
  private metrics: PerformanceMetrics[] = [];
  private sessionId: string;
  private userId?: string;
  private observers: PerformanceObserver[] = [];
  private thresholds: PerformanceThresholds = {
    fcp: { good: 1800, needsImprovement: 3000 },
    lcp: { good: 2500, needsImprovement: 4000 },
    fid: { good: 100, needsImprovement: 300 },
    cls: { good: 0.1, needsImprovement: 0.25 },
  };

  static getInstance(): PerformanceMonitorAdvanced {
    if (!PerformanceMonitorAdvanced.instance) {
      PerformanceMonitorAdvanced.instance = new PerformanceMonitorAdvanced();
    }
    return PerformanceMonitorAdvanced.instance;
  }

  private constructor() {
    this.sessionId = crypto.randomUUID();
    this.initializeMonitoring();
  }

  /**
   * Initialize performance monitoring
   */
  private initializeMonitoring(): void {
    this.setupWebVitalsObservers();
    this.setupResourceObserver();
    this.setupNavigationObserver();
    this.setupUserTimingObserver();
    this.collectInitialMetrics();
    
    logger.info('Advanced performance monitoring initialized', { sessionId: this.sessionId });
  }

  /**
   * Setup Web Vitals observers
   */
  private setupWebVitalsObservers(): void {
    if (!('PerformanceObserver' in window)) {
      logger.warn('PerformanceObserver not supported');
      return;
    }

    try {
      // Largest Contentful Paint (LCP)
      const lcpObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1] as PerformanceEntry;
        this.updateMetric('lcp', lastEntry.startTime);
      });
      lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
      this.observers.push(lcpObserver);

      // First Input Delay (FID)
      const fidObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry: any) => {
          this.updateMetric('fid', entry.processingStart - entry.startTime);
        });
      });
      fidObserver.observe({ entryTypes: ['first-input'] });
      this.observers.push(fidObserver);

      // Cumulative Layout Shift (CLS)
      let clsValue = 0;
      const clsObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry: any) => {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
            this.updateMetric('cls', clsValue);
          }
        });
      });
      clsObserver.observe({ entryTypes: ['layout-shift'] });
      this.observers.push(clsObserver);

    } catch (error) {
      logger.error('Error setting up Web Vitals observers', { error });
    }
  }

  /**
   * Setup resource timing observer
   */
  private setupResourceObserver(): void {
    try {
      const resourceObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        this.processResourceEntries(entries);
      });
      resourceObserver.observe({ entryTypes: ['resource'] });
      this.observers.push(resourceObserver);
    } catch (error) {
      logger.error('Error setting up resource observer', { error });
    }
  }

  /**
   * Setup navigation timing observer
   */
  private setupNavigationObserver(): void {
    try {
      const navigationObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry: any) => {
          this.updateMetric('domContentLoaded', entry.domContentLoadedEventEnd - entry.fetchStart);
          this.updateMetric('loadComplete', entry.loadEventEnd - entry.fetchStart);
          this.updateMetric('ttfb', entry.responseStart - entry.requestStart);
        });
      });
      navigationObserver.observe({ entryTypes: ['navigation'] });
      this.observers.push(navigationObserver);
    } catch (error) {
      logger.error('Error setting up navigation observer', { error });
    }
  }

  /**
   * Setup user timing observer for custom metrics
   */
  private setupUserTimingObserver(): void {
    try {
      const userTimingObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry) => {
          if (entry.entryType === 'measure') {
            this.recordCustomMetric(entry.name, entry.duration);
          }
        });
      });
      userTimingObserver.observe({ entryTypes: ['measure'] });
      this.observers.push(userTimingObserver);
    } catch (error) {
      logger.error('Error setting up user timing observer', { error });
    }
  }

  /**
   * Collect initial metrics
   */
  private collectInitialMetrics(): void {
    // First Contentful Paint (FCP)
    const fcpEntry = performance.getEntriesByName('first-contentful-paint')[0];
    if (fcpEntry) {
      this.updateMetric('fcp', fcpEntry.startTime);
    }

    // Memory information
    if ('memory' in performance) {
      const memory = (performance as any).memory;
      this.updateMetric('usedJSHeapSize', memory.usedJSHeapSize);
      this.updateMetric('totalJSHeapSize', memory.totalJSHeapSize);
      this.updateMetric('jsHeapSizeLimit', memory.jsHeapSizeLimit);
    }

    // Connection information
    if ('connection' in navigator) {
      const connection = (navigator as any).connection;
      this.updateMetric('connectionType', connection.effectiveType);
      this.updateMetric('connectionSpeed', connection.downlink + 'Mbps');
    }
  }

  /**
   * Process resource timing entries
   */
  private processResourceEntries(entries: PerformanceEntry[]): void {
    let totalSize = 0;
    let totalTime = 0;
    let count = 0;

    entries.forEach((entry: any) => {
      if (entry.transferSize) {
        totalSize += entry.transferSize;
      }
      totalTime += entry.duration;
      count++;
    });

    this.updateMetric('totalResourceSize', totalSize);
    this.updateMetric('resourceCount', count);
    this.updateMetric('averageResourceTime', count > 0 ? totalTime / count : 0);
  }

  /**
   * Update a specific metric
   */
  private updateMetric(key: keyof PerformanceMetrics, value: any): void {
    const currentMetrics = this.getCurrentMetrics();
    (currentMetrics as any)[key] = value;
    this.saveCurrentMetrics(currentMetrics);
  }

  /**
   * Get current metrics object
   */
  private getCurrentMetrics(): PerformanceMetrics {
    if (this.metrics.length === 0) {
      const newMetrics: PerformanceMetrics = {
        timestamp: Date.now(),
        sessionId: this.sessionId,
        userId: this.userId,
        apiResponseTimes: {},
        componentRenderTimes: {},
        userInteractions: 0,
      };
      this.metrics.push(newMetrics);
      return newMetrics;
    }
    return this.metrics[this.metrics.length - 1];
  }

  /**
   * Save current metrics
   */
  private saveCurrentMetrics(metrics: PerformanceMetrics): void {
    if (this.metrics.length > 0) {
      this.metrics[this.metrics.length - 1] = metrics;
    }
  }

  /**
   * Record API response time
   */
  recordApiCall(endpoint: string, duration: number): void {
    const metrics = this.getCurrentMetrics();
    if (!metrics.apiResponseTimes) {
      metrics.apiResponseTimes = {};
    }
    metrics.apiResponseTimes[endpoint] = duration;
    this.saveCurrentMetrics(metrics);
    
    logger.debug('API call recorded', { endpoint, duration });
  }

  /**
   * Record component render time
   */
  recordComponentRender(componentName: string, duration: number): void {
    const metrics = this.getCurrentMetrics();
    if (!metrics.componentRenderTimes) {
      metrics.componentRenderTimes = {};
    }
    metrics.componentRenderTimes[componentName] = duration;
    this.saveCurrentMetrics(metrics);
    
    logger.debug('Component render recorded', { componentName, duration });
  }

  /**
   * Record user interaction
   */
  recordUserInteraction(): void {
    const metrics = this.getCurrentMetrics();
    metrics.userInteractions = (metrics.userInteractions || 0) + 1;
    this.saveCurrentMetrics(metrics);
  }

  /**
   * Record custom metric
   */
  recordCustomMetric(name: string, value: number): void {
    logger.debug('Custom metric recorded', { name, value });
    
    // You can extend this to store custom metrics in the metrics object
    // For now, just log them
  }

  /**
   * Start measuring a custom timing
   */
  startMeasure(name: string): void {
    performance.mark(`${name}-start`);
  }

  /**
   * End measuring a custom timing
   */
  endMeasure(name: string): number {
    performance.mark(`${name}-end`);
    performance.measure(name, `${name}-start`, `${name}-end`);
    
    const measure = performance.getEntriesByName(name, 'measure')[0];
    return measure?.duration || 0;
  }

  /**
   * Set user ID for metrics
   */
  setUserId(userId: string): void {
    this.userId = userId;
    const metrics = this.getCurrentMetrics();
    metrics.userId = userId;
    this.saveCurrentMetrics(metrics);
  }

  /**
   * Get performance score based on Web Vitals
   */
  getPerformanceScore(): { score: number; details: Record<string, string> } {
    const metrics = this.getCurrentMetrics();
    const details: Record<string, string> = {};
    let totalScore = 0;
    let metricsCount = 0;

    // FCP Score
    if (metrics.fcp !== undefined) {
      const fcpScore = this.getMetricScore('fcp', metrics.fcp);
      details.fcp = this.getScoreLabel(fcpScore);
      totalScore += fcpScore;
      metricsCount++;
    }

    // LCP Score
    if (metrics.lcp !== undefined) {
      const lcpScore = this.getMetricScore('lcp', metrics.lcp);
      details.lcp = this.getScoreLabel(lcpScore);
      totalScore += lcpScore;
      metricsCount++;
    }

    // FID Score
    if (metrics.fid !== undefined) {
      const fidScore = this.getMetricScore('fid', metrics.fid);
      details.fid = this.getScoreLabel(fidScore);
      totalScore += fidScore;
      metricsCount++;
    }

    // CLS Score
    if (metrics.cls !== undefined) {
      const clsScore = this.getMetricScore('cls', metrics.cls);
      details.cls = this.getScoreLabel(clsScore);
      totalScore += clsScore;
      metricsCount++;
    }

    const finalScore = metricsCount > 0 ? Math.round(totalScore / metricsCount) : 0;
    
    return { score: finalScore, details };
  }

  /**
   * Get metric score (0-100)
   */
  private getMetricScore(metric: keyof PerformanceThresholds, value: number): number {
    const threshold = this.thresholds[metric];
    
    if (value <= threshold.good) {
      return 100;
    } else if (value <= threshold.needsImprovement) {
      const range = threshold.needsImprovement - threshold.good;
      const position = value - threshold.good;
      return Math.max(0, 100 - Math.round((position / range) * 50));
    } else {
      return 0;
    }
  }

  /**
   * Get score label
   */
  private getScoreLabel(score: number): string {
    if (score >= 90) return 'Excellent';
    if (score >= 70) return 'Bon';
    if (score >= 50) return 'À améliorer';
    return 'Faible';
  }

  /**
   * Collect and return current metrics
   */
  async collectMetrics(): Promise<PerformanceMetrics> {
    const metrics = this.getCurrentMetrics();
    
    // Update memory metrics
    if ('memory' in performance) {
      const memory = (performance as any).memory;
      metrics.usedJSHeapSize = memory.usedJSHeapSize;
      metrics.totalJSHeapSize = memory.totalJSHeapSize;
      metrics.jsHeapSizeLimit = memory.jsHeapSizeLimit;
    }

    // Update timestamp
    metrics.timestamp = Date.now();
    
    this.saveCurrentMetrics(metrics);
    
    // Create a snapshot for storage/transmission
    const snapshot = { ...metrics };
    
    // Start new metrics collection
    this.metrics.push({
      timestamp: Date.now(),
      sessionId: this.sessionId,
      userId: this.userId,
      apiResponseTimes: {},
      componentRenderTimes: {},
      userInteractions: 0,
    });
    
    return snapshot;
  }

  /**
   * Get all collected metrics
   */
  getAllMetrics(): PerformanceMetrics[] {
    return [...this.metrics];
  }

  /**
   * Clear all metrics
   */
  clearMetrics(): void {
    this.metrics = [];
    logger.info('Performance metrics cleared');
  }

  /**
   * Cleanup observers
   */
  cleanup(): void {
    this.observers.forEach(observer => {
      observer.disconnect();
    });
    this.observers = [];
    this.clearMetrics();
  }
}

// Export singleton instance
export const performanceMonitor = PerformanceMonitorAdvanced.getInstance();

// Export for React hook
export const usePerformanceMonitor = () => {
  return {
    recordApiCall: performanceMonitor.recordApiCall.bind(performanceMonitor),
    recordComponentRender: performanceMonitor.recordComponentRender.bind(performanceMonitor),
    recordUserInteraction: performanceMonitor.recordUserInteraction.bind(performanceMonitor),
    startMeasure: performanceMonitor.startMeasure.bind(performanceMonitor),
    endMeasure: performanceMonitor.endMeasure.bind(performanceMonitor),
    getPerformanceScore: performanceMonitor.getPerformanceScore.bind(performanceMonitor),
    setUserId: performanceMonitor.setUserId.bind(performanceMonitor),
  };
};