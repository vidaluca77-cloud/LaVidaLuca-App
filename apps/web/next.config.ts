import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Output configuration
  output: 'standalone',
  
  // Image optimization
  images: {
    domains: ['lavidaluca-backend.onrender.com'],
    formats: ['image/webp', 'image/avif'],
  },
  
  // Security headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()',
          },
        ],
      },
    ];
  },
  
  // Environment-specific redirects
  async redirects() {
    return [
      // Add any production redirects here
    ];
  },
  
  // Environment variables validation
  env: {
    NEXT_PUBLIC_ENV: process.env.NEXT_PUBLIC_ENV,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME,
  },
  
  // Webpack configuration for production
  webpack: (config, { dev, isServer }) => {
    // Production-specific webpack optimizations
    if (!dev && !isServer) {
      config.optimization.splitChunks.cacheGroups = {
        ...config.optimization.splitChunks.cacheGroups,
        default: false,
        vendors: false,
        framework: {
          chunks: 'all',
          name: 'framework',
          test: /(?<!node_modules.*)[\\/]node_modules[\\/](react|react-dom|scheduler|prop-types|use-subscription)[\\/]/,
          priority: 40,
          enforce: true,
        },
        lib: {
          test(module: any) {
            return module.size() > 160000 &&
              /node_modules[/\\]/.test(module.identifier());
          },
          name(module: any) {
            const hash = require('crypto').createHash('sha1');
            hash.update(module.identifier());
            return hash.digest('hex').substring(0, 8);
          },
          priority: 30,
          minChunks: 1,
          reuseExistingChunk: true,
        },
        commons: {
          name: 'commons',
          minChunks: 2,
          priority: 20,
        },
        shared: {
          name: 'shared',
          minChunks: 2,
          priority: 10,
          reuseExistingChunk: true,
        },
      };
    }
    
    return config;
  },
  
  // Production-specific compiler options
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
  
  // Strict mode for better production performance
  reactStrictMode: true,
  
  // Enable experimental features for production
  experimental: {
    optimizeCss: true,
    scrollRestoration: true,
  },
  
  // PWA and offline support
  generateEtags: false,
  
  // Compression
  compress: true,
  
  // Power optimizations
  poweredByHeader: false,
};

export default nextConfig;
