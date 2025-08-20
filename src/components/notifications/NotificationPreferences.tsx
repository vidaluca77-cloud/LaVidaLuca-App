'use client';

import React, { useState } from 'react';
import { useNotifications } from '@/hooks/useNotifications';
import { type NotificationPreferences as NotificationPreferencesType } from '@/lib/notifications';

interface NotificationPreferencesProps {
  className?: string;
  onClose?: () => void;
}

/**
 * Component for managing notification preferences
 */
export const NotificationPreferences: React.FC<NotificationPreferencesProps> = ({
  className = '',
  onClose,
}) => {
  const { 
    preferences, 
    updatePreferences, 
    registerPushNotifications, 
    requestPermission 
  } = useNotifications();

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleToggleNotifications = async (enabled: boolean) => {
    setIsLoading(true);
    setError(null);
    
    try {
      if (enabled) {
        const granted = await requestPermission();
        if (!granted) {
          setError('Permission de notification refusée. Activez les notifications dans les paramètres de votre navigateur.');
          setIsLoading(false);
          return;
        }
      }
      
      updatePreferences({ enabled });
      setSuccess(enabled ? 'Notifications activées' : 'Notifications désactivées');
    } catch (err) {
      setError('Erreur lors de la mise à jour des préférences');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTogglePushNotifications = async (pushEnabled: boolean) => {
    setIsLoading(true);
    setError(null);
    
    try {
      if (pushEnabled) {
        const subscription = await registerPushNotifications();
        if (!subscription) {
          setError('Impossible d\'activer les notifications push. Vérifiez les paramètres de votre navigateur.');
          setIsLoading(false);
          return;
        }
        setSuccess('Notifications push activées');
      } else {
        updatePreferences({ pushEnabled: false });
        setSuccess('Notifications push désactivées');
      }
    } catch (err) {
      setError('Erreur lors de la configuration des notifications push');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTypeToggle = (type: keyof NotificationPreferencesType['types'], enabled: boolean) => {
    updatePreferences({
      types: {
        ...preferences.types,
        [type]: enabled,
      },
    });
  };

  const handleQuietHoursToggle = (enabled: boolean) => {
    updatePreferences({
      quiet_hours: {
        ...preferences.quiet_hours,
        enabled,
      },
    });
  };

  const handleQuietHoursChange = (field: 'start' | 'end', value: string) => {
    updatePreferences({
      quiet_hours: {
        ...preferences.quiet_hours,
        [field]: value,
      },
    });
  };

  return (
    <div className={`bg-white rounded-lg shadow-lg border border-gray-200 p-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">
          Préférences de notification
        </h2>
        {onClose && (
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-lg p-1"
            aria-label="Fermer"
          >
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      {/* Error/Success Messages */}
      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}
      
      {success && (
        <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-sm text-green-700">{success}</p>
        </div>
      )}

      <div className="space-y-6">
        {/* Main Toggle */}
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-medium text-gray-900">Notifications</h3>
            <p className="text-sm text-gray-500">
              Recevoir des notifications de l'application
            </p>
          </div>
          <button
            type="button"
            disabled={isLoading}
            onClick={() => handleToggleNotifications(!preferences.enabled)}
            className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
              preferences.enabled ? 'bg-blue-600' : 'bg-gray-200'
            } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <span
              className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                preferences.enabled ? 'translate-x-5' : 'translate-x-0'
              }`}
            />
          </button>
        </div>

        {/* Push Notifications */}
        {preferences.enabled && (
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-medium text-gray-900">Notifications push</h3>
              <p className="text-sm text-gray-500">
                Recevoir des notifications même quand l'application est fermée
              </p>
            </div>
            <button
              type="button"
              disabled={isLoading}
              onClick={() => handleTogglePushNotifications(!preferences.pushEnabled)}
              className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                preferences.pushEnabled ? 'bg-blue-600' : 'bg-gray-200'
              } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <span
                className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                  preferences.pushEnabled ? 'translate-x-5' : 'translate-x-0'
                }`}
              />
            </button>
          </div>
        )}

        {/* Notification Types */}
        {preferences.enabled && (
          <div>
            <h3 className="text-sm font-medium text-gray-900 mb-3">
              Types de notifications
            </h3>
            <div className="space-y-3">
              {Object.entries({
                info: { label: 'Informations', description: 'Nouvelles fonctionnalités, conseils' },
                success: { label: 'Succès', description: 'Actions réussies, confirmations' },
                warning: { label: 'Avertissements', description: 'Actions à effectuer, rappels' },
                error: { label: 'Erreurs', description: 'Problèmes, échecs d\'actions' },
              }).map(([type, config]) => (
                <div key={type} className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-700">{config.label}</p>
                    <p className="text-xs text-gray-500">{config.description}</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => handleTypeToggle(
                      type as keyof NotificationPreferencesType['types'], 
                      !preferences.types[type as keyof NotificationPreferencesType['types']]
                    )}
                    className={`relative inline-flex h-5 w-9 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                      preferences.types[type as keyof NotificationPreferencesType['types']] ? 'bg-blue-600' : 'bg-gray-200'
                    }`}
                  >
                    <span
                      className={`pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                        preferences.types[type as keyof NotificationPreferencesType['types']] ? 'translate-x-4' : 'translate-x-0'
                      }`}
                    />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Quiet Hours */}
        {preferences.enabled && (
          <div>
            <div className="flex items-center justify-between mb-3">
              <div>
                <h3 className="text-sm font-medium text-gray-900">Heures de silence</h3>
                <p className="text-sm text-gray-500">
                  Suspendre les notifications pendant certaines heures
                </p>
              </div>
              <button
                type="button"
                onClick={() => handleQuietHoursToggle(!preferences.quiet_hours.enabled)}
                className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                  preferences.quiet_hours.enabled ? 'bg-blue-600' : 'bg-gray-200'
                }`}
              >
                <span
                  className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                    preferences.quiet_hours.enabled ? 'translate-x-5' : 'translate-x-0'
                  }`}
                />
              </button>
            </div>

            {preferences.quiet_hours.enabled && (
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="quiet-start" className="block text-xs font-medium text-gray-700 mb-1">
                    Début
                  </label>
                  <input
                    type="time"
                    id="quiet-start"
                    value={preferences.quiet_hours.start}
                    onChange={(e) => handleQuietHoursChange('start', e.target.value)}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label htmlFor="quiet-end" className="block text-xs font-medium text-gray-700 mb-1">
                    Fin
                  </label>
                  <input
                    type="time"
                    id="quiet-end"
                    value={preferences.quiet_hours.end}
                    onChange={(e) => handleQuietHoursChange('end', e.target.value)}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Browser Support Info */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <p className="text-xs text-gray-500">
          Les notifications push nécessitent un navigateur compatible et une connexion HTTPS. 
          Certaines fonctionnalités peuvent ne pas être disponibles sur tous les appareils.
        </p>
      </div>
    </div>
  );
};

export default NotificationPreferences;