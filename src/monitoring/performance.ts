import { logger } from '../lib/logger';

interface PerformanceMetric {
  name: string;
  value: number;
  timestamp: Date;
  metadata?: Record<string, any>;
}

interface RealTimeMetrics {
  pageLoad: number;
  apiCalls: {
    count: number;
    avgLatency: number;
    errorRate: number;
  };
  webVitals: {
    fcp: number;
    lcp: number;
    fid: number;
    cls: number;
  };
  memory?: {
    used: number;
    total: number;
  };
  connection?: {
    effectiveType: string;
    downlink: number;
  };
}

class PerformanceMonitor {
  private metrics: PerformanceMetric[] = [];
  private startTimes: Map<string, number> = new Map();
  private realTimeListeners: Set<(metrics: RealTimeMetrics) => void> = new Set();
  private realTimeInterval: NodeJS.Timeout | null = null;

  // Start timing an operation
  start(name: string) {
    this.startTimes.set(name, performance.now());
  }

  // End timing and record metric
  end(name: string, metadata?: Record<string, any>) {
    const startTime = this.startTimes.get(name);
    if (startTime === undefined) {
      logger.warn(`Performance timing '${name}' was ended without being started`);
      return;
    }

    const duration = performance.now() - startTime;
    this.startTimes.delete(name);
    
    this.recordMetric(name, duration, metadata);
  }

  // Record a metric directly
  recordMetric(name: string, value: number, metadata?: Record<string, any>) {
    const metric: PerformanceMetric = {
      name,
      value,
      timestamp: new Date(),
      metadata
    };

    this.metrics.push(metric);
    
    // Keep only last 1000 metrics
    if (this.metrics.length > 1000) {
      this.metrics.shift();
    }

    // Log the metric
    logger.timing(name, value, metadata);

    // Trigger real-time update if listeners are active
    if (this.realTimeListeners.size > 0) {
      this.updateRealTimeMetrics();
    }
  }

  // Get metrics
  getMetrics(): PerformanceMetric[] {
    return [...this.metrics];
  }

  getMetricsByName(name: string): PerformanceMetric[] {
    return this.metrics.filter(metric => metric.name === name);
  }

  // Clear metrics
  clearMetrics() {
    this.metrics = [];
  }

  // Real-time metrics management
  startRealTimeMonitoring(callback: (metrics: RealTimeMetrics) => void, interval: number = 5000): () => void {
    this.realTimeListeners.add(callback);

    // Start interval if this is the first listener
    if (this.realTimeListeners.size === 1 && !this.realTimeInterval) {
      this.realTimeInterval = setInterval(() => {
        this.updateRealTimeMetrics();
      }, interval);
    }

    // Initial update
    this.updateRealTimeMetrics();

    // Return unsubscribe function
    return () => {
      this.realTimeListeners.delete(callback);
      
      // Stop interval if no more listeners
      if (this.realTimeListeners.size === 0 && this.realTimeInterval) {
        clearInterval(this.realTimeInterval);
        this.realTimeInterval = null;
      }
    };
  }

  private updateRealTimeMetrics(): void {
    const now = Date.now();
    const fiveMinutesAgo = new Date(now - 5 * 60 * 1000);
    const recentMetrics = this.metrics.filter(m => m.timestamp >= fiveMinutesAgo);

    const metrics: RealTimeMetrics = {
      pageLoad: this.calculateAveragePageLoad(recentMetrics),
      apiCalls: this.calculateAPIMetrics(recentMetrics),
      webVitals: this.calculateWebVitals(recentMetrics),
      memory: this.getMemoryInfo(),
      connection: this.getConnectionInfo()
    };

    this.realTimeListeners.forEach(listener => {
      try {
        listener(metrics);
      } catch (error) {
        console.error('Error in real-time metrics listener:', error);
      }
    });
  }

  private calculateAveragePageLoad(metrics: PerformanceMetric[]): number {
    const pageLoadMetrics = metrics.filter(m => m.name === 'page_load');
    if (pageLoadMetrics.length === 0) return 0;
    
    const sum = pageLoadMetrics.reduce((acc, m) => acc + m.value, 0);
    return sum / pageLoadMetrics.length;
  }

