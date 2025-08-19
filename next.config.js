/** @type {import('next').NextConfig} */
const nextConfig = {
  // Remove static export for Vercel deployment to enable API routes
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  // Enable Vercel analytics
  experimental: {
    // appDir is now stable, no need to enable experimentally
  },
  // Environment variables that should be available to the client
  env: {
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    NEXT_PUBLIC_IA_API_URL: process.env.NEXT_PUBLIC_IA_API_URL,
    NEXT_PUBLIC_CONTACT_EMAIL: process.env.NEXT_PUBLIC_CONTACT_EMAIL,
    NEXT_PUBLIC_CONTACT_PHONE: process.env.NEXT_PUBLIC_CONTACT_PHONE,
  }
}

module.exports = nextConfig
