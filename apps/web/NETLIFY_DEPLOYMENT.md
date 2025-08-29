# Déploiement Netlify - La Vida Luca Frontend

## Configuration automatique

Le déploiement se fait automatiquement via GitHub Actions lors des push sur la branche `main`.

## Configuration manuelle

### 1. Connexion du repository à Netlify

1. Se connecter sur [Netlify](https://app.netlify.com)
2. Cliquer sur "Add new site" > "Import an existing project"
3. Connecter le repository GitHub `vidaluca77-cloud/LaVidaLuca-App`
4. Configurer les paramètres de build :
   - **Base directory**: `apps/web`
   - **Build command**: `npm run build`
   - **Publish directory**: `apps/web/out`

### 2. Variables d'environnement

Dans les paramètres Netlify du site, ajouter les variables d'environnement nécessaires :

```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com

# Contact Information
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789

# App Configuration
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### 3. Configuration des secrets GitHub

Pour le déploiement automatique, configurer ces secrets dans les paramètres GitHub :

- `NETLIFY_SITE_ID`: L'ID du site Netlify
- `NETLIFY_AUTH_TOKEN`: Token d'authentification Netlify

### 4. Déploiement manuel via CLI

```bash
# Installation du CLI Netlify
npm install -g netlify-cli

# Login
netlify login

# Build et déploiement
cd apps/web
npm run build
netlify deploy --prod --dir=out
```

## Optimisations

- **Static Export**: L'application est exportée en tant que site statique
- **Compression**: Gzip automatique par Netlify
- **CDN**: Distribution globale automatique
- **Headers**: Configuration de sécurité dans `netlify.toml`
- **Redirects**: Gestion des routes SPA

## Performance

- **Temps de build**: ~30-60 secondes
- **Déploiement**: ~10-30 secondes
- **Temps de propagation CDN**: ~1-2 minutes

## Debugging

### Logs de déploiement
- Consulter les logs dans l'interface Netlify
- Vérifier les GitHub Actions pour les erreurs

### Problèmes communs
- **Build failed**: Vérifier les dépendances et la configuration Next.js
- **404 errors**: Vérifier les redirects dans `netlify.toml`
- **Assets not loading**: Vérifier le `assetPrefix` dans `next.config.js`