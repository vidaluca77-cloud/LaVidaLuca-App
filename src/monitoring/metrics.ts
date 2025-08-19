import * as Sentry from '@sentry/nextjs';

// Custom metrics collection for La Vida Luca application
export interface MetricData {
  name: string;
  value: number;
  unit?: string;
  tags?: Record<string, string>;
  timestamp?: number;
}

class MetricsCollector {
  private static instance: MetricsCollector;
  private metricsBuffer: MetricData[] = [];
  private flushInterval = 30000; // 30 seconds
  private maxBufferSize = 100;

  private constructor() {
    // Auto-flush metrics periodically
    if (typeof window !== 'undefined') {
      setInterval(() => this.flush(), this.flushInterval);
    }
  }

  static getInstance(): MetricsCollector {
    if (!MetricsCollector.instance) {
      MetricsCollector.instance = new MetricsCollector();
    }
    return MetricsCollector.instance;
  }

  // Record a custom metric
  record(metric: Omit<MetricData, 'timestamp'>) {
    const metricWithTimestamp: MetricData = {
      ...metric,
      timestamp: Date.now(),
    };

    this.metricsBuffer.push(metricWithTimestamp);

    // Send to Sentry as a measurement
    Sentry.setMeasurement(metric.name, metric.value, metric.unit || 'none');

    // Also add as breadcrumb for debugging
    Sentry.addBreadcrumb({
      category: 'metric',
      message: `${metric.name}: ${metric.value}${metric.unit || ''}`,
      level: 'info',
      data: {
        name: metric.name,
        value: metric.value,
        unit: metric.unit,
        tags: metric.tags,
      },
    });

    // Flush if buffer is full
    if (this.metricsBuffer.length >= this.maxBufferSize) {
      this.flush();
    }
  }

  // Increment a counter metric
  increment(name: string, value: number = 1, tags?: Record<string, string>) {
    this.record({
      name,
      value,
      unit: 'count',
      tags,
    });
  }

  // Record timing/duration metrics
  timing(name: string, duration: number, tags?: Record<string, string>) {
    this.record({
      name,
      value: duration,
      unit: 'millisecond',
      tags,
    });
  }

  // Record gauge metrics (current value)
  gauge(name: string, value: number, unit?: string, tags?: Record<string, string>) {
    this.record({
      name,
      value,
      unit,
      tags,
    });
  }

  // Performance timing wrapper
  timeFunction<T>(name: string, fn: () => T, tags?: Record<string, string>): T {
    const startTime = performance.now();
    try {
      const result = fn();
      const duration = performance.now() - startTime;
      this.timing(name, duration, tags);
      return result;
    } catch (error) {
      const duration = performance.now() - startTime;
      this.timing(name, duration, { ...tags, error: 'true' });
      throw error;
    }
  }

  // Async performance timing wrapper
  async timeAsyncFunction<T>(
    name: string, 
    fn: () => Promise<T>, 
    tags?: Record<string, string>
  ): Promise<T> {
    const startTime = performance.now();
    try {
      const result = await fn();
      const duration = performance.now() - startTime;
      this.timing(name, duration, tags);
      return result;
    } catch (error) {
      const duration = performance.now() - startTime;
      this.timing(name, duration, { ...tags, error: 'true' });
      throw error;
    }
  }

  // Flush metrics buffer
  private flush() {
    if (this.metricsBuffer.length === 0) return;

    // In a real implementation, you might send these to a custom metrics endpoint
    // For now, we'll just clear the buffer as Sentry already received the measurements
    console.debug(`Flushed ${this.metricsBuffer.length} metrics to monitoring system`);
    this.metricsBuffer = [];
  }

  // Get current buffer size (for debugging)
  getBufferSize(): number {
    return this.metricsBuffer.length;
  }
}

// Export singleton instance
export const metrics = MetricsCollector.getInstance();

// Business-specific metrics helpers
export const businessMetrics = {
  // Page view tracking
  trackPageView(page: string, loadTime?: number) {
    metrics.increment('page.view', 1, { page });
    if (loadTime) {
      metrics.timing('page.load_time', loadTime, { page });
    }
  },

  // User interaction tracking
  trackUserAction(action: string, component?: string, metadata?: Record<string, any>) {
    metrics.increment('user.action', 1, { 
      action, 
      component: component || 'unknown' 
    });
    
    // Add breadcrumb for user behavior analysis
    Sentry.addBreadcrumb({
      category: 'user',
      message: `User ${action}`,
      level: 'info',
      data: {
        action,
        component,
        ...metadata,
      },
    });
  },

  // Form interaction tracking
  trackFormInteraction(formName: string, event: 'start' | 'complete' | 'error' | 'abandon') {
    metrics.increment('form.interaction', 1, { 
      form: formName, 
      event 
    });
  },

  // API call tracking
  trackApiCall(endpoint: string, method: string, duration: number, statusCode: number) {
    metrics.timing('api.call.duration', duration, {
      endpoint,
      method,
      status: statusCode.toString(),
    });

    metrics.increment('api.call', 1, {
      endpoint,
      method,
      status: statusCode.toString(),
    });
  },

  // Error tracking
  trackError(error: string, context?: string) {
    metrics.increment('error.count', 1, {
      error,
      context: context || 'unknown',
    });
  },

  // Performance metrics
  trackPerformance(metric: string, value: number, context?: string) {
    metrics.gauge(`performance.${metric}`, value, 'millisecond', {
      context: context || 'general',
    });
  },

  // Business-specific metrics for La Vida Luca
  trackContactFormSubmission(successful: boolean) {
    metrics.increment('contact.form.submission', 1, {
      successful: successful.toString(),
    });
  },

  trackCatalogueView(category?: string) {
    metrics.increment('catalogue.view', 1, {
      category: category || 'all',
    });
  },

  trackJoinFormInteraction(step: string) {
    metrics.increment('join.form.step', 1, {
      step,
    });
  },
};

// Performance observer for automatic metrics collection
if (typeof window !== 'undefined' && 'PerformanceObserver' in window) {
  try {
    // Observe navigation timing
    const navObserver = new PerformanceObserver((list) => {
      list.getEntries().forEach((entry) => {
        if (entry.entryType === 'navigation') {
          const navEntry = entry as PerformanceNavigationTiming;
          metrics.timing('navigation.total', navEntry.loadEventEnd - navEntry.navigationStart);
          metrics.timing('navigation.dom_content_loaded', navEntry.domContentLoadedEventEnd - navEntry.navigationStart);
          metrics.timing('navigation.first_paint', navEntry.loadEventStart - navEntry.navigationStart);
        }
      });
    });
    navObserver.observe({ entryTypes: ['navigation'] });

    // Observe largest contentful paint
    const lcpObserver = new PerformanceObserver((list) => {
      list.getEntries().forEach((entry) => {
        metrics.timing('performance.largest_contentful_paint', entry.startTime);
      });
    });
    lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });

    // Observe first input delay
    const fidObserver = new PerformanceObserver((list) => {
      list.getEntries().forEach((entry) => {
        const fidEntry = entry as PerformanceEventTiming;
        metrics.timing('performance.first_input_delay', fidEntry.processingStart - fidEntry.startTime);
      });
    });
    fidObserver.observe({ entryTypes: ['first-input'] });

  } catch (error) {
    console.warn('Performance observers not supported or failed to initialize:', error);
  }
}

export default metrics;