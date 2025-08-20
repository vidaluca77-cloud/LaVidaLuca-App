/**
 * Offline Status Indicator Component
 * Shows current online/offline status and sync information
 */

'use client';

import React, { useState, useEffect } from 'react';
import { WifiIcon, ExclamationTriangleIcon, CloudArrowUpIcon, CheckCircleIcon } from '@heroicons/react/24/outline';
import { offlineManager } from '@/lib/offlineManager';
import { logger } from '@/lib/logger';

interface OfflineStatusProps {
  className?: string;
  showDetails?: boolean;
}

interface SyncStatus {
  isOnline: boolean;
  isSyncing: boolean;
  lastSync: number | null;
  pendingCount: number;
  hasConflicts: boolean;
}

export const OfflineStatus: React.FC<OfflineStatusProps> = ({ 
  className = '', 
  showDetails = false 
}) => {
  const [status, setStatus] = useState<SyncStatus>({
    isOnline: typeof navigator !== 'undefined' ? navigator.onLine : true,
    isSyncing: false,
    lastSync: null,
    pendingCount: 0,
    hasConflicts: false
  });

  useEffect(() => {
    // Update online status
    const updateOnlineStatus = () => {
      setStatus(prev => ({ ...prev, isOnline: navigator.onLine }));
    };

    // Update sync status
    const updateSyncStatus = async () => {
      try {
        const activitiesStatus = await offlineManager.getSyncStatus('activities');
        const profilesStatus = await offlineManager.getSyncStatus('userProfiles');
        
        setStatus(prev => ({
          ...prev,
          pendingCount: activitiesStatus.pending + profilesStatus.pending,
          hasConflicts: activitiesStatus.conflicts > 0 || profilesStatus.conflicts > 0
        }));
      } catch (error) {
        logger.error('Failed to get sync status', { error });
      }
    };

    // Set up event listeners
    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);

    // Set up sync event listener
    const handleSyncResult = (result: any) => {
      setStatus(prev => ({
        ...prev,
        isSyncing: false,
        lastSync: Date.now(),
        pendingCount: Math.max(0, prev.pendingCount - result.synced)
      }));
    };

    offlineManager.onSync(handleSyncResult);

    // Initial status update
    updateSyncStatus();

    // Periodic status updates
    const interval = setInterval(updateSyncStatus, 30000); // Every 30 seconds

    return () => {
      window.removeEventListener('online', updateOnlineStatus);
      window.removeEventListener('offline', updateOnlineStatus);
      offlineManager.offSync(handleSyncResult);
      clearInterval(interval);
    };
  }, []);

  const handleSyncNow = async () => {
    if (status.isSyncing || !status.isOnline) return;

    setStatus(prev => ({ ...prev, isSyncing: true }));
    
    try {
      await offlineManager.synchronize();
    } catch (error) {
      logger.error('Manual sync failed', { error });
      setStatus(prev => ({ ...prev, isSyncing: false }));
    }
  };

  const getStatusIcon = () => {
    if (!status.isOnline) {
      return <WifiIcon className="h-5 w-5 text-red-500" />;
    }
    
    if (status.isSyncing) {
      return <CloudArrowUpIcon className="h-5 w-5 text-blue-500 animate-pulse" />;
    }
    
    if (status.hasConflicts) {
      return <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500" />;
    }
    
    if (status.pendingCount > 0) {
      return <CloudArrowUpIcon className="h-5 w-5 text-orange-500" />;
    }
    
    return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
  };

  const getStatusText = () => {
    if (!status.isOnline) {
      return 'Hors ligne';
    }
    
    if (status.isSyncing) {
      return 'Synchronisation...';
    }
    
    if (status.hasConflicts) {
      return 'Conflits détectés';
    }
    
    if (status.pendingCount > 0) {
      return `${status.pendingCount} en attente`;
    }
    
    return 'Synchronisé';
  };

  const getStatusColor = () => {
    if (!status.isOnline) return 'text-red-600 bg-red-50 border-red-200';
    if (status.isSyncing) return 'text-blue-600 bg-blue-50 border-blue-200';
    if (status.hasConflicts) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    if (status.pendingCount > 0) return 'text-orange-600 bg-orange-50 border-orange-200';
    return 'text-green-600 bg-green-50 border-green-200';
  };

  const formatLastSync = () => {
    if (!status.lastSync) return 'Jamais';
    
    const now = Date.now();
    const diff = now - status.lastSync;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    
    if (minutes < 1) return 'À l\'instant';
    if (minutes < 60) return `Il y a ${minutes}min`;
    if (hours < 24) return `Il y a ${hours}h`;
    return 'Il y a plus de 24h';
  };

  return (
    <div className={`inline-flex items-center ${className}`}>
      <div className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg border text-sm font-medium transition-colors ${getStatusColor()}`}>
        {getStatusIcon()}
        <span>{getStatusText()}</span>
        
        {showDetails && status.isOnline && status.pendingCount > 0 && !status.isSyncing && (
          <button
            onClick={handleSyncNow}
            className="ml-2 text-xs underline hover:no-underline focus:outline-none"
            title="Synchroniser maintenant"
          >
            Sync
          </button>
        )}
      </div>
      
      {showDetails && (
        <div className="ml-3 text-xs text-gray-500">
          Dernière sync: {formatLastSync()}
        </div>
      )}
    </div>
  );
};

export default OfflineStatus;