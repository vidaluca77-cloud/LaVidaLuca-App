'use client';

import React, { useState } from 'react';
import { useOffline } from '@/hooks/useOffline';
import SyncStatus from '@/components/offline/SyncStatus';

export default function OfflineDemoPage() {
  const [testData, setTestData] = useState('');
  const [cachedData, setCachedData] = useState<string | null>(null);
  const {
    status,
    isOnline,
    isOffline,
    isSyncing,
    cacheData,
    getCachedData,
    queueAction,
    sync,
    stats,
    lastSyncResult
  } = useOffline();

  const handleCacheData = async () => {
    if (!testData.trim()) return;
    
    const success = await cacheData('test-data', testData);
    if (success) {
      alert('Data cached successfully!');
    } else {
      alert('Failed to cache data');
    }
  };

  const handleGetCachedData = async () => {
    const data = await getCachedData<string>('test-data');
    setCachedData(data);
  };

  const handleQueueAction = async () => {
    try {
      const actionId = await queueAction(
        'api_call',
        '/api/test',
        'POST',
        { message: 'Test offline action', timestamp: Date.now() },
        {
          priority: 'medium',
          onSuccess: (result) => {
            console.log('Action succeeded:', result);
            alert('Queued action succeeded!');
          },
          onError: (error) => {
            console.error('Action failed:', error);
            alert('Queued action failed: ' + error);
          }
        }
      );
      alert(`Action queued with ID: ${actionId}`);
    } catch (error) {
      alert('Failed to queue action: ' + error);
    }
  };

  const handleManualSync = async () => {
    try {
      const result = await sync();
      alert(`Sync completed: ${result.actionsProcessed} actions processed, ${result.errors.length} errors`);
    } catch (error) {
      alert('Sync failed: ' + error);
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'online': return 'text-green-600';
      case 'offline': return 'text-red-600';
      case 'syncing': return 'text-yellow-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8">Offline & PWA Demo</h1>

      {/* Status Section */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Connection Status</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className={`text-2xl font-bold ${getStatusColor()}`}>
              {status.toUpperCase()}
            </div>
            <div className="text-sm text-gray-600">Status</div>
          </div>
          <div className="text-center">
            <div className={`text-2xl font-bold ${isOnline ? 'text-green-600' : 'text-red-600'}`}>
              {isOnline ? 'YES' : 'NO'}
            </div>
            <div className="text-sm text-gray-600">Online</div>
          </div>
          <div className="text-center">
            <div className={`text-2xl font-bold ${isSyncing ? 'text-yellow-600' : 'text-gray-400'}`}>
              {isSyncing ? 'YES' : 'NO'}
            </div>
            <div className="text-sm text-gray-600">Syncing</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {stats.pendingActions}
            </div>
            <div className="text-sm text-gray-600">Pending Actions</div>
          </div>
        </div>
      </div>

      {/* Data Caching Demo */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Data Caching Demo</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Test Data
            </label>
            <input
              type="text"
              value={testData}
              onChange={(e) => setTestData(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter some test data to cache..."
            />
          </div>
          
          <div className="flex gap-2">
            <button
              onClick={handleCacheData}
              disabled={!testData.trim()}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              Cache Data
            </button>
            <button
              onClick={handleGetCachedData}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              Get Cached Data
            </button>
          </div>

          {cachedData !== null && (
            <div className="mt-4 p-3 bg-gray-100 rounded-md">
              <strong>Cached Data:</strong> {cachedData || 'No data found'}
            </div>
          )}
        </div>
      </div>

      {/* Action Queuing Demo */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Action Queuing Demo</h2>
        <div className="space-y-4">
          <p className="text-gray-600">
            Queue an action that will be executed when you're back online.
          </p>
          
          <div className="flex gap-2">
            <button
              onClick={handleQueueAction}
              className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
            >
              Queue Test Action
            </button>
            <button
              onClick={handleManualSync}
              disabled={!isOnline}
              className="px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              Manual Sync
            </button>
          </div>

          {lastSyncResult && (
            <div className="mt-4 p-3 bg-gray-100 rounded-md">
              <strong>Last Sync Result:</strong>{' '}
              <span className={lastSyncResult.success ? 'text-green-600' : 'text-red-600'}>
                {lastSyncResult.success ? 'Success' : 'Failed'}
              </span>
              {' '}({lastSyncResult.actionsProcessed} actions processed)
              {lastSyncResult.errors.length > 0 && (
                <div className="text-red-600 text-sm mt-1">
                  Errors: {lastSyncResult.errors.join(', ')}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Sync Status Component */}
      <div className="mb-6">
        <SyncStatus detailed={true} />
      </div>

      {/* Instructions */}
      <div className="bg-blue-50 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4 text-blue-800">How to Test</h2>
        <ol className="list-decimal list-inside space-y-2 text-blue-700">
          <li>
            <strong>Cache Data:</strong> Enter some text and click "Cache Data" to store it locally.
          </li>
          <li>
            <strong>Queue Actions:</strong> Click "Queue Test Action" to add actions to the offline queue.
          </li>
          <li>
            <strong>Go Offline:</strong> Open your browser's Developer Tools (F12), go to Network tab, and enable "Offline" mode.
          </li>
          <li>
            <strong>Try Actions Offline:</strong> Notice how the status indicator changes and actions are queued.
          </li>
          <li>
            <strong>Go Back Online:</strong> Disable offline mode in Developer Tools and watch actions sync automatically.
          </li>
          <li>
            <strong>Install as PWA:</strong> Look for the install banner at the top or use your browser's install option.
          </li>
        </ol>
      </div>
    </div>
  );
}