# Monitoring Implementation Examples

This document provides examples of how to use the comprehensive monitoring features implemented for La Vida Luca.

## Overview

The monitoring system includes:
- **Error Tracking**: Comprehensive error boundaries and error reporting
- **Performance Monitoring**: Track page loads, API calls, and user interactions
- **Custom Metrics**: Application-specific metrics collection
- **Structured Logging**: Enhanced logging with Sentry integration
- **User Tracking**: Track user sessions and behavior patterns

## Quick Start Examples

### 1. Error Boundary Usage

```tsx
import ErrorBoundary, { withErrorBoundary, useErrorHandler } from '@/components/ErrorBoundary';

// Basic usage - wrap any component
function MyPage() {
  return (
    <ErrorBoundary>
      <SomeComponent />
    </ErrorBoundary>
  );
}

// Using HOC wrapper
const SafeComponent = withErrorBoundary(SomeComponent);

// Manual error reporting
function MyComponent() {
  const { reportError } = useErrorHandler();
  
  const handleClick = async () => {
    try {
      await riskyOperation();
    } catch (error) {
      reportError(error as Error, { 
        component: 'MyComponent',
        action: 'handleClick' 
      });
    }
  };
  
  return <button onClick={handleClick}>Action</button>;
}
```

### 2. Metrics Tracking

```tsx
import { metrics, businessMetrics } from '@/monitoring/metrics';

// Track page views
businessMetrics.trackPageView('/contact', 1250);

// Track user interactions
businessMetrics.trackUserAction('click', 'submit-button', {
  formName: 'contact-form',
  userId: 'user-123'
});

// Track custom metrics
metrics.increment('api.errors', 1, { endpoint: '/api/users' });
metrics.timing('page.render', 850, { page: 'home' });
metrics.gauge('memory.usage', 75, 'percent');

// Track API calls
businessMetrics.trackApiCall('/api/users', 'GET', 250, 200);

// Business-specific tracking
businessMetrics.trackContactFormSubmission(true);
businessMetrics.trackCatalogueView('vegetables');
businessMetrics.trackJoinFormInteraction('personal-info');

// Performance timing wrapper
const result = metrics.timeFunction('expensive-operation', () => {
  // Expensive computation
  return computeResult();
}, { component: 'dashboard' });

// Async performance timing
const data = await metrics.timeAsyncFunction('api-call', async () => {
  return await fetch('/api/data').then(r => r.json());
}, { endpoint: '/api/data' });
```

### 3. Enhanced Logging

```tsx
import { logger, logUtils } from '@/monitoring/logger';

// Basic logging
logger.info('User logged in', { userId: 'user-123' }, 'auth');
logger.warn('Rate limit approaching', { requests: 95, limit: 100 }, 'api');
logger.error('Database connection failed', { 
  host: 'db.example.com',
  retries: 3 
}, 'database');

// Exception logging
try {
  await riskyOperation();
} catch (error) {
  logger.exception(error as Error, { 
    operation: 'user-creation',
    userId: 'user-123' 
  }, 'user-service');
}

// Performance logging
logger.timing({
  name: 'page.load',
  duration: 1250,
  metadata: { page: '/dashboard', cached: false },
  component: 'performance'
});

// User action logging
logger.userAction('form-submit', {
  formName: 'contact',
  fields: ['name', 'email', 'message']
}, 'contact-form');

// API call logging
logger.apiCall('/api/users', 'POST', 300, 201, {
  requestSize: 1024,
  responseSize: 512
});

// Security event logging
logger.securityEvent('login-attempt', {
  ip: '192.168.1.1',
  success: false,
  reason: 'invalid-password'
}, 'auth');

// Business event logging
logger.businessEvent('subscription-created', {
  planType: 'premium',
  userId: 'user-123',
  amount: 29.99
});

// Form event tracking
logger.formEvent('contact-form', 'complete', {
  duration: 45000,
  fields: 3,
  errors: 0
});

// Navigation tracking
logger.navigation('/home', '/contact', 250);

// User context management
logger.setUser({ 
  id: 'user-123', 
  email: 'user@example.com', 
  role: 'admin' 
});
logger.clearUser();

// Performance wrapper utilities
const optimizedFunction = logUtils.withPerformanceLogging(
  expensiveFunction,
  'expensive-operation',
  'computation'
);

const optimizedAsyncFunction = logUtils.withAsyncPerformanceLogging(
  asyncFunction,
  'async-operation',
  'api'
);

// Logged fetch wrapper
const loggedFetch = logUtils.createLoggedFetch('https://api.example.com');
const response = await loggedFetch('/users', {
  method: 'POST',
  body: JSON.stringify({ name: 'John' })
});
```

### 4. Sentry Integration

```tsx
import { 
  setUser, 
  clearUser, 
  setContext, 
  setTag, 
  addBreadcrumb, 
  captureException, 
  captureMessage 
} from '@/monitoring/sentry';

// User tracking
setUser({
  id: 'user-123',
  email: 'user@example.com',
  username: 'johndoe',
  role: 'admin'
});

// Clear user on logout
clearUser();

// Set custom context
setContext('business', {
  subscriptionType: 'premium',
  feature: 'advanced-dashboard'
});

// Set tags for filtering
setTag('feature', 'contact-form');
setTags({
  environment: 'production',
  version: '2.1.0',
  feature: 'user-management'
});

// Add breadcrumbs for debugging
addBreadcrumb({
  message: 'User started form',
  category: 'user-action',
  level: 'info',
  data: { formName: 'contact', step: 1 }
});

// Capture exceptions with context
try {
  await criticalOperation();
} catch (error) {
  captureException(error as Error, {
    operation: 'critical-operation',
    userId: 'user-123',
    timestamp: Date.now()
  });
}

// Capture messages
captureMessage('User completed onboarding', 'info', {
  userId: 'user-123',
  duration: 45000,
  steps: 5
});
```

