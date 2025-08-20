/**
 * Custom metrics implementation for monitoring and analytics
 */

import * as Sentry from '@sentry/nextjs';

// Performance metrics interface
interface PerformanceMetric {
  name: string;
  value: number;
  unit: string;
  tags?: Record<string, string>;
  timestamp?: number;
}

// User interaction metrics interface
interface UserInteractionMetric {
  action: string;
  component: string;
  page: string;
  metadata?: Record<string, any>;
  timestamp?: number;
}

// Business metrics interface
interface BusinessMetric {
  event: string;
  value?: number;
  category: string;
  metadata?: Record<string, any>;
  timestamp?: number;
}

// Custom metrics class
class MetricsCollector {
  private enabled: boolean;
  private buffer: Array<PerformanceMetric | UserInteractionMetric | BusinessMetric>;
  private flushInterval: number;
  private flushTimer: NodeJS.Timeout | null;

  constructor() {
    this.enabled = typeof window !== 'undefined' && !!process.env.NEXT_PUBLIC_SENTRY_DSN;
    this.buffer = [];
    this.flushInterval = 30000; // 30 seconds
    this.flushTimer = null;
    
    if (this.enabled) {
      this.startFlushTimer();
    }
  }

  // Performance metrics
  recordPerformanceMetric(metric: PerformanceMetric): void {
    if (!this.enabled) return;

    const metricWithTimestamp = {
      ...metric,
      timestamp: metric.timestamp || Date.now(),
    };

    // Send to Sentry as a measurement
    Sentry.setMeasurement(metric.name, metric.value, metric.unit);
    
    // Add to buffer for batch processing
    this.buffer.push(metricWithTimestamp);
    
    // Add breadcrumb for debugging
    Sentry.addBreadcrumb({
      message: `Performance metric: ${metric.name}`,
      category: 'performance',
      level: 'info',
      data: metricWithTimestamp,
    });
  }

  // User interaction metrics
  recordUserInteraction(interaction: UserInteractionMetric): void {
    if (!this.enabled) return;

    const interactionWithTimestamp = {
      ...interaction,
      timestamp: interaction.timestamp || Date.now(),
    };

    // Send to Sentry as custom event
    Sentry.addBreadcrumb({
      message: `User interaction: ${interaction.action}`,
      category: 'user.interaction',
      level: 'info',
      data: interactionWithTimestamp,
    });

    this.buffer.push(interactionWithTimestamp);
  }

  // Business metrics
  recordBusinessMetric(metric: BusinessMetric): void {
    if (!this.enabled) return;

    const metricWithTimestamp = {
      ...metric,
      timestamp: metric.timestamp || Date.now(),
    };

    // Send to Sentry as custom event
    Sentry.withScope((scope) => {
      scope.setTag('metric_category', metric.category);
      scope.setContext('business_metric', metricWithTimestamp);
      Sentry.captureMessage(`Business metric: ${metric.event}`, 'info');
    });

    this.buffer.push(metricWithTimestamp);
  }

  // Page load metrics
  recordPageLoad(page: string, loadTime: number): void {
    this.recordPerformanceMetric({
      name: 'page_load_time',
      value: loadTime,
      unit: 'millisecond',
      tags: { page },
    });
  }

  // API response metrics
  recordApiResponse(endpoint: string, method: string, duration: number, status: number): void {
    this.recordPerformanceMetric({
      name: 'api_response_time',
      value: duration,
      unit: 'millisecond',
      tags: { endpoint, method, status: status.toString() },
    });
  }

  // Error metrics
  recordError(error: Error, context?: Record<string, any>): void {
    if (!this.enabled) return;

    Sentry.withScope((scope) => {
      if (context) {
        scope.setContext('error_context', context);
      }
      Sentry.captureException(error);
    });
  }

  // Feature usage metrics
  recordFeatureUsage(feature: string, page: string, metadata?: Record<string, any>): void {
    this.recordBusinessMetric({
      event: 'feature_used',
      category: 'engagement',
      metadata: { feature, page, ...metadata },
    });
  }

  // Form metrics
  recordFormSubmission(formName: string, success: boolean, validationErrors?: string[]): void {
    this.recordBusinessMetric({
      event: 'form_submission',
      category: 'conversion',
      metadata: { 
        form: formName, 
        success, 
        validation_errors: validationErrors?.length || 0 
      },
    });
  }

  // Search metrics
  recordSearch(query: string, resultsCount: number, page: string): void {
    this.recordBusinessMetric({
      event: 'search_performed',
      category: 'engagement',
      metadata: { 
        query_length: query.length, 
        results_count: resultsCount, 
        page 
      },
    });
  }

  // Navigation metrics
  recordNavigation(from: string, to: string, method: 'click' | 'browser' | 'programmatic'): void {
    this.recordUserInteraction({
      action: 'navigation',
      component: 'router',
      page: from,
      metadata: { to, method },
    });
  }

  // Flush metrics buffer
  private flush(): void {
    if (this.buffer.length === 0) return;

    // In a real implementation, you might send this to your analytics service
    console.debug(`Flushing ${this.buffer.length} metrics to analytics service`);
    
    // Clear buffer
    this.buffer = [];
  }

  private startFlushTimer(): void {
    this.flushTimer = setInterval(() => {
      this.flush();
    }, this.flushInterval);
  }

  // Cleanup
  destroy(): void {
    if (this.flushTimer) {
      clearInterval(this.flushTimer);
      this.flushTimer = null;
    }
    this.flush();
  }
}

// Create singleton instance
const metricsCollector = new MetricsCollector();

// Utility functions for common patterns
export const trackPageView = (page: string, referrer?: string) => {
  metricsCollector.recordBusinessMetric({
    event: 'page_view',
    category: 'engagement',
    metadata: { page, referrer },
  });
};

export const trackButtonClick = (buttonName: string, page: string, context?: Record<string, any>) => {
  metricsCollector.recordUserInteraction({
    action: 'click',
    component: 'button',
    page,
    metadata: { button_name: buttonName, ...context },
  });
};

export const trackFormError = (formName: string, field: string, error: string) => {
  metricsCollector.recordBusinessMetric({
    event: 'form_error',
    category: 'user_experience',
    metadata: { form: formName, field, error },
  });
};

export const trackApiError = (endpoint: string, method: string, status: number, error: string) => {
  metricsCollector.recordError(new Error(`API Error: ${method} ${endpoint}`), {
    endpoint,
    method,
    status,
    error_message: error,
  });
};

// Performance monitoring utilities
export const measureAsync = async <T>(
  name: string,
  fn: () => Promise<T>,
  tags?: Record<string, string>
): Promise<T> => {
  const start = performance.now();
  try {
    const result = await fn();
    const duration = performance.now() - start;
    metricsCollector.recordPerformanceMetric({
      name,
      value: duration,
      unit: 'millisecond',
      tags,
    });
    return result;
  } catch (error) {
    const duration = performance.now() - start;
    metricsCollector.recordPerformanceMetric({
      name: `${name}_error`,
      value: duration,
      unit: 'millisecond',
      tags: { ...tags, error: 'true' },
    });
    throw error;
  }
};

// Export the main collector and utilities
export {
  metricsCollector,
  type PerformanceMetric,
  type UserInteractionMetric,
  type BusinessMetric,
};

export default metricsCollector;