'use client';

import React, { useEffect, useState } from 'react';
import { pwaManager, PWAStatus } from '@/lib/pwaUtils';
import { 
  ArrowDownTrayIcon, 
  DevicePhoneMobileIcon, 
  CheckCircleIcon,
  ArrowPathIcon,
  ShareIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';

interface PWAInstallProps {
  className?: string;
  variant?: 'banner' | 'card' | 'button';
  showInstructions?: boolean;
}

export default function PWAInstall({ 
  className = '', 
  variant = 'banner',
  showInstructions = true 
}: PWAInstallProps) {
  const [pwaStatus, setPwaStatus] = useState<PWAStatus>({
    isInstallable: false,
    isInstalled: false,
    isStandalone: false,
    hasUpdate: false,
  });
  const [showModal, setShowModal] = useState(false);
  const [installing, setInstalling] = useState(false);
  const [updating, setUpdating] = useState(false);
  const [dismissed, setDismissed] = useState(false);
  const [instructions, setInstructions] = useState<string[]>([]);

  useEffect(() => {
    // Get initial PWA status
    setPwaStatus(pwaManager.getPWAStatus());

    // Subscribe to PWA status changes
    const unsubscribe = pwaManager.onStatusChange((status) => {
      setPwaStatus(status);
    });

    // Load installation instructions
    pwaManager.getInstallationInstructions().then(setInstructions);

    // Check if banner was previously dismissed
    const bannerDismissed = localStorage.getItem('pwa-banner-dismissed');
    if (bannerDismissed) {
      setDismissed(true);
    }

    return unsubscribe;
  }, []);

  const handleInstall = async () => {
    setInstalling(true);
    
    try {
      const success = await pwaManager.installApp();
      if (success) {
        setShowModal(false);
        setDismissed(true);
        localStorage.setItem('pwa-banner-dismissed', 'true');
      }
    } catch (error) {
      console.error('Installation failed:', error);
    } finally {
      setInstalling(false);
    }
  };

  const handleUpdate = async () => {
    setUpdating(true);
    
    try {
      await pwaManager.updateApp();
    } catch (error) {
      console.error('Update failed:', error);
    } finally {
      setUpdating(false);
    }
  };

  const handleShare = async () => {
    try {
      await pwaManager.shareApp();
    } catch (error) {
      console.error('Share failed:', error);
    }
  };

  const handleDismiss = () => {
    setDismissed(true);
    localStorage.setItem('pwa-banner-dismissed', 'true');
  };

  const openInstructions = () => {
    setShowModal(true);
  };

  // Don't show if installed or dismissed (for banner variant)
  if (pwaStatus.isInstalled || (dismissed && variant === 'banner')) {
    return null;
  }

  // Show update notification if available
  if (pwaStatus.hasUpdate) {
    return (
      <div className={`bg-blue-50 border border-blue-200 rounded-lg p-4 ${className}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <ArrowPathIcon className="h-6 w-6 text-blue-600" />
            <div>
              <h3 className="font-medium text-blue-900">Mise à jour disponible</h3>
              <p className="text-sm text-blue-700">
                Une nouvelle version de l'application est disponible.
              </p>
            </div>
          </div>
          <button
            onClick={handleUpdate}
            disabled={updating}
            className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {updating ? (
              <>
                <ArrowPathIcon className="h-4 w-4 animate-spin mr-2 inline" />
                Mise à jour...
              </>
            ) : (
              'Mettre à jour'
            )}
          </button>
        </div>
      </div>
    );
  }

  if (variant === 'button') {
    return (
      <button
        onClick={pwaStatus.isInstallable ? handleInstall : openInstructions}
        disabled={installing}
        className={`flex items-center gap-2 px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
      >
        {installing ? (
          <>
            <ArrowPathIcon className="h-4 w-4 animate-spin" />
            Installation...
          </>
        ) : (
          <>
            <ArrowDownTrayIcon className="h-4 w-4" />
            Installer l'app
          </>
        )}
      </button>
    );
  }

  if (variant === 'card') {
    return (
      <div className={`bg-white rounded-lg shadow-md border border-gray-200 p-6 ${className}`}>
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0">
            <DevicePhoneMobileIcon className="h-12 w-12 text-green-600" />
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Installer La Vida Luca
            </h3>
            <p className="text-gray-600 mb-4">
              Installez notre application pour une expérience optimale. 
              Accès hors ligne, notifications et performance améliorée.
            </p>
            <div className="flex gap-3">
              {pwaStatus.isInstallable ? (
                <button
                  onClick={handleInstall}
                  disabled={installing}
                  className="px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-md hover:bg-green-700 disabled:opacity-50"
                >
                  {installing ? 'Installation...' : 'Installer'}
                </button>
              ) : (
                <button
                  onClick={openInstructions}
                  className="px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-md hover:bg-green-700"
                >
                  Voir les instructions
                </button>
              )}
              <button
                onClick={handleShare}
                className="px-4 py-2 border border-gray-300 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-50"
              >
                <ShareIcon className="h-4 w-4 mr-2 inline" />
                Partager
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Default banner variant
  return (
    <>
      <div className={`bg-green-50 border border-green-200 rounded-lg p-4 ${className}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <DevicePhoneMobileIcon className="h-6 w-6 text-green-600" />
            <div>
              <h3 className="font-medium text-green-900">
                Installer La Vida Luca
              </h3>
              <p className="text-sm text-green-700">
                Installez l'app pour un accès rapide et des fonctionnalités hors ligne.
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {pwaStatus.isInstallable ? (
              <button
                onClick={handleInstall}
                disabled={installing}
                className="px-3 py-1 bg-green-600 text-white text-sm font-medium rounded-md hover:bg-green-700 disabled:opacity-50"
              >
                {installing ? 'Installation...' : 'Installer'}
              </button>
            ) : showInstructions ? (
              <button
                onClick={openInstructions}
                className="px-3 py-1 bg-green-600 text-white text-sm font-medium rounded-md hover:bg-green-700"
              >
                Instructions
              </button>
            ) : null}
            <button
              onClick={handleDismiss}
              className="p-1 text-green-600 hover:text-green-800"
            >
              <XMarkIcon className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Instructions Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={() => setShowModal(false)} />
            
            <div className="inline-block transform overflow-hidden rounded-lg bg-white px-4 pt-5 pb-4 text-left align-bottom shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6 sm:align-middle">
              <div>
                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
                  <DevicePhoneMobileIcon className="h-6 w-6 text-green-600" />
                </div>
                <div className="mt-3 text-center sm:mt-5">
                  <h3 className="text-lg font-medium leading-6 text-gray-900">
                    Installation de l'application
                  </h3>
                  <div className="mt-4 text-left">
                    <ol className="space-y-3 text-sm text-gray-600">
                      {instructions.map((instruction, index) => (
                        <li key={index} className="flex gap-3">
                          <span className="flex-shrink-0 w-6 h-6 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-xs font-medium">
                            {index + 1}
                          </span>
                          <span>{instruction}</span>
                        </li>
                      ))}
                    </ol>
                  </div>
                </div>
              </div>
              <div className="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="inline-flex w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 sm:col-start-1 sm:text-sm"
                >
                  Fermer
                </button>
                <button
                  type="button"
                  onClick={handleShare}
                  className="mt-3 inline-flex w-full justify-center rounded-md border border-transparent bg-green-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 sm:col-start-2 sm:mt-0 sm:text-sm"
                >
                  Partager l'app
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}