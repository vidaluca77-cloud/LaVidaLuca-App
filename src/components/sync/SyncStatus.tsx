/**
 * SyncStatus component for displaying synchronization status
 */

'use client';

import React from 'react';
import { useSync } from '@/hooks/useSync';

export interface SyncStatusProps {
  className?: string;
  showDetails?: boolean;
  showLastSync?: boolean;
  compact?: boolean;
}

export const SyncStatus: React.FC<SyncStatusProps> = ({
  className = '',
  showDetails = false,
  showLastSync = true,
  compact = false,
}) => {
  const { status, isOnline } = useSync({ autoInitialize: false });

  const getStatusColor = () => {
    if (!isOnline) return 'text-red-500';
    if (status.syncing > 0) return 'text-blue-500';
    if (status.failed > 0) return 'text-yellow-500';
    if (status.pending > 0) return 'text-orange-500';
    return 'text-green-500';
  };

  const getStatusIcon = () => {
    if (!isOnline) return '🔴';
    if (status.syncing > 0) return '🔄';
    if (status.failed > 0) return '⚠️';
    if (status.pending > 0) return '⏳';
    return '✅';
  };

  const getStatusText = () => {
    if (!isOnline) return 'Offline';
    if (status.syncing > 0) return 'Syncing';
    if (status.failed > 0) return 'Sync Issues';
    if (status.pending > 0) return 'Pending Sync';
    return 'Synced';
  };

  const formatLastSync = (date: Date | null) => {
    if (!date) return 'Never';
    
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / (1000 * 60));
    
    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
  };

  if (compact) {
    return (
      <div className={`flex items-center space-x-1 ${className}`}>
        <span className={`text-sm ${getStatusColor()}`}>
          {getStatusIcon()}
        </span>
        <span className={`text-xs ${getStatusColor()}`}>
          {getStatusText()}
        </span>
      </div>
    );
  }

  return (
    <div className={`flex items-center justify-between p-3 bg-gray-50 rounded-lg border ${className}`}>
      <div className="flex items-center space-x-3">
        <div className={`flex items-center space-x-2 ${getStatusColor()}`}>
          <span className="text-lg">{getStatusIcon()}</span>
          <span className="font-medium">{getStatusText()}</span>
        </div>
        
        {showLastSync && status.lastSyncTime && (
          <span className="text-xs text-gray-500">
            Last sync: {formatLastSync(status.lastSyncTime)}
          </span>
        )}
      </div>

      {showDetails && (
        <div className="flex items-center space-x-4 text-xs text-gray-600">
          {status.pending > 0 && (
            <span className="bg-orange-100 text-orange-800 px-2 py-1 rounded-full">
              {status.pending} pending
            </span>
          )}
          
          {status.syncing > 0 && (
            <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
              {status.syncing} syncing
            </span>
          )}
          
          {status.failed > 0 && (
            <span className="bg-red-100 text-red-800 px-2 py-1 rounded-full">
              {status.failed} failed
            </span>
          )}
          
          <span className="bg-gray-100 text-gray-800 px-2 py-1 rounded-full">
            Cache: {status.cacheSize}
          </span>
        </div>
      )}
    </div>
  );
};

export default SyncStatus;