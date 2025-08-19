import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Perform basic health checks
    const healthStatus = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: 'la-vida-luca-frontend',
      version: '1.0.0',
      environment: process.env.NODE_ENV || 'development',
      checks: {
        database: await checkDatabase(),
        external_apis: await checkExternalAPIs(),
      }
    };

    // If any critical check fails, return 503
    const hasFailures = Object.values(healthStatus.checks).some(check => !check.healthy);
    
    return NextResponse.json(healthStatus, {
      status: hasFailures ? 503 : 200,
      headers: {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
      }
    });
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        service: 'la-vida-luca-frontend',
        error: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 503 }
    );
  }
}

async function checkDatabase() {
  try {
    if (!process.env.NEXT_PUBLIC_SUPABASE_URL) {
      return { healthy: false, message: 'Supabase URL not configured' };
    }

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_SUPABASE_URL}/rest/v1/`,
      {
        headers: {
          'apikey': process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '',
          'Authorization': `Bearer ${process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''}`
        }
      }
    );

    return {
      healthy: response.ok,
      message: response.ok ? 'Database connection OK' : `Database error: ${response.status}`,
      response_time: Date.now()
    };
  } catch (error) {
    return {
      healthy: false,
      message: `Database connection failed: ${error instanceof Error ? error.message : 'Unknown error'}`
    };
  }
}

async function checkExternalAPIs() {
  try {
    if (!process.env.NEXT_PUBLIC_IA_API_URL) {
      return { healthy: false, message: 'IA API URL not configured' };
    }

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_IA_API_URL}/health`,
      { method: 'GET' }
    );

    return {
      healthy: response.ok,
      message: response.ok ? 'IA API connection OK' : `IA API error: ${response.status}`,
      response_time: Date.now()
    };
  } catch (error) {
    return {
      healthy: false,
      message: `IA API connection failed: ${error instanceof Error ? error.message : 'Unknown error'}`
    };
  }
}