# Processus de déploiement

## Vue d'ensemble

Le projet La Vida Luca utilise une architecture distribuée avec plusieurs environnements :

- **Frontend** : Vercel (Next.js)
- **API IA** : Render (FastAPI)
- **Base de données** : Supabase (PostgreSQL)

## Environnements

### Développement (local)
- Frontend : `http://localhost:3000`
- API IA : `http://localhost:8000`
- Base de données : Supabase dev

### Staging
- Frontend : `https://la-vida-luca-staging.vercel.app`
- API IA : `https://api-ia-staging.render.com`
- Base de données : Supabase staging

### Production
- Frontend : `https://la-vida-luca.vercel.app`
- API IA : `https://api-ia.render.com`
- Base de données : Supabase production

## Déploiement Frontend (Vercel)

### Configuration initiale

1. **Connecter le repository**
   ```bash
   # Via Vercel CLI
   npm i -g vercel
   vercel login
   vercel --prod
   ```

2. **Variables d'environnement**
   Dans le dashboard Vercel, configurer :
   ```
   NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
   NEXT_PUBLIC_IA_API_URL=https://api-ia.render.com
   NEXT_PUBLIC_CONTACT_EMAIL=vidaluca77@gmail.com
   NEXT_PUBLIC_CONTACT_PHONE=+33123456789
   NEXT_PUBLIC_SENTRY_DSN=https://your-sentry-dsn
   SENTRY_ORG=your-sentry-org
   SENTRY_PROJECT=la-vida-luca
   ```

3. **Configuration build**
   ```json
   {
     "buildCommand": "npm run build",
     "outputDirectory": "out",
     "installCommand": "npm install"
   }
   ```

### Déploiement automatique

Le déploiement se fait automatiquement sur :
- **Main branch** → Production
- **Develop branch** → Staging  
- **Feature branches** → Preview deployments

### Rollback

```bash
# Via CLI
vercel rollback https://la-vida-luca-abcd123.vercel.app

# Via dashboard
# 1. Aller dans Deployments
# 2. Cliquer sur "Promote to Production"
```

## Déploiement API IA (Render)

### Configuration initiale

1. **Créer un service Web**
   - Repository : `https://github.com/vidaluca77-cloud/LaVidaLuca-App`
   - Root Directory : `/apps/ia`
   - Runtime : Python 3.11
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Variables d'environnement**
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_SERVICE_KEY=your-service-key
   ALLOWED_ORIGINS=https://la-vida-luca.vercel.app
   SENTRY_DSN=https://your-sentry-dsn
   ```

3. **Health check**
   - Path : `/health`
   - Expected status : 200

### Monitoring

Render fournit automatiquement :
- Métriques CPU/Mémoire
- Logs en temps réel
- Health checks
- Alertes de downtime

## Base de données (Supabase)

### Setup initial

1. **Créer le projet**
   ```bash
   # Via CLI
   npm install -g supabase
   supabase login
   supabase projects create la-vida-luca
   ```

2. **Schema et données**
   ```bash
   # Appliquer le schema
   supabase db push
   
   # Exporter le schema actuel
   supabase db dump --data-only -f seed.sql
   ```

3. **Variables RLS (Row Level Security)**
   Activer RLS sur toutes les tables sensibles

### Backup et restore

```bash
# Backup automatique quotidien (inclus dans Supabase Pro)
# Backup manuel
supabase db dump -f backup-$(date +%Y%m%d).sql

# Restore
supabase db reset --db-url "postgresql://..."
```

## Monitoring et alertes

### Health checks

```bash
# Vérifier tous les services
curl https://la-vida-luca.vercel.app/api/health
curl https://api-ia.render.com/health
curl https://your-project.supabase.co/rest/v1/
```

### Alertes configurées

1. **Vercel**
   - Build failures
   - High error rate (>5%)
   - Performance regression

2. **Render**
   - Service down
   - High response time (>2s)
   - High memory usage (>80%)

3. **Supabase**
   - Database down
   - Connection pool exhausted
   - High query time

### Dashboards

**Sentry** : Monitoring des erreurs et performance
- Real-time error tracking
- Performance monitoring
- Release health

**Vercel Analytics** : Métriques frontend
- Page views
- Performance vitals
- Geographic data

## Processus de release

### 1. Préparation

```bash
# 1. Créer une branche release
git checkout -b release/v1.2.0

# 2. Mettre à jour la version
npm version patch|minor|major

# 3. Mettre à jour CHANGELOG.md
```

### 2. Tests

```bash
# Tests automatisés
npm run test:ci

# Tests manuels
npm run test:e2e

# Tests de charge
npm run test:load
```

### 3. Déploiement staging

```bash
# Push vers staging
git push origin release/v1.2.0

# Vérifier le déploiement
curl https://la-vida-luca-staging.vercel.app/api/health
```

### 4. Déploiement production

```bash
# Merge vers main
git checkout main
git merge release/v1.2.0
git push origin main

# Tag de version
git tag v1.2.0
git push origin v1.2.0
```

### 5. Post-déploiement

- Vérifier les health checks
- Surveiller les erreurs Sentry
- Valider les métriques clés
- Communiquer la release

## Rollback d'urgence

### Frontend (Vercel)
```bash
# Rollback immédiat
vercel rollback --token $VERCEL_TOKEN

# Ou via dashboard Vercel
```

### API (Render)
```bash
# Via dashboard Render
# 1. Aller dans Deployments
# 2. Cliquer sur "Redeploy" sur version précédente

# Ou redéployer un commit spécifique
git revert HEAD
git push origin main
```

### Base de données (Supabase)
```bash
# Restaurer depuis backup
supabase db reset --db-url "backup-url"

# Ou migration inverse
supabase migration down
```

## Variables d'environnement

### Production
```bash
# Frontend (Vercel)
NEXT_PUBLIC_SUPABASE_URL=https://prod.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=prod-anon-key
NEXT_PUBLIC_IA_API_URL=https://api-ia.render.com
NEXT_PUBLIC_SENTRY_DSN=https://sentry-dsn

# API (Render)  
SUPABASE_URL=https://prod.supabase.co
SUPABASE_SERVICE_KEY=prod-service-key
ALLOWED_ORIGINS=https://la-vida-luca.vercel.app
```

### Staging
```bash
# Frontend (Vercel)
NEXT_PUBLIC_SUPABASE_URL=https://staging.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=staging-anon-key
NEXT_PUBLIC_IA_API_URL=https://api-ia-staging.render.com

# API (Render)
SUPABASE_URL=https://staging.supabase.co
SUPABASE_SERVICE_KEY=staging-service-key
ALLOWED_ORIGINS=https://la-vida-luca-staging.vercel.app
```

## Sécurité

### Secrets management
- Variables sensibles via dashboard des plateformes
- Rotation régulière des clés API
- Accès limité aux environnements de production

### HTTPS
- Forcé sur tous les environnements
- Certificats SSL automatiques via Vercel/Render

### CORS
- Origines autorisées configurées strictement
- Headers de sécurité configurés

## Performance

### Optimisations
- Images optimisées (Vercel Image Optimization)
- Code splitting automatique (Next.js)
- CDN global (Vercel Edge Network)
- Cache navigateur configuré

### Métriques cibles
- First Contentful Paint < 1.5s
- Largest Contentful Paint < 2.5s
- Time to Interactive < 3.5s
- API response time < 500ms