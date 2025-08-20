'use client';

import React, { useState, useEffect } from 'react';
import { WifiIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

interface OfflineIndicatorProps {
  className?: string;
  showWhenOnline?: boolean;
}

export const OfflineIndicator: React.FC<OfflineIndicatorProps> = ({ 
  className = '', 
  showWhenOnline = false 
}) => {
  const [isOnline, setIsOnline] = useState(true);
  const [showNotification, setShowNotification] = useState(false);

  useEffect(() => {
    // Set initial state
    setIsOnline(navigator.onLine);

    const handleOnline = () => {
      setIsOnline(true);
      setShowNotification(true);
      // Hide notification after 3 seconds
      setTimeout(() => setShowNotification(false), 3000);
    };

    const handleOffline = () => {
      setIsOnline(false);
      setShowNotification(true);
    };

    // Add event listeners
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Cleanup
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Don't show anything if online and showWhenOnline is false
  if (isOnline && !showWhenOnline && !showNotification) {
    return null;
  }

  return (
    <div className={`fixed top-4 right-4 z-50 ${className}`}>
      {/* Status indicator */}
      <div
        className={`
          flex items-center gap-2 px-4 py-2 rounded-lg shadow-lg transition-all duration-300 text-sm font-medium
          ${isOnline 
            ? 'bg-green-500 text-white' 
            : 'bg-red-500 text-white'
          }
          ${showNotification ? 'opacity-100 translate-y-0' : 'opacity-70 -translate-y-1'}
        `}
      >
        {isOnline ? (
          <>
            <WifiIcon className="w-4 h-4" />
            <span>En ligne</span>
          </>
        ) : (
          <>
            <ExclamationTriangleIcon className="w-4 h-4" />
            <span>Mode hors ligne</span>
          </>
        )}
      </div>

      {/* Detailed offline message */}
      {!isOnline && (
        <div className="mt-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg text-sm text-yellow-800">
          <p className="font-medium mb-1">Fonctionnalités limitées</p>
          <p className="text-xs">
            Certaines fonctions nécessitent une connexion internet. 
            Vos actions seront synchronisées dès que la connexion sera rétablie.
          </p>
        </div>
      )}
    </div>
  );
};

export default OfflineIndicator;