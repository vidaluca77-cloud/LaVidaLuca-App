/**
 * Connection status hook for tracking online/offline state
 */

'use client';

import { useState, useEffect } from 'react';
import { logger } from '@/lib/logger';

export interface ConnectionStatus {
  isOnline: boolean;
  isSlowConnection: boolean;
  effectiveType: string;
  downlink?: number;
  rtt?: number;
}

export function useConnectionStatus(): ConnectionStatus {
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>(() => {
    if (typeof window === 'undefined') {
      return {
        isOnline: true,
        isSlowConnection: false,
        effectiveType: 'unknown'
      };
    }

    const connection = (navigator as any).connection || 
                      (navigator as any).mozConnection || 
                      (navigator as any).webkitConnection;

    return {
      isOnline: navigator.onLine,
      isSlowConnection: connection?.effectiveType === 'slow-2g' || connection?.effectiveType === '2g',
      effectiveType: connection?.effectiveType || 'unknown',
      downlink: connection?.downlink,
      rtt: connection?.rtt
    };
  });

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const updateConnectionStatus = () => {
      const connection = (navigator as any).connection || 
                        (navigator as any).mozConnection || 
                        (navigator as any).webkitConnection;

      const newStatus: ConnectionStatus = {
        isOnline: navigator.onLine,
        isSlowConnection: connection?.effectiveType === 'slow-2g' || connection?.effectiveType === '2g',
        effectiveType: connection?.effectiveType || 'unknown',
        downlink: connection?.downlink,
        rtt: connection?.rtt
      };

      setConnectionStatus(prevStatus => {
        // Log connection changes
        if (prevStatus.isOnline !== newStatus.isOnline) {
          logger.info(`Connection status changed: ${newStatus.isOnline ? 'online' : 'offline'}`, {
            effectiveType: newStatus.effectiveType,
            downlink: newStatus.downlink,
            rtt: newStatus.rtt
          });
        }

        return newStatus;
      });
    };

    // Listen for online/offline events
    window.addEventListener('online', updateConnectionStatus);
    window.addEventListener('offline', updateConnectionStatus);

    // Listen for connection changes if supported
    const connection = (navigator as any).connection || 
                      (navigator as any).mozConnection || 
                      (navigator as any).webkitConnection;

    if (connection) {
      connection.addEventListener('change', updateConnectionStatus);
    }

    // Initial check
    updateConnectionStatus();

    return () => {
      window.removeEventListener('online', updateConnectionStatus);
      window.removeEventListener('offline', updateConnectionStatus);
      
      if (connection) {
        connection.removeEventListener('change', updateConnectionStatus);
      }
    };
  }, []);

  return connectionStatus;
}