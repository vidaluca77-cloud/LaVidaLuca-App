import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  
  // Additional configuration
  environment: process.env.NODE_ENV,
  
  // Performance monitoring
  profilesSampleRate: 1.0,
  
  // Initial context
  initialScope: {
    tags: {
      component: "frontend"
    },
  },
  
  // Filter out known non-critical errors
  beforeSend(event) {
    // Filter out non-critical errors
    if (event.exception) {
      const error = event.exception.values?.[0];
      if (error?.type === 'ChunkLoadError') {
        return null; // Don't send chunk load errors
      }
      // Filter out network errors that are not actionable
      if (error?.type === 'TypeError' && error?.value?.includes('fetch')) {
        return null;
      }
    }
    
    // Add user agent and screen resolution to context
    if (typeof window !== 'undefined') {
      event.contexts = {
        ...event.contexts,
        browser: {
          name: navigator.userAgent,
          version: navigator.appVersion,
        },
        device: {
          screen_resolution: `${screen.width}x${screen.height}`,
          viewport_size: `${window.innerWidth}x${window.innerHeight}`,
        }
      };
    }
    
    return event;
  },
});

// Utility functions for user context
export const setUserContext = (user: {
  id?: string;
  email?: string;
  username?: string;
  role?: string;
  [key: string]: any;
}) => {
  Sentry.setUser(user);
};

export const setUserSession = (sessionData: {
  sessionId: string;
  startTime: Date;
  userAgent?: string;
  ipAddress?: string;
}) => {
  Sentry.setContext("session", {
    session_id: sessionData.sessionId,
    start_time: sessionData.startTime.toISOString(),
    user_agent: sessionData.userAgent,
    ip_address: sessionData.ipAddress,
  });
};

export const setPageContext = (pageData: {
  page: string;
  section?: string;
  feature?: string;
  loadTime?: number;
}) => {
  Sentry.setContext("page", pageData);
};

export const trackUserActivity = (activity: string, metadata?: Record<string, any>) => {
  Sentry.addBreadcrumb({
    message: activity,
    category: "user.activity",
    level: "info",
    data: metadata,
    timestamp: Date.now() / 1000,
  });
};