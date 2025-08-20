/**
 * usePWA hook for Progressive Web App functionality
 * Integrates PWA manager, service worker, and installation features
 */

'use client';

import { useEffect, useState, useCallback } from 'react';
import {
  PWAManager,
  PWACapabilities,
  PWAInstallState,
  createPWAManager,
  getPWAManager,
  isPWASupported,
  isRunningStandalone,
  canInstallPWA
} from '@/lib/pwa';
import { useNotifications } from './useNotifications';
import { logger } from '@/lib/logger';

export interface UsePWAOptions {
  autoRegisterServiceWorker?: boolean;
  serviceWorkerPath?: string;
  enableAutoInstallPrompt?: boolean;
  autoInstallPromptDelay?: number; // milliseconds
  enableUpdateNotifications?: boolean;
}

export interface UsePWAReturn {
  // PWA state
  capabilities: PWACapabilities;
  installState: PWAInstallState;
  isOfflineReady: boolean;
  updateAvailable: boolean;
  
  // Installation
  showInstallPrompt: () => Promise<boolean>;
  showInstallInstructions: () => void;
  canInstall: boolean;
  
  // Service Worker
  registerServiceWorker: (path?: string) => Promise<ServiceWorkerRegistration | null>;
  updateServiceWorker: () => Promise<boolean>;
  checkForUpdates: () => Promise<boolean>;
  
  // Utilities
  isSupported: boolean;
  isStandalone: boolean;
  resetInstallState: () => void;
  getInstallationGuidance: () => string;
}

