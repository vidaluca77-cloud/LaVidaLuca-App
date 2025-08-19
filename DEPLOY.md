# 🚀 Guide de Déploiement - La Vida Luca

Ce guide détaille le processus complet de déploiement de la plateforme La Vida Luca.

## 📋 Vue d'ensemble

L'architecture de déploiement comprend :
- **Frontend** : Next.js déployé sur Vercel
- **API IA** : FastAPI déployé sur Render (prévu)
- **Base de données** : Supabase
- **Monitoring** : Scripts inclus pour surveillance

## 🛠️ Prérequis

### Outils nécessaires
- Node.js 18+ et npm
- Git
- Compte GitHub
- Compte Vercel
- Compte Render (pour l'API IA)
- Compte Supabase

### Variables d'environnement
Créer un fichier `.env.local` avec :

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# API IA (à configurer quand disponible)
NEXT_PUBLIC_IA_API_URL=https://your-api.render.com

# Contact
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789

# Sécurité
ALLOWED_ORIGINS=https://your-site.vercel.app
```

## 🏗️ Étapes de déploiement

### 1. Préparation locale

```bash
# Cloner le repository
git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
cd LaVidaLuca-App

# Installer les dépendances
npm install

# Tester le build local
npm run build

# Lancer en mode développement
npm run dev
```

### 2. Configuration Supabase

1. **Créer un projet Supabase**
   - Aller sur [supabase.com](https://supabase.com)
   - Créer un nouveau projet
   - Noter l'URL et la clé anonyme

2. **Configuration de la base de données**
   ```sql
   -- Créer les tables principales
   CREATE TABLE users (
     id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
     email VARCHAR(255) UNIQUE NOT NULL,
     name VARCHAR(255),
     role VARCHAR(50) DEFAULT 'user',
     created_at TIMESTAMP DEFAULT NOW()
   );

   CREATE TABLE activities (
     id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
     title VARCHAR(255) NOT NULL,
     description TEXT,
     category VARCHAR(100),
     duration_min INTEGER,
     safety_level INTEGER DEFAULT 1,
     created_at TIMESTAMP DEFAULT NOW()
   );

   CREATE TABLE user_activities (
     id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
     user_id UUID REFERENCES users(id),
     activity_id UUID REFERENCES activities(id),
     completed_at TIMESTAMP,
     rating INTEGER CHECK (rating >= 1 AND rating <= 5)
   );
   ```

3. **Configurer l'authentification**
   - Activer l'authentification email/password
   - Configurer les URLs de redirection

### 3. Déploiement sur Vercel

1. **Via l'interface Vercel**
   - Connecter votre repository GitHub
   - Importer le projet
   - Configurer les variables d'environnement
   - Déployer

2. **Via CLI Vercel**
   ```bash
   # Installer Vercel CLI
   npm i -g vercel

   # Se connecter
   vercel login

   # Déployer
   vercel --prod
   ```

3. **Configuration Vercel**
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Output Directory: `out` (pour export statique)
   - Install Command: `npm install`

### 4. API IA sur Render (Prévu)

Quand l'API IA sera développée :

1. **Préparer le repository API**
   ```python
   # requirements.txt
   fastapi
   uvicorn
   python-multipart
   ```

2. **Déployer sur Render**
   - Connecter le repository
   - Choisir "Web Service"
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 5. Configuration DNS et domaine

1. **Domaine personnalisé**
   - Configurer dans Vercel
   - Ajouter les enregistrements DNS

2. **SSL/TLS**
   - Automatiquement géré par Vercel
   - Vérifier le certificat

## 🔧 Configuration avancée

### Optimisation des performances

1. **Images**
   ```javascript
   // next.config.js
   const nextConfig = {
     images: {
       domains: ['your-domain.com'],
       formats: ['image/webp', 'image/avif'],
     }
   }
   ```

2. **Cache**
   ```javascript
   // Headers de cache
   headers: [
     {
       source: '/api/:path*',
       headers: [
         { key: 'Cache-Control', value: 's-maxage=3600' }
       ]
     }
   ]
   ```

### Variables d'environnement par environnement

**Production (Vercel)**
```bash
NEXT_PUBLIC_SUPABASE_URL=https://prod-project.supabase.co
NEXT_PUBLIC_IA_API_URL=https://prod-api.render.com
ALLOWED_ORIGINS=https://lavidaluca.vercel.app
```

**Staging**
```bash
NEXT_PUBLIC_SUPABASE_URL=https://staging-project.supabase.co
NEXT_PUBLIC_IA_API_URL=https://staging-api.render.com
ALLOWED_ORIGINS=https://staging-lavidaluca.vercel.app
```

## 🔍 Vérification du déploiement

### Tests post-déploiement

1. **Fonctionnalités de base**
   ```bash
   # Tester les pages principales
   curl -I https://your-site.vercel.app/
   curl -I https://your-site.vercel.app/contact
   curl -I https://your-site.vercel.app/catalogue
   ```

2. **API endpoints**
   ```bash
   # Tester l'API contact
   curl -X POST https://your-site.vercel.app/api/contact \
     -H "Content-Type: application/json" \
     -d '{"name":"Test","email":"test@example.com","message":"Test"}'
   ```

3. **Performance**
   - Lighthouse score > 90
   - Temps de chargement < 3s
   - Core Web Vitals dans le vert

### Checklist de validation

- [ ] Site accessible via HTTPS
- [ ] Toutes les pages se chargent correctement
- [ ] Formulaire de contact fonctionne
- [ ] Navigation responsive
- [ ] SEO meta tags présents
- [ ] Images optimisées
- [ ] Performance satisfaisante

## 🚨 Dépannage

### Problèmes courants

1. **Erreur de build Next.js**
   ```bash
   # Nettoyer le cache
   rm -rf .next
   npm run build
   ```

2. **Variables d'environnement non détectées**
   - Vérifier la syntaxe `.env.local`
   - Redémarrer le serveur de développement
   - Vérifier la configuration Vercel

3. **Erreur Supabase connection**
   - Vérifier l'URL et la clé
   - Contrôler les politiques RLS
   - Tester la connectivité

4. **Performance lente**
   - Optimiser les images
   - Réduire la taille du bundle
   - Implémenter le cache

### Logs et monitoring

```bash
# Logs Vercel
vercel logs [deployment-id]

# Monitoring Supabase
# Via le dashboard Supabase > Logs
```

## 📈 Mise à jour et maintenance

### Déploiement continu

1. **Git workflow**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/nouvelle-fonctionnalite
   # Développement...
   git commit -m "feat: nouvelle fonctionnalité"
   git push origin feature/nouvelle-fonctionnalite
   # Créer une Pull Request
   ```

2. **Auto-déploiement**
   - Push sur `main` = déploiement automatique
   - Preview deployments pour les branches

### Backup et sécurité

1. **Backup Supabase**
   - Backup automatique quotidien
   - Export manuel si nécessaire

2. **Sécurité**
   - Rotation des clés API
   - Audit des accès
   - Monitoring des erreurs

## 📞 Support

En cas de problème :
1. Consulter les logs Vercel/Supabase
2. Vérifier la documentation officielle
3. Contacter l'équipe technique

---

**Dernière mise à jour** : $(date +'%d/%m/%Y')
**Version** : 1.0.0