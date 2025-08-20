/** @type {import('next').NextConfig} */
const { withSentryConfig } = require('@sentry/nextjs');
const { InjectManifest } = require('workbox-webpack-plugin');
const path = require('path');

const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.plugins.push(
        new InjectManifest({
          swSrc: path.join(__dirname, 'src/sw.ts'),
          swDest: path.join(config.output.path || '.next', 'sw.js'),
          additionalManifestEntries: [
            { url: '/', revision: null },
            { url: '/catalogue/', revision: null },
            { url: '/contact/', revision: null },
            { url: '/rejoindre/', revision: null },
          ]
        })
      );
    }
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
