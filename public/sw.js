/**
 * Enhanced Service Worker for La Vida Luca App
 * Handles caching, background sync, push notifications, and offline functionality
 */

const CACHE_NAME = 'la-vida-luca-v1';
const API_CACHE_NAME = 'la-vida-luca-api-v1';
const STATIC_CACHE_NAME = 'la-vida-luca-static-v1';

// Assets to cache immediately
const STATIC_ASSETS = [
  '/',
  '/manifest.webmanifest',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  // Add other critical assets
];

// API endpoints to cache
const CACHEABLE_APIS = [
  '/api/activities',
  '/api/users',
  '/api/catalogue',
];

// Background sync tasks
const backgroundTasks = new Map();

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('Service Worker installing...');
  
  event.waitUntil(
    Promise.all([
      caches.open(STATIC_CACHE_NAME).then((cache) => {
        return cache.addAll(STATIC_ASSETS);
      }),
      self.skipWaiting() // Activate immediately
    ])
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('Service Worker activating...');
  
  event.waitUntil(
    Promise.all([
      // Clean up old caches
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME && 
                cacheName !== API_CACHE_NAME && 
                cacheName !== STATIC_CACHE_NAME) {
              console.log('Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      }),
      self.clients.claim() // Take control immediately
    ])
  );
});

// Fetch event - implement caching strategies
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-HTTP requests
  if (!request.url.startsWith('http')) {
    return;
  }

  // Handle API requests
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(handleApiRequest(request));
    return;
  }

  // Handle static assets
  if (isStaticAsset(request)) {
    event.respondWith(handleStaticAsset(request));
    return;
  }

  // Handle navigation requests
  if (request.mode === 'navigate') {
    event.respondWith(handleNavigation(request));
    return;
  }

  // Default: network first, cache fallback
  event.respondWith(
    fetch(request).catch(() => {
      return caches.match(request);
    })
  );
});

// Background sync event
self.addEventListener('sync', (event) => {
  console.log('Background sync triggered:', event.tag);

  if (event.tag === 'force-sync-all') {
    event.waitUntil(syncAllPendingData());
    return;
  }

  if (event.tag.startsWith('sync-')) {
    const taskId = event.tag.replace('sync-', '');
    event.waitUntil(syncBackgroundTask(taskId));
    return;
  }

  if (event.tag.startsWith('retry-')) {
    const taskId = event.tag.replace('retry-', '');
    event.waitUntil(retryBackgroundTask(taskId));
    return;
  }
});

// Periodic sync event (if supported)
self.addEventListener('periodicsync', (event) => {
  console.log('Periodic sync triggered:', event.tag);

  switch (event.tag) {
    case 'data-sync':
      event.waitUntil(performDataSync());
      break;
    case 'cache-cleanup':
      event.waitUntil(cleanupCaches());
      break;
    case 'metrics-collection':
      event.waitUntil(collectMetrics());
      break;
    case 'analytics-sync':
      event.waitUntil(syncAnalytics());
      break;
    default:
      console.log('Unknown periodic sync tag:', event.tag);
  }
});

// Push notification event
self.addEventListener('push', (event) => {
  console.log('Push notification received');

  let notificationData = {
    title: 'La Vida Luca',
    body: 'Nouvelle notification',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    data: {},
  };

  if (event.data) {
    try {
      const data = event.data.json();
      notificationData = { ...notificationData, ...data };
    } catch (error) {
      console.error('Error parsing push data:', error);
    }
  }

  event.waitUntil(
    self.registration.showNotification(notificationData.title, {
      body: notificationData.body,
      icon: notificationData.icon,
      badge: notificationData.badge,
      data: notificationData.data,
      actions: notificationData.actions || [],
      requireInteraction: notificationData.requireInteraction || false,
    })
  );
});

// Notification click event
self.addEventListener('notificationclick', (event) => {
  console.log('Notification clicked:', event.notification.data);

  event.notification.close();

  const data = event.notification.data;
  let targetUrl = data.url || '/';

  // Handle action clicks
  if (event.action) {
    switch (event.action) {
      case 'open':
        targetUrl = data.url || '/';
        break;
      case 'dismiss':
        return; // Just close the notification
      default:
        targetUrl = data.actions?.[event.action]?.url || targetUrl;
    }
  }

  event.waitUntil(
    clients.matchAll({ type: 'window' }).then((clientList) => {
      // Check if there's already a window open
      for (const client of clientList) {
        if (client.url === targetUrl && 'focus' in client) {
          return client.focus();
        }
      }
      
      // Open new window
      if (clients.openWindow) {
        return clients.openWindow(targetUrl);
      }
    })
  );
});

// Message event - communication with main thread
self.addEventListener('message', (event) => {
  const { type, payload } = event.data;

  switch (type) {
    case 'schedule-background-task':
      backgroundTasks.set(payload.id, payload);
      console.log('Background task scheduled:', payload.id);
      break;
      
    case 'cancel-background-task':
      backgroundTasks.delete(payload.taskId);
      console.log('Background task cancelled:', payload.taskId);
      break;
      
    case 'update-background-sync-config':
      // Update background sync configuration
      console.log('Background sync config updated:', payload);
      break;
      
    default:
      console.log('Unknown message type:', type);
  }
});

