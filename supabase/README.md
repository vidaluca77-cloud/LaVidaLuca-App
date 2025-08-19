# Configuration Supabase pour La Vida Luca

Ce dossier contient la configuration et les migrations pour la base de données Supabase.

## Étapes de configuration

### 1. Créer un projet Supabase

1. Aller sur [https://supabase.com](https://supabase.com)
2. Se connecter avec le compte existant
3. Créer un nouveau projet :
   - **Nom** : La Vida Luca
   - **Base de données** : lavidaluca
   - **Région** : Europe (eu-west-1) - recommandée pour la France
   - **Mot de passe** : Générer un mot de passe fort

### 2. Récupérer les variables d'environnement

Après création du projet, aller dans **Settings** > **API** :

- **URL** : `https://votre-projet-id.supabase.co`
- **anon public** : `eyJ...` (clé publique)
- **service_role** : `eyJ...` (clé privée pour l'API)

### 3. Configurer l'authentification

Dans **Authentication** > **Settings** :

- **Site URL** : `https://la-vida-luca.vercel.app`
- **Redirect URLs** : 
  - `https://la-vida-luca.vercel.app/auth/callback`
  - `http://localhost:3000/auth/callback` (pour dev)

### 4. Importer le schéma

1. Aller dans **SQL Editor**
2. Exécuter le fichier `schema.sql`
3. Exécuter le fichier `seeds.sql` (données de test)

### 5. Configurer RLS (Row Level Security)

Les politiques de sécurité sont définies dans `schema.sql` pour :
- Accès public en lecture aux activités
- Accès authentifié pour les profils utilisateurs
- Accès restreint pour les données sensibles

## Structure de la base de données

- **activities** : Catalogue des 30 activités MFR
- **user_profiles** : Profils des utilisateurs
- **user_suggestions** : Suggestions personnalisées
- **contact_requests** : Demandes de contact
- **locations** : Lieux d'action de La Vida Luca

## Tests de connexion

Après configuration, tester :

```bash
# Test de connexion depuis l'app Next.js
curl -H "Authorization: Bearer anon-key" \
     -H "apikey: anon-key" \
     https://votre-projet.supabase.co/rest/v1/activities

# Test depuis l'API IA
curl -H "Authorization: Bearer service-key" \
     -H "apikey: service-key" \
     https://votre-projet.supabase.co/rest/v1/user_profiles
```