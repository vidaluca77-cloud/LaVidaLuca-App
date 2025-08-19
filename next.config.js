/** @type {import('next').NextConfig} */
const { withSentryConfig } = require('@sentry/nextjs');

const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  // Exclude apps/web from build to avoid conflicts
  webpack: (config) => {
    config.watchOptions = {
      ...config.watchOptions,
      ignored: ['**/apps/web/**', '**/node_modules/**']
    };
    return config;
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
