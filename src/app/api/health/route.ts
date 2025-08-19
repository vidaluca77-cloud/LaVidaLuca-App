// src/app/api/health/route.ts
import { NextRequest, NextResponse } from 'next/server';

interface HealthCheckResult {
  status: 'healthy' | 'unhealthy' | 'degraded';
  timestamp: string;
  version: string;
  services: {
    database: 'healthy' | 'unhealthy';
    ai_api: 'healthy' | 'unhealthy';
    cache: 'healthy' | 'unhealthy';
  };
  uptime: number;
  memory?: {
    used: number;
    total: number;
  };
}

const startTime = Date.now();

export async function GET(request: NextRequest) {
  try {
    const healthCheck: HealthCheckResult = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: process.env.npm_package_version || '1.0.0',
      uptime: Date.now() - startTime,
      services: {
        database: await checkDatabase(),
        ai_api: await checkAiApi(),
        cache: await checkCache(),
      },
    };

    // Ajouter les métriques mémoire si disponibles
    if (typeof process !== 'undefined' && process.memoryUsage) {
      const memUsage = process.memoryUsage();
      healthCheck.memory = {
        used: memUsage.rss,
        total: memUsage.heapTotal,
      };
    }

    // Déterminer le status global
    const serviceStatuses = Object.values(healthCheck.services);
    if (serviceStatuses.some(status => status === 'unhealthy')) {
      healthCheck.status = 'degraded';
    }

    const status = healthCheck.status === 'healthy' ? 200 : 503;
    
    return NextResponse.json(healthCheck, { status });
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        error: 'Health check failed',
      },
      { status: 503 }
    );
  }
}

async function checkDatabase(): Promise<'healthy' | 'unhealthy'> {
  try {
    // En réalité, ici on ferait un ping vers Supabase
    // Pour l'instant, on simule une vérification
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    if (!supabaseUrl) return 'unhealthy';
    
    // Simple check - en production, on ferait une vraie requête
    return 'healthy';
  } catch {
    return 'unhealthy';
  }
}

async function checkAiApi(): Promise<'healthy' | 'unhealthy'> {
  try {
    const aiApiUrl = process.env.NEXT_PUBLIC_IA_API_URL;
    if (!aiApiUrl) return 'unhealthy';
    
    // En production, on ferait un ping vers l'API IA
    return 'healthy';
  } catch {
    return 'unhealthy';
  }
}

async function checkCache(): Promise<'healthy' | 'unhealthy'> {
  try {
    // Pour l'instant, pas de cache externe configuré
    return 'healthy';
  } catch {
    return 'unhealthy';
  }
}