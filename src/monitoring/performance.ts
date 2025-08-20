import { logger } from '../lib/logger';
import { alertManager } from './alerts';

interface PerformanceMetric {
  name: string;
  value: number;
  timestamp: Date;
  metadata?: Record<string, any>;
}

interface WebVitalsMetrics {
  fcp?: number; // First Contentful Paint
  lcp?: number; // Largest Contentful Paint
  fid?: number; // First Input Delay
  cls?: number; // Cumulative Layout Shift
  ttfb?: number; // Time to First Byte
  inp?: number; // Interaction to Next Paint
}

class PerformanceMonitor {
  private metrics: PerformanceMetric[] = [];
  private startTimes: Map<string, number> = new Map();
  private webVitals: WebVitalsMetrics = {};
  private vitalsObservers: PerformanceObserver[] = [];

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

    // Check for performance issues
    this.checkPerformanceThresholds(name, value);
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
    this.webVitals = {};
  }

  // Get current Web Vitals
  getWebVitals(): WebVitalsMetrics {
    return { ...this.webVitals };
  }

  // Check performance thresholds and alert if needed
  private checkPerformanceThresholds(name: string, value: number) {
    const thresholds = {
      fcp: { good: 1800, poor: 3000 }, // First Contentful Paint (ms)
      lcp: { good: 2500, poor: 4000 }, // Largest Contentful Paint (ms)
      fid: { good: 100, poor: 300 },   // First Input Delay (ms)
      cls: { good: 0.1, poor: 0.25 },  // Cumulative Layout Shift (score)
      ttfb: { good: 800, poor: 1800 }, // Time to First Byte (ms)
      inp: { good: 200, poor: 500 }    // Interaction to Next Paint (ms)
    };

    const threshold = thresholds[name as keyof typeof thresholds];
    if (!threshold) return;

    if (value > threshold.poor) {
      alertManager.warning(`Poor ${name.toUpperCase()} performance detected`, {
        metric: name,
        value,
        threshold: threshold.poor,
        category: 'performance'
      });
    } else if (value > threshold.good) {
      alertManager.info(`${name.toUpperCase()} performance needs improvement`, {
        metric: name,
        value,
        threshold: threshold.good,
        category: 'performance'
      });
    }
  }

  // Enhanced Web Vitals monitoring
  observeWebVitals() {
    if (typeof window === 'undefined') return;

    try {
      // First Contentful Paint
      const fcpObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry) => {
          if (entry.name === 'first-contentful-paint') {
            this.webVitals.fcp = entry.startTime;
            this.recordMetric('fcp', entry.startTime, { type: 'web-vital' });
          }
        });
      });
      fcpObserver.observe({ entryTypes: ['paint'] });
      this.vitalsObservers.push(fcpObserver);

      // Largest Contentful Paint
      const lcpObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        this.webVitals.lcp = lastEntry.startTime;
        this.recordMetric('lcp', lastEntry.startTime, { type: 'web-vital' });
      });
      lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
      this.vitalsObservers.push(lcpObserver);

      // First Input Delay
      const fidObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry: any) => {
          if (entry.processingStart && entry.startTime) {
            const fid = entry.processingStart - entry.startTime;
            this.webVitals.fid = fid;
            this.recordMetric('fid', fid, { type: 'web-vital' });
          }
        });
      });
      fidObserver.observe({ entryTypes: ['first-input'] });
      this.vitalsObservers.push(fidObserver);

      // Cumulative Layout Shift
      let cumulativeLayoutShift = 0;
      const clsObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry: any) => {
          if (!entry.hadRecentInput) {
            cumulativeLayoutShift += entry.value;
            this.webVitals.cls = cumulativeLayoutShift;
            this.recordMetric('cls', cumulativeLayoutShift, { type: 'web-vital' });
          }
        });
      });
      clsObserver.observe({ entryTypes: ['layout-shift'] });
      this.vitalsObservers.push(clsObserver);

      // Time to First Byte (via Navigation Timing)
      this.measureTTFB();

      // Interaction to Next Paint (experimental)
      this.measureINP();

    } catch (error) {
      logger.error('Failed to initialize Web Vitals monitoring', { error });
    }
  }

  private measureTTFB() {
    if ('performance' in window && 'getEntriesByType' in performance) {
      const navEntry = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      if (navEntry && navEntry.responseStart && navEntry.requestStart) {
        const ttfb = navEntry.responseStart - navEntry.requestStart;
        this.webVitals.ttfb = ttfb;
        this.recordMetric('ttfb', ttfb, { type: 'web-vital' });
      }
    }
  }

  private measureINP() {
    // Interaction to Next Paint is still experimental
    // For now, we'll track using event timing API where available
    try {
      const inpObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry: any) => {
          if (entry.interactionId && entry.duration) {
            this.webVitals.inp = Math.max(this.webVitals.inp || 0, entry.duration);
            this.recordMetric('inp', entry.duration, { 
              type: 'web-vital',
              interactionId: entry.interactionId 
            });
          }
        });
      });
      inpObserver.observe({ entryTypes: ['event'] });
      this.vitalsObservers.push(inpObserver);
    } catch (error) {
      // INP observation not supported
      logger.debug('INP observation not supported', { error });
    }
  }

  // Disconnect all observers
  disconnectObservers() {
    this.vitalsObservers.forEach(observer => observer.disconnect());
    this.vitalsObservers = [];
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