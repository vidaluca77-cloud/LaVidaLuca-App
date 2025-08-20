import { NextRequest, NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

export async function POST(request: NextRequest) {
  try {
    const subscription = await request.json();
    
    // Validate subscription format
    if (!subscription.endpoint || !subscription.keys?.p256dh || !subscription.keys?.auth) {
      return NextResponse.json(
        { error: 'Invalid subscription format' },
        { status: 400 }
      );
    }

    // Log the subscription (in a real app, you'd store this in a database)
    logger.info('Push notification subscription received', {
      endpoint: subscription.endpoint,
      hasKeys: !!subscription.keys
    });

    // Here you would typically:
    // 1. Store the subscription in your database
    // 2. Associate it with the user
    // 3. Possibly send a welcome notification

    // For now, we'll just log it and return success
    console.log('New push subscription:', {
      endpoint: subscription.endpoint.substring(0, 50) + '...',
      p256dh: subscription.keys.p256dh.substring(0, 20) + '...',
      auth: subscription.keys.auth.substring(0, 20) + '...'
    });

    return NextResponse.json(
      { message: 'Subscription saved successfully' },
      { status: 200 }
    );
  } catch (error) {
    logger.error('Error saving push subscription', { error });
    
    return NextResponse.json(
      { error: 'Failed to save subscription' },
      { status: 500 }
    );
  }
}