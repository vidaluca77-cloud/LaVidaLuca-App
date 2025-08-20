/**
 * useNotifications hook for notification management
 * Provides React integration for browser and push notifications
 */

import { useEffect, useState, useCallback, useRef } from 'react';
import {
  NotificationManager,
  BrowserNotification,
  NotificationPermissionState,
  PushSubscription,
  createNotificationManager,
  getNotificationManager
} from '@/lib/notifications';
import { logger } from '@/lib/logger';

export interface UseNotificationsOptions {
  autoRequestPermission?: boolean;
  enablePush?: boolean;
  vapidPublicKey?: string;
  onNotificationClick?: (notification: BrowserNotification) => void;
  onNotificationClose?: (notification: BrowserNotification) => void;
  onNotificationError?: (notification: BrowserNotification) => void;
  onNotificationShow?: (notification: BrowserNotification) => void;
}

export interface UseNotificationsReturn {
  // Permission state
  permissionState: NotificationPermissionState;
  hasPermission: boolean;
  
  // Push subscription
  pushSubscription: PushSubscription | null;
  isPushSupported: boolean;
  
  // Active notifications
  activeNotifications: string[];
  
  // Actions
  requestPermission: () => Promise<NotificationPermission>;
  showNotification: (notification: BrowserNotification) => Promise<string>;
  closeNotification: (id: string) => boolean;
  closeNotificationByTag: (tag: string) => number;
  closeAllNotifications: () => number;
  
  // Push notifications
  subscribeToPush: (vapidKey?: string) => Promise<PushSubscription | null>;
  unsubscribeFromPush: () => Promise<boolean>;
  
  // Convenience methods
  notify: (title: string, body: string, options?: Partial<BrowserNotification>) => Promise<string>;
  notifySuccess: (title: string, body: string, options?: Partial<BrowserNotification>) => Promise<string>;
  notifyError: (title: string, body: string, options?: Partial<BrowserNotification>) => Promise<string>;
  notifyWarning: (title: string, body: string, options?: Partial<BrowserNotification>) => Promise<string>;
}

