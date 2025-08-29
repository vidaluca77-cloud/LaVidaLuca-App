/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configuration for Netlify deployment
  trailingSlash: true,
  
  // Image optimization for Netlify
  images: {
    domains: ['localhost', 'lavidaluca.fr'],
    unoptimized: true, // Required for static export
  },
  
  // Environment variables
  env: {
    NEXT_PUBLIC_APP_VERSION: process.env.npm_package_version || '1.0.0',
  },
  
  // Disable server-side features for static deployment
  output: 'export',
  
  // Ensure proper paths for static deployment
  assetPrefix: process.env.NODE_ENV === 'production' ? '' : '',
  
  // Disable features not supported in static export
  eslint: {
    ignoreDuringBuilds: true,
  },
};

module.exports = nextConfig;
