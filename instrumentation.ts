/**
 * Next.js Instrumentation File
 * This file is used to configure monitoring and observability tools
 */

export async function register() {
  // Initialize Sentry for server-side monitoring
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    await import('./sentry.server.config');
  }

  // Initialize Sentry for edge runtime
  if (process.env.NEXT_RUNTIME === 'edge') {
    await import('./sentry.edge.config');
  }
}