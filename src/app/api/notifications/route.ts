import { NextRequest, NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

/**
 * API route for handling notification subscriptions and sending notifications
 */

// Store push subscriptions (in production, use a proper database)
const subscriptions: Array<{
  id: string;
  endpoint: string;
  keys: {
    p256dh: string;
    auth: string;
  };
  userId?: string;
  createdAt: number;
}> = [];

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { endpoint, keys, userId } = body;

    if (!endpoint || !keys || !keys.p256dh || !keys.auth) {
      return NextResponse.json(
        { error: 'Missing required subscription data' },
        { status: 400 }
      );
    }

    // Check if subscription already exists
    const existingIndex = subscriptions.findIndex(sub => sub.endpoint === endpoint);
    
    const subscription = {
      id: crypto.randomUUID(),
      endpoint,
      keys,
      userId,
      createdAt: Date.now(),
    };

    if (existingIndex >= 0) {
      // Update existing subscription
      subscriptions[existingIndex] = subscription;
      logger.info('Push subscription updated', { subscriptionId: subscription.id, userId });
    } else {
      // Add new subscription
      subscriptions.push(subscription);
      logger.info('Push subscription added', { subscriptionId: subscription.id, userId });
    }

    return NextResponse.json({ 
      success: true, 
      subscriptionId: subscription.id,
      message: 'Subscription saved successfully' 
    });

  } catch (error) {
    logger.error('Error handling push subscription', { error });
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const userId = searchParams.get('userId');

    let filteredSubscriptions = [...subscriptions];

    if (userId) {
      filteredSubscriptions = filteredSubscriptions.filter(sub => sub.userId === userId);
    }

    return NextResponse.json({
      subscriptions: filteredSubscriptions.map(sub => ({
        id: sub.id,
        userId: sub.userId,
        createdAt: sub.createdAt,
        // Don't expose sensitive keys
      })),
      total: filteredSubscriptions.length,
    });

  } catch (error) {
    logger.error('Error retrieving subscriptions', { error });
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const endpoint = searchParams.get('endpoint');
    const subscriptionId = searchParams.get('id');

    if (!endpoint && !subscriptionId) {
      return NextResponse.json(
        { error: 'Missing endpoint or subscription ID' },
        { status: 400 }
      );
    }

    let removedCount = 0;

    if (subscriptionId) {
      const index = subscriptions.findIndex(sub => sub.id === subscriptionId);
      if (index >= 0) {
        subscriptions.splice(index, 1);
        removedCount = 1;
      }
    } else if (endpoint) {
      const index = subscriptions.findIndex(sub => sub.endpoint === endpoint);
      if (index >= 0) {
        subscriptions.splice(index, 1);
        removedCount = 1;
      }
    }

    logger.info('Push subscription removed', { endpoint, subscriptionId, removedCount });

    return NextResponse.json({ 
      success: true, 
      removedCount,
      message: 'Subscription removed successfully' 
    });

  } catch (error) {
    logger.error('Error removing push subscription', { error });
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}