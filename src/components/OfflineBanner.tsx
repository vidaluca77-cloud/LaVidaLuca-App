/**
 * Offline Banner component to show connection status
 */

'use client';

import React from 'react';
import { useConnectionStatus } from '@/hooks/useConnectionStatus';
import { ExclamationTriangleIcon, WifiIcon, SignalIcon } from '@heroicons/react/24/outline';

export function OfflineBanner() {
  const { isOnline, isSlowConnection, effectiveType } = useConnectionStatus();

  if (isOnline && !isSlowConnection) {
    return null; // Don't show banner when everything is good
  }

  return (
    <div
      className={`fixed top-0 left-0 right-0 z-50 p-3 text-center text-sm font-medium ${
        !isOnline
          ? 'bg-red-600 text-white'
          : 'bg-amber-500 text-amber-50'
      }`}
      role="alert"
      aria-live="polite"
    >
      <div className="flex items-center justify-center gap-2">
        {!isOnline ? (
          <>
            <ExclamationTriangleIcon className="h-4 w-4" />
            <span>Vous êtes hors ligne. Certaines fonctionnalités peuvent être limitées.</span>
          </>
        ) : isSlowConnection ? (
          <>
            <SignalIcon className="h-4 w-4" />
            <span>
              Connexion lente détectée ({effectiveType}). L'expérience peut être réduite.
            </span>
          </>
        ) : null}
      </div>
    </div>
  );
}

export default OfflineBanner;