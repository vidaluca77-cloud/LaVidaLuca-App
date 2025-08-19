# Guide de Déploiement - La Vida Luca

Ce guide explique comment déployer l'application La Vida Luca sur les différentes plateformes.

## Architecture de Déploiement

- **Vercel** : Hébergement du site web Next.js
- **Render** : Hébergement de l'API IA (FastAPI)  
- **Supabase** : Base de données et authentification

## 1. Configuration des Variables d'Environnement

### Variables pour Vercel (site web)
Copier le fichier `.env.example` et créer `.env.local` avec les vraies valeurs :

```bash
NEXT_PUBLIC_SUPABASE_URL=https://fdqpuxpusjeasdtqqiyo.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<clé-anon-supabase>
NEXT_PUBLIC_IA_API_URL=<url-render-api>
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789
ALLOWED_ORIGINS=<url-vercel>
```

### Variables pour Render (API IA)
Configurer dans le dashboard Render :

```bash
SUPABASE_URL=https://fdqpuxpusjeasdtqqiyo.supabase.co
SUPABASE_SERVICE_KEY=<clé-service-supabase>
ALLOWED_ORIGINS=<url-vercel>
```

## 2. Déploiement sur Vercel

1. Connecter le repository GitHub à Vercel
2. Configurer les variables d'environnement dans le dashboard Vercel
3. Le fichier `vercel.json` configurera automatiquement :
   - Build command : `npm run build`
   - Output directory : `out`
   - Headers de sécurité
   - Redirections

## 3. Déploiement sur Render

1. Créer un nouveau service Web sur Render
2. Connecter le repository GitHub
3. Configurer :
   - Root Directory : `./apps/ia`
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Le fichier `render.yaml` peut aussi être utilisé pour un déploiement Infrastructure as Code

## 4. Configuration Supabase

1. Créer un projet Supabase (déjà configuré : https://fdqpuxpusjeasdtqqiyo.supabase.co)
2. Importer le schéma SQL : `/infra/supabase/schema.sql`
3. Importer les données de base : `/infra/supabase/seeds.sql`
4. Configurer l'authentification selon les besoins
5. Récupérer les clés API et les ajouter aux variables d'environnement

## 5. Test du Déploiement

### Vérifier Vercel
- Accéder à l'URL Vercel
- Tester la navigation entre les pages
- Vérifier le formulaire de contact

### Vérifier Render  
- Accéder à `/health` pour le health check
- Tester l'endpoint `/recommend-activities`

### Vérifier Supabase
- Tester la connexion depuis l'application web
- Vérifier l'authentification si configurée

## 6. Fichiers de Configuration

### `vercel.json`
- Configuration optimisée pour l'export statique Next.js
- Headers de sécurité (CSRF, XSS, etc.)
- Gestion des redirections

### `render.yaml`
- Configuration Infrastructure as Code pour Render
- Service API IA avec health checks
- Variables d'environnement et scaling automatique

### `.env.example`
- Template pour toutes les variables d'environnement requises
- Ne contient aucune valeur secrète

## 7. Sécurité

- Toutes les clés secrètes doivent être configurées via les dashboards des plateformes
- CORS configuré pour limiter l'accès aux domaines autorisés
- Headers de sécurité configurés dans Vercel
- Variables d'environnement séparées par service

## Support

Pour toute question sur le déploiement, consulter :
- [Documentation Vercel](https://vercel.com/docs)
- [Documentation Render](https://render.com/docs)
- [Documentation Supabase](https://supabase.com/docs)