### 5. React Component Integration

```tsx
import { useEffect } from 'react';
import { businessMetrics } from '@/monitoring/metrics';
import { logger } from '@/monitoring/logger';
import ErrorBoundary from '@/components/ErrorBoundary';

function ContactPage() {
  useEffect(() => {
    // Track page view
    const startTime = performance.now();
    businessMetrics.trackPageView('/contact');
    
    return () => {
      // Track page exit
      const duration = performance.now() - startTime;
      logger.timing({
        name: 'page.view.duration',
        duration,
        metadata: { page: '/contact' },
        component: 'contact-page'
      });
    };
  }, []);

  const handleFormSubmit = async (formData: FormData) => {
    logger.formEvent('contact-form', 'start');
    
    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        body: formData
      });
      
      if (response.ok) {
        businessMetrics.trackContactFormSubmission(true);
        logger.formEvent('contact-form', 'complete', {
          success: true
        });
      } else {
        throw new Error(`HTTP ${response.status}`);
      }
    } catch (error) {
      businessMetrics.trackContactFormSubmission(false);
      logger.formEvent('contact-form', 'error', {
        error: error instanceof Error ? error.message : 'Unknown error'
      });
      throw error;
    }
  };

  return (
    <ErrorBoundary>
      <div>
        <h1>Contact</h1>
        <ContactForm onSubmit={handleFormSubmit} />
      </div>
    </ErrorBoundary>
  );
}
```

### 6. API Route Monitoring

```tsx
// pages/api/contact.ts or app/api/contact/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { logger } from '@/monitoring/logger';
import { captureException } from '@/monitoring/sentry';

export async function POST(request: NextRequest) {
  const startTime = performance.now();
  
  try {
    const data = await request.json();
    
    logger.info('Contact form submission received', {
      hasName: !!data.name,
      hasEmail: !!data.email,
      hasMessage: !!data.message
    }, 'contact-api');
    
    // Process the contact form
    await processContactForm(data);
    
    const duration = performance.now() - startTime;
    logger.apiCall('/api/contact', 'POST', duration, 200, {
      success: true
    });
    
    return NextResponse.json({ success: true });
    
  } catch (error) {
    const duration = performance.now() - startTime;
    
    logger.apiCall('/api/contact', 'POST', duration, 500, {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    });
    
    captureException(error as Error, {
      endpoint: '/api/contact',
      method: 'POST'
    });
    
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

### 7. Custom Hooks for Monitoring

```tsx
import { useEffect, useCallback } from 'react';
import { businessMetrics } from '@/monitoring/metrics';
import { logger } from '@/monitoring/logger';

// Custom hook for page tracking
export function usePageTracking(pageName: string) {
  useEffect(() => {
    const startTime = performance.now();
    businessMetrics.trackPageView(pageName);
    
    return () => {
      const duration = performance.now() - startTime;
      businessMetrics.trackPerformance('page_duration', duration, pageName);
    };
  }, [pageName]);
}

// Custom hook for user action tracking
export function useActionTracking() {
  return useCallback((action: string, component: string, metadata?: Record<string, any>) => {
    businessMetrics.trackUserAction(action, component, metadata);
    logger.userAction(action, metadata, component);
  }, []);
}

// Custom hook for form tracking
export function useFormTracking(formName: string) {
  const trackFormEvent = useCallback((event: 'start' | 'complete' | 'error' | 'abandon', metadata?: Record<string, any>) => {
    businessMetrics.trackFormInteraction(formName, event);
    logger.formEvent(formName, event, metadata);
  }, [formName]);
  
  return { trackFormEvent };
}

// Usage in components
function MyPage() {
  usePageTracking('/my-page');
  const trackAction = useActionTracking();
  const { trackFormEvent } = useFormTracking('signup');
  
  const handleButtonClick = () => {
    trackAction('click', 'signup-button', { location: 'header' });
  };
  
  const handleFormStart = () => {
    trackFormEvent('start');
  };
  
  // ... rest of component
}
```

## Environment Setup

Make sure to configure these environment variables:

```env
# .env.local
NEXT_PUBLIC_SENTRY_DSN=https://your-dsn@sentry.io/project-id
NEXT_PUBLIC_APP_VERSION=1.0.0
NEXT_PUBLIC_SITE_URL=https://your-domain.com

# For development
NODE_ENV=development

# For production
NODE_ENV=production
```

## Best Practices

1. **Error Boundaries**: Wrap major sections of your app with error boundaries
2. **Metrics**: Track business-critical events and performance metrics
3. **Logging**: Use structured logging with appropriate levels
4. **User Context**: Set user context early in the authentication flow
5. **Performance**: Monitor critical user journeys and API endpoints
6. **Testing**: Mock Sentry in tests to avoid sending test data

## Monitoring Dashboard

Access your monitoring data through:
- **Sentry Dashboard**: Error tracking, performance monitoring, user sessions
- **Custom Metrics**: Available through Sentry's measurements and custom events
- **Logs**: Structured logs available in Sentry breadcrumbs and messages

This comprehensive monitoring setup provides complete visibility into your application's health, performance, and user behavior.