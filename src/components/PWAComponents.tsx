/**
 * PWA Install Prompt Component
 * Shows install prompt and update notifications for PWA
 */

'use client';

import React from 'react';
import { usePWAInstall } from '@/hooks/usePWAInstall';
import { ArrowDownTrayIcon, ArrowPathIcon, XMarkIcon } from '@heroicons/react/24/outline';

interface PWAInstallPromptProps {
  onDismiss?: () => void;
  className?: string;
}

export const PWAInstallPrompt: React.FC<PWAInstallPromptProps> = ({
  onDismiss,
  className = '',
}) => {
  const { canInstall, installPWA } = usePWAInstall();

  const handleInstall = async () => {
    const success = await installPWA();
    if (success && onDismiss) {
      onDismiss();
    }
  };

  if (!canInstall) {
    return null;
  }

  return (
    <div className={`bg-blue-50 border border-blue-200 rounded-lg p-4 ${className}`}>
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <ArrowDownTrayIcon className="w-5 h-5 text-blue-400" />
        </div>
        
        <div className="ml-3 flex-1">
          <h3 className="text-sm font-medium text-blue-800">
            Installer l'application
          </h3>
          
          <p className="mt-1 text-sm text-blue-700">
            Installez La Vida Luca sur votre appareil pour un accès rapide et une expérience hors ligne.
          </p>
          
          <div className="mt-3 flex space-x-3">
            <button
              onClick={handleInstall}
              className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <ArrowDownTrayIcon className="w-4 h-4 mr-1" />
              Installer
            </button>
            
            {onDismiss && (
              <button
                onClick={onDismiss}
                className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Plus tard
              </button>
            )}
          </div>
        </div>
        
        {onDismiss && (
          <div className="ml-3 flex-shrink-0">
            <button
              onClick={onDismiss}
              className="inline-flex rounded-md text-blue-400 hover:text-blue-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <span className="sr-only">Fermer</span>
              <XMarkIcon className="w-5 h-5" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

interface PWAUpdateNotificationProps {
  onUpdate?: () => void;
  onDismiss?: () => void;
}

export const PWAUpdateNotification: React.FC<PWAUpdateNotificationProps> = ({
  onUpdate,
  onDismiss,
}) => {
  const { serviceWorkerUpdated, updateServiceWorker } = usePWAInstall();

  const handleUpdate = () => {
    updateServiceWorker();
    if (onUpdate) {
      onUpdate();
    }
  };

  if (!serviceWorkerUpdated) {
    return null;
  }

  return (
    <div className="fixed bottom-4 right-4 z-50 max-w-sm">
      <div className="bg-green-50 border border-green-200 rounded-lg shadow-lg p-4">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <ArrowPathIcon className="w-5 h-5 text-green-400" />
          </div>
          
          <div className="ml-3 flex-1">
            <h3 className="text-sm font-medium text-green-800">
              Mise à jour disponible
            </h3>
            
            <p className="mt-1 text-sm text-green-700">
              Une nouvelle version de l'application est disponible.
            </p>
            
            <div className="mt-3 flex space-x-3">
              <button
                onClick={handleUpdate}
                className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              >
                <ArrowPathIcon className="w-4 h-4 mr-1" />
                Mettre à jour
              </button>
              
              {onDismiss && (
                <button
                  onClick={onDismiss}
                  className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                >
                  Plus tard
                </button>
              )}
            </div>
          </div>
          
          {onDismiss && (
            <div className="ml-3 flex-shrink-0">
              <button
                onClick={onDismiss}
                className="inline-flex rounded-md text-green-400 hover:text-green-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              >
                <span className="sr-only">Fermer</span>
                <XMarkIcon className="w-5 h-5" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

interface PWAStatusIndicatorProps {
  className?: string;
}

export const PWAStatusIndicator: React.FC<PWAStatusIndicatorProps> = ({
  className = '',
}) => {
  const { isStandalone, canInstall, serviceWorkerReady } = usePWAInstall();

  if (!isStandalone && !canInstall && !serviceWorkerReady) {
    return null;
  }

  return (
    <div className={`inline-flex items-center text-sm text-gray-500 ${className}`}>
      {isStandalone && (
        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
          PWA Installée
        </span>
      )}
      
      {!isStandalone && serviceWorkerReady && (
        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
          Mode Hors Ligne Activé
        </span>
      )}
      
      {canInstall && (
        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
          Installation Disponible
        </span>
      )}
    </div>
  );
};