export const useNotifications = (
  options: UseNotificationsOptions = {}
): UseNotificationsReturn => {
  const {
    autoRequestPermission = false,
    enablePush = false,
    vapidPublicKey,
    onNotificationClick,
    onNotificationClose,
    onNotificationError,
    onNotificationShow,
  } = options;

  // State
  const [permissionState, setPermissionState] = useState<NotificationPermissionState>({
    permission: 'default',
    supported: false,
    pushSupported: false,
    serviceWorkerSupported: false,
  });

  const [pushSubscription, setPushSubscription] = useState<PushSubscription | null>(null);
  const [activeNotifications, setActiveNotifications] = useState<string[]>([]);

  // Refs
  const managerRef = useRef<NotificationManager | null>(null);

  // Initialize notification manager
  useEffect(() => {
    managerRef.current = createNotificationManager();

    // Set up event handlers
    if (onNotificationClick) {
      managerRef.current.on('onClick', onNotificationClick);
    }
    if (onNotificationClose) {
      managerRef.current.on('onClose', onNotificationClose);
    }
    if (onNotificationError) {
      managerRef.current.on('onError', onNotificationError);
    }
    if (onNotificationShow) {
      managerRef.current.on('onShow', onNotificationShow);
    }

    // Update initial state
    const initialPermissionState = managerRef.current.getPermissionState();
    setPermissionState(initialPermissionState);

    const initialPushSubscription = managerRef.current.getPushSubscription();
    setPushSubscription(initialPushSubscription);

    const initialActiveNotifications = managerRef.current.getActiveNotifications();
    setActiveNotifications(initialActiveNotifications);

    logger.info('Notification manager initialized in hook', {
      permission: initialPermissionState.permission,
      supported: initialPermissionState.supported,
      pushSupported: initialPermissionState.pushSupported
    }, 'notifications-hook');

    return () => {
      // Clean up event handlers
      if (onNotificationClick) {
        managerRef.current?.off('onClick', onNotificationClick);
      }
      if (onNotificationClose) {
        managerRef.current?.off('onClose', onNotificationClose);
      }
      if (onNotificationError) {
        managerRef.current?.off('onError', onNotificationError);
      }
      if (onNotificationShow) {
        managerRef.current?.off('onShow', onNotificationShow);
      }
    };
  }, []);

  // Auto-request permission
  useEffect(() => {
    if (autoRequestPermission && permissionState.permission === 'default') {
      requestPermission();
    }
  }, [autoRequestPermission, permissionState.permission]);

  // Auto-setup push notifications
  useEffect(() => {
    if (
      enablePush &&
      vapidPublicKey &&
      permissionState.permission === 'granted' &&
      permissionState.pushSupported &&
      !pushSubscription
    ) {
      subscribeToPush(vapidPublicKey);
    }
  }, [enablePush, vapidPublicKey, permissionState, pushSubscription]);

  // Update active notifications periodically
  useEffect(() => {
    const updateActiveNotifications = () => {
      if (managerRef.current) {
        const notifications = managerRef.current.getActiveNotifications();
        setActiveNotifications(notifications);
      }
    };

    const interval = setInterval(updateActiveNotifications, 1000);
    return () => clearInterval(interval);
  }, []);

  // Request permission function
  const requestPermission = useCallback(async (): Promise<NotificationPermission> => {
    if (!managerRef.current) {
      logger.warn('Attempted to request permission but manager not initialized', {}, 'notifications-hook');
      return 'denied';
    }

    try {
      const permission = await managerRef.current.requestPermission();
      const newPermissionState = managerRef.current.getPermissionState();
      setPermissionState(newPermissionState);
      
      logger.info('Permission requested via hook', { permission }, 'notifications-hook');
      
      return permission;
    } catch (error) {
      logger.error('Error requesting permission via hook', {
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 'notifications-hook');
      
      return 'denied';
    }
  }, []);

  // Show notification function
  const showNotification = useCallback(async (notification: BrowserNotification): Promise<string> => {
    if (!managerRef.current) {
      throw new Error('Notification manager not initialized');
    }

    try {
      const id = await managerRef.current.showNotification(notification);
      
      // Update active notifications
      const newActiveNotifications = managerRef.current.getActiveNotifications();
      setActiveNotifications(newActiveNotifications);
      
      logger.info('Notification shown via hook', {
        id,
        title: notification.title
      }, 'notifications-hook');
      
      return id;
    } catch (error) {
      logger.error('Error showing notification via hook', {
        title: notification.title,
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 'notifications-hook');
      
      throw error;
    }
  }, []);

  // Close notification function
  const closeNotification = useCallback((id: string): boolean => {
    if (!managerRef.current) {
      return false;
    }

    const success = managerRef.current.closeNotification(id);
    
    if (success) {
      const newActiveNotifications = managerRef.current.getActiveNotifications();
      setActiveNotifications(newActiveNotifications);
      
      logger.debug('Notification closed via hook', { id }, 'notifications-hook');
    }
    
    return success;
  }, []);

  // Close notification by tag function
  const closeNotificationByTag = useCallback((tag: string): number => {
    if (!managerRef.current) {
      return 0;
    }

    const count = managerRef.current.closeNotificationByTag(tag);
    
    if (count > 0) {
      const newActiveNotifications = managerRef.current.getActiveNotifications();
      setActiveNotifications(newActiveNotifications);
      
      logger.debug('Notifications closed by tag via hook', { tag, count }, 'notifications-hook');
    }
    
    return count;
  }, []);

  // Close all notifications function
  const closeAllNotifications = useCallback((): number => {
    if (!managerRef.current) {
      return 0;
    }

    const count = managerRef.current.closeAllNotifications();
    setActiveNotifications([]);
    
    if (count > 0) {
      logger.info('All notifications closed via hook', { count }, 'notifications-hook');
    }
    
    return count;
  }, []);

  // Subscribe to push function
  const subscribeToPush = useCallback(async (vapidKey?: string): Promise<PushSubscription | null> => {
    if (!managerRef.current) {
      logger.warn('Attempted to subscribe to push but manager not initialized', {}, 'notifications-hook');
      return null;
    }

    const key = vapidKey || vapidPublicKey;
    if (!key) {
      logger.warn('No VAPID public key provided for push subscription', {}, 'notifications-hook');
      return null;
    }

    try {
      const subscription = await managerRef.current.subscribeToPush(key);
      setPushSubscription(subscription);
      
      logger.info('Push subscription created via hook', {
        hasSubscription: !!subscription
      }, 'notifications-hook');
      
      return subscription;
    } catch (error) {
      logger.error('Error subscribing to push via hook', {
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 'notifications-hook');
      
      return null;
    }
  }, [vapidPublicKey]);

  // Unsubscribe from push function
  const unsubscribeFromPush = useCallback(async (): Promise<boolean> => {
    if (!managerRef.current) {
      return false;
    }

    try {
      const success = await managerRef.current.unsubscribeFromPush();
      
      if (success) {
        setPushSubscription(null);
        logger.info('Push subscription removed via hook', {}, 'notifications-hook');
      }
      
      return success;
    } catch (error) {
      logger.error('Error unsubscribing from push via hook', {
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 'notifications-hook');
      
      return false;
    }
  }, []);

  // Convenience methods
  const notify = useCallback(
    (title: string, body: string, options?: Partial<BrowserNotification>): Promise<string> => {
      return showNotification({ title, body, ...options });
    },
    [showNotification]
  );

  const notifySuccess = useCallback(
    (title: string, body: string, options?: Partial<BrowserNotification>): Promise<string> => {
      if (!managerRef.current) {
        throw new Error('Notification manager not initialized');
      }
      return managerRef.current.notifySuccess(title, body, options);
    },
    []
  );

  const notifyError = useCallback(
    (title: string, body: string, options?: Partial<BrowserNotification>): Promise<string> => {
      if (!managerRef.current) {
        throw new Error('Notification manager not initialized');
      }
      return managerRef.current.notifyError(title, body, options);
    },
    []
  );

  const notifyWarning = useCallback(
    (title: string, body: string, options?: Partial<BrowserNotification>): Promise<string> => {
      if (!managerRef.current) {
        throw new Error('Notification manager not initialized');
      }
      return managerRef.current.notifyWarning(title, body, options);
    },
    []
  );

  return {
    // State
    permissionState,
    hasPermission: permissionState.permission === 'granted',
    pushSubscription,
    isPushSupported: permissionState.pushSupported,
    activeNotifications,
    
    // Actions
    requestPermission,
    showNotification,
    closeNotification,
    closeNotificationByTag,
    closeAllNotifications,
    
    // Push notifications
    subscribeToPush,
    unsubscribeFromPush,
    
    // Convenience methods
    notify,
    notifySuccess,
    notifyError,
    notifyWarning,
  };
};

/**
 * Hook for simple notification display
 */
export const useSimpleNotifications = (): {
  notify: (title: string, body: string) => Promise<void>;
  notifySuccess: (message: string) => Promise<void>;
  notifyError: (message: string) => Promise<void>;
  notifyWarning: (message: string) => Promise<void>;
  hasPermission: boolean;
  requestPermission: () => Promise<NotificationPermission>;
} => {
  const {
    notify: showNotify,
    notifySuccess: showSuccess,
    notifyError: showError,
    notifyWarning: showWarning,
    hasPermission,
    requestPermission,
  } = useNotifications({ autoRequestPermission: true });

  const notify = useCallback(async (title: string, body: string): Promise<void> => {
    try {
      await showNotify(title, body);
    } catch (error) {
      logger.error('Error in simple notification', {
        title,
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 'notifications-hook');
    }
  }, [showNotify]);

  const notifySuccess = useCallback(async (message: string): Promise<void> => {
    try {
      await showSuccess('Success', message);
    } catch (error) {
      logger.error('Error in success notification', {
        message,
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 'notifications-hook');
    }
  }, [showSuccess]);

  const notifyError = useCallback(async (message: string): Promise<void> => {
    try {
      await showError('Error', message);
    } catch (error) {
      logger.error('Error in error notification', {
        message,
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 'notifications-hook');
    }
  }, [showError]);

  const notifyWarning = useCallback(async (message: string): Promise<void> => {
    try {
      await showWarning('Warning', message);
    } catch (error) {
      logger.error('Error in warning notification', {
        message,
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 'notifications-hook');
    }
  }, [showWarning]);

  return {
    notify,
    notifySuccess,
    notifyError,
    notifyWarning,
    hasPermission,
    requestPermission,
  };
};

/**
 * Hook for managing notification permissions
 */
export const useNotificationPermission = (): {
  permission: NotificationPermission;
  isSupported: boolean;
  isGranted: boolean;
  isDenied: boolean;
  isDefault: boolean;
  requestPermission: () => Promise<NotificationPermission>;
} => {
  const { permissionState, requestPermission } = useNotifications();

  return {
    permission: permissionState.permission,
    isSupported: permissionState.supported,
    isGranted: permissionState.permission === 'granted',
    isDenied: permissionState.permission === 'denied',
    isDefault: permissionState.permission === 'default',
    requestPermission,
  };
};