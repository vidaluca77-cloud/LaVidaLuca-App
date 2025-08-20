/**
 * Offline Indicator Component
 * Shows current offline/online status with visual feedback
 */

'use client';

import React, { useState, useEffect } from 'react';
import { offlineManager, OfflineStatus } from '@/lib/offline/OfflineManager';

interface OfflineIndicatorProps {
  className?: string;
  showText?: boolean;
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'inline';
}

export const OfflineIndicator: React.FC<OfflineIndicatorProps> = ({
  className = '',
  showText = true,
  position = 'top-right'
}) => {
  const [status, setStatus] = useState<OfflineStatus>('online');
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Initialize offline manager
    offlineManager.init();

    // Get current status
    setStatus(offlineManager.getStatus());

    // Listen for status changes
    const unsubscribe = offlineManager.addStatusListener((newStatus) => {
      setStatus(newStatus);
      
      // Show indicator when offline or syncing
      setIsVisible(newStatus !== 'online');
    });

    return unsubscribe;
  }, []);

  // Don't show indicator when online (unless inline)
  if (!isVisible && position !== 'inline') {
    return null;
  }

  const getStatusConfig = (status: OfflineStatus) => {
    switch (status) {
      case 'offline':
        return {
          color: 'bg-red-500',
          text: 'Offline',
          icon: '⚠️',
          description: 'You are currently offline. Actions will be saved and synced when connection is restored.'
        };
      case 'syncing':
        return {
          color: 'bg-yellow-500',
          text: 'Syncing',
          icon: '🔄',
          description: 'Syncing your offline actions...'
        };
      case 'online':
      default:
        return {
          color: 'bg-green-500',
          text: 'Online',
          icon: '✅',
          description: 'You are connected and all actions are being saved immediately.'
        };
    }
  };

  const config = getStatusConfig(status);

  const getPositionClasses = () => {
    if (position === 'inline') return '';
    
    const base = 'fixed z-50';
    switch (position) {
      case 'top-left':
        return `${base} top-4 left-4`;
      case 'top-right':
        return `${base} top-4 right-4`;
      case 'bottom-left':
        return `${base} bottom-4 left-4`;
      case 'bottom-right':
        return `${base} bottom-4 right-4`;
      default:
        return `${base} top-4 right-4`;
    }
  };

  const indicatorClasses = [
    'flex items-center gap-2 px-3 py-2 rounded-lg shadow-lg text-white text-sm font-medium',
    'transition-all duration-300 ease-in-out',
    config.color,
    getPositionClasses(),
    className
  ].filter(Boolean).join(' ');

  return (
    <div 
      className={indicatorClasses}
      title={config.description}
      role="status"
      aria-live="polite"
      aria-label={`Connection status: ${config.text}`}
    >
      <span className="text-lg" role="img" aria-hidden="true">
        {config.icon}
      </span>
      
      {showText && (
        <span>{config.text}</span>
      )}

      {status === 'syncing' && (
        <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
      )}
    </div>
  );
};

export default OfflineIndicator;