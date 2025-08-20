'use client';

import React from 'react';
import { useServiceWorker } from '@/lib/serviceWorker';
import { ArrowPathIcon, XMarkIcon } from '@heroicons/react/24/outline';

interface ServiceWorkerUpdateProps {
  className?: string;
}

export const ServiceWorkerUpdate: React.FC<ServiceWorkerUpdateProps> = ({ className = '' }) => {
  const { updateAvailable, isUpdating, activateUpdate } = useServiceWorker();
  const [dismissed, setDismissed] = React.useState(false);

  if (!updateAvailable || dismissed) {
    return null;
  }

  return (
    <div className={`fixed top-4 left-4 right-4 md:left-auto md:right-4 md:max-w-sm z-50 ${className}`}>
      <div className="bg-blue-600 text-white rounded-lg shadow-lg p-4">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0">
            <ArrowPathIcon className="w-5 h-5 mt-0.5" />
          </div>
          
          <div className="flex-1 min-w-0">
            <h3 className="text-sm font-medium mb-1">
              Mise à jour disponible
            </h3>
            <p className="text-xs opacity-90 mb-3">
              Une nouvelle version de l'application est prête à être installée.
            </p>
            
            <div className="flex gap-2">
              <button
                onClick={activateUpdate}
                disabled={isUpdating}
                className="flex-1 bg-white text-blue-600 text-xs font-medium py-2 px-3 rounded-md hover:bg-blue-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isUpdating ? (
                  <span className="flex items-center gap-2">
                    <ArrowPathIcon className="w-3 h-3 animate-spin" />
                    Mise à jour...
                  </span>
                ) : (
                  'Mettre à jour'
                )}
              </button>
              <button
                onClick={() => setDismissed(true)}
                className="flex-shrink-0 text-white/70 hover:text-white transition-colors p-1"
                aria-label="Ignorer"
              >
                <XMarkIcon className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ServiceWorkerUpdate;