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
  
  // Custom tags for filtering
  initialScope: {
    tags: {
      component: "frontend",
      application: "lavidaluca-app"
    },
  },
  
  // Filter out known non-critical errors
  beforeSend(event) {
    // Filter out non-critical errors
    if (event.exception) {
      const error = event.exception.values?.[0];
      if (error?.type === 'ChunkLoadError' || error?.type === 'ResizeObserver loop limit exceeded') {
        return null; // Don't send chunk load errors or resize observer errors
      }
    }
    
    // Add user context if available
    if (typeof window !== 'undefined') {
      const userProfile = localStorage.getItem('userProfile');
      if (userProfile) {
        try {
          const profile = JSON.parse(userProfile);
          event.user = {
            id: `${profile.location || 'anonymous'}-${Date.now()}`,
            location: profile.location,
            preferences: profile.preferences?.join(','),
          };
        } catch (e) {
          // Ignore parsing errors
        }
      }
    }
    
    return event;
  },
  
  // Custom integrations for better error context
  integrations: [
    new Sentry.Integrations.HttpContext(),
    new Sentry.Integrations.UserAgent(),
  ],
});