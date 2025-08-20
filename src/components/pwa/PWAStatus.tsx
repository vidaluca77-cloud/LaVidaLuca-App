/**
 * PWAStatus component for displaying PWA installation and update status
 */

'use client';

import React, { useState } from 'react';
import { usePWA } from '@/hooks/usePWA';

export interface PWAStatusProps {
  className?: string;
  showInstallPrompt?: boolean;
  showUpdatePrompt?: boolean;
  showCapabilities?: boolean;
  compact?: boolean;
}

export const PWAStatus: React.FC<PWAStatusProps> = ({
  className = '',
  showInstallPrompt = true,
  showUpdatePrompt = true,
  showCapabilities = false,
  compact = false,
}) => {
  const {
    capabilities,
    installState,
    updateAvailable,
    isOfflineReady,
    showInstallPrompt: triggerInstallPrompt,
    updateServiceWorker,
    getInstallationGuidance,
    isSupported,
    isStandalone,
  } = usePWA();

  const [isUpdating, setIsUpdating] = useState(false);
  const [isInstalling, setIsInstalling] = useState(false);

  const handleInstall = async () => {
    if (isInstalling) return;
    
    setIsInstalling(true);
    try {
      await triggerInstallPrompt();
    } finally {
      setIsInstalling(false);
    }
  };

  const handleUpdate = async () => {
    if (isUpdating) return;
    
    setIsUpdating(true);
    try {
      await updateServiceWorker();
    } finally {
      setIsUpdating(false);
    }
  };

  const getInstallStatusColor = () => {
    if (installState.isInstalled || isStandalone) return 'text-green-600';
    if (installState.canInstall) return 'text-blue-600';
    return 'text-gray-600';
  };

  const getInstallStatusText = () => {
    if (installState.isInstalled || isStandalone) return 'Installée';
    if (installState.canInstall) return 'Peut être installée';
    return 'Installation non disponible';
  };

  const getInstallStatusIcon = () => {
    if (installState.isInstalled || isStandalone) return '✅';
    if (installState.canInstall) return '📱';
    return '❓';
  };

  if (compact) {
    return (
      <div className={`flex items-center space-x-2 ${className}`}>
        <span className="text-sm">{getInstallStatusIcon()}</span>
        <span className={`text-xs font-medium ${getInstallStatusColor()}`}>
          PWA
        </span>
        {updateAvailable && (
          <span className="text-xs bg-orange-100 text-orange-800 px-2 py-0.5 rounded-full">
            Mise à jour
          </span>
        )}
      </div>
    );
  }

  if (!isSupported) {
    return (
      <div className={`p-4 bg-yellow-50 border border-yellow-200 rounded-lg ${className}`}>
        <div className="flex items-center space-x-2">
          <span className="text-yellow-600">ℹ️</span>
          <div>
            <p className="text-sm font-medium text-yellow-800">
              PWA non supportée
            </p>
            <p className="text-xs text-yellow-600">
              Votre navigateur ne supporte pas les fonctionnalités PWA
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg border shadow-sm ${className}`}>
      <div className="p-4 border-b">
        <h3 className="text-lg font-semibold text-gray-900">
          Application Progressive Web (PWA)
        </h3>
      </div>

      <div className="p-4 space-y-4">
        {/* Installation Status */}
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center space-x-3">
            <span className="text-2xl">{getInstallStatusIcon()}</span>
            <div>
              <p className="font-medium text-gray-900">Statut d'installation</p>
              <p className={`text-sm ${getInstallStatusColor()}`}>
                {getInstallStatusText()}
              </p>
            </div>
          </div>
          
          {showInstallPrompt && installState.canInstall && !installState.isInstalled && (
            <button
              onClick={handleInstall}
              disabled={isInstalling}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 text-sm"
            >
              {isInstalling ? 'Installation...' : 'Installer'}
            </button>
          )}
        </div>

        {/* Update Status */}
        {(updateAvailable || isOfflineReady) && (
          <div className="space-y-2">
            {updateAvailable && showUpdatePrompt && (
              <div className="flex items-center justify-between p-3 bg-orange-50 border border-orange-200 rounded-lg">
                <div className="flex items-center space-x-2">
                  <span className="text-orange-600">🔄</span>
                  <div>
                    <p className="text-sm font-medium text-orange-800">
                      Mise à jour disponible
                    </p>
                    <p className="text-xs text-orange-600">
                      Une nouvelle version de l'application est prête
                    </p>
                  </div>
                </div>
                <button
                  onClick={handleUpdate}
                  disabled={isUpdating}
                  className="px-3 py-1 bg-orange-600 text-white rounded-md hover:bg-orange-700 disabled:opacity-50 text-sm"
                >
                  {isUpdating ? 'Mise à jour...' : 'Mettre à jour'}
                </button>
              </div>
            )}

            {isOfflineReady && (
              <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                <div className="flex items-center space-x-2">
                  <span className="text-green-600">📱</span>
                  <div>
                    <p className="text-sm font-medium text-green-800">
                      Mode hors-ligne activé
                    </p>
                    <p className="text-xs text-green-600">
                      L'application fonctionne maintenant sans connexion internet
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Installation Guide */}
        {installState.canInstall && !installState.isInstalled && (
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm font-medium text-blue-800 mb-2">
              Comment installer l'application :
            </p>
            <p className="text-xs text-blue-600">
              {getInstallationGuidance()}
            </p>
          </div>
        )}

        {/* Capabilities */}
        {showCapabilities && (
          <div className="p-3 bg-gray-50 rounded-lg">
            <p className="text-sm font-medium text-gray-900 mb-3">
              Fonctionnalités disponibles
            </p>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="flex items-center justify-between">
                <span>Service Worker</span>
                <span className={capabilities.supportsServiceWorker ? 'text-green-600' : 'text-red-600'}>
                  {capabilities.supportsServiceWorker ? '✅' : '❌'}
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <span>Mode hors-ligne</span>
                <span className={capabilities.supportsOffline ? 'text-green-600' : 'text-red-600'}>
                  {capabilities.supportsOffline ? '✅' : '❌'}
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <span>Notifications Push</span>
                <span className={capabilities.supportsPush ? 'text-green-600' : 'text-red-600'}>
                  {capabilities.supportsPush ? '✅' : '❌'}
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <span>Sync arrière-plan</span>
                <span className={capabilities.supportsBackgroundSync ? 'text-green-600' : 'text-red-600'}>
                  {capabilities.supportsBackgroundSync ? '✅' : '❌'}
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <span>Installation</span>
                <span className={capabilities.isInstallable ? 'text-green-600' : 'text-red-600'}>
                  {capabilities.isInstallable ? '✅' : '❌'}
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <span>Plateforme</span>
                <span className="text-gray-600 capitalize">
                  {capabilities.platform}
                </span>
              </div>
            </div>
          </div>
        )}

        {/* App Status */}
        {(installState.isInstalled || isStandalone) && (
          <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center space-x-2">
              <span className="text-green-600">🎉</span>
              <div>
                <p className="text-sm font-medium text-green-800">
                  Application installée avec succès!
                </p>
                <p className="text-xs text-green-600">
                  Vous pouvez maintenant utiliser l'application même sans connexion internet
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PWAStatus;