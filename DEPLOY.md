# Guide de déploiement La Vida Luca

Ce guide détaille les étapes pour déployer l'application complète La Vida Luca sur les plateformes Vercel, Render et Supabase.

## 📋 Prérequis

- Compte Vercel existant
- Compte Render existant  
- Créer un compte Supabase (gratuit)
- Repository GitHub accessible

## 🚀 Étape 1 : Configuration Supabase

### 1.1 Créer le projet

1. Aller sur [https://supabase.com](https://supabase.com)
2. Se connecter et créer un nouveau projet :
   - **Nom** : La Vida Luca
   - **Base de données** : lavidaluca
   - **Région** : Europe (West) - eu-west-1
   - **Mot de passe** : Générer un mot de passe fort

### 1.2 Récupérer les clés

Après création, aller dans **Settings** > **API** :
- **URL** : `https://[votre-id].supabase.co`
- **anon public** : `eyJ...` (à utiliser côté client)
- **service_role** : `eyJ...` (à utiliser côté serveur)

### 1.3 Importer le schéma

1. Aller dans **SQL Editor**
2. Exécuter le fichier `supabase/migrations/001_initial_schema.sql`
3. Exécuter le fichier `supabase/migrations/002_seed_data.sql`

### 1.4 Configurer l'authentification

Dans **Authentication** > **Settings** :
- **Site URL** : `https://la-vida-luca.vercel.app`
- **Redirect URLs** : Ajouter `https://la-vida-luca.vercel.app/auth/callback`

## 🌐 Étape 2 : Déploiement Vercel (Frontend)

### 2.1 Connecter le repository

1. Aller sur [https://vercel.com](https://vercel.com)
2. Importer le repository `vidaluca77-cloud/LaVidaLuca-App`
3. Choisir le framework "Next.js"

### 2.2 Configurer les variables d'environnement

Dans les **Settings** du projet Vercel, ajouter :

```
NEXT_PUBLIC_SUPABASE_URL=https://[votre-id].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=[clé-publique-supabase]
NEXT_PUBLIC_IA_API_URL=https://lavidaluca-ia-api.onrender.com
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789
```

### 2.3 Déployer

Le déploiement se fait automatiquement. Le site sera accessible via :
`https://la-vida-luca.vercel.app`

## 🖥️ Étape 3 : Déploiement Render (API IA)

### 3.1 Créer le service web

1. Aller sur [https://render.com](https://render.com)
2. Créer un nouveau **Web Service**
3. Connecter le repository `vidaluca77-cloud/LaVidaLuca-App`
4. Configuration :
   - **Name** : lavidaluca-ia-api
   - **Root Directory** : `apps/ia`
   - **Environment** : Python 3
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan** : Starter (gratuit)

### 3.2 Configurer les variables d'environnement

Dans les **Environment Variables** du service Render :

```
SUPABASE_URL=https://[votre-id].supabase.co
SUPABASE_ANON_KEY=[clé-publique-supabase]
SUPABASE_SERVICE_KEY=[clé-service-supabase]
ALLOWED_ORIGINS=https://la-vida-luca.vercel.app,http://localhost:3000
ENVIRONMENT=production
OPENAI_API_KEY=[votre-clé-openai]
```

### 3.3 Déployer

Le déploiement se fait automatiquement. L'API sera accessible via :
`https://lavidaluca-ia-api.onrender.com`

## ✅ Étape 4 : Tests et validation

### 4.1 Tester la connexion Supabase

```bash
curl -H "Authorization: Bearer [anon-key]" \
     -H "apikey: [anon-key]" \
     https://[votre-id].supabase.co/rest/v1/activities
```

### 4.2 Tester l'API IA

```bash
curl https://lavidaluca-ia-api.onrender.com/health
```

### 4.3 Tester l'application complète

1. Aller sur `https://la-vida-luca.vercel.app`
2. Vérifier que la page d'accueil se charge
3. Tester le formulaire de contact
4. Vérifier le catalogue d'activités

## 🔧 Configuration avancée

### Variables d'environnement complètes

Copier `.env.example` et remplir toutes les valeurs :

**Pour Vercel (Frontend)** :
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `NEXT_PUBLIC_IA_API_URL`
- `NEXT_PUBLIC_CONTACT_EMAIL`
- `NEXT_PUBLIC_CONTACT_PHONE`

**Pour Render (API IA)** :
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_KEY`
- `ALLOWED_ORIGINS`
- `OPENAI_API_KEY`
- `ENVIRONMENT`

### Domaine personnalisé (optionnel)

1. **Vercel** : Ajouter le domaine dans Settings > Domains
2. **Supabase** : Mettre à jour les Redirect URLs
3. **Render** : Mettre à jour ALLOWED_ORIGINS

## 🐛 Dépannage

### Erreurs communes

**Build Vercel échoue** :
- Vérifier que toutes les variables d'environnement sont définies
- Contrôler les erreurs TypeScript dans les logs

**API Render ne démarre pas** :
- Vérifier les requirements.txt
- Contrôler les logs de démarrage
- Valider la commande uvicorn

**Connexion Supabase échoue** :
- Vérifier les URLs et clés
- Contrôler les politiques RLS
- Valider les CORS dans Supabase

### Support

Pour toute question sur le déploiement :
1. Vérifier les logs des services
2. Consulter la documentation des plateformes
3. Tester en local d'abord

## 📈 Monitoring

Une fois déployé, surveiller :
- **Vercel** : Analytics et Core Web Vitals
- **Render** : Logs et métriques de performance
- **Supabase** : Usage de la base de données

Les trois services offrent des tableaux de bord pour le monitoring en temps réel.