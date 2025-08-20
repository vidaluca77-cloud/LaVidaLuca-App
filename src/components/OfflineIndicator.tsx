'use client';

import React, { useEffect, useState } from 'react';
import { offlineManager, NetworkStatus } from '@/lib/offlineManager';
import { WifiIcon, NoSymbolIcon, CloudIcon } from '@heroicons/react/24/outline';

interface OfflineIndicatorProps {
  className?: string;
  showDetails?: boolean;
}

export default function OfflineIndicator({ className = '', showDetails = false }: OfflineIndicatorProps) {
  const [networkStatus, setNetworkStatus] = useState<NetworkStatus>({ isOnline: true });
  const [syncInProgress, setSyncInProgress] = useState(false);

  useEffect(() => {
    // Get initial status
    setNetworkStatus(offlineManager.getNetworkStatus());

    // Subscribe to network status changes
    const unsubscribe = offlineManager.onNetworkStatusChange((status) => {
      setNetworkStatus(status);
    });

    // Check sync status periodically
    const checkSyncStatus = () => {
      setSyncInProgress(offlineManager.isSyncInProgress());
    };

    const syncInterval = setInterval(checkSyncStatus, 1000);
    checkSyncStatus();

    return () => {
      unsubscribe();
      clearInterval(syncInterval);
    };
  }, []);

  const getStatusIcon = () => {
    if (syncInProgress) {
      return <CloudIcon className="h-5 w-5 animate-pulse text-blue-500" />;
    }
    
    if (networkStatus.isOnline) {
      return <WifiIcon className="h-5 w-5 text-green-500" />;
    }
    
    return <NoSymbolIcon className="h-5 w-5 text-red-500" />;
  };

  const getStatusText = () => {
    if (syncInProgress) {
      return 'Synchronisation...';
    }
    
    if (networkStatus.isOnline) {
      return 'En ligne';
    }
    
    return 'Hors ligne';
  };

  const getDetailedStatus = () => {
    if (!showDetails) return null;

    return (
      <div className="text-xs text-gray-500 mt-1">
        {networkStatus.connectionType && (
          <div>Type: {networkStatus.connectionType}</div>
        )}
        {networkStatus.effectiveType && (
          <div>Vitesse: {networkStatus.effectiveType}</div>
        )}
      </div>
    );
  };

  const baseClasses = "flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium";
  const statusClasses = networkStatus.isOnline 
    ? "bg-green-50 text-green-700 border border-green-200"
    : "bg-red-50 text-red-700 border border-red-200";

  if (syncInProgress) {
    return (
      <div className={`${baseClasses} bg-blue-50 text-blue-700 border border-blue-200 ${className}`}>
        {getStatusIcon()}
        <span>{getStatusText()}</span>
        {getDetailedStatus()}
      </div>
    );
  }

  return (
    <div className={`${baseClasses} ${statusClasses} ${className}`}>
      {getStatusIcon()}
      <span>{getStatusText()}</span>
      {getDetailedStatus()}
    </div>
  );
}