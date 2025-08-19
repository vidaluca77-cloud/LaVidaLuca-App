/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  swcMinify: true,
  poweredByHeader: false,
  compress: true,
}

module.exports = nextConfig
