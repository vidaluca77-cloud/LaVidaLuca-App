'use client';

import { Metadata } from 'next';

// Since this is client-side only, remove the Metadata export
// export const metadata: Metadata = {
//   title: 'Mode hors ligne - La Vida Luca',
//   description: 'Cette page s\'affiche lorsque vous êtes hors ligne',
// };

export default function OfflinePage() {
  const handleRefresh = () => {
    if (typeof window !== 'undefined') {
      window.location.reload();
    }
  };

  const handleGoHome = () => {
    if (typeof window !== 'undefined') {
      window.location.href = '/';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-500 to-green-600 flex items-center justify-center p-4">
      <div className="max-w-md mx-auto text-center text-white">
        <div className="mb-8">
          <div className="w-24 h-24 mx-auto mb-6 bg-white/10 rounded-full flex items-center justify-center text-4xl">
            🌱
          </div>
          <h1 className="text-3xl font-bold mb-4">Mode hors ligne</h1>
          <p className="text-lg opacity-90 mb-6">
            Vous êtes actuellement hors ligne. Certaines fonctionnalités peuvent être limitées, 
            mais vous pouvez toujours consulter le contenu déjà mis en cache.
          </p>
        </div>

        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 mb-6 border border-white/20">
          <div className="flex items-center justify-between">
            <span className="font-medium">📡 Statut de connexion:</span>
            <span className="text-yellow-200">Hors ligne</span>
          </div>
        </div>

        <div className="space-y-3">
          <button 
            onClick={handleRefresh}
            className="w-full bg-white/20 hover:bg-white/30 backdrop-blur-sm border border-white/30 rounded-lg px-6 py-3 font-medium transition-all duration-200"
          >
            Vérifier la connexion
          </button>
          
          <button 
            onClick={handleGoHome}
            className="w-full bg-white/20 hover:bg-white/30 backdrop-blur-sm border border-white/30 rounded-lg px-6 py-3 font-medium transition-all duration-200"
          >
            Retour à l'accueil
          </button>
        </div>

        <div className="mt-8 text-sm opacity-80">
          <p>
            💡 <strong>Astuce:</strong> Les données que vous créez hors ligne seront automatiquement 
            synchronisées lorsque la connexion sera rétablie.
          </p>
        </div>
      </div>
    </div>
  );
}