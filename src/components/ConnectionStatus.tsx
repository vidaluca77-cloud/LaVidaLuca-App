/**
 * Connection Status component to show network state
 */

'use client';

import React from 'react';
import { useConnectionStatus } from '@/hooks/useConnectionStatus';
import { 
  WifiIcon, 
  NoSymbolIcon, 
  SignalIcon,
  ClockIcon 
} from '@heroicons/react/24/outline';

interface ConnectionStatusProps {
  showDetails?: boolean;
  className?: string;
}

export function ConnectionStatus({ showDetails = false, className = '' }: ConnectionStatusProps) {
  const { isOnline, isSlowConnection, effectiveType, downlink, rtt } = useConnectionStatus();

  const getConnectionIcon = () => {
    if (!isOnline) {
      return <NoSymbolIcon className="h-4 w-4 text-red-500" />;
    }
    if (isSlowConnection) {
      return <SignalIcon className="h-4 w-4 text-amber-500" />;
    }
    return <WifiIcon className="h-4 w-4 text-green-500" />;
  };

  const getConnectionStatus = () => {
    if (!isOnline) return 'Hors ligne';
    if (isSlowConnection) return 'Connexion lente';
    return 'En ligne';
  };

  const getConnectionColor = () => {
    if (!isOnline) return 'text-red-600';
    if (isSlowConnection) return 'text-amber-600';
    return 'text-green-600';
  };

  if (!showDetails) {
    return (
      <div className={`inline-flex items-center gap-1 ${className}`} title={getConnectionStatus()}>
        {getConnectionIcon()}
        <span className={`text-xs font-medium ${getConnectionColor()}`}>
          {getConnectionStatus()}
        </span>
      </div>
    );
  }

  return (
    <div className={`bg-white border border-gray-200 rounded-lg p-4 ${className}`}>
      <div className="flex items-center gap-2 mb-3">
        {getConnectionIcon()}
        <h3 className="text-sm font-medium text-gray-900">État de la connexion</h3>
      </div>

      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-600">Statut:</span>
          <span className={`font-medium ${getConnectionColor()}`}>
            {getConnectionStatus()}
          </span>
        </div>

        {isOnline && (
          <>
            <div className="flex justify-between">
              <span className="text-gray-600">Type:</span>
              <span className="text-gray-900 font-mono text-xs">
                {effectiveType || 'Inconnu'}
              </span>
            </div>

            {downlink && (
              <div className="flex justify-between">
                <span className="text-gray-600">Débit:</span>
                <span className="text-gray-900 font-mono text-xs">
                  {downlink.toFixed(1)} Mbps
                </span>
              </div>
            )}

            {rtt && (
              <div className="flex justify-between">
                <span className="text-gray-600">Latence:</span>
                <span className="text-gray-900 font-mono text-xs">
                  {rtt} ms
                </span>
              </div>
            )}
          </>
        )}

        {!isOnline && (
          <div className="flex items-center gap-1 mt-2 p-2 bg-red-50 rounded text-red-700">
            <ClockIcon className="h-4 w-4" />
            <span className="text-xs">
              Les données seront synchronisées quand la connexion sera rétablie
            </span>
          </div>
        )}

        {isSlowConnection && (
          <div className="flex items-center gap-1 mt-2 p-2 bg-amber-50 rounded text-amber-700">
            <SignalIcon className="h-4 w-4" />
            <span className="text-xs">
              Le chargement peut être plus lent que d'habitude
            </span>
          </div>
        )}
      </div>
    </div>
  );
}

export default ConnectionStatus;