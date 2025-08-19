// src/components/NotificationToast.tsx
'use client';

import { useEffect } from 'react';
import { useAppSelector, useAppDispatch, removeNotification } from '../store/hooks';
import { selectNotifications } from '../store/selectors';

export default function NotificationToast() {
  const notifications = useAppSelector(selectNotifications);
  const dispatch = useAppDispatch();

  useEffect(() => {
    // Auto-remove notifications after 5 seconds
    notifications.forEach(notification => {
      setTimeout(() => {
        dispatch(removeNotification(notification.id));
      }, 5000);
    });
  }, [notifications, dispatch]);

  if (notifications.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {notifications.map(notification => (
        <div
          key={notification.id}
          className={`p-4 rounded-lg shadow-lg max-w-sm animate-slide-in ${
            notification.type === 'success' ? 'bg-green-500 text-white' :
            notification.type === 'error' ? 'bg-red-500 text-white' :
            notification.type === 'warning' ? 'bg-yellow-500 text-white' :
            'bg-blue-500 text-white'
          }`}
        >
          <div className="flex justify-between items-start">
            <p className="text-sm font-medium">{notification.message}</p>
            <button
              onClick={() => dispatch(removeNotification(notification.id))}
              className="ml-2 text-white hover:text-gray-200"
            >
              ×
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}