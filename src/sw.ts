/// <reference lib="webworker" />

import { cleanupOutdatedCaches, createHandlerBoundToURL, precacheAndRoute } from 'workbox-precaching';
import { NavigationRoute, registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst, StaleWhileRevalidate } from 'workbox-strategies';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';
import { ExpirationPlugin } from 'workbox-expiration';

declare const self: ServiceWorkerGlobalScope;

// Precache all routes and assets
precacheAndRoute(self.__WB_MANIFEST);

// Clean up outdated caches
cleanupOutdatedCaches();

// Navigation fallback
const handler = createHandlerBoundToURL('/');
const navigationRoute = new NavigationRoute(handler, {
  denylist: [/^\/_/, /\/[^/?]+\.[^/]+$/],
});
registerRoute(navigationRoute);

// Cache strategies for different types of resources

// Images - Cache First with long expiration
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 days
      }),
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
    ],
  })
);

// Static assets (JS, CSS) - Stale While Revalidate
registerRoute(
  ({ request }) =>
    request.destination === 'script' ||
    request.destination === 'style',
  new StaleWhileRevalidate({
    cacheName: 'static-resources',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
    ],
  })
);

// API calls - Network First with short fallback
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/'),
  new NetworkFirst({
    cacheName: 'api-cache',
    networkTimeoutSeconds: 3,
    plugins: [
      new ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 5 * 60, // 5 minutes
      }),
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
    ],
  })
);

// Fonts - Cache First with very long expiration
registerRoute(
  ({ request }) => request.destination === 'font',
  new CacheFirst({
    cacheName: 'fonts',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 10,
        maxAgeSeconds: 365 * 24 * 60 * 60, // 1 year
      }),
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
    ],
  })
);

// Documents/Pages - Network First
registerRoute(
  ({ request }) => request.destination === 'document',
  new NetworkFirst({
    cacheName: 'pages',
    networkTimeoutSeconds: 3,
    plugins: [
      new ExpirationPlugin({
        maxEntries: 20,
        maxAgeSeconds: 24 * 60 * 60, // 1 day
      }),
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
    ],
  })
);

// Background sync for offline actions
interface OfflineAction {
  id: string;
  type: string;
  data: any;
  timestamp: number;
}

let offlineQueue: OfflineAction[] = [];

// Listen for messages from the main thread
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'QUEUE_OFFLINE_ACTION') {
    const action: OfflineAction = {
      id: crypto.randomUUID(),
      type: event.data.actionType,
      data: event.data.data,
      timestamp: Date.now(),
    };
    
    offlineQueue.push(action);
    
    // Try to sync immediately if online
    if (navigator.onLine) {
      processOfflineQueue();
    }
  }
});

// Register background sync
self.addEventListener('sync', (event) => {
  if (event.tag === 'offline-sync') {
    event.waitUntil(processOfflineQueue());
  }
});

// Process offline queue
async function processOfflineQueue() {
  const queueCopy = [...offlineQueue];
  offlineQueue = [];

  for (const action of queueCopy) {
    try {
      await processOfflineAction(action);
    } catch (error) {
      console.error('Failed to process offline action:', action, error);
      // Re-add to queue if processing failed
      offlineQueue.push(action);
    }
  }

  // Notify main thread about queue status
  const clients = await self.clients.matchAll();
  clients.forEach(client => {
    client.postMessage({
      type: 'OFFLINE_QUEUE_STATUS',
      queueLength: offlineQueue.length,
    });
  });
}

// Process individual offline actions
async function processOfflineAction(action: OfflineAction) {
  switch (action.type) {
    case 'CONTACT_FORM_SUBMIT':
      return await fetch('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(action.data),
      });
    
    case 'USER_PREFERENCE_UPDATE':
      // Store locally and sync when online
      return await storeUserPreference(action.data);
    
    default:
      console.warn('Unknown offline action type:', action.type);
  }
}

// Store user preferences locally
async function storeUserPreference(data: any) {
  // This would be implemented to sync with backend when online
  return Promise.resolve();
}

// Listen for network status changes
self.addEventListener('online', () => {
  processOfflineQueue();
});

// Push notification handling
self.addEventListener('push', (event) => {
  if (!event.data) {
    return;
  }

  const data = event.data.json();
  const title = data.title || 'La Vida Luca';
  const options = {
    body: data.body,
    icon: '/icons/icon-192.png',
    badge: '/icons/icon-192.png',
    data: data.url,
    ...data.options,
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.notification.data) {
    event.waitUntil(
      self.clients.openWindow(event.notification.data)
    );
  }
});

// Skip waiting for immediate activation
self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});