/**
 * PWA Install Banner Component
 * Shows a banner prompting users to install the PWA
 */

'use client';

import React, { useState, useEffect } from 'react';
import { pwaManager } from '@/lib/pwa/PWAManager';

interface PWAInstallBannerProps {
  className?: string;
}

export const PWAInstallBanner: React.FC<PWAInstallBannerProps> = ({
  className = ''
}) => {
  const [showBanner, setShowBanner] = useState(false);
  const [isInstalling, setIsInstalling] = useState(false);
  const [isInstalled, setIsInstalled] = useState(false);

  useEffect(() => {
    // Initialize PWA manager
    pwaManager.init();

    // Check if already installed
    if (pwaManager.isPWA()) {
      setIsInstalled(true);
      return;
    }

    // Listen for install prompt availability
    const handleInstallAvailable = () => {
      setShowBanner(true);
    };

    const handleInstalled = () => {
      setIsInstalled(true);
      setShowBanner(false);
    };

    window.addEventListener('pwa-install-available', handleInstallAvailable);
    window.addEventListener('pwa-installed', handleInstalled);

    return () => {
      window.removeEventListener('pwa-install-available', handleInstallAvailable);
      window.removeEventListener('pwa-installed', handleInstalled);
    };
  }, []);

  const handleInstall = async () => {
    setIsInstalling(true);
    
    try {
      const result = await pwaManager.showInstallPrompt();
      
      if (result === 'accepted') {
        setShowBanner(false);
      } else if (result === 'dismissed') {
        setShowBanner(false);
      }
    } catch (error) {
      console.error('Installation failed:', error);
    } finally {
      setIsInstalling(false);
    }
  };

  const handleDismiss = () => {
    setShowBanner(false);
    
    // Remember dismissal for this session
    sessionStorage.setItem('pwa-banner-dismissed', 'true');
  };

  // Don't show if installed, dismissed, or not available
  if (isInstalled || !showBanner || sessionStorage.getItem('pwa-banner-dismissed')) {
    return null;
  }

  return (
    <div 
      className={`
        bg-gradient-to-r from-green-600 to-green-700 text-white p-4 shadow-lg
        ${className}
      `}
      role="banner"
      aria-label="Install app banner"
    >
      <div className="flex items-center justify-between max-w-6xl mx-auto">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white bg-opacity-20 rounded-lg flex items-center justify-center">
            <span className="text-2xl">🌱</span>
          </div>
          
          <div>
            <h3 className="font-semibold text-lg mb-1">
              Install La Vida Luca App
            </h3>
            <p className="text-green-100 text-sm">
              Get the full experience with offline access and notifications
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleInstall}
            disabled={isInstalling}
            className="
              bg-white text-green-700 px-4 py-2 rounded-lg font-medium
              hover:bg-green-50 transition-colors duration-200
              disabled:opacity-50 disabled:cursor-not-allowed
              flex items-center gap-2
            "
          >
            {isInstalling ? (
              <>
                <div className="animate-spin h-4 w-4 border-2 border-green-700 border-t-transparent rounded-full" />
                Installing...
              </>
            ) : (
              <>
                <span>📱</span>
                Install
              </>
            )}
          </button>

          <button
            onClick={handleDismiss}
            className="
              text-green-100 hover:text-white p-2 rounded-lg
              transition-colors duration-200
            "
            aria-label="Dismiss install banner"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default PWAInstallBanner;