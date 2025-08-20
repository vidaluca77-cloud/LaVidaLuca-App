'use client';

import React, { useState } from 'react';
import { useNotifications } from '@/lib/notifications';
import { 
  BellIcon, 
  BellSlashIcon, 
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline';

interface NotificationSettingsProps {
  className?: string;
}

export const NotificationSettings: React.FC<NotificationSettingsProps> = ({ className = '' }) => {
  const {
    isSupported,
    permission,
    isSubscribed,
    isLoading,
    requestPermission,
    subscribe,
    unsubscribe,
    testNotification
  } = useNotifications();
  
  const [showDetails, setShowDetails] = useState(false);
  const [testLoading, setTestLoading] = useState(false);

  const handleToggleNotifications = async () => {
    try {
      if (isSubscribed) {
        await unsubscribe();
      } else {
        if (permission !== 'granted') {
          await requestPermission();
        }
        await subscribe();
      }
    } catch (error) {
      console.error('Error toggling notifications:', error);
    }
  };

  const handleTestNotification = async () => {
    setTestLoading(true);
    try {
      await testNotification();
    } catch (error) {
      console.error('Test notification failed:', error);
    } finally {
      setTestLoading(false);
    }
  };

  if (!isSupported) {
    return (
      <div className={`p-4 bg-gray-50 rounded-lg border ${className}`}>
        <div className="flex items-center gap-3">
          <BellSlashIcon className="w-5 h-5 text-gray-400" />
          <div>
            <h3 className="font-medium text-gray-900">Notifications non supportées</h3>
            <p className="text-sm text-gray-600">
              Votre navigateur ne supporte pas les notifications push.
            </p>
          </div>
        </div>
      </div>
    );
  }

  const getStatusIcon = () => {
    if (permission === 'granted' && isSubscribed) {
      return <CheckCircleIcon className="w-5 h-5 text-green-600" />;
    } else if (permission === 'denied') {
      return <ExclamationTriangleIcon className="w-5 h-5 text-red-600" />;
    } else {
      return <InformationCircleIcon className="w-5 h-5 text-blue-600" />;
    }
  };

  const getStatusText = () => {
    if (permission === 'granted' && isSubscribed) {
      return { title: 'Notifications activées', description: 'Vous recevrez des notifications importantes.' };
    } else if (permission === 'denied') {
      return { 
        title: 'Notifications bloquées', 
        description: 'Activez les notifications dans les paramètres de votre navigateur.' 
      };
    } else if (permission === 'granted' && !isSubscribed) {
      return { 
        title: 'Notifications disponibles', 
        description: 'Cliquez pour activer les notifications.' 
      };
    } else {
      return { 
        title: 'Notifications disponibles', 
        description: 'Restez informé des nouveautés et événements importants.' 
      };
    }
  };

  const status = getStatusText();

  return (
    <div className={`p-4 bg-white rounded-lg border ${className}`}>
      {/* Main toggle */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {getStatusIcon()}
          <div>
            <h3 className="font-medium text-gray-900">{status.title}</h3>
            <p className="text-sm text-gray-600">{status.description}</p>
          </div>
        </div>
        
        {permission !== 'denied' && (
          <button
            onClick={handleToggleNotifications}
            disabled={isLoading}
            className={`
              relative inline-flex h-6 w-11 items-center rounded-full transition-colors
              ${isSubscribed ? 'bg-green-600' : 'bg-gray-200'}
              ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
            `}
          >
            <span
              className={`
                inline-block h-4 w-4 transform rounded-full bg-white transition-transform
                ${isSubscribed ? 'translate-x-6' : 'translate-x-1'}
              `}
            />
          </button>
        )}
      </div>

      {/* Additional options */}
      {isSubscribed && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-900">Tester les notifications</p>
              <p className="text-xs text-gray-600">Vérifiez que tout fonctionne correctement</p>
            </div>
            <button
              onClick={handleTestNotification}
              disabled={testLoading}
              className="px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 transition-colors disabled:opacity-50"
            >
              {testLoading ? 'Test...' : 'Tester'}
            </button>
          </div>
        </div>
      )}

      {/* Show details toggle */}
      <button
        onClick={() => setShowDetails(!showDetails)}
        className="mt-3 text-xs text-gray-500 hover:text-gray-700 transition-colors"
      >
        {showDetails ? 'Masquer les détails' : 'Voir les détails'}
      </button>

      {/* Details */}
      {showDetails && (
        <div className="mt-3 p-3 bg-gray-50 rounded-md">
          <h4 className="text-xs font-medium text-gray-900 mb-2">Types de notifications</h4>
          <ul className="text-xs text-gray-600 space-y-1">
            <li>• Nouvelles activités disponibles</li>
            <li>• Événements et ateliers</li>
            <li>• Mises à jour importantes</li>
            <li>• Rappels de participation</li>
          </ul>
          
          <div className="mt-3 pt-3 border-t border-gray-200">
            <p className="text-xs text-gray-500">
              <strong>Permission:</strong> {permission}<br />
              <strong>Abonné:</strong> {isSubscribed ? 'Oui' : 'Non'}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default NotificationSettings;