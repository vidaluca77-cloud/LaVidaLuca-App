/**
 * Example integration showing how to use all real-time sync, offline, and PWA features
 * This demonstrates the complete integration of all the implemented features
 */

'use client';

import React, { useEffect } from 'react';
import { useWebSocket } from '@/hooks/useWebSocket';
import { useSync } from '@/hooks/useSync';
import { useNotifications } from '@/hooks/useNotifications';
import { usePWA } from '@/hooks/usePWA';
import { SyncStatus } from '@/components/sync/SyncStatus';
import { SyncQueue } from '@/components/sync/SyncQueue';
import { ConnectionStatus } from '@/components/realtime/ConnectionStatus';
import { NotificationCenter } from '@/components/notifications/NotificationCenter';
import { PWAStatus } from '@/components/pwa/PWAStatus';
import { defaultSyncStrategies } from '@/lib/syncStrategies';
import { logger } from '@/lib/logger';

export interface RealTimeAppDemoProps {
  websocketUrl?: string;
  enablePushNotifications?: boolean;
  vapidPublicKey?: string;
}

export const RealTimeAppDemo: React.FC<RealTimeAppDemoProps> = ({
  websocketUrl = 'wss://localhost:8080/ws',
  enablePushNotifications = false,
  vapidPublicKey,
}) => {
  // Initialize WebSocket connection
  const {
    isConnected,
    isConnecting,
    connect,
    disconnect,
    send,
    subscribe,
  } = useWebSocket(websocketUrl, {
    autoConnect: true,
    reconnectInterval: 5000,
    maxReconnectAttempts: 10,
    onOpen: () => {
      logger.info('WebSocket connected in demo', {}, 'demo');
    },
    onClose: () => {
      logger.info('WebSocket disconnected in demo', {}, 'demo');
    },
    onError: (error) => {
      logger.error('WebSocket error in demo', { error }, 'demo');
    },
  });

  // Initialize sync manager
  const {
    queueSync,
    registerStrategy,
    forceSync,
    cache,
    getCached,
  } = useSync({
    autoInitialize: true,
    strategies: defaultSyncStrategies,
    onSyncComplete: (item) => {
      logger.info('Sync completed in demo', { item }, 'demo');
    },
    onSyncError: (item, error) => {
      logger.error('Sync failed in demo', { item, error }, 'demo');
    },
  });

  // Initialize notifications
  const {
    hasPermission,
    requestPermission,
    subscribeToPush,
    notify,
    notifySuccess,
  } = useNotifications({
    autoRequestPermission: true,
    enablePush: enablePushNotifications,
    vapidPublicKey,
  });

  // Initialize PWA
  const {
    capabilities,
    showInstallPrompt,
    updateServiceWorker,
    isOfflineReady,
  } = usePWA({
    autoRegisterServiceWorker: true,
    enableAutoInstallPrompt: false,
    enableUpdateNotifications: true,
  });

  // Set up WebSocket message handlers
  useEffect(() => {
    // Handle real-time data updates
    const unsubscribeData = subscribe('data-update', (message) => {
      logger.info('Received data update', { message }, 'demo');
      
      // Cache the updated data
      if (message.payload?.data && message.payload?.key) {
        cache(message.payload.key, message.payload.data);
      }
      
      // Show notification for important updates
      if (message.payload?.important && hasPermission) {
        notify(
          'Mise à jour en temps réel',
          message.payload.description || 'Nouvelles données disponibles'
        );
      }
    });

    // Handle sync requests from server
    const unsubscribeSync = subscribe('sync-request', (message) => {
      logger.info('Received sync request', { message }, 'demo');
      
      if (message.payload?.action === 'force-sync') {
        forceSync();
      }
    });

    // Handle notifications from server
    const unsubscribeNotification = subscribe('notification', (message) => {
      logger.info('Received notification', { message }, 'demo');
      
      if (hasPermission && message.payload) {
        notify(
          message.payload.title || 'Notification',
          message.payload.body || '',
          {
            icon: message.payload.icon,
            tag: message.payload.tag,
            data: message.payload.data,
          }
        );
      }
    });

    return () => {
      unsubscribeData();
      unsubscribeSync();
      unsubscribeNotification();
    };
  }, [subscribe, cache, hasPermission, notify, forceSync]);

  // Demo functions
  const handleSendMessage = () => {
    if (isConnected) {
      send({
        type: 'demo-message',
        payload: {
          message: 'Hello from client!',
          timestamp: new Date().toISOString(),
        },
      });
    }
  };

  const handleQueueApiCall = () => {
    queueSync(
      `demo-api-${Date.now()}`,
      'api-call',
      {
        endpoint: '/api/demo',
        method: 'POST',
        body: {
          message: 'Demo API call',
          timestamp: new Date().toISOString(),
        },
      },
      'medium'
    );
  };

  const handleQueueContactForm = () => {
    queueSync(
      `contact-${Date.now()}`,
      'contact-form',
      {
        name: 'John Doe',
        email: 'john@example.com',
        subject: 'Demo Contact Form',
        message: 'This is a demo contact form submission',
      },
      'high'
    );
  };

  const handleCacheData = () => {
    const demoData = {
      id: Date.now(),
      title: 'Demo Data',
      content: 'This is some demo data that will be cached',
      timestamp: new Date().toISOString(),
    };
    
    cache('demo-data', demoData, 60000); // Cache for 1 minute
    
    notifySuccess('Data cached!', 'Demo data has been cached successfully');
  };

  const handleGetCachedData = () => {
    const cachedData = getCached('demo-data');
    
    if (cachedData) {
      notify('Cached Data Found', `Found cached data: ${JSON.stringify(cachedData)}`);
    } else {
      notify('No Cached Data', 'No cached data found for demo-data key');
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Real-Time Sync & PWA Demo
        </h1>
        <p className="text-gray-600">
          Démonstration complète des fonctionnalités temps réel, synchronisation et PWA
        </p>
      </div>

      {/* Status Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <ConnectionStatus showDetails />
        <SyncStatus showDetails showLastSync />
        <PWAStatus compact />
      </div>

      {/* Demo Controls */}
      <div className="bg-white rounded-lg border shadow-sm p-6">
        <h2 className="text-xl font-semibold mb-4">Demo Controls</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button
            onClick={handleSendMessage}
            disabled={!isConnected}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send Message
          </button>
          
          <button
            onClick={handleQueueApiCall}
            className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
          >
            Queue API Call
          </button>
          
          <button
            onClick={handleQueueContactForm}
            className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
          >
            Queue Contact Form
          </button>
          
          <button
            onClick={handleCacheData}
            className="px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700"
          >
            Cache Demo Data
          </button>
          
          <button
            onClick={handleGetCachedData}
            className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
          >
            Get Cached Data
          </button>
          
          <button
            onClick={() => requestPermission()}
            disabled={hasPermission}
            className="px-4 py-2 bg-yellow-600 text-white rounded-md hover:bg-yellow-700 disabled:opacity-50"
          >
            Request Notifications
          </button>
          
          <button
            onClick={() => showInstallPrompt()}
            disabled={!capabilities.isInstallable}
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
          >
            Install App
          </button>
          
          <button
            onClick={() => forceSync()}
            className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
          >
            Force Sync
          </button>
        </div>
      </div>

      {/* Component Demos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sync Components */}
        <div className="space-y-4">
          <SyncQueue showControls />
        </div>

        {/* Notification & PWA Components */}
        <div className="space-y-4">
          <NotificationCenter
            showPermissionStatus
            showPushStatus={enablePushNotifications}
            allowTestNotifications
          />
        </div>
      </div>

      {/* Full PWA Status */}
      <PWAStatus showCapabilities showInstallPrompt showUpdatePrompt />

      {/* Connection Details */}
      <ConnectionStatus showDetails showRetryInfo />

      {/* Instructions */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">
          Comment utiliser cette démonstration
        </h3>
        <div className="text-sm text-blue-800 space-y-2">
          <p>
            <strong>WebSocket:</strong> Testez la connexion temps réel en envoyant des messages.
            La reconnexion automatique se déclenchera si la connexion est perdue.
          </p>
          <p>
            <strong>Synchronisation:</strong> Ajoutez des éléments à la queue de synchronisation.
            Ils seront traités automatiquement en arrière-plan.
          </p>
          <p>
            <strong>Cache:</strong> Mettez en cache des données localement avec TTL.
            Les données expirées sont automatiquement nettoyées.
          </p>
          <p>
            <strong>Notifications:</strong> Demandez les permissions et testez différents types
            de notifications navigateur.
          </p>
          <p>
            <strong>PWA:</strong> Installez l'application et testez les fonctionnalités hors-ligne.
            Le Service Worker gère automatiquement la mise en cache.
          </p>
        </div>
      </div>
    </div>
  );
};

export default RealTimeAppDemo;