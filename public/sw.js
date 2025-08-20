/**
 * Service Worker for La Vida Luca App
 * Handles caching, offline functionality, and push notifications
 */

const CACHE_NAME = 'lavidaluca-v1';
const OFFLINE_URL = '/offline';

// Define cache strategies for different resource types
const CACHE_STRATEGIES = {
  // Cache first strategy for static assets
  CACHE_FIRST: 'cache-first',
  // Network first strategy for API calls
  NETWORK_FIRST: 'network-first',
  // Stale while revalidate for images and other assets
  STALE_WHILE_REVALIDATE: 'stale-while-revalidate',
};

// Resources to cache immediately
const PRECACHE_RESOURCES = [
  '/',
  '/offline',
  '/manifest.webmanifest',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
];

// API endpoints that should be cached
const API_CACHE_PATTERNS = [
  /^https:\/\/api\.lavidaluca\.com\/activities/,
  /^https:\/\/api\.lavidaluca\.com\/users/,
  /\/api\/activities/,
  /\/api\/users/,
];

// Resources that should use stale-while-revalidate
const STALE_WHILE_REVALIDATE_PATTERNS = [
  /\.(?:png|jpg|jpeg|svg|gif|webp)$/,
  /\.(?:css|js)$/,
  /\/_next\/static\//,
];

// Install event - cache essential resources
self.addEventListener('install', (event) => {
  console.log('[SW] Install event');
  
  event.waitUntil(
    (async () => {
      try {
        const cache = await caches.open(CACHE_NAME);
        console.log('[SW] Caching precache resources');
        await cache.addAll(PRECACHE_RESOURCES);
        console.log('[SW] Precache complete');
      } catch (error) {
        console.error('[SW] Precache failed:', error);
      }
    })()
  );

  // Take control immediately
  self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activate event');
  
  event.waitUntil(
    (async () => {
      // Clean up old caches
      const cacheNames = await caches.keys();
      const oldCaches = cacheNames.filter(name => name !== CACHE_NAME);
      
      await Promise.all(
        oldCaches.map(name => {
          console.log('[SW] Deleting old cache:', name);
          return caches.delete(name);
        })
      );

      // Take control of all clients
      await self.clients.claim();
      console.log('[SW] Claimed all clients');
    })()
  );
});

// Fetch event - handle all network requests
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip chrome-extension and other non-http requests
  if (!url.protocol.startsWith('http')) {
    return;
  }

  event.respondWith(handleFetch(request));
});

async function handleFetch(request) {
  const url = new URL(request.url);
  
  try {
    // Determine cache strategy based on request
    if (isApiRequest(url)) {
      return await networkFirstStrategy(request);
    } else if (isStaticAsset(url)) {
      return await staleWhileRevalidateStrategy(request);
    } else {
      return await cacheFirstStrategy(request);
    }
  } catch (error) {
    console.error('[SW] Fetch failed:', error);
    return await handleOfflineFallback(request);
  }
}

function isApiRequest(url) {
  return API_CACHE_PATTERNS.some(pattern => pattern.test(url.href));
}

function isStaticAsset(url) {
  return STALE_WHILE_REVALIDATE_PATTERNS.some(pattern => pattern.test(url.pathname));
}

// Cache first strategy - try cache first, then network
async function cacheFirstStrategy(request) {
  const cache = await caches.open(CACHE_NAME);
  const cachedResponse = await cache.match(request);
  
  if (cachedResponse) {
    console.log('[SW] Cache hit:', request.url);
    return cachedResponse;
  }

  console.log('[SW] Cache miss, fetching:', request.url);
  const networkResponse = await fetch(request);
  
  // Cache successful responses
  if (networkResponse && networkResponse.status === 200) {
    cache.put(request, networkResponse.clone());
  }
  
  return networkResponse;
}

