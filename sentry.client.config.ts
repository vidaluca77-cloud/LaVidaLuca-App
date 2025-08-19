import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,

  // Additional configuration
  environment: process.env.NODE_ENV,

  // Performance monitoring
  profilesSampleRate: 1.0,

  // Filter out known non-critical errors
  beforeSend(event) {
    // Filter out non-critical errors
    if (event.exception) {
      const error = event.exception.values?.[0];
      if (error?.type === 'ChunkLoadError') {
        return null; // Don't send chunk load errors
      }
    }
    return event;
  },
});
