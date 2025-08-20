/**
 * PWA Install Prompt Component
 * Handles PWA installation prompts and updates
 */

'use client';

import React, { useState, useEffect } from 'react';
import { ArrowDownTrayIcon, XMarkIcon, ArrowPathIcon } from '@heroicons/react/24/outline';
import { pwaManager } from '@/lib/pwaManager';
import { logger } from '@/lib/logger';

interface PWAInstallPromptProps {
  className?: string;
}

interface InstallState {
  canInstall: boolean;
  isInstalled: boolean;
  isStandalone: boolean;
  showInstallPrompt: boolean;
  showUpdatePrompt: boolean;
  isUpdating: boolean;
}

export const PWAInstallPrompt: React.FC<PWAInstallPromptProps> = ({ className = '' }) => {
  const [state, setState] = useState<InstallState>({
    canInstall: false,
    isInstalled: false,
    isStandalone: false,
    showInstallPrompt: false,
    showUpdatePrompt: false,
    isUpdating: false
  });

  useEffect(() => {
    // Initialize state
    const updateInstallState = () => {
      const installState = pwaManager.getInstallationState();
      setState(prev => ({
        ...prev,
        canInstall: installState.canInstall,
        isInstalled: installState.isInstalled,
        isStandalone: installState.isStandalone,
        showInstallPrompt: installState.canInstall && !installState.isInstalled
      }));
    };

    // Set up event listeners
    const handleInstallStateChange = (installState: any) => {
      setState(prev => ({
        ...prev,
        canInstall: installState.canInstall,
        isInstalled: installState.isInstalled,
        isStandalone: installState.isStandalone,
        showInstallPrompt: installState.canInstall && !installState.isInstalled
      }));
    };

    const handleUpdateStateChange = (updateState: any) => {
      setState(prev => ({
        ...prev,
        showUpdatePrompt: updateState.isUpdateAvailable,
        isUpdating: updateState.isUpdating
      }));
    };

    pwaManager.onInstallStateChange(handleInstallStateChange);
    pwaManager.onUpdateStateChange(handleUpdateStateChange);

    // Initial state
    updateInstallState();

    return () => {
      pwaManager.offInstallStateChange(handleInstallStateChange);
      pwaManager.offUpdateStateChange(handleUpdateStateChange);
    };
  }, []);

  const handleInstall = async () => {
    try {
      const result = await pwaManager.promptInstall();
      if (result && result.outcome === 'accepted') {
        logger.info('PWA installation accepted');
        setState(prev => ({ ...prev, showInstallPrompt: false }));
      }
    } catch (error) {
      logger.error('PWA installation failed', { error });
    }
  };

  const handleUpdate = async () => {
    try {
      setState(prev => ({ ...prev, isUpdating: true }));
      await pwaManager.applyUpdate();
    } catch (error) {
      logger.error('PWA update failed', { error });
      setState(prev => ({ ...prev, isUpdating: false }));
    }
  };

  const dismissInstallPrompt = () => {
    setState(prev => ({ ...prev, showInstallPrompt: false }));
    // Store dismissal in localStorage to avoid showing again soon
    if (typeof window !== 'undefined') {
      localStorage.setItem('pwa-install-dismissed', Date.now().toString());
    }
  };

  const dismissUpdatePrompt = () => {
    setState(prev => ({ ...prev, showUpdatePrompt: false }));
  };

  // Don't show install prompt if recently dismissed
  const shouldShowInstallPrompt = () => {
    if (typeof window === 'undefined') return false;
    
    const lastDismissed = localStorage.getItem('pwa-install-dismissed');
    if (lastDismissed && Date.now() - parseInt(lastDismissed) < 7 * 24 * 60 * 60 * 1000) { // 7 days
      return false;
    }
    return state.showInstallPrompt;
  };

  if (!shouldShowInstallPrompt() && !state.showUpdatePrompt) {
    return null;
  }

  return (
    <div className={className}>
      {/* Install Prompt */}
      {shouldShowInstallPrompt() && (
        <div className="fixed bottom-4 left-4 right-4 md:left-auto md:right-4 md:w-96 bg-white border border-gray-200 rounded-lg shadow-lg p-4 z-50">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              <ArrowDownTrayIcon className="h-6 w-6 text-green-600" />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="text-sm font-medium text-gray-900">
                Installer l'application
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                Ajoutez La Vida Luca à votre écran d'accueil pour un accès rapide et une expérience hors ligne.
              </p>
              <div className="flex space-x-2 mt-3">
                <button
                  onClick={handleInstall}
                  className="bg-green-600 text-white px-3 py-1.5 rounded text-sm font-medium hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
                >
                  Installer
                </button>
                <button
                  onClick={dismissInstallPrompt}
                  className="bg-gray-100 text-gray-700 px-3 py-1.5 rounded text-sm font-medium hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                >
                  Plus tard
                </button>
              </div>
            </div>
            <button
              onClick={dismissInstallPrompt}
              className="flex-shrink-0 text-gray-400 hover:text-gray-600 focus:outline-none"
            >
              <XMarkIcon className="h-5 w-5" />
            </button>
          </div>
        </div>
      )}

      {/* Update Prompt */}
      {state.showUpdatePrompt && (
        <div className="fixed top-4 left-4 right-4 md:left-auto md:right-4 md:w-96 bg-blue-50 border border-blue-200 rounded-lg shadow-lg p-4 z-50">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              {state.isUpdating ? (
                <ArrowPathIcon className="h-6 w-6 text-blue-600 animate-spin" />
              ) : (
                <ArrowPathIcon className="h-6 w-6 text-blue-600" />
              )}
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="text-sm font-medium text-blue-900">
                {state.isUpdating ? 'Mise à jour en cours...' : 'Mise à jour disponible'}
              </h3>
              <p className="text-sm text-blue-700 mt-1">
                {state.isUpdating 
                  ? 'L\'application se met à jour. Veuillez patienter...'
                  : 'Une nouvelle version de l\'application est disponible avec des améliorations et corrections.'
                }
              </p>
              {!state.isUpdating && (
                <div className="flex space-x-2 mt-3">
                  <button
                    onClick={handleUpdate}
                    className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  >
                    Mettre à jour
                  </button>
                  <button
                    onClick={dismissUpdatePrompt}
                    className="bg-blue-100 text-blue-700 px-3 py-1.5 rounded text-sm font-medium hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  >
                    Plus tard
                  </button>
                </div>
              )}
            </div>
            {!state.isUpdating && (
              <button
                onClick={dismissUpdatePrompt}
                className="flex-shrink-0 text-blue-400 hover:text-blue-600 focus:outline-none"
              >
                <XMarkIcon className="h-5 w-5" />
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default PWAInstallPrompt;