  private calculateAPIMetrics(metrics: PerformanceMetric[]): RealTimeMetrics['apiCalls'] {
    const apiMetrics = metrics.filter(m => m.name === 'api_call');
    
    if (apiMetrics.length === 0) {
      return { count: 0, avgLatency: 0, errorRate: 0 };
    }

    const totalLatency = apiMetrics.reduce((acc, m) => acc + m.value, 0);
    const errorCount = apiMetrics.filter(m => m.metadata?.error).length;

    return {
      count: apiMetrics.length,
      avgLatency: totalLatency / apiMetrics.length,
      errorRate: (errorCount / apiMetrics.length) * 100
    };
  }

  private calculateWebVitals(metrics: PerformanceMetric[]): RealTimeMetrics['webVitals'] {
    const getLatestMetric = (name: string) => {
      const filtered = metrics
        .filter(m => m.name === name && m.metadata?.type === 'web-vital')
        .sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
      return filtered.length > 0 ? filtered[0].value : 0;
    };

    return {
      fcp: getLatestMetric('fcp'),
      lcp: getLatestMetric('lcp'),
      fid: getLatestMetric('fid'),
      cls: getLatestMetric('cls')
    };
  }

  private getMemoryInfo(): RealTimeMetrics['memory'] | undefined {
    if (typeof window === 'undefined' || !(performance as any).memory) {
      return undefined;
    }

    const memory = (performance as any).memory;
    return {
      used: memory.usedJSHeapSize,
      total: memory.totalJSHeapSize
    };
  }

  private getConnectionInfo(): RealTimeMetrics['connection'] | undefined {
    if (typeof window === 'undefined' || !(navigator as any).connection) {
      return undefined;
    }

    const connection = (navigator as any).connection;
    return {
      effectiveType: connection.effectiveType || 'unknown',
      downlink: connection.downlink || 0
    };
  }

  // Monitor Web Vitals
  observeWebVitals() {
    if (typeof window === 'undefined') return;

    // First Contentful Paint
    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach((entry) => {
        if (entry.name === 'first-contentful-paint') {
          this.recordMetric('fcp', entry.startTime, { type: 'web-vital' });
        }
      });
    }).observe({ entryTypes: ['paint'] });

    // Largest Contentful Paint
    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      const lastEntry = entries[entries.length - 1];
      this.recordMetric('lcp', lastEntry.startTime, { type: 'web-vital' });
    }).observe({ entryTypes: ['largest-contentful-paint'] });

    // First Input Delay
    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach((entry: any) => {
        if (entry.processingStart && entry.startTime) {
          const fid = entry.processingStart - entry.startTime;
          this.recordMetric('fid', fid, { type: 'web-vital' });
        }
      });
    }).observe({ entryTypes: ['first-input'] });

    // Cumulative Layout Shift
    let cumulativeLayoutShift = 0;
    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach((entry: any) => {
        if (!entry.hadRecentInput) {
          cumulativeLayoutShift += entry.value;
        }
      });
      this.recordMetric('cls', cumulativeLayoutShift, { type: 'web-vital' });
    }).observe({ entryTypes: ['layout-shift'] });
  }

  // Monitor API calls
  wrapFetch() {
    if (typeof window === 'undefined') return;
    
    const originalFetch = window.fetch;
    const monitor = this;
    
    window.fetch = async function(...args) {
      const startTime = performance.now();
      const url = args[0] as string;
      const options = args[1] as RequestInit;
      const method = options?.method || 'GET';
      
      try {
        const response = await originalFetch.apply(this, args);
        const duration = performance.now() - startTime;
        
        monitor.recordMetric('api_call', duration, {
          url,
          method,
          status: response.status,
          success: response.ok
        });
        
        return response;
      } catch (error) {
        const duration = performance.now() - startTime;
        
        monitor.recordMetric('api_call', duration, {
          url,
          method,
          error: true,
          errorMessage: error instanceof Error ? error.message : 'Unknown error'
        });
        
        throw error;
      }
    };
  }
}

export const performanceMonitor = new PerformanceMonitor();

// Auto-initialize in browser
if (typeof window !== 'undefined') {
  performanceMonitor.observeWebVitals();
  performanceMonitor.wrapFetch();
}