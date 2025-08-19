import { logger } from '../lib/logger';

interface PerformanceMetric {
  name: string;
  value: number;
  timestamp: Date;
  metadata?: Record<string, any>;
}

class PerformanceMonitor {
  private metrics: PerformanceMetric[] = [];
  private startTimes: Map<string, number> = new Map();

  // Start timing an operation
  start(name: string) {
    this.startTimes.set(name, performance.now());
  }

  // End timing and record metric
  end(name: string, metadata?: Record<string, any>) {
    const startTime = this.startTimes.get(name);
    if (startTime === undefined) {
      logger.warn(
        `Performance timing '${name}' was ended without being started`
      );
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
      metadata,
    };

    this.metrics.push(metric);

    // Keep only last 1000 metrics
    if (this.metrics.length > 1000) {
      this.metrics.shift();
    }

    // Log the metric
    logger.timing(name, value, metadata);
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

  // Monitor Web Vitals
  observeWebVitals() {
    if (typeof window === 'undefined') return;

    // First Contentful Paint
    new PerformanceObserver(list => {
      const entries = list.getEntries();
      entries.forEach(entry => {
        if (entry.name === 'first-contentful-paint') {
          this.recordMetric('fcp', entry.startTime, { type: 'web-vital' });
        }
      });
    }).observe({ entryTypes: ['paint'] });

    // Largest Contentful Paint
    new PerformanceObserver(list => {
      const entries = list.getEntries();
      const lastEntry = entries[entries.length - 1];
      this.recordMetric('lcp', lastEntry.startTime, { type: 'web-vital' });
    }).observe({ entryTypes: ['largest-contentful-paint'] });

    // First Input Delay
    new PerformanceObserver(list => {
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
    new PerformanceObserver(list => {
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

    window.fetch = async function (...args) {
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
          success: response.ok,
        });

        return response;
      } catch (error) {
        const duration = performance.now() - startTime;

        monitor.recordMetric('api_call', duration, {
          url,
          method,
          error: true,
          errorMessage:
            error instanceof Error ? error.message : 'Unknown error',
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
