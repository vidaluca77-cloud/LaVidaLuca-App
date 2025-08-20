/**
 * ConnectionStatus component for displaying real-time connection status
 */

'use client';

import React from 'react';
import { useWebSocketStatus } from '@/hooks/useWebSocket';

export interface ConnectionStatusProps {
  className?: string;
  showDetails?: boolean;
  compact?: boolean;
  showRetryInfo?: boolean;
}

export const ConnectionStatus: React.FC<ConnectionStatusProps> = ({
  className = '',
  showDetails = false,
  compact = false,
  showRetryInfo = true,
}) => {
  const { isConnected, isConnecting, reconnectAttempts, queuedMessages } = useWebSocketStatus();

  const getStatusColor = () => {
    if (isConnected) return 'text-green-500';
    if (isConnecting) return 'text-blue-500';
    return 'text-red-500';
  };

  const getStatusBgColor = () => {
    if (isConnected) return 'bg-green-50 border-green-200';
    if (isConnecting) return 'bg-blue-50 border-blue-200';
    return 'bg-red-50 border-red-200';
  };

  const getStatusIcon = () => {
    if (isConnected) return '🟢';
    if (isConnecting) return '🔄';
    return '🔴';
  };

  const getStatusText = () => {
    if (isConnected) return 'Connected';
    if (isConnecting) {
      if (reconnectAttempts > 0) {
        return `Reconnecting (${reconnectAttempts})`;
      }
      return 'Connecting';
    }
    return 'Disconnected';
  };

  const getStatusDescription = () => {
    if (isConnected) return 'Real-time updates active';
    if (isConnecting) return 'Establishing connection...';
    return 'Real-time updates unavailable';
  };

  if (compact) {
    return (
      <div className={`flex items-center space-x-2 ${className}`}>
        <span className="text-sm">{getStatusIcon()}</span>
        <span className={`text-xs font-medium ${getStatusColor()}`}>
          {getStatusText()}
        </span>
        {queuedMessages > 0 && (
          <span className="text-xs bg-orange-100 text-orange-800 px-2 py-0.5 rounded-full">
            {queuedMessages} queued
          </span>
        )}
      </div>
    );
  }

  return (
    <div className={`p-4 rounded-lg border ${getStatusBgColor()} ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2">
            <span className="text-lg">{getStatusIcon()}</span>
            <div>
              <div className={`font-semibold ${getStatusColor()}`}>
                {getStatusText()}
              </div>
              <div className="text-sm text-gray-600">
                {getStatusDescription()}
              </div>
            </div>
          </div>

          {/* Connecting animation */}
          {isConnecting && (
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
            </div>
          )}
        </div>

        {showDetails && (
          <div className="flex items-center space-x-4 text-xs">
            {queuedMessages > 0 && (
              <div className="text-center">
                <div className="font-semibold text-orange-600">{queuedMessages}</div>
                <div className="text-gray-600">Queued</div>
              </div>
            )}

            {reconnectAttempts > 0 && showRetryInfo && (
              <div className="text-center">
                <div className="font-semibold text-blue-600">{reconnectAttempts}</div>
                <div className="text-gray-600">Retries</div>
              </div>
            )}

            <div className="flex items-center space-x-1">
              <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className="text-gray-600">WebSocket</span>
            </div>
          </div>
        )}
      </div>

      {/* Additional status information */}
      {showDetails && (
        <div className="mt-3 pt-3 border-t border-gray-200">
          <div className="grid grid-cols-2 gap-4 text-xs">
            <div>
              <span className="text-gray-600">Status:</span>
              <span className={`ml-1 font-medium ${getStatusColor()}`}>
                {isConnected ? 'Online' : isConnecting ? 'Connecting' : 'Offline'}
              </span>
            </div>
            
            <div>
              <span className="text-gray-600">Mode:</span>
              <span className="ml-1 font-medium text-gray-900">
                Real-time
              </span>
            </div>

            {queuedMessages > 0 && (
              <div className="col-span-2">
                <span className="text-gray-600">Queue:</span>
                <span className="ml-1 font-medium text-orange-600">
                  {queuedMessages} message{queuedMessages > 1 ? 's' : ''} pending
                </span>
              </div>
            )}

            {!isConnected && !isConnecting && (
              <div className="col-span-2">
                <span className="text-gray-600">Info:</span>
                <span className="ml-1 text-red-600">
                  Messages will be queued until connection is restored
                </span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Reconnecting message */}
      {isConnecting && reconnectAttempts > 0 && (
        <div className="mt-3 p-2 bg-blue-100 rounded-md">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            <span className="text-sm text-blue-800">
              Attempting to reconnect... (Attempt {reconnectAttempts})
            </span>
          </div>
        </div>
      )}

      {/* Disconnected warning */}
      {!isConnected && !isConnecting && (
        <div className="mt-3 p-2 bg-red-100 rounded-md">
          <div className="flex items-center space-x-2">
            <span className="text-red-600">⚠️</span>
            <span className="text-sm text-red-800">
              Connection lost. Real-time updates are disabled.
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default ConnectionStatus;