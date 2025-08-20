/**
 * Offline page - Displayed when users are offline and content is not cached
 */

import { OfflineFallback } from '@/components/offline';

export default function OfflinePage() {
  return (
    <div className="min-h-[50vh] flex items-center justify-center">
      <OfflineFallback
        title="Vous êtes hors ligne"
        message="Vous n'êtes pas connecté à Internet. Certaines fonctionnalités peuvent être limitées. Reconnectez-vous pour accéder à tout le contenu."
        showRetry={true}
        className="max-w-lg mx-auto"
      />
    </div>
  );
}

export const metadata = {
  title: "Hors ligne",
  description: "Page affichée lorsque vous êtes hors ligne",
};