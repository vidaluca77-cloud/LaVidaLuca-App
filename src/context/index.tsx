'use client';

import React, { ReactNode } from 'react';
import { AuthProvider } from './AuthContext';
import { NotificationProvider } from './NotificationContext';

interface ProvidersProps {
  children: ReactNode;
}

export const Providers: React.FC<ProvidersProps> = ({ children }) => {
  return (
    <NotificationProvider>
      <AuthProvider>
        {children}
      </AuthProvider>
    </NotificationProvider>
  );
};

// Export all context hooks for convenience
export { useAuth } from './AuthContext';
export { useNotification } from './NotificationContext';