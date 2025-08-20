import { NextRequest, NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

export async function POST(request: NextRequest) {
  try {
    // Log the unsubscription (in a real app, you'd remove from database)
    logger.info('Push notification unsubscription received');

    // Here you would typically:
    // 1. Remove the subscription from your database
    // 2. Clean up any user associations

    console.log('Push subscription removed');

    return NextResponse.json(
      { message: 'Unsubscribed successfully' },
      { status: 200 }
    );
  } catch (error) {
    logger.error('Error unsubscribing from push notifications', { error });
    
    return NextResponse.json(
      { error: 'Failed to unsubscribe' },
      { status: 500 }
    );
  }
}