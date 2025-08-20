/** @type {import('next').NextConfig} */
const nextConfig = {
  // Basic configuration for compatibility
  output: 'standalone',
  
  // Image optimization
  images: {
    domains: ['localhost', 'lavidaluca.fr'],
  },
  
  // Environment variables
  env: {
    NEXT_PUBLIC_APP_VERSION: process.env.npm_package_version || '1.0.0',
  },
};

module.exports = nextConfig;
