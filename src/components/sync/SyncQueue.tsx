/**
 * SyncQueue component for managing sync queue operations
 */

'use client';

import React, { useState } from 'react';
import { useSyncQueue } from '@/hooks/useSync';

export interface SyncQueueProps {
  className?: string;
  showControls?: boolean;
  autoRefresh?: boolean;
}

export const SyncQueue: React.FC<SyncQueueProps> = ({
  className = '',
  showControls = true,
  autoRefresh = true,
}) => {
  const {
    queueSize,
    pendingItems,
    failedItems,
    isProcessing,
    clearQueue,
    forceSync,
  } = useSyncQueue();

  const [isForcing, setIsForcing] = useState(false);

  const handleForceSync = async () => {
    if (isForcing) return;
    
    setIsForcing(true);
    try {
      await forceSync();
    } catch (error) {
      console.error('Error forcing sync:', error);
    } finally {
      setIsForcing(false);
    }
  };

  const handleClearQueue = () => {
    if (window.confirm('Are you sure you want to clear the sync queue? This will remove all pending items.')) {
      clearQueue();
    }
  };

  const getQueueStatusColor = () => {
    if (failedItems > 0) return 'text-red-600';
    if (isProcessing || isForcing) return 'text-blue-600';
    if (pendingItems > 0) return 'text-orange-600';
    return 'text-green-600';
  };

  const getQueueStatusText = () => {
    if (isForcing) return 'Force syncing...';
    if (isProcessing) return 'Processing queue...';
    if (failedItems > 0) return `${failedItems} failed item${failedItems > 1 ? 's' : ''}`;
    if (pendingItems > 0) return `${pendingItems} pending item${pendingItems > 1 ? 's' : ''}`;
    return 'Queue empty';
  };

  return (
    <div className={`bg-white rounded-lg border shadow-sm ${className}`}>
      <div className="p-4 border-b">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">Sync Queue</h3>
          <span className={`text-sm font-medium ${getQueueStatusColor()}`}>
            {getQueueStatusText()}
          </span>
        </div>
      </div>

      <div className="p-4">
        {/* Queue statistics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-gray-900">{queueSize}</div>
            <div className="text-xs text-gray-600">Total Items</div>
          </div>
          
          <div className="text-center p-3 bg-orange-50 rounded-lg">
            <div className="text-2xl font-bold text-orange-600">{pendingItems}</div>
            <div className="text-xs text-gray-600">Pending</div>
          </div>
          
          <div className="text-center p-3 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">
              {isProcessing ? '...' : '0'}
            </div>
            <div className="text-xs text-gray-600">Processing</div>
          </div>
          
          <div className="text-center p-3 bg-red-50 rounded-lg">
            <div className="text-2xl font-bold text-red-600">{failedItems}</div>
            <div className="text-xs text-gray-600">Failed</div>
          </div>
        </div>

        {/* Progress indicator */}
        {(isProcessing || isForcing) && (
          <div className="mb-4">
            <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
              <span>{isForcing ? 'Force syncing' : 'Processing queue'}</span>
              <span className="text-blue-600">In progress</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-blue-600 h-2 rounded-full animate-pulse w-1/3"></div>
            </div>
          </div>
        )}

        {/* Action buttons */}
        {showControls && (
          <div className="flex items-center space-x-3">
            <button
              onClick={handleForceSync}
              disabled={isForcing || (queueSize === 0)}
              className={`
                px-4 py-2 rounded-md text-sm font-medium transition-colors
                ${isForcing || queueSize === 0
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
                }
              `}
            >
              {isForcing ? (
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Syncing...</span>
                </div>
              ) : (
                'Force Sync'
              )}
            </button>

            <button
              onClick={handleClearQueue}
              disabled={queueSize === 0 || isProcessing || isForcing}
              className={`
                px-4 py-2 rounded-md text-sm font-medium transition-colors
                ${queueSize === 0 || isProcessing || isForcing
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-red-600 text-white hover:bg-red-700'
                }
              `}
            >
              Clear Queue
            </button>
          </div>
        )}

        {/* Empty state */}
        {queueSize === 0 && !isProcessing && !isForcing && (
          <div className="text-center py-8 text-gray-500">
            <div className="text-4xl mb-2">✨</div>
            <p className="text-lg font-medium">All synced up!</p>
            <p className="text-sm">No items in the sync queue</p>
          </div>
        )}

        {/* Queue status messages */}
        {failedItems > 0 && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center space-x-2">
              <span className="text-red-600">⚠️</span>
              <div>
                <p className="text-sm font-medium text-red-800">
                  {failedItems} item{failedItems > 1 ? 's' : ''} failed to sync
                </p>
                <p className="text-xs text-red-600">
                  These items will be retried automatically when connection is restored
                </p>
              </div>
            </div>
          </div>
        )}

        {pendingItems > 0 && !isProcessing && (
          <div className="mt-4 p-3 bg-orange-50 border border-orange-200 rounded-lg">
            <div className="flex items-center space-x-2">
              <span className="text-orange-600">⏳</span>
              <div>
                <p className="text-sm font-medium text-orange-800">
                  {pendingItems} item{pendingItems > 1 ? 's' : ''} waiting to sync
                </p>
                <p className="text-xs text-orange-600">
                  Items will be synced automatically in the background
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SyncQueue;