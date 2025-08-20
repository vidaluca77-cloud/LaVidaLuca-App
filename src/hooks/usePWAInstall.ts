/**
 * PWA Installation Hook
 * Handles PWA installation prompts and service worker registration
 */

import { useState, useEffect } from 'react';

interface BeforeInstallPromptEvent extends Event {
  prompt(): Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

interface PWAInstallStatus {
  canInstall: boolean;
  isInstalled: boolean;
  isStandalone: boolean;
  installPrompt: BeforeInstallPromptEvent | null;
  serviceWorkerReady: boolean;
  serviceWorkerUpdated: boolean;
}

export function usePWAInstall() {
  const [status, setStatus] = useState<PWAInstallStatus>({
    canInstall: false,
    isInstalled: false,
    isStandalone: false,
    installPrompt: null,
    serviceWorkerReady: false,
    serviceWorkerUpdated: false,
  });

  useEffect(() => {
    if (typeof window === 'undefined') return;

    // Check if running in standalone mode
    const isStandalone = window.matchMedia('(display-mode: standalone)').matches ||
                        (window.navigator as any).standalone === true;

    setStatus(prev => ({ ...prev, isStandalone, isInstalled: isStandalone }));

    // Listen for beforeinstallprompt event
    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault();
      setStatus(prev => ({
        ...prev,
        canInstall: true,
        installPrompt: e as BeforeInstallPromptEvent,
      }));
    };

    // Listen for app installed event
    const handleAppInstalled = () => {
      setStatus(prev => ({
        ...prev,
        isInstalled: true,
        canInstall: false,
        installPrompt: null,
      }));
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    window.addEventListener('appinstalled', handleAppInstalled);

    // Register service worker
    registerServiceWorker();

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, []);

  const registerServiceWorker = async () => {
    if ('serviceWorker' in navigator) {
      try {
        const registration = await navigator.serviceWorker.register('/sw.js');
        
        setStatus(prev => ({ ...prev, serviceWorkerReady: true }));

        // Check for updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          if (newWorker) {
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                setStatus(prev => ({ ...prev, serviceWorkerUpdated: true }));
              }
            });
          }
        });

        // Listen for messages from service worker
        navigator.serviceWorker.addEventListener('message', (event) => {
          if (event.data && event.data.type === 'OFFLINE_QUEUE_STATUS') {
            // Handle queue status updates from service worker
            console.log('Queue status from SW:', event.data.queueLength);
          }
        });

      } catch (error) {
        console.error('Service worker registration failed:', error);
      }
    }
  };

  const installPWA = async (): Promise<boolean> => {
    if (!status.installPrompt) {
      return false;
    }

    try {
      await status.installPrompt.prompt();
      const { outcome } = await status.installPrompt.userChoice;
      
      if (outcome === 'accepted') {
        setStatus(prev => ({
          ...prev,
          canInstall: false,
          installPrompt: null,
        }));
        return true;
      }
    } catch (error) {
      console.error('PWA installation failed:', error);
    }

    return false;
  };

  const updateServiceWorker = () => {
    if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
      navigator.serviceWorker.controller.postMessage({ type: 'SKIP_WAITING' });
      window.location.reload();
    }
  };

  return {
    ...status,
    installPWA,
    updateServiceWorker,
  };
}