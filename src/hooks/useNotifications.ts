'use client';

import { useState, useEffect, useCallback } from 'react';
import { 
  notificationManager, 
  type Notification, 
  type NotificationPreferences, 
  type NotificationType,
  type PushSubscriptionData 
} from '@/lib/notifications';
import { logger } from '@/lib/logger';

export interface UseNotificationsReturn {
  notifications: Notification[];
  unreadCount: number;
  preferences: NotificationPreferences;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  addNotification: (
    type: NotificationType,
    title: string,
    message: string,
    options?: {
      action?: { label: string; url: string };
      metadata?: Record<string, any>;
      showBrowser?: boolean;
    }
  ) => string;
  markAsRead: (id: string) => void;
  markAllAsRead: () => void;
  removeNotification: (id: string) => void;
  clearAll: () => void;
  updatePreferences: (updates: Partial<NotificationPreferences>) => void;
  
  // Push notifications
  registerPushNotifications: () => Promise<PushSubscriptionData | null>;
  requestPermission: () => Promise<boolean>;
  
  // Convenience methods
  showInfo: (title: string, message: string, options?: any) => string;
  showSuccess: (title: string, message: string, options?: any) => string;
  showWarning: (title: string, message: string, options?: any) => string;
  showError: (title: string, message: string, options?: any) => string;
}

/**
 * Hook for managing notifications in React components
 */
export const useNotifications = (): UseNotificationsReturn => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [preferences, setPreferences] = useState<NotificationPreferences>(
    notificationManager.getPreferences()
  );
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Initialize and subscribe to changes
  useEffect(() => {
    try {
      // Get initial state
      setNotifications(notificationManager.getNotifications());
      setPreferences(notificationManager.getPreferences());
      setIsLoading(false);

      // Subscribe to changes
      const unsubscribe = notificationManager.subscribe((newNotifications) => {
        setNotifications(newNotifications);
      });

      return unsubscribe;
    } catch (err) {
      logger.error('Error initializing notifications hook', { error: err });
      setError('Failed to initialize notifications');
      setIsLoading(false);
    }
  }, []);

  // Add notification
  const addNotification = useCallback((
    type: NotificationType,
    title: string,
    message: string,
    options?: {
      action?: { label: string; url: string };
      metadata?: Record<string, any>;
      showBrowser?: boolean;
    }
  ): string => {
    try {
      return notificationManager.addNotification(type, title, message, options);
    } catch (err) {
      logger.error('Error adding notification', { error: err });
      setError('Failed to add notification');
      return '';
    }
  }, []);

  // Mark as read
  const markAsRead = useCallback((id: string) => {
    try {
      notificationManager.markAsRead(id);
    } catch (err) {
      logger.error('Error marking notification as read', { error: err, id });
      setError('Failed to mark notification as read');
    }
  }, []);

  // Mark all as read
  const markAllAsRead = useCallback(() => {
    try {
      notificationManager.markAllAsRead();
    } catch (err) {
      logger.error('Error marking all notifications as read', { error: err });
      setError('Failed to mark all notifications as read');
    }
  }, []);

  // Remove notification
  const removeNotification = useCallback((id: string) => {
    try {
      notificationManager.removeNotification(id);
    } catch (err) {
      logger.error('Error removing notification', { error: err, id });
      setError('Failed to remove notification');
    }
  }, []);

  // Clear all notifications
  const clearAll = useCallback(() => {
    try {
      notificationManager.clearAll();
    } catch (err) {
      logger.error('Error clearing all notifications', { error: err });
      setError('Failed to clear notifications');
    }
  }, []);

  // Update preferences
  const updatePreferences = useCallback((updates: Partial<NotificationPreferences>) => {
    try {
      notificationManager.updatePreferences(updates);
      setPreferences(notificationManager.getPreferences());
    } catch (err) {
      logger.error('Error updating notification preferences', { error: err });
      setError('Failed to update preferences');
    }
  }, []);

  // Register push notifications
  const registerPushNotifications = useCallback(async (): Promise<PushSubscriptionData | null> => {
    try {
      setError(null);
      const subscription = await notificationManager.registerPushNotifications();
      
      if (subscription) {
        setPreferences(notificationManager.getPreferences());
      }
      
      return subscription;
    } catch (err) {
      logger.error('Error registering push notifications', { error: err });
      setError('Failed to register push notifications');
      return null;
    }
  }, []);

  // Request permission
  const requestPermission = useCallback(async (): Promise<boolean> => {
    try {
      setError(null);
      return await notificationManager.requestPermission();
    } catch (err) {
      logger.error('Error requesting notification permission', { error: err });
      setError('Failed to request notification permission');
      return false;
    }
  }, []);

  // Convenience methods
  const showInfo = useCallback((title: string, message: string, options?: any) => {
    return addNotification('info', title, message, options);
  }, [addNotification]);

  const showSuccess = useCallback((title: string, message: string, options?: any) => {
    return addNotification('success', title, message, options);
  }, [addNotification]);

  const showWarning = useCallback((title: string, message: string, options?: any) => {
    return addNotification('warning', title, message, options);
  }, [addNotification]);

  const showError = useCallback((title: string, message: string, options?: any) => {
    return addNotification('error', title, message, options);
  }, [addNotification]);

  // Calculate unread count
  const unreadCount = notifications.filter(n => !n.read).length;

  return {
    notifications,
    unreadCount,
    preferences,
    isLoading,
    error,
    
    // Actions
    addNotification,
    markAsRead,
    markAllAsRead,
    removeNotification,
    clearAll,
    updatePreferences,
    
    // Push notifications
    registerPushNotifications,
    requestPermission,
    
    // Convenience methods
    showInfo,
    showSuccess,
    showWarning,
    showError,
  };
};

/**
 * Hook for quick notification actions without full state management
 */
export const useNotificationActions = () => {
  const addNotification = useCallback((
    type: NotificationType,
    title: string,
    message: string,
    options?: any
  ) => {
    return notificationManager.addNotification(type, title, message, options);
  }, []);

  return {
    showInfo: useCallback((title: string, message: string, options?: any) => 
      addNotification('info', title, message, options), [addNotification]),
    showSuccess: useCallback((title: string, message: string, options?: any) => 
      addNotification('success', title, message, options), [addNotification]),
    showWarning: useCallback((title: string, message: string, options?: any) => 
      addNotification('warning', title, message, options), [addNotification]),
    showError: useCallback((title: string, message: string, options?: any) => 
      addNotification('error', title, message, options), [addNotification]),
  };
};