/**
 * Sync Status Component
 * Shows sync progress and statistics for offline actions
 */

'use client';

import React, { useState, useEffect } from 'react';
import { offlineManager, SyncResult } from '@/lib/offline/OfflineManager';

interface SyncStatusProps {
  className?: string;
  detailed?: boolean;
}

interface Stats {
  total: number;
  byType: Record<string, number>;
  lastSync?: Date;
}

export const SyncStatus: React.FC<SyncStatusProps> = ({
  className = '',
  detailed = false
}) => {
  const [stats, setStats] = useState<Stats>({ total: 0, byType: {} });
  const [lastSyncResult, setLastSyncResult] = useState<SyncResult | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const offlineStats = await offlineManager.getStats();
        setStats({
          total: offlineStats.deferredActions.total,
          byType: offlineStats.deferredActions.byType,
          lastSync: offlineStats.lastSync
        });
      } catch (error) {
        console.error('Error loading sync stats:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadStats();

    // Listen for sync events
    const unsubscribe = offlineManager.addSyncListener((result) => {
      setLastSyncResult(result);
      loadStats(); // Refresh stats after sync
    });

    // Refresh stats periodically
    const interval = setInterval(loadStats, 30000); // Every 30 seconds

    return () => {
      unsubscribe();
      clearInterval(interval);
    };
  }, []);

  const handleManualSync = async () => {
    try {
      await offlineManager.sync();
    } catch (error) {
      console.error('Manual sync failed:', error);
    }
  };

  if (isLoading) {
    return (
      <div className={`animate-pulse bg-gray-200 rounded-lg p-4 ${className}`}>
        <div className="h-4 bg-gray-300 rounded w-1/2 mb-2"></div>
        <div className="h-3 bg-gray-300 rounded w-1/4"></div>
      </div>
    );
  }

  const hasActions = stats.total > 0;
  const isOnline = offlineManager.isOnline();

  return (
    <div className={`bg-white rounded-lg border shadow-sm p-4 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-gray-900">
          Sync Status
        </h3>
        
        {isOnline && hasActions && (
          <button
            onClick={handleManualSync}
            className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
          >
            Sync Now
          </button>
        )}
      </div>

      {/* Quick Status */}
      <div className="mb-4">
        {hasActions ? (
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-yellow-500 rounded-full animate-pulse" />
            <span className="text-sm text-gray-600">
              {stats.total} action{stats.total !== 1 ? 's' : ''} pending sync
            </span>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-500 rounded-full" />
            <span className="text-sm text-gray-600">All synced</span>
          </div>
        )}
      </div>

      {/* Detailed View */}
      {detailed && (
        <>
          {/* Actions by Type */}
          {hasActions && (
            <div className="mb-4">
              <h4 className="text-sm font-medium text-gray-700 mb-2">
                Pending Actions
              </h4>
              <div className="space-y-1">
                {Object.entries(stats.byType).map(([type, count]) => (
                  <div key={type} className="flex justify-between text-sm">
                    <span className="text-gray-600 capitalize">
                      {type.replace('_', ' ')}
                    </span>
                    <span className="font-medium">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Last Sync */}
          {stats.lastSync && (
            <div className="mb-4">
              <h4 className="text-sm font-medium text-gray-700 mb-1">
                Last Sync
              </h4>
              <p className="text-sm text-gray-600">
                {new Intl.DateTimeFormat('en-US', {
                  dateStyle: 'short',
                  timeStyle: 'short'
                }).format(stats.lastSync)}
              </p>
            </div>
          )}

          {/* Last Sync Result */}
          {lastSyncResult && (
            <div className="border-t pt-3">
              <h4 className="text-sm font-medium text-gray-700 mb-2">
                Latest Sync Result
              </h4>
              
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  {lastSyncResult.success ? (
                    <>
                      <div className="w-2 h-2 bg-green-500 rounded-full" />
                      <span className="text-sm text-green-700">Successful</span>
                    </>
                  ) : (
                    <>
                      <div className="w-2 h-2 bg-red-500 rounded-full" />
                      <span className="text-sm text-red-700">Failed</span>
                    </>
                  )}
                </div>

                <div className="text-sm text-gray-600">
                  <p>
                    Processed: {lastSyncResult.actionsProcessed} action{lastSyncResult.actionsProcessed !== 1 ? 's' : ''}
                  </p>
                  
                  {lastSyncResult.errors.length > 0 && (
                    <div className="mt-2">
                      <p className="font-medium text-red-700 mb-1">Errors:</p>
                      <ul className="list-disc list-inside space-y-1">
                        {lastSyncResult.errors.map((error, index) => (
                          <li key={index} className="text-red-600 text-xs">
                            {error}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                <p className="text-xs text-gray-500">
                  {new Intl.DateTimeFormat('en-US', {
                    timeStyle: 'medium'
                  }).format(new Date(lastSyncResult.timestamp))}
                </p>
              </div>
            </div>
          )}
        </>
      )}

      {/* Offline Warning */}
      {!isOnline && hasActions && (
        <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <div className="flex items-start gap-2">
            <span className="text-yellow-600 mt-0.5">⚠️</span>
            <div>
              <p className="text-sm font-medium text-yellow-800">
                Offline Mode
              </p>
              <p className="text-xs text-yellow-700 mt-1">
                Your actions will be synced automatically when connection is restored.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SyncStatus;