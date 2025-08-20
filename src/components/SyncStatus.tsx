'use client';

import React, { useEffect, useState } from 'react';
import { offlineManager, OfflineData } from '@/lib/offlineManager';
import { ArrowPathIcon, CheckCircleIcon, ExclamationTriangleIcon, ClockIcon } from '@heroicons/react/24/outline';

interface SyncStatusProps {
  className?: string;
}

export default function SyncStatus({ className = '' }: SyncStatusProps) {
  const [pendingData, setPendingData] = useState<OfflineData[]>([]);
  const [syncInProgress, setSyncInProgress] = useState(false);
  const [lastSyncTime, setLastSyncTime] = useState<Date | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {
    loadPendingData();

    // Refresh data periodically
    const interval = setInterval(loadPendingData, 5000);
    
    // Listen for network changes to trigger sync
    const unsubscribe = offlineManager.onNetworkStatusChange((status) => {
      if (status.isOnline) {
        setTimeout(loadPendingData, 1000); // Refresh after potential sync
      }
    });

    return () => {
      clearInterval(interval);
      unsubscribe();
    };
  }, []);

  const loadPendingData = async () => {
    try {
      const pending = await offlineManager.getPendingSyncData();
      setPendingData(pending);
      setSyncInProgress(offlineManager.isSyncInProgress());
      
      // Update last sync time if no pending data and we're online
      if (pending.length === 0 && offlineManager.getNetworkStatus().isOnline) {
        setLastSyncTime(new Date());
      }
    } catch (error) {
      console.error('Error loading pending data:', error);
    }
  };

  const handleManualSync = async () => {
    if (offlineManager.getNetworkStatus().isOnline && !syncInProgress) {
      await offlineManager.syncWhenOnline();
      setTimeout(loadPendingData, 1000);
    }
  };

  const formatRelativeTime = (date: Date) => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    
    if (minutes < 1) return 'À l\'instant';
    if (minutes < 60) return `Il y a ${minutes} min`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `Il y a ${hours}h`;
    const days = Math.floor(hours / 24);
    return `Il y a ${days}j`;
  };

  const getDataTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      'activity': 'Activité',
      'user_profile': 'Profil',
      'comment': 'Commentaire',
      'rating': 'Évaluation',
    };
    return labels[type] || type;
  };

  const getActionLabel = (action: string) => {
    const labels: Record<string, string> = {
      'create': 'Créer',
      'update': 'Modifier',
      'delete': 'Supprimer',
    };
    return labels[action] || action;
  };

  const getSyncStatus = () => {
    if (syncInProgress) {
      return {
        icon: <ArrowPathIcon className="h-5 w-5 animate-spin text-blue-500" />,
        text: 'Synchronisation en cours...',
        bgColor: 'bg-blue-50',
        textColor: 'text-blue-700',
        borderColor: 'border-blue-200'
      };
    }

    if (pendingData.length > 0) {
      return {
        icon: <ClockIcon className="h-5 w-5 text-orange-500" />,
        text: `${pendingData.length} élément(s) en attente`,
        bgColor: 'bg-orange-50',
        textColor: 'text-orange-700',
        borderColor: 'border-orange-200'
      };
    }

    return {
      icon: <CheckCircleIcon className="h-5 w-5 text-green-500" />,
      text: 'Synchronisé',
      bgColor: 'bg-green-50',
      textColor: 'text-green-700',
      borderColor: 'border-green-200'
    };
  };

  const status = getSyncStatus();
  const isOnline = offlineManager.getNetworkStatus().isOnline;

  return (
    <div className={`${className}`}>
      <div
        className={`flex items-center justify-between p-3 rounded-lg border ${status.bgColor} ${status.textColor} ${status.borderColor} cursor-pointer`}
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center gap-3">
          {status.icon}
          <div>
            <div className="font-medium">{status.text}</div>
            {lastSyncTime && pendingData.length === 0 && (
              <div className="text-xs text-gray-500">
                Dernière sync: {formatRelativeTime(lastSyncTime)}
              </div>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2">
          {isOnline && pendingData.length > 0 && !syncInProgress && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleManualSync();
              }}
              className="px-3 py-1 text-xs bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Synchroniser
            </button>
          )}
          
          {!isOnline && (
            <div className="flex items-center gap-1 text-xs">
              <ExclamationTriangleIcon className="h-4 w-4 text-red-500" />
              <span className="text-red-600">Hors ligne</span>
            </div>
          )}

          <div className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`}>
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
      </div>

      {isExpanded && pendingData.length > 0 && (
        <div className="mt-2 space-y-2">
          {pendingData.map((item) => (
            <div
              key={item.id}
              className="flex items-center justify-between p-2 bg-gray-50 rounded-md text-sm"
            >
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-orange-400 rounded-full"></div>
                <span className="font-medium">{getDataTypeLabel(item.type)}</span>
                <span className="text-gray-500">•</span>
                <span className="text-gray-600">{getActionLabel(item.action)}</span>
              </div>
              <div className="text-xs text-gray-500">
                {formatRelativeTime(new Date(item.timestamp))}
              </div>
            </div>
          ))}
        </div>
      )}

      {isExpanded && pendingData.length === 0 && (
        <div className="mt-2 p-3 bg-gray-50 rounded-md text-sm text-gray-600 text-center">
          Aucune donnée en attente de synchronisation
        </div>
      )}
    </div>
  );
}