/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    // Remove deprecated appDir option
  },
  // Remove output: 'export' for proper Vercel deployment
  trailingSlash: true,
  images: {
    unoptimized: true
  }
}

module.exports = nextConfig
