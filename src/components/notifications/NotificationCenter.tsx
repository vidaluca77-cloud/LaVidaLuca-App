/**
 * NotificationCenter component for managing browser notifications
 */

'use client';

import React, { useState } from 'react';
import { useNotifications } from '@/hooks/useNotifications';

export interface NotificationCenterProps {
  className?: string;
  showPermissionStatus?: boolean;
  showPushStatus?: boolean;
  allowTestNotifications?: boolean;
}

export const NotificationCenter: React.FC<NotificationCenterProps> = ({
  className = '',
  showPermissionStatus = true,
  showPushStatus = true,
  allowTestNotifications = false,
}) => {
  const {
    permissionState,
    hasPermission,
    pushSubscription,
    isPushSupported,
    activeNotifications,
    requestPermission,
    subscribeToPush,
    unsubscribeFromPush,
    closeAllNotifications,
    notifySuccess,
    notifyError,
    notifyWarning,
  } = useNotifications();

  const [isRequestingPermission, setIsRequestingPermission] = useState(false);
  const [isManagingPush, setIsManagingPush] = useState(false);

  const handleRequestPermission = async () => {
    if (isRequestingPermission) return;
    
    setIsRequestingPermission(true);
    try {
      await requestPermission();
    } catch (error) {
      console.error('Error requesting permission:', error);
    } finally {
      setIsRequestingPermission(false);
    }
  };

  const handleTogglePush = async () => {
    if (isManagingPush) return;
    
    setIsManagingPush(true);
    try {
      if (pushSubscription) {
        await unsubscribeFromPush();
      } else {
        // You would need to provide your VAPID public key here
        const vapidKey = process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY;
        if (vapidKey) {
          await subscribeToPush(vapidKey);
        }
      }
    } catch (error) {
      console.error('Error managing push subscription:', error);
    } finally {
      setIsManagingPush(false);
    }
  };

  const getPermissionStatusColor = () => {
    switch (permissionState.permission) {
      case 'granted': return 'text-green-600';
      case 'denied': return 'text-red-600';
      default: return 'text-yellow-600';
    }
  };

  const getPermissionStatusText = () => {
    switch (permissionState.permission) {
      case 'granted': return 'Granted';
      case 'denied': return 'Denied';
      default: return 'Not requested';
    }
  };

  const handleTestNotification = async (type: 'success' | 'error' | 'warning') => {
    try {
      const timestamp = new Date().toLocaleTimeString();
      
      switch (type) {
        case 'success':
          await notifySuccess('Test successful!', `This is a test success notification sent at ${timestamp}`);
          break;
        case 'error':
          await notifyError('Test error!', `This is a test error notification sent at ${timestamp}`);
          break;
        case 'warning':
          await notifyWarning('Test warning!', `This is a test warning notification sent at ${timestamp}`);
          break;
      }
    } catch (error) {
      console.error('Error showing test notification:', error);
    }
  };

  return (
    <div className={`bg-white rounded-lg border shadow-sm ${className}`}>
      <div className="p-4 border-b">
        <h3 className="text-lg font-semibold text-gray-900">Notification Center</h3>
      </div>

      <div className="p-4 space-y-4">
        {/* Browser Support Status */}
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div>
            <p className="font-medium text-gray-900">Browser Support</p>
            <p className="text-sm text-gray-600">
              {permissionState.supported ? 'Notifications supported' : 'Notifications not supported'}
            </p>
          </div>
          <span className={`text-2xl ${permissionState.supported ? 'text-green-600' : 'text-red-600'}`}>
            {permissionState.supported ? '✅' : '❌'}
          </span>
        </div>

        {/* Permission Status */}
        {showPermissionStatus && permissionState.supported && (
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div>
              <p className="font-medium text-gray-900">Permission Status</p>
              <p className={`text-sm ${getPermissionStatusColor()}`}>
                {getPermissionStatusText()}
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <span className={`text-2xl ${getPermissionStatusColor()}`}>
                {hasPermission ? '✅' : '⚠️'}
              </span>
              {!hasPermission && permissionState.permission !== 'denied' && (
                <button
                  onClick={handleRequestPermission}
                  disabled={isRequestingPermission}
                  className="px-3 py-1 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 disabled:opacity-50"
                >
                  {isRequestingPermission ? 'Requesting...' : 'Request'}
                </button>
              )}
            </div>
          </div>
        )}

        {/* Push Notifications Status */}
        {showPushStatus && isPushSupported && hasPermission && (
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div>
              <p className="font-medium text-gray-900">Push Notifications</p>
              <p className={`text-sm ${pushSubscription ? 'text-green-600' : 'text-gray-600'}`}>
                {pushSubscription ? 'Enabled' : 'Disabled'}
              </p>
            </div>
            <button
              onClick={handleTogglePush}
              disabled={isManagingPush}
              className={`px-3 py-1 text-sm rounded-md transition-colors ${
                pushSubscription
                  ? 'bg-red-600 text-white hover:bg-red-700'
                  : 'bg-green-600 text-white hover:bg-green-700'
              } disabled:opacity-50`}
            >
              {isManagingPush ? 'Working...' : (pushSubscription ? 'Disable' : 'Enable')}
            </button>
          </div>
        )}

        {/* Active Notifications */}
        <div className="p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <p className="font-medium text-gray-900">Active Notifications</p>
            {activeNotifications.length > 0 && (
              <button
                onClick={closeAllNotifications}
                className="px-2 py-1 bg-red-600 text-white text-xs rounded-md hover:bg-red-700"
              >
                Close All
              </button>
            )}
          </div>
          <p className="text-sm text-gray-600">
            {activeNotifications.length === 0 
              ? 'No active notifications' 
              : `${activeNotifications.length} notification${activeNotifications.length > 1 ? 's' : ''} active`
            }
          </p>
        </div>

        {/* Test Notifications */}
        {allowTestNotifications && hasPermission && (
          <div className="p-3 bg-gray-50 rounded-lg">
            <p className="font-medium text-gray-900 mb-3">Test Notifications</p>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => handleTestNotification('success')}
                className="px-3 py-2 bg-green-600 text-white text-sm rounded-md hover:bg-green-700"
              >
                Test Success
              </button>
              <button
                onClick={() => handleTestNotification('warning')}
                className="px-3 py-2 bg-yellow-600 text-white text-sm rounded-md hover:bg-yellow-700"
              >
                Test Warning
              </button>
              <button
                onClick={() => handleTestNotification('error')}
                className="px-3 py-2 bg-red-600 text-white text-sm rounded-md hover:bg-red-700"
              >
                Test Error
              </button>
            </div>
          </div>
        )}

        {/* Help Text */}
        {permissionState.permission === 'denied' && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center space-x-2">
              <span className="text-red-600">⚠️</span>
              <div>
                <p className="text-sm font-medium text-red-800">
                  Notifications are blocked
                </p>
                <p className="text-xs text-red-600">
                  To enable notifications, please allow them in your browser settings and refresh the page
                </p>
              </div>
            </div>
          </div>
        )}

        {!permissionState.supported && (
          <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
            <div className="flex items-center space-x-2">
              <span className="text-yellow-600">ℹ️</span>
              <div>
                <p className="text-sm font-medium text-yellow-800">
                  Notifications not supported
                </p>
                <p className="text-xs text-yellow-600">
                  Your browser does not support notifications
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default NotificationCenter;