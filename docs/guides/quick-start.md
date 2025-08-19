# Guide de démarrage rapide

## Prérequis

- Node.js 18+ 
- npm ou yarn
- Git

## Installation

1. **Cloner le repository**
   ```bash
   git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
   cd LaVidaLuca-App
   ```

2. **Installer les dépendances**
   ```bash
   npm install
   ```

3. **Configuration des variables d'environnement**
   ```bash
   cp .env.local.example .env.local
   ```
   
   Configurer les variables :
   ```
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   NEXT_PUBLIC_IA_API_URL=your_ia_api_url
   NEXT_PUBLIC_SENTRY_DSN=your_sentry_dsn
   ```

4. **Démarrer en développement**
   ```bash
   npm run dev
   ```

5. **Ouvrir l'application**
   Aller à [http://localhost:3000](http://localhost:3000)

## Déploiement

### Vercel (Frontend)
1. Connecter le repository à Vercel
2. Configurer les variables d'environnement
3. Déployer automatiquement depuis `main`

### Render (API IA)
1. Créer un nouveau service sur Render
2. Connecter le dossier `/apps/ia`
3. Configurer les variables d'environnement

### Supabase (Base de données)
1. Créer un nouveau projet Supabase
2. Importer le schéma depuis `/infra/supabase/schema.sql`
3. Configurer l'authentification

## Tests

```bash
# Lancer les tests
npm test

# Tests en mode watch
npm run test:watch

# Coverage
npm run test:coverage
```

## Build

```bash
# Build de production
npm run build

# Vérifier le build
npm run start
```

## Troubleshooting

### Erreur de build
- Vérifier les variables d'environnement
- S'assurer que toutes les dépendances sont installées
- Nettoyer le cache : `rm -rf .next node_modules && npm install`

### Problème de connexion API
- Vérifier que l'API IA est déployée
- Contrôler les URLs dans les variables d'environnement
- Tester les endpoints avec un outil comme Postman