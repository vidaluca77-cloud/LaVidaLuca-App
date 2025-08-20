/**
 * PWA Update Notification component
 */

'use client';

import React, { useState, useEffect } from 'react';
import { serviceWorkerManager } from '@/lib/serviceWorker';
import { ArrowPathIcon, XMarkIcon } from '@heroicons/react/24/outline';

export function PWAUpdateNotification() {
  const [showUpdate, setShowUpdate] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);

  useEffect(() => {
    const handleStatusChange = (status: any) => {
      if (status.updateAvailable) {
        setShowUpdate(true);
      }
    };

    serviceWorkerManager.onStatusChange(handleStatusChange);

    return () => {
      serviceWorkerManager.removeStatusListener(handleStatusChange);
    };
  }, []);

  const handleUpdate = async () => {
    setIsUpdating(true);
    try {
      await serviceWorkerManager.skipWaiting();
      // The page will reload automatically after the update
    } catch (error) {
      console.error('Failed to update:', error);
      setIsUpdating(false);
    }
  };

  const handleDismiss = () => {
    setShowUpdate(false);
  };

  if (!showUpdate) {
    return null;
  }

  return (
    <div
      className="fixed bottom-4 left-4 right-4 md:left-auto md:right-4 md:w-96 z-50 bg-white border border-gray-200 rounded-lg shadow-lg p-4"
      role="alert"
      aria-live="assertive"
    >
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0">
          <ArrowPathIcon className="h-5 w-5 text-blue-600" />
        </div>
        <div className="flex-1">
          <h3 className="text-sm font-medium text-gray-900">
            Mise à jour disponible
          </h3>
          <p className="mt-1 text-sm text-gray-600">
            Une nouvelle version de l'application est disponible. Redémarrer pour appliquer les améliorations.
          </p>
          <div className="mt-3 flex gap-2">
            <button
              onClick={handleUpdate}
              disabled={isUpdating}
              className="inline-flex items-center gap-1 px-3 py-1.5 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-md"
            >
              {isUpdating ? (
                <>
                  <ArrowPathIcon className="h-4 w-4 animate-spin" />
                  Mise à jour...
                </>
              ) : (
                'Redémarrer'
              )}
            </button>
            <button
              onClick={handleDismiss}
              className="px-3 py-1.5 text-sm font-medium text-gray-700 hover:text-gray-800"
            >
              Plus tard
            </button>
          </div>
        </div>
        <button
          onClick={handleDismiss}
          className="flex-shrink-0 text-gray-400 hover:text-gray-600"
          aria-label="Fermer"
        >
          <XMarkIcon className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
}

export default PWAUpdateNotification;