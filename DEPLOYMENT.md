# 🚀 Déploiement La Vida Luca

Ce guide vous explique comment déployer l'application La Vida Luca sur Vercel (frontend) et Render (backend).

## 📋 Prérequis

- Compte GitHub avec accès au repository
- Compte Vercel (gratuit)
- Compte Render (gratuit)
- Clé API OpenAI

## 🌐 Déploiement Frontend (Vercel)

### 1. Configuration automatique

Le fichier `vercel.json` est déjà configuré pour :
- ✅ Optimisation des builds Next.js
- ✅ Redirection des API vers le backend Render
- ✅ Headers de sécurité
- ✅ Configuration des variables d'environnement

### 2. Étapes de déploiement

1. **Connecter le repository à Vercel**
   ```bash
   # Aller sur vercel.com
   # Importer le projet depuis GitHub
   # Sélectionner le repository LaVidaLuca-App
   ```

2. **Configuration des variables d'environnement**
   Dans le dashboard Vercel, ajouter :
   ```
   NEXT_PUBLIC_API_URL=https://lavidaluca-backend.onrender.com
   NEXT_PUBLIC_APP_ENV=production
   ```

3. **Déploiement automatique**
   ```bash
   git push origin main
   # Vercel déploie automatiquement à chaque push
   ```

## 🔧 Déploiement Backend (Render)

### 1. Configuration automatique

Le fichier `apps/backend/render.yaml` est configuré pour :
- ✅ Service Python avec FastAPI
- ✅ Base de données PostgreSQL
- ✅ Variables d'environnement sécurisées
- ✅ Health checks automatiques

### 2. Étapes de déploiement

1. **Créer les services sur Render**
   ```bash
   # Aller sur render.com
   # Nouveau Web Service
   # Connecter le repository GitHub
   # Sélectionner apps/backend comme répertoire racine
   ```

2. **Configuration de la base de données**
   ```bash
   # Créer une nouvelle base PostgreSQL
   # Le nom doit être "lavidaluca-db" (comme dans render.yaml)
   ```

3. **Variables d'environnement**
   Configurer dans le dashboard Render :
   ```
   OPENAI_API_KEY=votre_clé_openai
   # Les autres variables sont automatiquement configurées
   ```

## 🔄 Scripts de déploiement

### Script automatisé
```bash
./deploy.sh
```

### Scripts NPM
```bash
# Development complet
npm run dev:full

# Build et test
npm run web:build
npm run backend:test

# Installation complète
npm run setup
```

## 🔗 Configuration des domaines

### 1. Frontend (Vercel)
- Domain principal : `https://lavidaluca-app.vercel.app`
- Domaine personnalisé : `https://lavidaluca.fr` (optionnel)

### 2. Backend (Render)
- URL API : `https://lavidaluca-backend.onrender.com`
- Endpoints :
  - Health check : `/health`
  - Documentation : `/docs`
  - API : `/api/v1/*`

## 🔧 Variables d'environnement

### Frontend (.env)
```bash
NEXT_PUBLIC_API_URL=https://lavidaluca-backend.onrender.com
NEXT_PUBLIC_APP_ENV=production
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### Backend (Render Dashboard)
```bash
ENVIRONMENT=production
DATABASE_URL=postgresql://... # Auto-configuré par Render
JWT_SECRET_KEY=... # Auto-généré par Render
OPENAI_API_KEY=sk-... # À configurer manuellement
CORS_ORIGINS=["https://lavidaluca-app.vercel.app"]
```

## 🔍 Monitoring

### Health Checks
- Frontend : Monitored par Vercel
- Backend : `/health` endpoint configuré

### Logs
- Frontend : Vercel Dashboard > Functions
- Backend : Render Dashboard > Logs

### Métriques
- Backend : `/metrics` endpoint (Prometheus format)

## 🚨 Dépannage

### Erreurs communes

1. **Build frontend échoue**
   ```bash
   cd apps/web && npm run lint
   # Corriger les erreurs TypeScript/ESLint
   ```

2. **Backend ne démarre pas**
   ```bash
   # Vérifier les logs Render
   # Vérifier la configuration de la base de données
   ```

3. **API non accessible**
   ```bash
   # Vérifier CORS_ORIGINS dans Render
   # Vérifier NEXT_PUBLIC_API_URL dans Vercel
   ```

## 📞 Support

Pour toute question sur le déploiement :
1. Vérifier les logs de déploiement
2. Consulter la documentation Vercel/Render
3. Vérifier la configuration des variables d'environnement

---

🎉 **Votre application La Vida Luca est maintenant prête pour le déploiement !**