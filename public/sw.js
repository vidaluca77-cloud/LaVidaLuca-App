/**
 * Service Worker for La Vida Luca App
 * Provides offline functionality and caching strategies
 */

const CACHE_VERSION = 'v1.0.0';
const STATIC_CACHE = `static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `dynamic-${CACHE_VERSION}`;
const API_CACHE = `api-${CACHE_VERSION}`;

// Resources to cache immediately on install
const STATIC_ASSETS = [
  '/',
  '/manifest.webmanifest',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/catalogue',
  '/contact',
  '/rejoindre',
  // Add critical CSS/JS files that Next.js generates
  '/_next/static/css/',
  '/_next/static/chunks/'
];

// API endpoints to cache
const API_ENDPOINTS = [
  '/api/contact',
  '/api/activities',
  '/api/suggestions'
];

// Maximum number of items in dynamic cache
const MAX_DYNAMIC_CACHE_SIZE = 50;
const MAX_API_CACHE_SIZE = 20;

/**
 * Install event - cache static assets
 */
self.addEventListener('install', event => {
  console.log('[SW] Installing service worker');
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        console.log('[SW] Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('[SW] Service worker installed successfully');
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('[SW] Error during installation:', error);
      })
  );
});

/**
 * Activate event - clean up old caches
 */
self.addEventListener('activate', event => {
  console.log('[SW] Activating service worker');
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames
            .filter(cacheName => {
              // Remove old caches
              return cacheName.startsWith('static-') && cacheName !== STATIC_CACHE ||
                     cacheName.startsWith('dynamic-') && cacheName !== DYNAMIC_CACHE ||
                     cacheName.startsWith('api-') && cacheName !== API_CACHE;
            })
            .map(cacheName => {
              console.log('[SW] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            })
        );
      })
      .then(() => {
        console.log('[SW] Service worker activated');
        return self.clients.claim();
      })
  );
});

/**
 * Fetch event - handle requests with caching strategies
 */
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-HTTP requests
  if (!request.url.startsWith('http')) {
    return;
  }
  
  // Skip Chrome extensions
  if (url.protocol === 'chrome-extension:') {
    return;
  }

  // API requests - Network First with cache fallback
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirstStrategy(request, API_CACHE, MAX_API_CACHE_SIZE));
  }
  // Static assets - Cache First
  else if (isStaticAsset(url)) {
    event.respondWith(cacheFirstStrategy(request, STATIC_CACHE));
  }
  // Pages - Stale While Revalidate
  else if (url.origin === self.location.origin) {
    event.respondWith(staleWhileRevalidateStrategy(request, DYNAMIC_CACHE, MAX_DYNAMIC_CACHE_SIZE));
  }
});

/**
 * Network First Strategy - for API calls
 */
async function networkFirstStrategy(request, cacheName, maxSize) {
  try {
    // Try network first
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Cache successful responses
      const cache = await caches.open(cacheName);
      await limitCacheSize(cache, maxSize);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[SW] Network failed, trying cache:', request.url);
    
    // Fallback to cache
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline page for failed API calls
    return new Response(
      JSON.stringify({ 
        error: 'Offline', 
        message: 'Cette fonctionnalité nécessite une connexion internet' 
      }),
      { 
        status: 503,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}

/**
 * Cache First Strategy - for static assets
 */
async function cacheFirstStrategy(request, cacheName) {
  // Try cache first
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }
  
  // Fallback to network
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    console.log('[SW] Asset not available:', request.url);
    // Could return a fallback asset here
    throw error;
  }
}

/**
 * Stale While Revalidate Strategy - for pages
 */
async function staleWhileRevalidateStrategy(request, cacheName, maxSize) {
  const cachedResponse = await caches.match(request);
  
  const networkPromise = fetch(request)
    .then(response => {
      if (response.ok) {
        const cache = caches.open(cacheName);
        cache.then(c => {
          limitCacheSize(c, maxSize);
          c.put(request, response.clone());
        });
      }
      return response;
    })
    .catch(() => {
      // Silently fail network requests in this strategy
      return null;
    });
  
  // Return cached version immediately if available
  if (cachedResponse) {
    return cachedResponse;
  }
  
  // Otherwise wait for network
  return networkPromise || new Response('Offline', { status: 503 });
}

/**
 * Utility function to check if URL is a static asset
 */
function isStaticAsset(url) {
  return url.pathname.startsWith('/_next/static/') ||
         url.pathname.startsWith('/icons/') ||
         url.pathname.endsWith('.png') ||
         url.pathname.endsWith('.jpg') ||
         url.pathname.endsWith('.jpeg') ||
         url.pathname.endsWith('.svg') ||
         url.pathname.endsWith('.webp') ||
         url.pathname.endsWith('.css') ||
         url.pathname.endsWith('.js');
}

/**
 * Limit cache size by removing oldest entries
 */
async function limitCacheSize(cache, maxSize) {
  const keys = await cache.keys();
  if (keys.length > maxSize) {
    // Remove oldest entries
    const entriesToDelete = keys.slice(0, keys.length - maxSize);
    await Promise.all(entriesToDelete.map(key => cache.delete(key)));
  }
}

/**
 * Handle background sync for offline actions
 */
self.addEventListener('sync', event => {
  console.log('[SW] Background sync:', event.tag);
  
  if (event.tag === 'offline-actions') {
    event.waitUntil(processOfflineActions());
  }
});

/**
 * Process queued offline actions
 */
async function processOfflineActions() {
  try {
    // Get offline actions from IndexedDB or localStorage
    const actions = await getOfflineActions();
    
    for (const action of actions) {
      try {
        await fetch(action.url, {
          method: action.method,
          headers: action.headers,
          body: action.body
        });
        
        // Remove successful action from queue
        await removeOfflineAction(action.id);
        
        // Notify clients of successful sync
        self.clients.matchAll().then(clients => {
          clients.forEach(client => {
            client.postMessage({
              type: 'OFFLINE_ACTION_SYNCED',
              action: action
            });
          });
        });
        
      } catch (error) {
        console.log('[SW] Failed to sync action:', action, error);
      }
    }
  } catch (error) {
    console.error('[SW] Error processing offline actions:', error);
  }
}

/**
 * Handle push notifications
 */
self.addEventListener('push', event => {
  console.log('[SW] Push message received');
  
  const options = {
    body: event.data ? event.data.text() : 'Nouvelle notification',
    icon: '/icons/icon-192.png',
    badge: '/icons/icon-192.png',
    vibrate: [200, 100, 200],
    actions: [
      { action: 'view', title: 'Voir', icon: '/icons/icon-192.png' },
      { action: 'dismiss', title: 'Ignorer' }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('La Vida Luca', options)
  );
});

/**
 * Handle notification clicks
 */
self.addEventListener('notificationclick', event => {
  event.notification.close();
  
  if (event.action === 'view') {
    event.waitUntil(
      self.clients.openWindow('/')
    );
  }
});

/**
 * Placeholder functions for offline action management
 * These would integrate with IndexedDB or localStorage
 */
async function getOfflineActions() {
  // Implementation would fetch from storage
  return [];
}

async function removeOfflineAction(id) {
  // Implementation would remove from storage
  console.log('[SW] Removing offline action:', id);
}

/**
 * Send message to all clients
 */
function broadcastMessage(message) {
  self.clients.matchAll().then(clients => {
    clients.forEach(client => client.postMessage(message));
  });
}

console.log('[SW] Service worker script loaded');