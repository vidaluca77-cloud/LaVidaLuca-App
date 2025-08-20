/**
 * PWA Update Notification Component
 * Shows notification when a new version of the app is available
 */

'use client';

import React, { useState, useEffect } from 'react';
import { pwaManager } from '@/lib/pwa/PWAManager';

interface PWAUpdateNotificationProps {
  className?: string;
  position?: 'top' | 'bottom';
}

export const PWAUpdateNotification: React.FC<PWAUpdateNotificationProps> = ({
  className = '',
  position = 'bottom'
}) => {
  const [showUpdate, setShowUpdate] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);

  useEffect(() => {
    // Listen for update availability
    const handleUpdateAvailable = () => {
      setShowUpdate(true);
    };

    window.addEventListener('sw-update-available', handleUpdateAvailable);

    return () => {
      window.removeEventListener('sw-update-available', handleUpdateAvailable);
    };
  }, []);

  const handleUpdate = async () => {
    setIsUpdating(true);
    
    try {
      await pwaManager.applyUpdate();
      // The page will reload automatically after update
    } catch (error) {
      console.error('Update failed:', error);
      setIsUpdating(false);
    }
  };

  const handleDismiss = () => {
    setShowUpdate(false);
  };

  if (!showUpdate) {
    return null;
  }

  const positionClasses = position === 'top' 
    ? 'top-4' 
    : 'bottom-4';

  return (
    <div 
      className={`
        fixed left-4 right-4 z-50 ${positionClasses}
        ${className}
      `}
    >
      <div 
        className="
          bg-white border border-gray-200 rounded-lg shadow-lg p-4 max-w-md mx-auto
          animate-slide-up
        "
        role="alert"
        aria-live="polite"
      >
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
              <svg
                className="w-5 h-5 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                />
              </svg>
            </div>
          </div>

          <div className="flex-1">
            <h3 className="text-sm font-semibold text-gray-900 mb-1">
              App Update Available
            </h3>
            <p className="text-sm text-gray-600 mb-3">
              A new version of La Vida Luca is ready. Update now to get the latest features and improvements.
            </p>

            <div className="flex gap-2">
              <button
                onClick={handleUpdate}
                disabled={isUpdating}
                className="
                  bg-blue-600 text-white px-3 py-1.5 rounded text-sm font-medium
                  hover:bg-blue-700 transition-colors duration-200
                  disabled:opacity-50 disabled:cursor-not-allowed
                  flex items-center gap-1.5
                "
              >
                {isUpdating ? (
                  <>
                    <div className="animate-spin h-3 w-3 border-2 border-white border-t-transparent rounded-full" />
                    Updating...
                  </>
                ) : (
                  <>
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                      />
                    </svg>
                    Update Now
                  </>
                )}
              </button>

              <button
                onClick={handleDismiss}
                className="
                  text-gray-600 hover:text-gray-800 px-3 py-1.5 text-sm
                  transition-colors duration-200
                "
              >
                Later
              </button>
            </div>
          </div>

          <button
            onClick={handleDismiss}
            className="
              flex-shrink-0 text-gray-400 hover:text-gray-600 p-1
              transition-colors duration-200
            "
            aria-label="Dismiss update notification"
          >
            <svg
              className="w-4 h-4"
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

export default PWAUpdateNotification;