# Real-Time Synchronization, Offline Capabilities, and PWA Features

This implementation provides comprehensive real-time synchronization, offline capabilities, and Progressive Web App (PWA) features for the La Vida Luca application.

## 🚀 Features Implemented

### 1. WebSocket Manager (`src/lib/websocket.ts`)
- **Connection Management**: Auto-reconnect with exponential backoff
- **Event Handling**: Type-safe message handling with subscription system
- **Message Queue**: Offline message queuing with automatic flush on reconnect
- **Heartbeat**: Connection health monitoring
- **Error Recovery**: Robust error handling and retry logic

### 2. Sync Manager (`src/lib/syncManager.ts`)
- **Cache Management**: TTL-based caching with automatic cleanup
- **Retry Strategies**: Configurable retry intervals and attempts
- **Background Sync**: Queue-based synchronization with priority handling
- **Strategy Pattern**: Pluggable sync strategies for different data types
- **Offline Support**: Full offline queue management

### 3. Notification System (`src/lib/notifications.ts`)
- **Browser Notifications**: Full Web Notifications API support
- **Push Notifications**: Service Worker-based push notifications
- **Permission Management**: Automatic permission requests
- **Notification Types**: Success, error, warning, and custom notifications
- **Fallback Support**: Graceful degradation for unsupported browsers

### 4. PWA Manager (`src/lib/pwa.ts`)
- **Installation Detection**: Cross-platform installation capabilities
- **Service Worker**: Automatic registration and management
- **Update Management**: App update detection and handling
- **Platform Detection**: iOS, Android, and desktop support
- **Installation Guidance**: Platform-specific installation instructions

### 5. Service Worker (`public/sw.js`)
- **Offline Caching**: Static assets and API response caching
- **Background Sync**: Queue processing when online
- **Push Notifications**: Server-sent notification handling
- **Cache Strategies**: Network-first, cache-first, and stale-while-revalidate
- **Offline Fallbacks**: Custom offline pages and error handling

## 🎯 React Hooks

### useWebSocket
```typescript
import { useWebSocket } from '@/hooks/useWebSocket';

const {
  isConnected,
  isConnecting,
  send,
  subscribe,
  connect,
  disconnect
} = useWebSocket('wss://your-websocket-url', {
  autoConnect: true,
  onOpen: () => console.log('Connected!'),
  onMessage: (message) => console.log('Message:', message)
});

// Subscribe to specific message types
useEffect(() => {
  const unsubscribe = subscribe('data-update', (message) => {
    // Handle data updates
  });
  return unsubscribe;
}, [subscribe]);
```

### useSync
```typescript
import { useSync } from '@/hooks/useSync';
import { defaultSyncStrategies } from '@/lib/syncStrategies';

const {
  queueSync,
  cache,
  getCached,
  forceSync,
  status
} = useSync({
  strategies: defaultSyncStrategies,
  onSyncComplete: (item) => console.log('Synced:', item)
});

// Queue a sync operation
queueSync('contact-form', 'contact-form', {
  name: 'John Doe',
  email: 'john@example.com',
  message: 'Hello world'
}, 'high');

// Cache data with TTL
cache('user-profile', userData, 3600000); // 1 hour
```

### useNotifications
```typescript
import { useNotifications } from '@/hooks/useNotifications';

const {
  hasPermission,
  requestPermission,
  notify,
  notifySuccess,
  subscribeToPush
} = useNotifications({
  autoRequestPermission: true,
  enablePush: true,
  vapidPublicKey: 'your-vapid-key'
});

// Show notifications
await notifySuccess('Success!', 'Operation completed');
await notify('Custom notification', 'With custom options', {
  icon: '/custom-icon.png',
  requireInteraction: true
});
```

### usePWA
```typescript
import { usePWA } from '@/hooks/usePWA';

const {
  capabilities,
  installState,
  showInstallPrompt,
  updateServiceWorker,
  isOfflineReady
} = usePWA({
  autoRegisterServiceWorker: true,
  enableUpdateNotifications: true
});

// Show install prompt
if (installState.canInstall) {
  await showInstallPrompt();
}

// Update the app
if (updateAvailable) {
  await updateServiceWorker();
}
```

## 🎨 UI Components

### Sync Components
```typescript
import { SyncStatus, SyncQueue } from '@/components/sync';

// Show sync status
<SyncStatus showDetails showLastSync />

// Manage sync queue
<SyncQueue showControls />
```

### Real-time Components
```typescript
import { ConnectionStatus } from '@/components/realtime';

// Show WebSocket connection status
<ConnectionStatus showDetails showRetryInfo />
```

### Notification Components
```typescript
import { NotificationCenter } from '@/components/notifications';

// Notification management center
<NotificationCenter
  showPermissionStatus
  showPushStatus
  allowTestNotifications
/>
```

### PWA Components
```typescript
import { PWAStatus } from '@/components/pwa';

// PWA installation and status
<PWAStatus
  showCapabilities
  showInstallPrompt
  showUpdatePrompt
/>
```

