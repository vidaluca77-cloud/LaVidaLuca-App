import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  
  // Edge runtime specific configuration
  environment: process.env.NODE_ENV,
  
  initialScope: {
    tags: {
      component: "edge",
    },
  },
});