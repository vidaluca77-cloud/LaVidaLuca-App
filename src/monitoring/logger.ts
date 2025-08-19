import * as Sentry from '@sentry/nextjs';

// Enhanced logging interface with Sentry integration
interface LogEntry {
  timestamp: Date;
  level: 'debug' | 'info' | 'warn' | 'error';
  message: string;
  metadata?: Record<string, any>;
  component?: string;
  userId?: string;
  sessionId?: string;
  traceId?: string;
}

interface PerformanceLogEntry {
  name: string;
  duration: number;
  metadata?: Record<string, any>;
  component?: string;
}

class EnhancedLogger {
  private serviceName = 'la-vida-luca-frontend';
  private sessionId: string;

  constructor() {
    // Generate a session ID for tracking user sessions
    this.sessionId = this.generateSessionId();
    
    // Set session context in Sentry
    Sentry.setContext('session', {
      id: this.sessionId,
      startTime: new Date().toISOString(),
    });
  }

  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private log(level: LogEntry['level'], message: string, metadata?: Record<string, any>, component?: string) {
    const entry: LogEntry = {
      timestamp: new Date(),
      level,
      message,
      metadata,
      component,
      sessionId: this.sessionId,
      traceId: Sentry.getCurrentHub().getScope()?.getTransaction()?.traceId,
    };

    // Send to Sentry based on log level
    if (level === 'error') {
      Sentry.captureMessage(message, 'error', {
        contexts: {
          log: {
            level,
            component,
            sessionId: this.sessionId,
            metadata,
          },
        },
        tags: {
          log_level: level,
          component: component || 'unknown',
        },
      });
    } else if (level === 'warn') {
      Sentry.captureMessage(message, 'warning', {
        contexts: {
          log: {
            level,
            component,
            sessionId: this.sessionId,
            metadata,
          },
        },
        tags: {
          log_level: level,
          component: component || 'unknown',
        },
      });
    }

    // Add breadcrumb for all log levels
    Sentry.addBreadcrumb({
      category: 'log',
      message,
      level: this.mapLogLevelToSentryLevel(level),
      data: {
        component,
        metadata,
        sessionId: this.sessionId,
      },
    });

    // Console output with structured logging
    if (process.env.NODE_ENV === 'production') {
      console.log(JSON.stringify({
        service: this.serviceName,
        ...entry,
        timestamp: entry.timestamp.toISOString(),
      }));
    } else {
      // Readable logging in development
      const timestamp = entry.timestamp.toISOString();
      const componentStr = component ? `[${component}] ` : '';
      const sessionStr = `[${this.sessionId.split('_')[2]}] `;
      console.log(`${timestamp} [${level.toUpperCase()}] ${sessionStr}${componentStr}${message}`, metadata || '');
    }
  }

  private mapLogLevelToSentryLevel(level: LogEntry['level']): Sentry.SeverityLevel {
    const mapping: Record<LogEntry['level'], Sentry.SeverityLevel> = {
      debug: 'debug',
      info: 'info',
      warn: 'warning',
      error: 'error',
    };
    return mapping[level];
  }

  // Basic logging methods
  debug(message: string, metadata?: Record<string, any>, component?: string) {
    this.log('debug', message, metadata, component);
  }

  info(message: string, metadata?: Record<string, any>, component?: string) {
    this.log('info', message, metadata, component);
  }

  warn(message: string, metadata?: Record<string, any>, component?: string) {
    this.log('warn', message, metadata, component);
  }

  error(message: string, metadata?: Record<string, any>, component?: string) {
    this.log('error', message, metadata, component);
  }

  // Exception logging with stack trace
  exception(error: Error, context?: Record<string, any>, component?: string) {
    // Capture the full exception in Sentry
    Sentry.captureException(error, {
      contexts: {
        log: {
          component,
          sessionId: this.sessionId,
          context,
        },
      },
      tags: {
        log_type: 'exception',
        component: component || 'unknown',
      },
    });

    // Also log as error
    this.error(`Exception: ${error.message}`, {
      name: error.name,
      stack: error.stack,
      ...context,
    }, component);
  }

  // Performance logging
  timing(entry: PerformanceLogEntry) {
    const message = `Performance: ${entry.name}`;
    const metadata = {
      duration_ms: entry.duration,
      performance_metric: entry.name,
      ...entry.metadata,
    };

    this.info(message, metadata, entry.component || 'performance');

    // Send performance data to Sentry
    Sentry.setMeasurement(entry.name, entry.duration, 'millisecond');
  }

  // User action logging with enhanced context
  userAction(action: string, metadata?: Record<string, any>, component?: string) {
    const message = `User action: ${action}`;
    
    // Enhance metadata with user context
    const enhancedMetadata = {
      action_type: 'user_interaction',
      timestamp: Date.now(),
      url: typeof window !== 'undefined' ? window.location.href : 'server',
      userAgent: typeof window !== 'undefined' ? window.navigator.userAgent : 'server',
      ...metadata,
    };

    this.info(message, enhancedMetadata, component || 'user');

    // Set user action context in Sentry
    Sentry.setContext('userAction', {
      action,
      timestamp: new Date().toISOString(),
      ...metadata,
    });
  }

