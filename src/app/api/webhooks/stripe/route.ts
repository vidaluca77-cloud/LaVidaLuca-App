import { NextRequest, NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

/**
 * Stripe Webhook Handler for La Vida Luca App
 * Handles subscription events, payment confirmations, and other Stripe events
 */

const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET;

export async function POST(request: NextRequest) {
  try {
    if (!STRIPE_WEBHOOK_SECRET) {
      logger.error('Stripe webhook secret not configured');
      return NextResponse.json({ error: 'Webhook not configured' }, { status: 500 });
    }

    const body = await request.text();
    const signature = request.headers.get('stripe-signature');

    if (!signature) {
      logger.error('Missing Stripe signature');
      return NextResponse.json({ error: 'Missing signature' }, { status: 400 });
    }

    // In a real implementation, verify the webhook signature with Stripe
    // const event = stripe.webhooks.constructEvent(body, signature, STRIPE_WEBHOOK_SECRET);
    
    // For now, parse the event directly (not secure for production)
    const event = JSON.parse(body);

    logger.info('Stripe webhook received', { 
      type: event.type, 
      id: event.id 
    });

    // Handle different event types
    switch (event.type) {
      case 'payment_intent.succeeded':
        await handlePaymentSuccess(event.data.object);
        break;

      case 'payment_intent.payment_failed':
        await handlePaymentFailed(event.data.object);
        break;

      case 'customer.subscription.created':
        await handleSubscriptionCreated(event.data.object);
        break;

      case 'customer.subscription.updated':
        await handleSubscriptionUpdated(event.data.object);
        break;

      case 'customer.subscription.deleted':
        await handleSubscriptionCanceled(event.data.object);
        break;

      case 'invoice.payment_succeeded':
        await handleInvoicePaymentSuccess(event.data.object);
        break;

      case 'invoice.payment_failed':
        await handleInvoicePaymentFailed(event.data.object);
        break;

      case 'checkout.session.completed':
        await handleCheckoutSessionCompleted(event.data.object);
        break;

      default:
        logger.info('Unhandled Stripe webhook event', { type: event.type });
    }

    return NextResponse.json({ received: true });

  } catch (error) {
    logger.error('Error processing Stripe webhook', { error });
    return NextResponse.json(
      { error: 'Webhook processing failed' },
      { status: 500 }
    );
  }
}

/**
 * Handle successful payment
 */
async function handlePaymentSuccess(paymentIntent: any) {
  logger.info('Payment succeeded', {
    paymentIntentId: paymentIntent.id,
    amount: paymentIntent.amount,
    currency: paymentIntent.currency,
    customerId: paymentIntent.customer,
  });

  // Update user payment status
  // Send confirmation notification
  // Update analytics
  
  // Example: Send push notification
  await sendNotificationToUser(paymentIntent.customer, {
    title: 'Paiement confirmé',
    body: `Votre paiement de ${formatAmount(paymentIntent.amount, paymentIntent.currency)} a été traité avec succès.`,
    data: {
      type: 'payment_success',
      paymentIntentId: paymentIntent.id,
    },
  });
}

/**
 * Handle failed payment
 */
async function handlePaymentFailed(paymentIntent: any) {
  logger.warn('Payment failed', {
    paymentIntentId: paymentIntent.id,
    amount: paymentIntent.amount,
    currency: paymentIntent.currency,
    customerId: paymentIntent.customer,
    lastPaymentError: paymentIntent.last_payment_error,
  });

  // Notify user of payment failure
  await sendNotificationToUser(paymentIntent.customer, {
    title: 'Échec du paiement',
    body: 'Votre paiement n\'a pas pu être traité. Veuillez vérifier vos informations de paiement.',
    data: {
      type: 'payment_failed',
      paymentIntentId: paymentIntent.id,
    },
  });
}

/**
 * Handle subscription creation
 */
async function handleSubscriptionCreated(subscription: any) {
  logger.info('Subscription created', {
    subscriptionId: subscription.id,
    customerId: subscription.customer,
    status: subscription.status,
    planId: subscription.items.data[0]?.price?.id,
  });

  // Update user subscription status
  // Send welcome notification
  await sendNotificationToUser(subscription.customer, {
    title: 'Abonnement activé',
    body: 'Bienvenue ! Votre abonnement La Vida Luca est maintenant actif.',
    data: {
      type: 'subscription_created',
      subscriptionId: subscription.id,
    },
  });
}

/**
 * Handle subscription update
 */
async function handleSubscriptionUpdated(subscription: any) {
  logger.info('Subscription updated', {
    subscriptionId: subscription.id,
    customerId: subscription.customer,
    status: subscription.status,
    planId: subscription.items.data[0]?.price?.id,
  });

  // Update user subscription status
  // Send update notification if needed
}

/**
 * Handle subscription cancellation
 */
async function handleSubscriptionCanceled(subscription: any) {
  logger.info('Subscription canceled', {
    subscriptionId: subscription.id,
    customerId: subscription.customer,
    canceledAt: subscription.canceled_at,
  });

  // Update user subscription status
  // Send cancellation confirmation
  await sendNotificationToUser(subscription.customer, {
    title: 'Abonnement annulé',
    body: 'Votre abonnement La Vida Luca a été annulé. Vous conservez l\'accès jusqu\'à la fin de votre période de facturation.',
    data: {
      type: 'subscription_canceled',
      subscriptionId: subscription.id,
    },
  });
}

/**
 * Handle successful invoice payment
 */
async function handleInvoicePaymentSuccess(invoice: any) {
  logger.info('Invoice payment succeeded', {
    invoiceId: invoice.id,
    customerId: invoice.customer,
    amount: invoice.amount_paid,
    subscriptionId: invoice.subscription,
  });

  // Update payment records
  // Send payment confirmation
}

/**
 * Handle failed invoice payment
 */
async function handleInvoicePaymentFailed(invoice: any) {
  logger.warn('Invoice payment failed', {
    invoiceId: invoice.id,
    customerId: invoice.customer,
    amount: invoice.amount_due,
    subscriptionId: invoice.subscription,
  });

  // Handle failed payment
  // Send notification to user
  await sendNotificationToUser(invoice.customer, {
    title: 'Échec du renouvellement',
    body: 'Le renouvellement de votre abonnement a échoué. Veuillez mettre à jour vos informations de paiement.',
    data: {
      type: 'invoice_payment_failed',
      invoiceId: invoice.id,
    },
  });
}

/**
 * Handle completed checkout session
 */
async function handleCheckoutSessionCompleted(session: any) {
  logger.info('Checkout session completed', {
    sessionId: session.id,
    customerId: session.customer,
    mode: session.mode,
    amount: session.amount_total,
  });

  // Process successful checkout
  // Update user access
  // Send confirmation
}

/**
 * Send notification to user
 */
async function sendNotificationToUser(customerId: string, notification: any) {
  try {
    // In a real implementation, you would:
    // 1. Look up user by Stripe customer ID
    // 2. Get their push notification subscriptions
    // 3. Send push notifications
    
    logger.info('Sending notification to user', {
      customerId,
      notification: notification.title,
    });

    // For now, just log the notification
    // In production, integrate with your notification system

  } catch (error) {
    logger.error('Error sending notification to user', { error, customerId });
  }
}

/**
 * Format amount for display
 */
function formatAmount(amount: number, currency: string): string {
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: currency.toUpperCase(),
  }).format(amount / 100); // Stripe amounts are in cents
}