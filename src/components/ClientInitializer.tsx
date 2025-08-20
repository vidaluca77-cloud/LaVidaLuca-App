/**
 * Client-side initialization component
 * Handles service worker registration and other client-only features
 */

'use client';

import { useEffect } from 'react';
import { serviceWorkerManager } from '@/lib/serviceWorker';
import { cacheManager } from '@/lib/cache';
import { backgroundSyncManager } from '@/lib/backgroundSync';
import { logger } from '@/lib/logger';

export function ClientInitializer() {
  useEffect(() => {
    // Initialize client-side services
    const initializeServices = async () => {
      try {
        // Initialize cache manager
        await cacheManager.init();
        logger.info('Cache manager initialized');

        // Initialize service worker
        await serviceWorkerManager.init();
        logger.info('Service worker manager initialized');

        // Background sync manager is initialized automatically
        logger.info('Background sync manager initialized');

        // Log that initialization is complete
        logger.info('Client-side services initialized successfully');
      } catch (error) {
        logger.error('Failed to initialize client-side services', { error });
      }
    };

    initializeServices();
  }, []);

  // This component doesn't render anything
  return null;
}

export default ClientInitializer;