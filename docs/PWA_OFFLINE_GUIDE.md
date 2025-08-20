# Mode Hors Ligne et PWA - Guide d'Utilisation

Cette documentation décrit les nouvelles fonctionnalités hors ligne et PWA implémentées dans l'application La Vida Luca.

## 🌐 Fonctionnalités Hors Ligne

### Cache Intelligent
- **IndexedDB** comme stockage principal
- **LocalStorage** comme fallback
- Expiration automatique des données
- Nettoyage périodique du cache

### File d'Attente des Actions
- Actions mises en file d'attente automatiquement hors ligne
- Synchronisation automatique lors de la reconnexion
- Gestion des priorités (high, normal, low)
- Retry automatique avec backoff

### Types d'Actions Supportées
- Soumission de formulaires de contact
- Préférences utilisateur
- Interactions avec les activités

## 📱 Progressive Web App (PWA)

### Service Worker
- Mise en cache automatique des ressources
- Stratégies de cache optimisées :
  - **Cache First** pour les images et fonts
  - **Network First** pour les pages et API
  - **Stale While Revalidate** pour les assets statiques

### Installation
- Prompt d'installation automatique
- Support multi-plateforme (desktop et mobile)
- Raccourcis dans le manifest PWA
- Icônes adaptatives

### Fonctionnalités Hors Ligne
- Navigation hors ligne complète
- Formulaires fonctionnels en mode hors ligne
- Indicateurs visuels de statut de connexion

## 🎛️ Interface Utilisateur

### Indicateurs de Statut
- **ConnectionStatusIndicator** : Indicateur compact dans l'en-tête
- **OfflineBanner** : Bannière d'alerte en haut de page
- **OfflineNotification** : Notification flottante

### Installation PWA
- **PWAInstallPrompt** : Prompt d'installation élégant
- **PWAUpdateNotification** : Notification de mise à jour
- **PWAStatusIndicator** : Indicateur de statut PWA

## 📊 Monitoring et Dashboard

### Nouvelles Métriques
- Statut de connexion en temps réel
- Taille du cache (IndexedDB + LocalStorage)
- Longueur de la file d'attente hors ligne
- État du Service Worker

### Dashboard de Monitoring
Accessible à `/monitoring` en mode développement :
- Métriques PWA et hors ligne
- Statut de synchronisation
- Performance du cache
- Diagnostics en temps réel

## 🔧 Configuration

### Variables d'Environnement
```bash
# Optional: Désactiver la promotion d'installation PWA
NEXT_PUBLIC_DISABLE_PWA_PROMPT=true

# Optional: Taille maximale du cache (en MB)
NEXT_PUBLIC_MAX_CACHE_SIZE=50
```

### Next.js Configuration
Le projet utilise Workbox pour la génération automatique du Service Worker :
```javascript
// next.config.js
const { InjectManifest } = require('workbox-webpack-plugin');
```

## 📝 API et Hooks

### Hook useConnectionStatus
```typescript
const {
  isOnline,
  isOfflineMode,
  queueLength,
  isProcessing,
  lastOnline,
  lastOffline
} = useConnectionStatus();
```

### Hook usePWAInstall
```typescript
const {
  canInstall,
  isInstalled,
  isStandalone,
  serviceWorkerReady,
  installPWA,
  updateServiceWorker
} = usePWAInstall();
```

### Offline Queue Manager
```typescript
// Ajouter une action à la file d'attente
await offlineQueue.enqueue('CONTACT_FORM_SUBMIT', formData, {
  priority: 'high'
});

// Surveiller les événements de synchronisation
offlineQueue.onSync((action, success) => {
  console.log(`Action ${action.type} ${success ? 'réussie' : 'échouée'}`);
});
```

### Cache Manager
```typescript
// Stocker des données
await offlineCacheManager.set('user-preferences', userData, {
  maxAge: 24 * 60 * 60 * 1000 // 24 heures
});

// Récupérer des données
const userData = await offlineCacheManager.get('user-preferences');
```

## 🧪 Tests

### Tests Unitaires
- Tests complets pour tous les composants
- Tests des hooks avec mocking approprié
- Tests de l'offline cache manager
- Tests de la file d'attente

### Commandes de Test
```bash
# Tests des fonctionnalités hors ligne
npm test tests/lib/

# Tests des hooks
npm test tests/hooks/

# Tests des composants
npm test tests/components/
```

## 🚀 Performance

### Métriques Cibles
- **Cache Hit Rate** > 80%
- **Queue Processing Time** < 2s
- **Service Worker Activation** < 500ms
- **PWA Install Success Rate** > 90%

### Optimisations
- Compression automatique avec Workbox
- Précaching des ressources critiques
- Lazy loading des composants PWA
- Débouncing des mises à jour de statut

## 🔒 Sécurité et Confidentialité

### Protection des Données
- Chiffrement optionnel des données sensibles
- Nettoyage automatique du cache expiré
- Respect du RGPD pour les données hors ligne
- Isolation du cache par origine

### Service Worker
- Content Security Policy (CSP) compatible
- Mise à jour sécurisée du Service Worker
- Validation des actions mises en file d'attente
- Filtrage des requêtes sensibles

## 📚 Ressources Supplémentaires

- [Documentation Workbox](https://developers.google.com/web/tools/workbox)
- [Guide PWA de Google](https://web.dev/progressive-web-apps/)
- [IndexedDB API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)