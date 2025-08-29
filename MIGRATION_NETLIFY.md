# Migration de Vercel vers Netlify

## Vue d'ensemble

Ce document décrit la migration complète du déploiement de l'application La Vida Luca de Vercel vers Netlify.

## Changements effectués

### 1. Configuration Next.js (`apps/web/next.config.js`)

**Avant (Vercel):**
```javascript
const nextConfig = {
  output: 'standalone',
  images: {
    domains: ['localhost', 'lavidaluca.fr'],
  },
};
```

**Après (Netlify):**
```javascript
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    domains: ['localhost', 'lavidaluca.fr'],
    unoptimized: true,
  },
};
```

### 2. Configuration de déploiement

- **Supprimé**: `vercel.json`
- **Ajouté**: `netlify.toml` avec configuration complète

### 3. GitHub Actions (`.github/workflows/deploy.yml`)

- Remplacé l'action Vercel par l'action Netlify
- Mise à jour des secrets requis
- Optimisation du processus de build

### 4. Documentation

- Mise à jour de `README.md`
- Création de `apps/web/NETLIFY_DEPLOYMENT.md`
- Mise à jour de `apps/web/README.md`

## Configuration requise

### Secrets GitHub

Remplacer les anciens secrets Vercel par les nouveaux secrets Netlify :

**À supprimer:**
- `VERCEL_TOKEN`
- `VERCEL_PROJECT_ID`
- `VERCEL_ORG_ID`

**À ajouter:**
- `NETLIFY_SITE_ID`
- `NETLIFY_AUTH_TOKEN`

### Configuration Netlify

1. **Créer un nouveau site sur Netlify**
2. **Connecter le repository GitHub**
3. **Configuration automatique** via `netlify.toml`:
   - Base directory: `apps/web`
   - Build command: `npm run build`
   - Publish directory: `apps/web/out`

## Avantages de la migration

### Performance
- **Static Export**: Site entièrement statique
- **CDN Global**: Distribution optimisée
- **Temps de build**: Plus rapide (~30-60s)

### Fonctionnalités
- **Headers de sécurité**: Configuration avancée
- **Redirects**: Gestion fine des routes
- **Edge Functions**: Possibilité d'ajout futur

### Coûts
- **Netlify gratuit**: Jusqu'à 100GB de bande passante
- **Builds illimités**: Pour les projets open source

## Vérifications post-migration

### ✅ Build
- [x] Build Next.js réussie
- [x] Export statique généré dans `apps/web/out/`
- [x] Assets optimisés

### ✅ Configuration
- [x] `netlify.toml` configuré
- [x] GitHub Actions mis à jour
- [x] Documentation mise à jour

### 🔄 À faire après déploiement
- [ ] Configurer les secrets GitHub
- [ ] Tester le déploiement automatique
- [ ] Vérifier les redirects et headers
- [ ] Configurer le domaine personnalisé
- [ ] Mettre à jour les URLs de l'API backend

## Rollback (si nécessaire)

En cas de problème, la restauration est possible :

1. **Restaurer `vercel.json`**
2. **Restaurer `next.config.js`** avec `output: 'standalone'`
3. **Restaurer les GitHub Actions** Vercel
4. **Reconfigurer les secrets** Vercel

Les fichiers de sauvegarde sont disponibles dans l'historique Git.

## Support

Pour toute question sur cette migration :
- Consulter `apps/web/NETLIFY_DEPLOYMENT.md`
- Vérifier les logs GitHub Actions
- Consulter la documentation Netlify officielle