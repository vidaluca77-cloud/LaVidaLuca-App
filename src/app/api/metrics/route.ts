// src/app/api/metrics/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Valider les données reçues
    if (!body.type) {
      return NextResponse.json(
        { error: 'Type de métrique requis' },
        { status: 400 }
      );
    }

    // Log de la métrique pour debugging
    logger.debug('Métrique reçue', {
      type: body.type,
      timestamp: body.timestamp || new Date().toISOString(),
      userAgent: request.headers.get('user-agent'),
      ip: request.ip || 'unknown'
    });

    // En production, ici on enverrait vers un service de métriques
    // comme Datadog, New Relic, ou un service custom
    
    return NextResponse.json({ success: true });
  } catch (error) {
    logger.error('Erreur lors de l\'enregistrement de métrique', error as Error);
    
    return NextResponse.json(
      { error: 'Erreur interne' },
      { status: 500 }
    );
  }
}

// GET pour récupérer des métriques (pour debug)
export async function GET(request: NextRequest) {
  // En production, cet endpoint serait sécurisé
  if (process.env.NODE_ENV === 'production') {
    return NextResponse.json({ error: 'Non autorisé' }, { status: 403 });
  }

  // Retourner des métriques factices pour le développement
  return NextResponse.json({
    timestamp: new Date().toISOString(),
    metrics: {
      page_views: Math.floor(Math.random() * 1000),
      unique_visitors: Math.floor(Math.random() * 100),
      api_calls: Math.floor(Math.random() * 500),
      errors: Math.floor(Math.random() * 10),
    }
  });
}