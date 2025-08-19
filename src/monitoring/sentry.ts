import * as Sentry from "@sentry/nextjs";

// Comprehensive Sentry configuration for La Vida Luca application
export const initSentry = () => {
  Sentry.init({
    dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
    
    // Environment configuration
    environment: process.env.NODE_ENV,
    release: process.env.NEXT_PUBLIC_APP_VERSION || "1.0.0",
    
    // Performance monitoring
    tracesSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 1.0,
    profilesSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 1.0,
    
    // Session replay
    replaysSessionSampleRate: 0.1,
    replaysOnErrorSampleRate: 1.0,
    
    // Error filtering
    beforeSend(event, hint) {
      // Filter out known non-critical errors
      const error = hint.originalException;
      
      if (error instanceof Error) {
        // Filter chunk load errors (common in deployments)
        if (error.name === 'ChunkLoadError' || error.message?.includes('Loading chunk')) {
          return null;
        }
        
        // Filter network errors that are not actionable
        if (error.message?.includes('NetworkError') || error.message?.includes('Failed to fetch')) {
          return null;
        }
        
        // Filter extension-related errors
        if (error.stack?.includes('extension://') || error.stack?.includes('moz-extension://')) {
          return null;
        }
      }
      
      return event;
    },
    
    // Enhanced error context
    beforeBreadcrumb(breadcrumb, hint) {
      // Add more context to navigation breadcrumbs
      if (breadcrumb.category === 'navigation') {
        breadcrumb.data = {
          ...breadcrumb.data,
          timestamp: new Date().toISOString(),
          userAgent: typeof window !== 'undefined' ? window.navigator.userAgent : 'server',
        };
      }
      
      return breadcrumb;
    },
    
    // Initial scope configuration
    initialScope: {
      tags: {
        component: "frontend",
        app: "la-vida-luca",
      },
      contexts: {
        app: {
          name: "La Vida Luca",
          version: process.env.NEXT_PUBLIC_APP_VERSION || "1.0.0",
        },
      },
    },
  });
};

// User tracking utilities
export const setUser = (user: {
  id: string;
  email?: string;
  username?: string;
  role?: string;
}) => {
  Sentry.setUser({
    id: user.id,
    email: user.email,
    username: user.username,
    role: user.role,
  });
};

export const clearUser = () => {
  Sentry.setUser(null);
};

// Custom context utilities
export const setContext = (key: string, context: Record<string, any>) => {
  Sentry.setContext(key, context);
};

// Tag utilities
export const setTag = (key: string, value: string) => {
  Sentry.setTag(key, value);
};

export const setTags = (tags: Record<string, string>) => {
  Sentry.setTags(tags);
};

// Breadcrumb utilities
export const addBreadcrumb = (breadcrumb: {
  message: string;
  category?: string;
  level?: Sentry.SeverityLevel;
  data?: Record<string, any>;
}) => {
  Sentry.addBreadcrumb({
    message: breadcrumb.message,
    category: breadcrumb.category || "custom",
    level: breadcrumb.level || "info",
    data: breadcrumb.data,
    timestamp: Date.now() / 1000,
  });
};

// Performance monitoring utilities
export const startTransaction = (name: string, op: string) => {
  return Sentry.startSpan({
    name,
    op,
  }, (span) => span);
};

export const captureException = (error: Error, context?: Record<string, any>) => {
  return Sentry.captureException(error, {
    contexts: context ? { custom: context } : undefined,
  });
};

export const captureMessage = (message: string, level: Sentry.SeverityLevel = "info", context?: Record<string, any>) => {
  return Sentry.captureMessage(message, level, {
    contexts: context ? { custom: context } : undefined,
  });
};

// Initialize Sentry immediately when this module is imported
if (typeof window !== 'undefined' || process.env.NODE_ENV === 'production') {
  initSentry();
}