/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    unoptimized: true
  },
  // Remove static export for Vercel deployment
  // output: 'export',
  // trailingSlash: true,
}

module.exports = nextConfig
