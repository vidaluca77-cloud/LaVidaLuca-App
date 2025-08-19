import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Basic health check
    const healthData = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      environment: process.env.NODE_ENV || 'development',
      services: {
        database: await checkDatabase(),
        ia_api: await checkIAAPI()
      }
    };

    return NextResponse.json(healthData);
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        error: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 503 }
    );
  }
}

async function checkDatabase() {
  try {
    // Check Supabase connection
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    if (!supabaseUrl) {
      return { status: 'unknown', message: 'Supabase URL not configured' };
    }

    const response = await fetch(`${supabaseUrl}/rest/v1/`, {
      method: 'HEAD',
      headers: {
        'apikey': process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '',
        'Authorization': `Bearer ${process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''}`
      },
      signal: AbortSignal.timeout(5000)
    });

    return {
      status: response.ok ? 'healthy' : 'unhealthy',
      responseTime: response.headers.get('X-Response-Time') || 'unknown'
    };
  } catch (error) {
    return {
      status: 'unhealthy',
      error: error instanceof Error ? error.message : 'Connection failed'
    };
  }
}

async function checkIAAPI() {
  try {
    const iaApiUrl = process.env.NEXT_PUBLIC_IA_API_URL;
    if (!iaApiUrl) {
      return { status: 'unknown', message: 'IA API URL not configured' };
    }

    const response = await fetch(`${iaApiUrl}/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(5000)
    });

    if (response.ok) {
      const data = await response.json();
      return {
        status: data.status === 'healthy' ? 'healthy' : 'unhealthy',
        apiVersion: data.version || 'unknown'
      };
    } else {
      return {
        status: 'unhealthy',
        statusCode: response.status
      };
    }
  } catch (error) {
    return {
      status: 'unreachable',
      error: error instanceof Error ? error.message : 'Connection failed'
    };
  }
}