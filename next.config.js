import { withSentryConfig } from "@sentry/nextjs";

/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    // Removed deprecated appDir option
  },
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  }
}

// Configuration Sentry
const sentryWebpackPluginOptions = {
  // Pour plus d'options voir https://github.com/getsentry/sentry-webpack-plugin#options
  org: process.env.SENTRY_ORG,
  project: process.env.SENTRY_PROJECT,
  silent: true, // Supprime les logs lors du build
  widenClientFileUpload: true, // Upload d'un range plus large de fichiers client
  hideSourceMaps: true, // Cache les source maps des bundles finaux
  disableLogger: true, // Supprime automatiquement les logs Sentry en production
  automaticVercelMonitors: true, // Active les monitors Vercel automatiques
};

export default withSentryConfig(nextConfig, sentryWebpackPluginOptions);
