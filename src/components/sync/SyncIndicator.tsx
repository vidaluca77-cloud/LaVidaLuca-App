'use client';

import { useState, useEffect } from 'react';
import { useSync } from '@/hooks/useSync';

interface SyncIndicatorProps {
  className?: string;
  showDetails?: boolean;
  position?: 'fixed' | 'static';
}

/**
 * Visual indicator for sync status and offline state
 */
export const SyncIndicator: React.FC<SyncIndicatorProps> = ({
  className = '',
  showDetails = false,
  position = 'static',
}) => {
  const { 
    status, 
    isOnline, 
    lastSync, 
    pendingChanges, 
    failedChanges,
    error 
  } = useSync();
  
  const [showTooltip, setShowTooltip] = useState(false);

  const getSyncConfig = () => {
    if (!isOnline) {
      return {
        color: 'text-gray-600',
        bgColor: 'bg-gray-100',
        borderColor: 'border-gray-300',
        icon: '⚪',
        label: 'Hors ligne',
        description: 'Données en mode local',
        pulseColor: '',
      };
    }

    switch (status) {
      case 'syncing':
        return {
          color: 'text-blue-600',
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200',
          icon: '🔄',
          label: 'Synchronisation...',
          description: 'Mise à jour des données',
          pulseColor: 'bg-blue-400',
        };
      case 'success':
        return {
          color: 'text-green-600',
          bgColor: 'bg-green-50',
          borderColor: 'border-green-200',
          icon: '✅',
          label: 'Synchronisé',
          description: 'Données à jour',
          pulseColor: '',
        };
      case 'error':
        return {
          color: 'text-red-600',
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200',
          icon: '❌',
          label: 'Erreur',
          description: 'Problème de synchronisation',
          pulseColor: '',
        };
      case 'conflict':
        return {
          color: 'text-orange-600',
          bgColor: 'bg-orange-50',
          borderColor: 'border-orange-200',
          icon: '⚠️',
          label: 'Conflit',
          description: 'Données en conflit',
          pulseColor: '',
        };
      case 'idle':
      default:
        return {
          color: 'text-gray-600',
          bgColor: 'bg-gray-50',
          borderColor: 'border-gray-200',
          icon: '⏸️',
          label: 'En attente',
          description: 'Prêt à synchroniser',
          pulseColor: '',
        };
    }
  };

  const syncConfig = getSyncConfig();

  const formatLastSync = (date: Date | null) => {
    if (!date) return 'Jamais synchronisé';
    
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    
    if (minutes < 1) return 'Synchronisé à l\'instant';
    if (minutes < 60) return `Synchronisé il y a ${minutes}min`;
    if (hours < 24) return `Synchronisé il y a ${hours}h`;
    return `Synchronisé le ${date.toLocaleDateString()}`;
  };

  const baseClasses = position === 'fixed' 
    ? 'fixed bottom-4 right-4 z-50' 
    : '';

  if (showDetails) {
    return (
      <div className={`${syncConfig.bgColor} ${syncConfig.borderColor} border rounded-lg p-3 ${baseClasses} ${className}`}>
        <div className="flex items-center space-x-3">
          <div className="relative">
            <span className="text-lg">{syncConfig.icon}</span>
            {status === 'syncing' && (
              <div className={`absolute -top-1 -right-1 w-3 h-3 ${syncConfig.pulseColor} rounded-full animate-ping`}></div>
            )}
          </div>
          
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <h4 className={`text-sm font-medium ${syncConfig.color}`}>
                {syncConfig.label}
              </h4>
              {(pendingChanges > 0 || failedChanges > 0) && (
                <div className="flex space-x-2 text-xs">
                  {pendingChanges > 0 && (
                    <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                      {pendingChanges} en attente
                    </span>
                  )}
                  {failedChanges > 0 && (
                    <span className="bg-red-100 text-red-800 px-2 py-1 rounded-full">
                      {failedChanges} échec(s)
                    </span>
                  )}
                </div>
              )}
            </div>
            
            <p className="text-sm text-gray-500 mt-1">
              {syncConfig.description}
            </p>
            
            {lastSync && (
              <p className="text-xs text-gray-400 mt-1">
                {formatLastSync(lastSync)}
              </p>
            )}
            
            {error && (
              <p className="text-xs text-red-500 mt-1 truncate" title={error}>
                {error}
              </p>
            )}
          </div>
        </div>
      </div>
    );
  }

  // Compact version
  return (
    <div 
      className={`relative inline-flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${syncConfig.bgColor} ${syncConfig.borderColor} border cursor-pointer ${baseClasses} ${className}`}
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      <div className="relative">
        <span className="text-xs">{syncConfig.icon}</span>
        {status === 'syncing' && (
          <div className={`absolute -top-1 -right-1 w-2 h-2 ${syncConfig.pulseColor} rounded-full animate-ping`}></div>
        )}
      </div>
      
      <span className={`font-medium ${syncConfig.color}`}>
        {syncConfig.label}
      </span>
      
      {(pendingChanges > 0 || failedChanges > 0) && (
        <span className="bg-yellow-400 text-yellow-900 text-xs px-1.5 py-0.5 rounded-full font-medium">
          {pendingChanges + failedChanges}
        </span>
      )}

      {/* Tooltip */}
      {showTooltip && (
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg whitespace-nowrap z-50">
          <div className="text-center">
            <div className="font-medium">{syncConfig.description}</div>
            {lastSync && (
              <div className="text-gray-300 mt-1">{formatLastSync(lastSync)}</div>
            )}
            {error && (
              <div className="text-red-300 mt-1">{error}</div>
            )}
          </div>
          {/* Arrow */}
          <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-gray-900"></div>
        </div>
      )}
    </div>
  );
};

export default SyncIndicator;