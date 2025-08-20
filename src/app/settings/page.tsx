import NotificationSettings from '@/components/NotificationSettings';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Paramètres',
  description: 'Configurez vos préférences et paramètres de l\'application'
};

export default function SettingsPage() {
  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Paramètres</h1>
      
      <div className="space-y-6">
        {/* Notifications Section */}
        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Notifications</h2>
          <NotificationSettings />
        </section>

        {/* Cache and Offline Section */}
        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Mode hors ligne</h2>
          <div className="p-4 bg-white rounded-lg border">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-medium text-gray-900">Cache des données</h3>
                <p className="text-sm text-gray-600">
                  Les données sont automatiquement mises en cache pour une utilisation hors ligne.
                </p>
              </div>
            </div>
            
            <div className="mt-4 p-3 bg-blue-50 rounded-md">
              <h4 className="text-sm font-medium text-blue-900 mb-2">Fonctionnalités hors ligne</h4>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Navigation des pages visitées</li>
                <li>• Consultation des activités en cache</li>
                <li>• Soumission de formulaires (synchronisés plus tard)</li>
                <li>• Accès aux informations de contact</li>
              </ul>
            </div>
          </div>
        </section>

        {/* PWA Section */}
        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Application</h2>
          <div className="p-4 bg-white rounded-lg border">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-medium text-gray-900">Installation sur l'écran d'accueil</h3>
                <p className="text-sm text-gray-600">
                  Installez l'application pour un accès rapide et une meilleure expérience.
                </p>
              </div>
            </div>
            
            <div className="mt-4 p-3 bg-green-50 rounded-md">
              <h4 className="text-sm font-medium text-green-900 mb-2">Avantages de l'installation</h4>
              <ul className="text-sm text-green-800 space-y-1">
                <li>• Lancement rapide depuis l'écran d'accueil</li>
                <li>• Fonctionnement hors ligne</li>
                <li>• Notifications push</li>
                <li>• Interface plein écran</li>
              </ul>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}