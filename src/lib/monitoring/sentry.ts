import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  integrations: [
    new Sentry.BrowserTracing({
      tracePropagationTargets: [
        "localhost", 
        "la-vida-luca.vercel.app",
        /^https:\/\/.*\.render\.com/
      ],
    }),
  ],
  environment: process.env.NODE_ENV,
  beforeSend: (event) => {
    // Filter out non-production errors in development
    if (process.env.NODE_ENV === 'development') {
      return null;
    }
    return event;
  },
});

export default Sentry;