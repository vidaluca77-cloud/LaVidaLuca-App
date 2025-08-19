import { NextResponse } from 'next/server';

export async function GET() {
  const metrics = {
    timestamp: new Date().toISOString(),
    service: 'la-vida-luca-frontend',
    version: '1.0.0',
    environment: process.env.NODE_ENV || 'development',
    performance: {
      uptime: process.uptime ? process.uptime() : null,
      memory: process.memoryUsage ? process.memoryUsage() : null,
      node_version: process.version || null,
    },
    features: {
      analytics_enabled: process.env.NEXT_PUBLIC_ENABLE_ANALYTICS === 'true',
      error_tracking_enabled: process.env.NEXT_PUBLIC_ENABLE_ERROR_TRACKING === 'true',
      maintenance_mode: process.env.NEXT_PUBLIC_MAINTENANCE_MODE === 'true',
    },
    database: {
      configured: !!process.env.NEXT_PUBLIC_SUPABASE_URL,
      url_set: !!process.env.NEXT_PUBLIC_SUPABASE_URL,
      key_set: !!process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    },
    external_services: {
      ia_api_configured: !!process.env.NEXT_PUBLIC_IA_API_URL,
      ia_api_url: process.env.NEXT_PUBLIC_IA_API_URL ? 'configured' : 'missing',
    }
  };

  return NextResponse.json(metrics, {
    headers: {
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0'
    }
  });
}