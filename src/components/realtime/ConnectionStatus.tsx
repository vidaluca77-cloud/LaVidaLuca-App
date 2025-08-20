'use client';

import React from 'react';
import { useWebSocket } from '@/hooks/useWebSocket';

interface ConnectionStatusProps {
  className?: string;
  showDetails?: boolean;
}

/**
 * Component that displays the current WebSocket connection status
 */
export const ConnectionStatus: React.FC<ConnectionStatusProps> = ({
  className = '',
  showDetails = false,
}) => {
  const { status, isConnected, connectionTime, error } = useWebSocket();

  const getStatusConfig = () => {
    switch (status) {
      case 'connected':
        return {
          color: 'text-green-600',
          bgColor: 'bg-green-100',
          borderColor: 'border-green-200',
          icon: '🟢',
          label: 'Connecté',
          description: 'Temps réel activé',
        };
      case 'connecting':
        return {
          color: 'text-yellow-600',
          bgColor: 'bg-yellow-100',
          borderColor: 'border-yellow-200',
          icon: '🟡',
          label: 'Connexion...',
          description: 'Établissement de la connexion',
        };
      case 'reconnecting':
        return {
          color: 'text-orange-600',
          bgColor: 'bg-orange-100',
          borderColor: 'border-orange-200',
          icon: '🟠',
          label: 'Reconnexion...',
          description: 'Tentative de reconnexion',
        };
      case 'error':
        return {
          color: 'text-red-600',
          bgColor: 'bg-red-100',
          borderColor: 'border-red-200',
          icon: '🔴',
          label: 'Erreur',
          description: 'Problème de connexion',
        };
      case 'disconnected':
      default:
        return {
          color: 'text-gray-600',
          bgColor: 'bg-gray-100',
          borderColor: 'border-gray-200',
          icon: '⚪',
          label: 'Hors ligne',
          description: 'Mode hors ligne',
        };
    }
  };

  const statusConfig = getStatusConfig();

  const formatConnectionTime = (time: Date | null) => {
    if (!time) return null;
    
    const now = new Date();
    const diff = now.getTime() - time.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    
    if (minutes < 1) return 'Connecté depuis moins d\'une minute';
    if (minutes < 60) return `Connecté depuis ${minutes} minute${minutes > 1 ? 's' : ''}`;
    return `Connecté depuis ${hours} heure${hours > 1 ? 's' : ''}`;
  };

  if (showDetails) {
    return (
      <div className={`${statusConfig.bgColor} ${statusConfig.borderColor} border rounded-lg p-4 ${className}`}>
        <div className="flex items-center space-x-3">
          <span className="text-lg">{statusConfig.icon}</span>
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <h3 className={`text-sm font-medium ${statusConfig.color}`}>
                {statusConfig.label}
              </h3>
              {status === 'connecting' || status === 'reconnecting' ? (
                <div className="flex space-x-1">
                  <div className={`w-2 h-2 ${statusConfig.bgColor} rounded-full animate-pulse`}></div>
                  <div className={`w-2 h-2 ${statusConfig.bgColor} rounded-full animate-pulse`} style={{ animationDelay: '0.2s' }}></div>
                  <div className={`w-2 h-2 ${statusConfig.bgColor} rounded-full animate-pulse`} style={{ animationDelay: '0.4s' }}></div>
                </div>
              ) : null}
            </div>
            <p className="text-sm text-gray-500 mt-1">
              {statusConfig.description}
            </p>
            {isConnected && connectionTime && (
              <p className="text-xs text-gray-400 mt-1">
                {formatConnectionTime(connectionTime)}
              </p>
            )}
            {error && (
              <p className="text-xs text-red-500 mt-1">
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
    <div className={`inline-flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${statusConfig.bgColor} ${statusConfig.borderColor} border ${className}`}>
      <span className="text-xs">{statusConfig.icon}</span>
      <span className={`font-medium ${statusConfig.color}`}>
        {statusConfig.label}
      </span>
      {(status === 'connecting' || status === 'reconnecting') && (
        <div className="flex space-x-1">
          <div className={`w-1 h-1 ${statusConfig.color.replace('text-', 'bg-')} rounded-full animate-pulse`}></div>
          <div className={`w-1 h-1 ${statusConfig.color.replace('text-', 'bg-')} rounded-full animate-pulse`} style={{ animationDelay: '0.3s' }}></div>
          <div className={`w-1 h-1 ${statusConfig.color.replace('text-', 'bg-')} rounded-full animate-pulse`} style={{ animationDelay: '0.6s' }}></div>
        </div>
      )}
    </div>
  );
};

/**
 * Minimal connection indicator (just a dot)
 */
export const ConnectionIndicator: React.FC<{ className?: string }> = ({ className = '' }) => {
  const { status } = useWebSocket();

  const getIndicatorColor = () => {
    switch (status) {
      case 'connected':
        return 'bg-green-500';
      case 'connecting':
      case 'reconnecting':
        return 'bg-yellow-500 animate-pulse';
      case 'error':
        return 'bg-red-500';
      case 'disconnected':
      default:
        return 'bg-gray-400';
    }
  };

  return (
    <div 
      className={`w-3 h-3 rounded-full ${getIndicatorColor()} ${className}`}
      title={`État de connexion: ${status}`}
    />
  );
};

export default ConnectionStatus;