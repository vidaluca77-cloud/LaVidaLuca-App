'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { NotificationState } from '@/types';
import { Toast } from '@/components/ui';

interface NotificationContextType {
  showNotification: (
    type: NotificationState['type'],
    message: string,
    duration?: number
  ) => void;
  showSuccess: (message: string, duration?: number) => void;
  showError: (message: string, duration?: number) => void;
  showWarning: (message: string, duration?: number) => void;
  showInfo: (message: string, duration?: number) => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

interface NotificationProviderProps {
  children: ReactNode;
}

export const NotificationProvider: React.FC<NotificationProviderProps> = ({ children }) => {
  const [notifications, setNotifications] = useState<NotificationState[]>([]);

  const removeNotification = (id: string) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  };

  const showNotification = (
    type: NotificationState['type'],
    message: string,
    duration = 5000
  ) => {
    const id = `notification-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const notification: NotificationState = {
      id,
      type,
      message,
      duration,
    };

    setNotifications(prev => [...prev, notification]);
  };

  const showSuccess = (message: string, duration?: number) => {
    showNotification('success', message, duration);
  };

  const showError = (message: string, duration?: number) => {
    showNotification('error', message, duration);
  };

  const showWarning = (message: string, duration?: number) => {
    showNotification('warning', message, duration);
  };

  const showInfo = (message: string, duration?: number) => {
    showNotification('info', message, duration);
  };

  const value: NotificationContextType = {
    showNotification,
    showSuccess,
    showError,
    showWarning,
    showInfo,
  };

  return (
    <NotificationContext.Provider value={value}>
      {children}
      
      {/* Toast container */}
      <div className="fixed top-4 right-4 z-50 space-y-2 max-w-sm">
        {notifications.map(notification => (
          <Toast
            key={notification.id}
            id={notification.id}
            type={notification.type}
            message={notification.message}
            duration={notification.duration}
            onClose={removeNotification}
          />
        ))}
      </div>
    </NotificationContext.Provider>
  );
};

export const useNotification = (): NotificationContextType => {
  const context = useContext(NotificationContext);
  if (context === undefined) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }
  return context;
};