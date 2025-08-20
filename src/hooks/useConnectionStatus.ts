/**
 * Connection Status Hook
 * Tracks online/offline status and queue status
 */

import { useState, useEffect } from 'react';
import { offlineQueue } from '@/lib/offline-queue';

export interface ConnectionStatus {
  isOnline: boolean;
  isOfflineMode: boolean;
  queueLength: number;
  isProcessing: boolean;
  lastOnline: Date | null;
  lastOffline: Date | null;
}

export function useConnectionStatus(): ConnectionStatus {
  const [status, setStatus] = useState<ConnectionStatus>({
    isOnline: true, // Default to true for SSR
    isOfflineMode: false,
    queueLength: 0,
    isProcessing: false,
    lastOnline: null,
    lastOffline: null,
  });

  useEffect(() => {
    if (typeof window === 'undefined') return;

    // Set initial online status
    setStatus(prev => ({ ...prev, isOnline: navigator.onLine }));

    const updateConnectionStatus = () => {
      const queueStatus = offlineQueue.getQueueStatus();
      const isOnline = navigator.onLine;
      
      setStatus(prev => ({
        ...prev,
        isOnline,
        isOfflineMode: !isOnline || queueStatus.length > 0,
        queueLength: queueStatus.length,
        isProcessing: queueStatus.isProcessing,
        lastOnline: isOnline && !prev.isOnline ? new Date() : prev.lastOnline,
        lastOffline: !isOnline && prev.isOnline ? new Date() : prev.lastOffline,
      }));
    };

    // Initial status
    updateConnectionStatus();

    // Listen for online/offline events
    const handleOnline = () => updateConnectionStatus();
    const handleOffline = () => updateConnectionStatus();

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Listen for queue changes
    const handleQueueSync = () => updateConnectionStatus();
    offlineQueue.onSync(handleQueueSync);

    // Periodic status check
    const interval = setInterval(updateConnectionStatus, 5000);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      offlineQueue.offSync(handleQueueSync);
      clearInterval(interval);
    };
  }, []);

  return status;
}