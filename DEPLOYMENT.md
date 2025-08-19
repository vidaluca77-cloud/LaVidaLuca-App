# Deployment Guide - La Vida Luca

Ce guide vous accompagne dans le déploiement complet de l'application La Vida Luca sur les plateformes Vercel, Render et Supabase.

## 🏗️ Architecture de déploiement

- **Frontend (Next.js)** → Vercel
- **API IA (FastAPI)** → Render  
- **Base de données** → Supabase
- **CI/CD** → GitHub Actions

## 📋 Prérequis

- Compte GitHub
- Compte Vercel
- Compte Render
- Compte Supabase
- Node.js 18+ (pour le développement local)
- Python 3.11+ (pour l'API IA)

## 🚀 Étapes de déploiement

### 1. Préparation Supabase

1. Créer un nouveau projet sur [supabase.com](https://supabase.com)
2. Noter l'URL du projet et la clé anonyme
3. Aller dans SQL Editor et exécuter le fichier `infra/supabase/migrations/20240819000001_initial_schema.sql`
4. Exécuter ensuite le fichier `infra/supabase/seeds.sql` pour les données initiales
5. Configurer l'authentification selon vos besoins

### 2. Déploiement Vercel (Frontend)

1. Connecter votre repository GitHub à Vercel
2. Configurer les variables d'environnement dans Vercel :
   ```
   NEXT_PUBLIC_SUPABASE_URL=votre_url_supabase
   NEXT_PUBLIC_SUPABASE_ANON_KEY=votre_cle_anonyme_supabase
   NEXT_PUBLIC_IA_API_URL=https://votre-api.onrender.com
   NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
   NEXT_PUBLIC_CONTACT_PHONE=+33123456789
   ```
3. Déployer depuis le dashboard Vercel ou laisser le déploiement automatique

### 3. Déploiement Render (API IA)

1. Créer un nouveau Web Service sur [render.com](https://render.com)
2. Connecter votre repository GitHub
3. Configurer le service :
   - **Build Command** : `cd apps/ia && pip install -r requirements.txt`
   - **Start Command** : `cd apps/ia && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Python Version** : 3.11
4. Configurer les variables d'environnement :
   ```
   ALLOWED_ORIGINS=https://votre-app.vercel.app
   SUPABASE_URL=votre_url_supabase
   SUPABASE_SERVICE_KEY=votre_cle_service_supabase
   ```
5. Déployer le service

### 4. Configuration GitHub Actions

1. Aller dans Settings > Secrets and variables > Actions de votre repository
2. Ajouter les secrets suivants :
   ```
   VERCEL_TOKEN=votre_token_vercel
   VERCEL_ORG_ID=votre_org_id_vercel
   VERCEL_PROJECT_ID=votre_project_id_vercel
   RENDER_SERVICE_ID=votre_service_id_render
   RENDER_API_KEY=votre_api_key_render
   SUPABASE_PROJECT_REF=votre_project_ref_supabase
   SUPABASE_ACCESS_TOKEN=votre_access_token_supabase
   VERCEL_PRODUCTION_URL=https://votre-app.vercel.app
   RENDER_SERVICE_URL=https://votre-api.onrender.com
   ```

### 5. Test du déploiement

1. Pusher vos changements sur la branche `main`
2. Vérifier que le workflow GitHub Actions s'exécute correctement
3. Tester les endpoints :
   - Frontend : `https://votre-app.vercel.app`
   - API Health : `https://votre-api.onrender.com/health`
   - Database : connexion via Supabase Dashboard

## 🔧 Configuration post-déploiement

### Monitoring

1. Exécuter le script de health check :
   ```bash
   ./scripts/monitoring/health-check.sh
   ```

2. Configurer le monitoring de performance :
   ```bash
   node scripts/monitoring/performance-monitor.js
   ```

### Variables d'environnement de production

Copier le fichier `.env.example` et configurer :

```bash
cp .env.example .env.production
# Éditer .env.production avec vos valeurs de production
```

### Sécurité

- [ ] Configurer les headers de sécurité (déjà inclus dans `vercel.json`)
- [ ] Vérifier les politiques RLS dans Supabase
- [ ] Configurer les domaines autorisés pour CORS
- [ ] Activer HTTPS (automatique sur Vercel/Render)

## 📊 Surveillance et maintenance

### Health Checks automatiques

Le pipeline CI/CD inclut des vérifications automatiques :
- Build et tests
- Sécurité (Trivy scan)
- Déploiement
- Tests de santé post-déploiement

### Logs et debugging

- **Vercel** : Dashboard > Functions > Logs
- **Render** : Dashboard > Logs
- **Supabase** : Dashboard > Logs

### Métriques

Utiliser les scripts de monitoring pour :
- Temps de réponse
- Disponibilité
- Erreurs
- Performance

## 🔄 Mise à jour

1. Développer et tester localement
2. Pusher sur une branche feature
3. Créer une Pull Request
4. Merger vers `main` après validation
5. Le déploiement se fait automatiquement via GitHub Actions

## 🆘 Dépannage

### Erreurs communes

1. **Build failed on Vercel**
   - Vérifier les variables d'environnement
   - Vérifier la compatibilité Next.js

2. **API unreachable on Render**
   - Vérifier les logs Render
   - Vérifier les dépendances Python

3. **Database connection issues**
   - Vérifier les credentials Supabase
   - Vérifier les politiques RLS

### Support

Pour toute question ou problème :
- Consulter les logs des plateformes
- Vérifier la documentation officielle
- Contacter l'équipe de développement

## 📚 Ressources

- [Documentation Vercel](https://vercel.com/docs)
- [Documentation Render](https://render.com/docs)
- [Documentation Supabase](https://supabase.com/docs)
- [Documentation GitHub Actions](https://docs.github.com/en/actions)