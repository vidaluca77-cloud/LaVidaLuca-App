import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  
  // Server-specific configuration
  environment: process.env.NODE_ENV,
  
  // Enable performance monitoring
  profilesSampleRate: 1.0,
  
  // Additional server context
  initialScope: {
    tags: {
      component: "server",
    },
  },
});