// Network first strategy - try network first, fallback to cache
async function networkFirstStrategy(request) {
  const cache = await caches.open(CACHE_NAME);
  
  try {
    console.log('[SW] Network first:', request.url);
    const networkResponse = await fetch(request);
    
    // Cache successful responses
    if (networkResponse && networkResponse.status === 200) {
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[SW] Network failed, trying cache:', request.url);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    throw error;
  }
}

// Stale while revalidate strategy - return cache immediately, update in background
async function staleWhileRevalidateStrategy(request) {
  const cache = await caches.open(CACHE_NAME);
  const cachedResponse = await cache.match(request);
  
  // Fetch from network in background to update cache
  const fetchPromise = fetch(request).then(response => {
    if (response && response.status === 200) {
      cache.put(request, response.clone());
    }
    return response;
  }).catch(error => {
    console.error('[SW] Background fetch failed:', error);
  });

  // Return cached version immediately if available
  if (cachedResponse) {
    console.log('[SW] Stale while revalidate - cache hit:', request.url);
    return cachedResponse;
  }

  // If no cache, wait for network
  console.log('[SW] Stale while revalidate - no cache, waiting for network:', request.url);
  return await fetchPromise;
}

// Handle offline fallbacks
async function handleOfflineFallback(request) {
  const url = new URL(request.url);
  
  // For navigation requests, show offline page
  if (request.mode === 'navigate') {
    const cache = await caches.open(CACHE_NAME);
    const offlinePage = await cache.match(OFFLINE_URL);
    return offlinePage || new Response('Offline - Page not available', {
      status: 503,
      statusText: 'Service Unavailable'
    });
  }

  // For images, return a placeholder
  if (request.destination === 'image') {
    return new Response(
      '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" fill="#f0f0f0"/><text x="100" y="100" text-anchor="middle" dy=".3em" fill="#999">Image indisponible</text></svg>',
      { headers: { 'Content-Type': 'image/svg+xml' } }
    );
  }

  // For other requests, return a generic error
  return new Response('Resource not available offline', {
    status: 503,
    statusText: 'Service Unavailable'
  });
}

// Handle push events
self.addEventListener('push', (event) => {
  console.log('[SW] Push event received');
  
  let notificationData = {
    title: 'La Vida Luca',
    body: 'Vous avez une nouvelle notification',
    icon: '/icons/icon-192.png',
    badge: '/icons/icon-192.png',
    tag: 'default',
    data: {}
  };

  if (event.data) {
    try {
      const data = event.data.json();
      notificationData = { ...notificationData, ...data };
    } catch (error) {
      console.error('[SW] Error parsing push data:', error);
      notificationData.body = event.data.text() || notificationData.body;
    }
  }

  event.waitUntil(
    self.registration.showNotification(notificationData.title, {
      body: notificationData.body,
      icon: notificationData.icon,
      badge: notificationData.badge,
      tag: notificationData.tag,
      data: notificationData.data,
      requireInteraction: notificationData.requireInteraction || false,
      actions: notificationData.actions || [
        { action: 'view', title: 'Voir' },
        { action: 'close', title: 'Fermer' }
      ]
    })
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
  console.log('[SW] Notification click:', event.action);
  
  event.notification.close();

  if (event.action === 'close') {
    return;
  }

  // Default action or 'view' action
  event.waitUntil(
    (async () => {
      const clients = await self.clients.matchAll({ type: 'window' });
      
      // If app is already open, focus it
      if (clients.length > 0) {
        const client = clients[0];
        await client.focus();
        
        // Navigate to specific page if data contains URL
        if (event.notification.data && event.notification.data.url) {
          client.postMessage({
            type: 'NOTIFICATION_CLICK',
            url: event.notification.data.url,
            data: event.notification.data
          });
        }
      } else {
        // Open new window
        const url = event.notification.data?.url || '/';
        await self.clients.openWindow(url);
      }
    })()
  );
});

// Handle background sync
self.addEventListener('sync', (event) => {
  console.log('[SW] Background sync:', event.tag);
  
  if (event.tag === 'offline-sync') {
    event.waitUntil(syncOfflineData());
  }
});

async function syncOfflineData() {
  try {
    // This would typically communicate with your offline manager
    console.log('[SW] Syncing offline data...');
    
    // Send message to all clients to trigger sync
    const clients = await self.clients.matchAll();
    clients.forEach(client => {
      client.postMessage({
        type: 'BACKGROUND_SYNC',
        tag: 'offline-sync'
      });
    });
    
    console.log('[SW] Offline data sync completed');
  } catch (error) {
    console.error('[SW] Offline data sync failed:', error);
    throw error;
  }
}

// Handle messages from main thread
self.addEventListener('message', (event) => {
  console.log('[SW] Message received:', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  } else if (event.data && event.data.type === 'CLAIM_CLIENTS') {
    self.clients.claim();
  }
});

// Cache management utilities
async function cleanupOldCaches() {
  const cacheNames = await caches.keys();
  const oldCaches = cacheNames.filter(name => name !== CACHE_NAME);
  
  return Promise.all(
    oldCaches.map(name => caches.delete(name))
  );
}

async function getCacheSize() {
  const cache = await caches.open(CACHE_NAME);
  const requests = await cache.keys();
  
  let totalSize = 0;
  for (const request of requests) {
    const response = await cache.match(request);
    if (response) {
      const blob = await response.blob();
      totalSize += blob.size;
    }
  }
  
  return { count: requests.length, size: totalSize };
}

console.log('[SW] Service Worker loaded');