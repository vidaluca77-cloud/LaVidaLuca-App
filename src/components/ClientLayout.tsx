/**
 * Client-side layout wrapper for offline and PWA functionality
 */

'use client';

import { useEffect } from 'react';
import { offlineManager } from '@/lib/offline/OfflineManager';
import { pwaManager } from '@/lib/pwa/PWAManager';
import OfflineIndicator from '@/components/offline/OfflineIndicator';
import PWAInstallBanner from '@/components/pwa/PWAInstallBanner';
import PWAUpdateNotification from '@/components/pwa/PWAUpdateNotification';

interface ClientLayoutProps {
  children: React.ReactNode;
}

export const ClientLayout: React.FC<ClientLayoutProps> = ({ children }) => {
  useEffect(() => {
    // Initialize offline manager and PWA features
    const initializeOfflineAndPWA = async () => {
      try {
        // Initialize offline functionality
        await offlineManager.init({
          autoSync: true,
          syncInterval: 30000, // 30 seconds
          maxCacheAge: 24 * 60 * 60 * 1000, // 24 hours
          enableNotifications: true
        });

        // Initialize PWA features
        await pwaManager.init();

        console.log('Offline and PWA features initialized successfully');
      } catch (error) {
        console.error('Failed to initialize offline/PWA features:', error);
      }
    };

    initializeOfflineAndPWA();

    // Cleanup on unmount
    return () => {
      offlineManager.destroy();
    };
  }, []);

  return (
    <>
      {/* PWA Install Banner */}
      <PWAInstallBanner />
      
      {/* Offline Status Indicator */}
      <OfflineIndicator position="top-right" />
      
      {/* PWA Update Notification */}
      <PWAUpdateNotification position="bottom" />
      
      {/* Main content */}
      {children}
    </>
  );
};