export const usePWA = (options: UsePWAOptions = {}): UsePWAReturn => {
  const {
    autoRegisterServiceWorker = true,
    serviceWorkerPath = '/sw.js',
    enableAutoInstallPrompt = false,
    autoInstallPromptDelay = 5000,
    enableUpdateNotifications = true,
  } = options;

  // State
  const [pwaManager, setPwaManager] = useState<PWAManager | null>(null);
  const [capabilities, setCapabilities] = useState<PWACapabilities>({
    isInstallable: false,
    isStandalone: false,
    isInstalled: false,
    supportsServiceWorker: false,
    supportsManifest: false,
    supportsPush: false,
    supportsNotifications: false,
    supportsBackgroundSync: false,
    supportsOffline: false,
    platform: 'unknown',
  });
  const [installState, setInstallState] = useState<PWAInstallState>({
    canInstall: false,
    isInstalled: false,
    installPromptAvailable: false,
    installPromptShown: false,
    userDismissedPrompt: false,
    lastPromptDate: null,
  });
  const [isOfflineReady, setIsOfflineReady] = useState(false);
  const [updateAvailable, setUpdateAvailable] = useState(false);

  // Notifications hook for update notifications
  const { notifySuccess, notifyWarning, hasPermission } = useNotifications({
    autoRequestPermission: false
  });

  // Initialize PWA manager
  useEffect(() => {
    const manager = createPWAManager();
    setPwaManager(manager);

    // Set up event handlers
    manager.setEventHandlers({
      onInstallPromptAvailable: () => {
        logger.info('PWA install prompt available', {}, 'pwa-hook');
        updateState(manager);
        
        // Auto-show install prompt if enabled
        if (enableAutoInstallPrompt && !installState.userDismissedPrompt) {
          setTimeout(() => {
            showInstallPrompt();
          }, autoInstallPromptDelay);
        }
      },
      
      onInstallPromptShown: () => {
        logger.info('PWA install prompt shown', {}, 'pwa-hook');
        updateState(manager);
      },
      
      onInstallAccepted: () => {
        logger.info('PWA installation accepted', {}, 'pwa-hook');
        updateState(manager);
        
        if (hasPermission) {
          notifySuccess('App installée!', 'La Vida Luca a été installée avec succès.');
        }
      },
      
      onInstallDismissed: () => {
        logger.info('PWA installation dismissed', {}, 'pwa-hook');
        updateState(manager);
      },
      
      onInstallationStateChange: (state) => {
        setInstallState(state);
      },
      
      onOfflineReady: () => {
        logger.info('PWA offline ready', {}, 'pwa-hook');
        setIsOfflineReady(true);
        
        if (hasPermission && enableUpdateNotifications) {
          notifySuccess('Mode hors-ligne activé', 'L\'application est maintenant disponible hors ligne.');
        }
      },
      
      onNeedsRefresh: () => {
        logger.info('PWA needs refresh', {}, 'pwa-hook');
        setUpdateAvailable(true);
        
        if (hasPermission && enableUpdateNotifications) {
          notifyWarning('Mise à jour disponible', 'Une nouvelle version de l\'application est disponible.');
        }
      },
    });

    // Update initial state
    updateState(manager);

    // Auto-register service worker
    if (autoRegisterServiceWorker) {
      manager.registerServiceWorker(serviceWorkerPath).then((registration) => {
        if (registration) {
          logger.info('Service worker auto-registered via PWA hook', {}, 'pwa-hook');
        }
      }).catch((error) => {
        logger.error('Service worker auto-registration failed', {
          error: error instanceof Error ? error.message : 'Unknown error'
        }, 'pwa-hook');
      });
    }

    return () => {
      // Cleanup if needed
    };
  }, []);

  // Update state from PWA manager
  const updateState = useCallback((manager: PWAManager) => {
    setCapabilities(manager.getCapabilities());
    setInstallState(manager.getInstallState());
  }, []);

  // Show install prompt
  const showInstallPrompt = useCallback(async (): Promise<boolean> => {
    if (!pwaManager) {
      logger.warn('Attempted to show install prompt but PWA manager not initialized', {}, 'pwa-hook');
      return false;
    }

    try {
      const success = await pwaManager.showInstallPrompt();
      updateState(pwaManager);
      
      logger.info('Install prompt shown via hook', { success }, 'pwa-hook');
      return success;
    } catch (error) {
      logger.error('Error showing install prompt via hook', {
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 'pwa-hook');
      return false;
    }
  }, [pwaManager]);

  // Show install instructions
  const showInstallInstructions = useCallback((): void => {
    if (!pwaManager) {
      return;
    }

    pwaManager.showIOSInstallInstructions();
    updateState(pwaManager);
  }, [pwaManager]);

  // Register service worker
  const registerServiceWorker = useCallback(async (path?: string): Promise<ServiceWorkerRegistration | null> => {
    if (!pwaManager) {
      logger.warn('Attempted to register service worker but PWA manager not initialized', {}, 'pwa-hook');
      return null;
    }

    try {
      const registration = await pwaManager.registerServiceWorker(path || serviceWorkerPath);
      
      if (registration) {
        logger.info('Service worker registered via hook', { path }, 'pwa-hook');
      }
      
      return registration;
    } catch (error) {
      logger.error('Service worker registration failed via hook', {
        path,
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 'pwa-hook');
      return null;
    }
  }, [pwaManager, serviceWorkerPath]);

  // Update service worker
  const updateServiceWorker = useCallback(async (): Promise<boolean> => {
    if (!pwaManager) {
      return false;
    }

    try {
      const success = await pwaManager.updateServiceWorker();
      
      if (success) {
        setUpdateAvailable(false);
        logger.info('Service worker updated via hook', {}, 'pwa-hook');
        
        if (hasPermission && enableUpdateNotifications) {
          notifySuccess('Application mise à jour', 'L\'application a été mise à jour vers la dernière version.');
        }
      }
      
      return success;
    } catch (error) {
      logger.error('Service worker update failed via hook', {
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 'pwa-hook');
      return false;
    }
  }, [pwaManager, hasPermission, enableUpdateNotifications, notifySuccess]);

  // Check for updates
  const checkForUpdates = useCallback(async (): Promise<boolean> => {
    if (!pwaManager) {
      return false;
    }

    try {
      const hasUpdate = await pwaManager.checkForUpdates();
      setUpdateAvailable(hasUpdate);
      
      logger.info('Checked for updates via hook', { hasUpdate }, 'pwa-hook');
      return hasUpdate;
    } catch (error) {
      logger.error('Error checking for updates via hook', {
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 'pwa-hook');
      return false;
    }
  }, [pwaManager]);

  // Reset install state
  const resetInstallState = useCallback((): void => {
    if (!pwaManager) {
      return;
    }

    pwaManager.resetInstallState();
    updateState(pwaManager);
    
    logger.info('Install state reset via hook', {}, 'pwa-hook');
  }, [pwaManager]);

  // Get installation guidance
  const getInstallationGuidance = useCallback((): string => {
    if (!pwaManager) {
      return 'PWA functionality not available';
    }

    return pwaManager.getInstallationGuidance();
  }, [pwaManager]);

  return {
    // State
    capabilities,
    installState,
    isOfflineReady,
    updateAvailable,
    
    // Installation
    showInstallPrompt,
    showInstallInstructions,
    canInstall: installState.canInstall,
    
    // Service Worker
    registerServiceWorker,
    updateServiceWorker,
    checkForUpdates,
    
    // Utilities
    isSupported: isPWASupported(),
    isStandalone: isRunningStandalone(),
    resetInstallState,
    getInstallationGuidance,
  };
};

/**
 * Hook for PWA installation flow
 */
export const usePWAInstallation = (): {
  canInstall: boolean;
  isInstalled: boolean;
  showInstallPrompt: () => Promise<boolean>;
  installationGuidance: string;
} => {
  const {
    capabilities,
    installState,
    showInstallPrompt,
    getInstallationGuidance,
  } = usePWA({ enableAutoInstallPrompt: false });

  return {
    canInstall: installState.canInstall,
    isInstalled: installState.isInstalled || capabilities.isStandalone,
    showInstallPrompt,
    installationGuidance: getInstallationGuidance(),
  };
};

/**
 * Hook for PWA update management
 */
export const usePWAUpdates = (): {
  updateAvailable: boolean;
  isOfflineReady: boolean;
  updateApp: () => Promise<boolean>;
  checkForUpdates: () => Promise<boolean>;
} => {
  const {
    updateAvailable,
    isOfflineReady,
    updateServiceWorker,
    checkForUpdates,
  } = usePWA({ enableUpdateNotifications: true });

  return {
    updateAvailable,
    isOfflineReady,
    updateApp: updateServiceWorker,
    checkForUpdates,
  };
};