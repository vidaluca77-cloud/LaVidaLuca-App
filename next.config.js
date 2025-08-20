/** @type {import('next').NextConfig} */
const { withSentryConfig } = require('@sentry/nextjs');

const nextConfig = {
  // Removed output: 'export' to enable API routes
  trailingSlash: true,
  images: {
    unoptimized: true
  }
}

const sentryWebpackPluginOptions = {
  // For all available options, see:
  // https://github.com/getsentry/sentry-webpack-plugin#options
  silent: true,
  org: process.env.SENTRY_ORG,
  project: process.env.SENTRY_PROJECT,
}

// Export configuration with Sentry
module.exports = withSentryConfig(nextConfig, sentryWebpackPluginOptions)
