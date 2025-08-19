// src/app/api/logs/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const logEntry = await request.json();
    
    // Ajouter des métadonnées de la requête
    const enrichedLog = {
      ...logEntry,
      userAgent: request.headers.get('user-agent'),
      ip: request.ip || 'unknown',
      referer: request.headers.get('referer'),
    };

    // En production, envoyer vers un service de logging
    // comme Winston, Pino, ou un service cloud
    console.log('[LOG]', JSON.stringify(enrichedLog));
    
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Erreur lors de l\'enregistrement du log:', error);
    
    return NextResponse.json(
      { error: 'Erreur interne' },
      { status: 500 }
    );
  }
}