## 🔧 Sync Strategies

Custom sync strategies can be created for different data types:

```typescript
import { SyncStrategy } from '@/lib/syncManager';

const customSyncStrategy: SyncStrategy = {
  name: 'custom-sync',
  
  canSync: (item) => item.type === 'custom-data',
  
  sync: async (item) => {
    try {
      const response = await fetch('/api/custom', {
        method: 'POST',
        body: JSON.stringify(item.data)
      });
      return response.ok;
    } catch (error) {
      return false;
    }
  },
  
  onSuccess: (item) => {
    console.log('Custom sync successful:', item);
  },
  
  onFailure: (item, error) => {
    console.error('Custom sync failed:', item, error);
  }
};

// Register the strategy
syncManager.registerStrategy(customSyncStrategy);
```

## 📱 PWA Configuration

### Manifest (`public/manifest.webmanifest`)
The manifest includes:
- App metadata and descriptions
- Icons for different sizes and purposes
- App shortcuts
- Screenshots for app stores
- Display and orientation preferences

### Service Worker Features
- **Static Caching**: App shell and critical resources
- **API Caching**: Network-first strategy with fallbacks
- **Background Sync**: Retry failed operations when online
- **Push Notifications**: Handle server-sent notifications
- **Update Management**: Detect and install app updates

## 🛠️ Integration Examples

### Complete Integration
```typescript
import { RealTimeAppDemo } from '@/components/demo';

// Full-featured demo component
<RealTimeAppDemo
  websocketUrl="wss://your-websocket-server"
  enablePushNotifications={true}
  vapidPublicKey="your-vapid-public-key"
/>
```

### Contact Form with Offline Support
```typescript
const handleSubmit = async (formData) => {
  try {
    // Try immediate submission
    const response = await fetch('/api/contact', {
      method: 'POST',
      body: JSON.stringify(formData)
    });
    
    if (response.ok) {
      notifySuccess('Message sent!', 'Your message was sent successfully');
    } else {
      throw new Error('Submission failed');
    }
  } catch (error) {
    // Queue for later if offline
    queueSync(`contact-${Date.now()}`, 'contact-form', formData, 'high');
    notifyWarning('Queued for sending', 'Your message will be sent when connection is restored');
  }
};
```

### Real-time Data Updates
```typescript
useEffect(() => {
  const unsubscribe = subscribe('activity-update', (message) => {
    // Update local state
    setActivities(prev => updateActivity(prev, message.payload));
    
    // Cache updated data
    cache(`activity-${message.payload.id}`, message.payload, 3600000);
    
    // Show notification for important updates
    if (message.payload.important) {
      notify('Activity Updated', message.payload.title);
    }
  });
  
  return unsubscribe;
}, [subscribe, cache, notify]);
```

## 🔍 Monitoring & Logging

All components integrate with the existing monitoring system:

```typescript
import { logger } from '@/lib/logger';
import { alertManager } from '@/monitoring/alerts';

// Structured logging
logger.info('WebSocket connected', { url, duration }, 'websocket');

// Alert management
alertManager.warning('High sync queue size', { queueSize: 100 });
```

## 🧪 Testing

### Running Tests
```bash
npm test                    # Run all tests
npm run test:coverage      # Run with coverage
npm run test:watch         # Watch mode
```

### Building
```bash
npm run build              # Production build
npm run dev                # Development server
```

## 📋 Best Practices

1. **Error Handling**: Always wrap async operations in try-catch blocks
2. **Resource Cleanup**: Unsubscribe from WebSocket events in useEffect cleanup
3. **Cache Management**: Set appropriate TTL values for cached data
4. **Notification Permissions**: Request permissions contextually, not on page load
5. **Offline UX**: Provide clear feedback when operations are queued offline
6. **PWA Installation**: Show install prompts at appropriate moments
7. **Service Worker Updates**: Handle updates gracefully without disrupting user experience

## 🔗 Dependencies

The implementation uses only standard Web APIs and React:
- WebSocket API for real-time communication
- Notification API for browser notifications
- Service Worker API for offline capabilities
- IndexedDB for persistent storage (via built-in browser support)
- Push API for push notifications

No additional external dependencies were added to maintain the lightweight nature of the application.

## 🚀 Deployment Considerations

1. **HTTPS Required**: PWA features require HTTPS in production
2. **Service Worker Scope**: Ensure service worker is served from root
3. **VAPID Keys**: Generate and configure VAPID keys for push notifications
4. **Cache Headers**: Configure appropriate cache headers for static assets
5. **WebSocket URL**: Use secure WebSocket (wss://) in production
6. **Icon Assets**: Ensure all manifest icons are available
7. **Fallback Pages**: Provide offline fallback pages

This implementation provides a robust foundation for real-time, offline-capable, and installable web applications while maintaining excellent TypeScript support and integration with existing monitoring systems.