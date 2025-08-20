/**
 * Connection Status Indicator Component
 * Shows online/offline status and queue information
 */

'use client';

import React from 'react';
import { useConnectionStatus } from '@/hooks/useConnectionStatus';
import { WifiIcon, CloudArrowUpIcon, ClockIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

interface ConnectionStatusIndicatorProps {
  className?: string;
  showDetails?: boolean;
}

export const ConnectionStatusIndicator: React.FC<ConnectionStatusIndicatorProps> = ({
  className = '',
  showDetails = false,
}) => {
  const status = useConnectionStatus();

  const getStatusColor = () => {
    if (status.isOnline && status.queueLength === 0) return 'text-green-500 bg-green-50';
    if (status.isOnline && status.queueLength > 0) return 'text-yellow-500 bg-yellow-50';
    return 'text-red-500 bg-red-50';
  };

  const getStatusIcon = () => {
    if (status.isOnline && status.queueLength === 0) {
      return <WifiIcon className="w-4 h-4" />;
    }
    if (status.isOnline && status.queueLength > 0) {
      return <CloudArrowUpIcon className="w-4 h-4" />;
    }
    return <ExclamationTriangleIcon className="w-4 h-4" />;
  };

  const getStatusText = () => {
    if (status.isOnline && status.queueLength === 0) return 'En ligne';
    if (status.isOnline && status.queueLength > 0) return 'Synchronisation';
    return 'Hors ligne';
  };

  const formatLastSeen = (date: Date | null) => {
    if (!date) return null;
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    
    if (diff < 60000) return 'À l\'instant';
    if (diff < 3600000) return `Il y a ${Math.floor(diff / 60000)} min`;
    if (diff < 86400000) return `Il y a ${Math.floor(diff / 3600000)} h`;
    return `Il y a ${Math.floor(diff / 86400000)} j`;
  };

  return (
    <div className={`inline-flex items-center ${className}`}>
      <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm font-medium ${getStatusColor()}`}>
        {getStatusIcon()}
        <span>{getStatusText()}</span>
        
        {status.isProcessing && (
          <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-current"></div>
        )}
        
        {status.queueLength > 0 && (
          <span className="inline-flex items-center justify-center px-2 py-0.5 text-xs font-bold leading-none text-white bg-red-500 rounded-full">
            {status.queueLength}
          </span>
        )}
      </div>

      {showDetails && (
        <div className="ml-3 text-xs text-gray-500">
          {status.isOnline ? (
            <div>
              {status.lastOffline && (
                <div>Dernière déconnexion: {formatLastSeen(status.lastOffline)}</div>
              )}
              {status.queueLength > 0 && (
                <div>{status.queueLength} action(s) en attente</div>
              )}
            </div>
          ) : (
            <div>
              {status.lastOnline && (
                <div>Dernière connexion: {formatLastSeen(status.lastOnline)}</div>
              )}
              <div>{status.queueLength} action(s) en file d'attente</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

interface OfflineNotificationProps {
  onRetry?: () => void;
  onDismiss?: () => void;
}

export const OfflineNotification: React.FC<OfflineNotificationProps> = ({
  onRetry,
  onDismiss,
}) => {
  const status = useConnectionStatus();

  if (status.isOnline && status.queueLength === 0) {
    return null;
  }

  return (
    <div className="fixed top-4 right-4 z-50 max-w-sm">
      <div className={`rounded-lg shadow-lg p-4 ${
        status.isOnline 
          ? 'bg-yellow-50 border border-yellow-200' 
          : 'bg-red-50 border border-red-200'
      }`}>
        <div className="flex items-start">
          <div className="flex-shrink-0">
            {status.isOnline ? (
              <CloudArrowUpIcon className="w-5 h-5 text-yellow-400" />
            ) : (
              <ExclamationTriangleIcon className="w-5 h-5 text-red-400" />
            )}
          </div>
          
          <div className="ml-3 flex-1">
            <h3 className={`text-sm font-medium ${
              status.isOnline ? 'text-yellow-800' : 'text-red-800'
            }`}>
              {status.isOnline ? 'Synchronisation en cours' : 'Mode hors ligne'}
            </h3>
            
            <p className={`mt-1 text-sm ${
              status.isOnline ? 'text-yellow-700' : 'text-red-700'
            }`}>
              {status.isOnline 
                ? `${status.queueLength} action(s) en cours de synchronisation.`
                : `Vous êtes hors ligne. ${status.queueLength} action(s) seront synchronisées lors de la reconnexion.`
              }
            </p>
            
            {!status.isOnline && onRetry && (
              <div className="mt-3">
                <button
                  onClick={onRetry}
                  className="text-sm font-medium text-red-800 hover:text-red-900 underline"
                >
                  Réessayer la connexion
                </button>
              </div>
            )}
          </div>
          
          {onDismiss && (
            <div className="ml-3 flex-shrink-0">
              <button
                onClick={onDismiss}
                className={`inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                  status.isOnline
                    ? 'text-yellow-500 hover:bg-yellow-100 focus:ring-yellow-600'
                    : 'text-red-500 hover:bg-red-100 focus:ring-red-600'
                }`}
              >
                <span className="sr-only">Fermer</span>
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

interface OfflineBannerProps {
  onSync?: () => void;
}

export const OfflineBanner: React.FC<OfflineBannerProps> = ({ onSync }) => {
  const status = useConnectionStatus();

  if (status.isOnline) {
    return null;
  }

  return (
    <div className="bg-red-600 text-white">
      <div className="max-w-7xl mx-auto py-2 px-3 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between flex-wrap">
          <div className="w-0 flex-1 flex items-center">
            <span className="flex p-2 rounded-lg bg-red-800">
              <ExclamationTriangleIcon className="h-5 w-5 text-white" />
            </span>
            <p className="ml-3 font-medium text-white">
              <span>
                Mode hors ligne activé. {status.queueLength} action(s) en attente de synchronisation.
              </span>
            </p>
          </div>
          
          {onSync && (
            <div className="order-3 mt-2 flex-shrink-0 w-full sm:order-2 sm:mt-0 sm:w-auto">
              <button
                onClick={onSync}
                className="flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-red-600 bg-white hover:bg-red-50"
              >
                <ClockIcon className="h-4 w-4 mr-1" />
                Synchroniser maintenant
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};