# Guide de Déploiement - La Vida Luca

Ce guide détaille le processus de déploiement de la plateforme La Vida Luca avec toutes ses composantes.

## 🏗️ Architecture

- **Frontend** : Next.js déployé sur Vercel
- **API IA** : FastAPI déployé sur Render
- **Base de données** : Supabase (PostgreSQL + Auth)
- **CI/CD** : GitHub Actions

## 🚀 Déploiement Automatique

### 1. Configuration des Secrets GitHub

Dans les paramètres du repository GitHub, configurez les secrets suivants :

#### Vercel
```
VERCEL_TOKEN=<votre-token-vercel>
VERCEL_ORG_ID=<votre-org-id>
VERCEL_PROJECT_ID=<votre-project-id>
```

#### Render
```
RENDER_API_KEY=<votre-api-key-render>
RENDER_SERVICE_ID=<votre-service-id>
```

#### Supabase
```
NEXT_PUBLIC_SUPABASE_URL=https://votre-projet.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<votre-anon-key>
SUPABASE_SERVICE_KEY=<votre-service-key>
```

#### Contact
```
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=02.31.00.00.00
```

#### IA
```
NEXT_PUBLIC_IA_API_URL=https://votre-api.onrender.com
OPENAI_API_KEY=<votre-openai-key>
```

### 2. Déploiement par Branches

- **`main`** → Production automatique
- **`develop`** → Staging automatique  
- **Pull Requests** → Preview automatique

## 🔧 Configuration Manuelle

### 1. Supabase

1. Créer un nouveau projet sur [supabase.com](https://supabase.com)
2. Exécuter les scripts SQL dans l'ordre :
   ```bash
   # Dans l'éditeur SQL de Supabase
   1. infra/supabase/schema.sql
   2. infra/supabase/policies.sql
   3. infra/supabase/seeds.sql (optionnel, pour les données de test)
   ```
3. Configurer l'authentification :
   - Activer l'inscription par email
   - Configurer les redirections
   - Définir les rôles utilisateurs

### 2. Vercel

1. Connecter le repository GitHub
2. Configurer les variables d'environnement
3. Le déploiement se fait automatiquement

### 3. Render

1. Créer un nouveau Web Service
2. Connecter le repository GitHub
3. Configurer le build :
   - **Build Command** : `cd apps/ia && pip install -r requirements.txt`
   - **Start Command** : `cd apps/ia && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Configurer les variables d'environnement

## 🧪 Tests et Qualité

### Tests Automatiques

Les tests s'exécutent automatiquement sur chaque push/PR :

- **Linting** : ESLint pour Next.js, Flake8 pour Python
- **Tests unitaires** : Jest pour le frontend, Pytest pour l'API
- **Build** : Vérification que l'application se construit correctement

### Tests Manuels

```bash
# Frontend
npm run lint
npm run build

# API IA
cd apps/ia
pip install -r requirements.txt
pytest
black --check .
flake8 .
```

## 🔒 Sécurité

### Variables d'Environnement

- Utilisez des secrets GitHub pour les valeurs sensibles
- Ne commitez jamais de vraies clés API
- Utilisez des environnements séparés (dev/staging/prod)

### Base de Données

- Row Level Security (RLS) activé sur toutes les tables
- Politiques d'accès granulaires
- Authentification obligatoire pour les données sensibles

### API

- CORS configuré pour les domaines autorisés
- Rate limiting (à implémenter)
- Validation des entrées avec Pydantic

## 📊 Monitoring

### Logs

- **Vercel** : Logs automatiques disponibles dans le dashboard
- **Render** : Logs en temps réel dans l'interface
- **Supabase** : Logs des requêtes et erreurs

### Métriques

- **Performances** : Core Web Vitals via Vercel Analytics
- **Erreurs** : Monitoring automatique des 500 errors
- **Usage** : Statistiques d'utilisation des API

## 🔄 Workflows CI/CD

### Main Workflow (`.github/workflows/ci-cd.yml`)

1. **Tests** : Lint + Build + Tests unitaires
2. **Security** : Scan de vulnérabilités avec Trivy
3. **Deploy** : 
   - Staging sur branche `develop`
   - Production sur branche `main`

### Preview Workflow (`.github/workflows/preview.yml`)

- Déploiement automatique des PR
- Commentaire avec l'URL de preview
- Mise à jour automatique à chaque push

## 🚨 Dépannage

### Erreurs Courantes

1. **Build Failed** : Vérifier les variables d'environnement
2. **API 500** : Vérifier les logs Render et la config Supabase
3. **CORS Errors** : Vérifier la config ALLOWED_ORIGINS

### Rollback

- **Vercel** : Rollback via l'interface ou CLI
- **Render** : Redéploiement de la version précédente
- **Supabase** : Migrations SQL pour les changements de schéma

## 📞 Support

Pour toute question technique :
- Issues GitHub pour les bugs
- Discussions GitHub pour les questions
- Email : tech@lavidaluca.fr