// API request handler - network first, cache fallback
async function handleApiRequest(request) {
  const cache = await caches.open(API_CACHE_NAME);
  
  try {
    // Try network first
    const networkResponse = await fetch(request);
    
    // Cache successful responses
    if (networkResponse.ok && request.method === 'GET') {
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('Network failed, trying cache:', request.url);
    
    // Fallback to cache
    const cachedResponse = await cache.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline response
    return new Response(
      JSON.stringify({ 
        error: 'Network unavailable', 
        offline: true,
        message: 'Cette fonctionnalité nécessite une connexion internet'
      }),
      { 
        status: 503,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}

// Static asset handler - cache first
async function handleStaticAsset(request) {
  const cache = await caches.open(STATIC_CACHE_NAME);
  
  // Try cache first
  const cachedResponse = await cache.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }
  
  // Fetch and cache
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    console.log('Failed to fetch static asset:', request.url);
    throw error;
  }
}

// Navigation handler - network first, cache fallback
async function handleNavigation(request) {
  try {
    const networkResponse = await fetch(request);
    return networkResponse;
  } catch (error) {
    // Return cached index.html for SPA
    const cache = await caches.open(STATIC_CACHE_NAME);
    const offlinePage = await cache.match('/');
    return offlinePage || new Response('Offline', { status: 503 });
  }
}

// Check if request is for static asset
function isStaticAsset(request) {
  const url = new URL(request.url);
  return url.pathname.match(/\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$/);
}

// Sync all pending data
async function syncAllPendingData() {
  console.log('Syncing all pending data...');
  
  try {
    // Sync cached API data
    await syncCachedApiData();
    
    // Sync background tasks
    for (const [taskId, task] of backgroundTasks) {
      await syncBackgroundTask(taskId);
    }
    
    console.log('All data synced successfully');
  } catch (error) {
    console.error('Error syncing all data:', error);
  }
}

// Sync cached API data
async function syncCachedApiData() {
  // Implementation for syncing cached API modifications
  console.log('Syncing cached API data...');
}

// Sync background task
async function syncBackgroundTask(taskId) {
  const task = backgroundTasks.get(taskId);
  if (!task) {
    console.log('Task not found:', taskId);
    return;
  }

  try {
    console.log('Syncing background task:', task.type);
    
    switch (task.type) {
      case 'data-sync':
        await syncDataTask(task);
        break;
      case 'file-upload':
        await syncFileUpload(task);
        break;
      case 'analytics':
        await syncAnalyticsEvent(task);
        break;
      case 'notification':
        await syncNotification(task);
        break;
      default:
        console.log('Unknown task type:', task.type);
    }
    
    // Remove completed task
    backgroundTasks.delete(taskId);
    
    // Notify main thread
    await notifyMainThread('background-sync-complete', { taskId, result: 'success' });
    
  } catch (error) {
    console.error('Error syncing background task:', error);
    
    // Update retry count
    task.retryCount = (task.retryCount || 0) + 1;
    
    if (task.retryCount >= task.maxRetries) {
      backgroundTasks.delete(taskId);
    }
    
    // Notify main thread
    await notifyMainThread('background-sync-failed', { taskId, error: error.message });
  }
}

// Retry background task
async function retryBackgroundTask(taskId) {
  console.log('Retrying background task:', taskId);
  await syncBackgroundTask(taskId);
}

// Sync data task
async function syncDataTask(task) {
  const { data, endpoint, method } = task.data;
  
  const response = await fetch(endpoint, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: method !== 'GET' ? JSON.stringify(data) : undefined,
  });
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  
  return await response.json();
}

// Sync file upload
async function syncFileUpload(task) {
  const { fileName, fileType, fileData, endpoint } = task.data;
  
  // Convert base64 back to blob
  const response = await fetch(fileData);
  const blob = await response.blob();
  
  const formData = new FormData();
  formData.append('file', blob, fileName);
  
  const uploadResponse = await fetch(endpoint, {
    method: 'POST',
    body: formData,
  });
  
  if (!uploadResponse.ok) {
    throw new Error(`Upload failed: ${uploadResponse.statusText}`);
  }
  
  return await uploadResponse.json();
}

// Sync analytics event
async function syncAnalyticsEvent(task) {
  const response = await fetch('/api/analytics', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ events: [task.data] }),
  });
  
  if (!response.ok) {
    throw new Error(`Analytics sync failed: ${response.statusText}`);
  }
}

// Sync notification
async function syncNotification(task) {
  const response = await fetch('/api/notifications', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(task.data),
  });
  
  if (!response.ok) {
    throw new Error(`Notification sync failed: ${response.statusText}`);
  }
}

// Periodic sync handlers
async function performDataSync() {
  console.log('Performing periodic data sync...');
  try {
    await fetch('/api/sync/periodic', { method: 'POST' });
  } catch (error) {
    console.error('Periodic data sync failed:', error);
  }
}

async function cleanupCaches() {
  console.log('Cleaning up caches...');
  
  // Clean old cache entries
  const cacheNames = await caches.keys();
  for (const cacheName of cacheNames) {
    const cache = await caches.open(cacheName);
    const requests = await cache.keys();
    
    for (const request of requests) {
      const response = await cache.match(request);
      if (response) {
        const date = response.headers.get('date');
        if (date && Date.now() - new Date(date).getTime() > 7 * 24 * 60 * 60 * 1000) {
          await cache.delete(request);
        }
      }
    }
  }
}

async function collectMetrics() {
  console.log('Collecting metrics...');
  // Implementation for metrics collection
}

async function syncAnalytics() {
  console.log('Syncing analytics...');
  // Implementation for analytics sync
}

// Notify main thread
async function notifyMainThread(type, payload) {
  const clients = await self.clients.matchAll();
  clients.forEach(client => {
    client.postMessage({ type, payload });
  });
}

console.log('Service Worker script loaded');