  // API call logging with comprehensive details
  apiCall(
    url: string, 
    method: string, 
    duration: number, 
    status: number, 
    metadata?: Record<string, any>
  ) {
    const message = `API call: ${method} ${url}`;
    const apiMetadata = {
      duration_ms: duration,
      status_code: status,
      method,
      url,
      success: status >= 200 && status < 400,
      ...metadata,
    };

    // Log as error if API call failed
    if (status >= 400) {
      this.error(message, apiMetadata, 'api');
    } else {
      this.info(message, apiMetadata, 'api');
    }

    // Performance timing
    this.timing({
      name: `api.${method.toLowerCase()}.duration`,
      duration,
      metadata: {
        endpoint: url,
        status,
      },
      component: 'api',
    });
  }

  // Security event logging
  securityEvent(event: string, details: Record<string, any>, component?: string) {
    const message = `Security event: ${event}`;
    
    // Security events are always warnings or errors
    this.warn(message, {
      security_event: event,
      timestamp: Date.now(),
      ...details,
    }, component || 'security');

    // Set security context in Sentry
    Sentry.setContext('security', {
      event,
      timestamp: new Date().toISOString(),
      ...details,
    });
  }

  // Business logic logging specific to La Vida Luca
  businessEvent(event: string, metadata?: Record<string, any>) {
    this.info(`Business event: ${event}`, {
      business_event: event,
      timestamp: Date.now(),
      ...metadata,
    }, 'business');
  }

  // Form interaction logging
  formEvent(formName: string, event: 'view' | 'start' | 'complete' | 'error' | 'abandon', metadata?: Record<string, any>) {
    const message = `Form ${event}: ${formName}`;
    
    this.info(message, {
      form_name: formName,
      form_event: event,
      timestamp: Date.now(),
      ...metadata,
    }, 'form');

    // Track form funnel in Sentry
    Sentry.addBreadcrumb({
      category: 'form',
      message,
      level: 'info',
      data: {
        formName,
        event,
        ...metadata,
      },
    });
  }

  // Navigation logging
  navigation(from: string, to: string, duration?: number) {
    const message = `Navigation: ${from} -> ${to}`;
    
    this.info(message, {
      navigation_from: from,
      navigation_to: to,
      duration_ms: duration,
      timestamp: Date.now(),
    }, 'navigation');
  }

  // Set user context for all future logs
  setUser(user: { id: string; email?: string; role?: string }) {
    // Update Sentry user context
    Sentry.setUser({
      id: user.id,
      email: user.email,
      role: user.role,
    });

    this.info('User context set', {
      user_id: user.id,
      user_role: user.role,
    }, 'auth');
  }

  // Clear user context
  clearUser() {
    Sentry.setUser(null);
    this.info('User context cleared', {}, 'auth');
  }

  // Get current session ID
  getSessionId(): string {
    return this.sessionId;
  }

  // Manual flush for critical scenarios
  flush(): Promise<boolean> {
    return Sentry.flush(2000); // 2 second timeout
  }
}

// Export singleton instance
export const logger = new EnhancedLogger();

// Utility functions for common logging patterns
export const logUtils = {
  // Wrap a function with automatic performance logging
  withPerformanceLogging<T extends (...args: any[]) => any>(
    fn: T,
    name: string,
    component?: string
  ): T {
    return ((...args: any[]) => {
      const startTime = performance.now();
      try {
        const result = fn(...args);
        const duration = performance.now() - startTime;
        logger.timing({ name, duration, component });
        return result;
      } catch (error) {
        const duration = performance.now() - startTime;
        logger.timing({ 
          name, 
          duration, 
          component,
          metadata: { error: true }
        });
        throw error;
      }
    }) as T;
  },

  // Wrap an async function with automatic performance logging
  withAsyncPerformanceLogging<T extends (...args: any[]) => Promise<any>>(
    fn: T,
    name: string,
    component?: string
  ): T {
    return (async (...args: any[]) => {
      const startTime = performance.now();
      try {
        const result = await fn(...args);
        const duration = performance.now() - startTime;
        logger.timing({ name, duration, component });
        return result;
      } catch (error) {
        const duration = performance.now() - startTime;
        logger.timing({ 
          name, 
          duration, 
          component,
          metadata: { error: true }
        });
        throw error;
      }
    }) as T;
  },

  // Wrap fetch with automatic API logging
  createLoggedFetch(baseUrl?: string) {
    return async (url: string, options?: RequestInit) => {
      const fullUrl = baseUrl ? `${baseUrl}${url}` : url;
      const method = options?.method || 'GET';
      const startTime = performance.now();

      try {
        const response = await fetch(fullUrl, options);
        const duration = performance.now() - startTime;
        
        logger.apiCall(fullUrl, method, duration, response.status, {
          requestSize: options?.body ? JSON.stringify(options.body).length : 0,
          responseType: response.headers.get('content-type'),
        });

        return response;
      } catch (error) {
        const duration = performance.now() - startTime;
        logger.apiCall(fullUrl, method, duration, 0, {
          error: error instanceof Error ? error.message : 'Unknown error',
        });
        throw error;
      }
    };
  },
};

export default logger;