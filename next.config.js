/** @type {import('next').NextConfig} */
const { withSentryConfig } = require('@sentry/nextjs');

const nextConfig = {
  // Remove static export for Vercel deployment to enable API routes and server features
  // output: 'export', 
  // trailingSlash: true,
  
  // Image optimization configuration
  images: {
    // For Vercel deployment, we can use the optimized image service
    domains: ['lavidaluca.fr', 'lavidaluca.vercel.app'],
    formats: ['image/webp', 'image/avif'],
    // unoptimized: true // Remove this to enable Vercel's image optimization
  },
  
  // Compression and performance
  compress: true,
  poweredByHeader: false,
  
  // Headers for security and performance
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on'
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload'
          },
          {
            key: 'Server',
            value: 'vercel'
          }
        ]
      }
    ];
  },
  
  // Redirects for better SEO
  async redirects() {
    return [
      {
        source: '/home',
        destination: '/',
        permanent: true,
      },
    ];
  },
  
  // Webpack optimizations
  webpack: (config, { dev, isServer }) => {
    // Optimize bundle in production
    if (!dev && !isServer) {
      config.resolve.alias = {
        ...config.resolve.alias,
        // Optimize lodash imports
        'lodash': 'lodash-es'
      };
    }
    return config;
  },
  
  // Experimental features for better performance
  experimental: {
    // optimizeCss: true, // Disabled due to critters dependency issue
    scrollRestoration: true,
  }
}

const sentryWebpackPluginOptions = {
  // For all available options, see:
  // https://github.com/getsentry/sentry-webpack-plugin#options
  silent: true,
  org: process.env.SENTRY_ORG,
  project: process.env.SENTRY_PROJECT,
  hideSourceMaps: true,
}

// Export configuration with Sentry
module.exports = withSentryConfig(nextConfig, sentryWebpackPluginOptions)
