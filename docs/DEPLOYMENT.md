# Guide de Déploiement - La Vida Luca

Ce guide détaille le processus complet de déploiement de l'application La Vida Luca sur Vercel (frontend) et Render (backend API).

## Architecture

- **Frontend**: Next.js 14 déployé sur Vercel
- **Backend**: FastAPI déployé sur Render
- **Base de données**: Supabase (PostgreSQL + Auth)
- **IA/ML**: Intégration OpenAI (optionnelle)

## 🚀 Déploiement Frontend (Vercel)

### 1. Prérequis
- Compte Vercel
- Repository GitHub connecté
- Variables d'environnement configurées

### 2. Configuration Vercel

#### Variables d'environnement requises :
```bash
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_IA_API_URL=https://lavidaluca-ia-api.onrender.com
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33 1 23 45 67 89
```

#### Déploiement automatique :
1. Connecter le repository à Vercel
2. Configurer les variables d'environnement dans l'interface Vercel
3. Le fichier `vercel.json` est déjà configuré
4. Déploiement automatique à chaque push sur `main`

### 3. Domaine personnalisé (optionnel)
- Configurer `la-vida-luca.fr` dans les paramètres Vercel
- Mettre à jour `metadataBase` dans `src/app/layout.tsx`

## 🖥️ Déploiement Backend (Render)

### 1. Prérequis
- Compte Render
- Repository GitHub connecté

### 2. Configuration Render

#### Création du service :
1. Aller sur Render Dashboard
2. "New +" → "Web Service"
3. Connecter le repository GitHub
4. Configurer :
   - **Name**: `lavidaluca-ia-api`
   - **Region**: Europe (Frankfurt)
   - **Branch**: `main`
   - **Root Directory**: `apps/ia`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### Variables d'environnement Render :
```bash
PORT=10000
ALLOWED_ORIGINS=https://la-vida-luca.vercel.app
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your_supabase_service_role_key
OPENAI_API_KEY=your_openai_api_key  # Optionnel
RENDER_ENVIRONMENT=production
```

### 3. Déploiement avec render.yaml (automatique)
Le fichier `render.yaml` à la racine configure automatiquement le déploiement.

## 🗄️ Configuration Base de Données (Supabase)

### 1. Création du projet Supabase
1. Aller sur [supabase.com](https://supabase.com)
2. Créer un nouveau projet
3. Noter l'URL et les clés API

### 2. Initialisation du schéma
```bash
# Dans l'éditeur SQL de Supabase, exécuter dans l'ordre :
# 1. infra/supabase/schema.sql
# 2. infra/supabase/seeds.sql
```

### 3. Configuration de l'authentification
- Activer les providers souhaités (Email, Google, etc.)
- Configurer les URL de redirection :
  - `https://la-vida-luca.vercel.app/auth/callback`
  - `http://localhost:3000/auth/callback` (développement)

## 🔧 Variables d'Environnement Complètes

### Frontend (.env.local)
```bash
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
NEXT_PUBLIC_IA_API_URL=https://lavidaluca-ia-api.onrender.com
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33 1 23 45 67 89
```

### Backend (apps/ia/.env)
```bash
PORT=8000
ALLOWED_ORIGINS=https://la-vida-luca.vercel.app,http://localhost:3000
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=service_role_key_here
OPENAI_API_KEY=sk-...  # Optionnel
RENDER_ENVIRONMENT=production
```

## 🧪 Tests de Déploiement

### 1. Vérification Frontend
```bash
# Développement local
npm run dev
# Build de production
npm run build
```

### 2. Vérification Backend
```bash
cd apps/ia
# Installation des dépendances
pip install -r requirements.txt
# Test local
uvicorn main:app --reload
# Test de l'API
curl http://localhost:8000/health
```

### 3. Test de bout en bout
1. Accéder à `https://la-vida-luca.vercel.app`
2. Vérifier le chargement des pages
3. Tester l'API via `https://lavidaluca-ia-api.onrender.com/docs`

## 📋 Checklist de Déploiement

### Avant le déploiement
- [ ] Tests locaux passent (frontend + backend)
- [ ] Variables d'environnement configurées
- [ ] Base de données Supabase créée et configurée
- [ ] Comptes Vercel et Render créés

### Frontend (Vercel)
- [ ] Repository connecté à Vercel
- [ ] Variables d'environnement configurées
- [ ] Build réussi
- [ ] Domaine configuré (optionnel)

### Backend (Render)
- [ ] Service Render créé
- [ ] Variables d'environnement configurées
- [ ] Health check fonctionnel (`/health`)
- [ ] Documentation API accessible (`/docs`)

### Base de données (Supabase)
- [ ] Projet créé
- [ ] Schéma importé (`schema.sql`)
- [ ] Données d'exemple importées (`seeds.sql`)
- [ ] Authentification configurée
- [ ] RLS (Row Level Security) activé

### Post-déploiement
- [ ] Test de toutes les fonctionnalités
- [ ] Vérification des logs (Vercel + Render)
- [ ] Test des connexions inter-services
- [ ] Documentation mise à jour

## 🔍 Surveillance et Maintenance

### Logs et Monitoring
- **Vercel**: Dashboard → Functions → View Function Logs
- **Render**: Dashboard → Service → Logs
- **Supabase**: Dashboard → Logs

### Métriques importantes
- Temps de réponse API
- Taux d'erreur
- Utilisation de la base de données
- Performance frontend (Core Web Vitals)

## 🆘 Dépannage Courant

### Frontend ne se charge pas
1. Vérifier les variables d'environnement Vercel
2. Contrôler les logs de build
3. Vérifier la configuration du domaine

### API inaccessible
1. Vérifier l'URL dans `NEXT_PUBLIC_IA_API_URL`
2. Contrôler les logs Render
3. Tester le health check : `/health`

### Erreurs base de données
1. Vérifier les variables Supabase
2. Contrôler les politiques RLS
3. Vérifier les permissions

### CORS Errors
1. Mettre à jour `ALLOWED_ORIGINS` dans le backend
2. Vérifier l'URL frontend dans la configuration

## 📞 Support

Pour toute question concernant le déploiement :
- Consulter la documentation officielle des plateformes
- Vérifier les logs d'erreur
- Contacter l'équipe technique du projet

---

**Note**: Ce guide suppose l'utilisation des plans gratuits de Vercel et Render. Pour une utilisation en production avec plus de trafic, considérer les plans payants.