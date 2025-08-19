# Guide de Déploiement - La Vida Luca

Ce guide détaille les étapes pour déployer la plateforme La Vida Luca sur Vercel (frontend) et Render (backend).

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vercel        │    │   Render        │    │   Supabase      │
│   (Frontend)    │────│   (Backend)     │────│   (Database)    │
│   Next.js       │    │   FastAPI       │    │   PostgreSQL    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prérequis

### Outils nécessaires
- Node.js 18+ et npm
- Python 3.11+
- Git
- Comptes sur : Vercel, Render, Supabase

### Variables d'environnement requises
```bash
# Frontend (Vercel)
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
NEXT_PUBLIC_IA_API_URL=https://la-vida-luca-api.onrender.com
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33 1 23 45 67 89

# Backend (Render)
DATABASE_URL=postgresql://user:password@host:port/database
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=service_role_key
ALLOWED_ORIGINS=https://la-vida-luca.vercel.app,https://la-vida-luca-web.onrender.com
ENVIRONMENT=production
API_SECRET_KEY=your-strong-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```

## 🚀 Déploiement automatisé

### Option 1 : Script de déploiement

```bash
# Cloner le repository
git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
cd LaVidaLuca-App

# Configurer les variables d'environnement
export VERCEL_TOKEN="your-vercel-token"
export RENDER_API_KEY="your-render-api-key"
export RENDER_SERVICE_ID="your-service-id"

# Exécuter le script de déploiement
chmod +x scripts/deploy.sh
./scripts/deploy.sh production
```

### Option 2 : CI/CD avec GitHub Actions

Le déploiement automatique se déclenche sur push vers `main`. Configurer les secrets GitHub :

```
VERCEL_TOKEN
VERCEL_ORG_ID  
VERCEL_PROJECT_ID
RENDER_API_KEY
RENDER_SERVICE_ID
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
NEXT_PUBLIC_IA_API_URL
WEB_URL
API_URL
DISCORD_WEBHOOK_URL (optionnel)
```

## 🔧 Déploiement manuel

### 1. Configuration Supabase

#### Créer un projet Supabase
1. Aller sur [supabase.com](https://supabase.com)
2. Créer un nouveau projet "la-vida-luca"
3. Noter l'URL et les clés API

#### Configurer la base de données
```sql
-- Créer les tables principales
CREATE TABLE activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    summary TEXT NOT NULL,
    duration_min INTEGER NOT NULL,
    skill_tags TEXT[] NOT NULL DEFAULT '{}',
    seasonality TEXT[] NOT NULL DEFAULT '{}',
    safety_level INTEGER NOT NULL CHECK (safety_level BETWEEN 1 AND 3),
    materials TEXT[] NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE registrations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    activity_id UUID REFERENCES activities(id),
    participant_name VARCHAR(255) NOT NULL,
    participant_email VARCHAR(255) NOT NULL,
    participant_phone VARCHAR(20),
    participant_type VARCHAR(20) NOT NULL,
    requested_date DATE NOT NULL,
    participants_count INTEGER NOT NULL DEFAULT 1,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    special_requirements TEXT,
    emergency_contact TEXT,
    assigned_instructor VARCHAR(255),
    location VARCHAR(255),
    notes TEXT,
    confirmed_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes pour les performances
CREATE INDEX idx_activities_category ON activities(category);
CREATE INDEX idx_activities_slug ON activities(slug);
CREATE INDEX idx_registrations_activity_id ON registrations(activity_id);
CREATE INDEX idx_registrations_email ON registrations(participant_email);
CREATE INDEX idx_registrations_status ON registrations(status);
```

### 2. Déploiement Backend (Render)

#### Méthode 1 : Via render.yaml (recommandée)
1. Connecter le repository GitHub à Render
2. Le fichier `render.yaml` configure automatiquement les services
3. Configurer les variables d'environnement dans Render

#### Méthode 2 : Manuel
1. Créer un nouveau "Web Service" sur Render
2. Connecter le repository GitHub
3. Configuration :
   - **Root Directory** : `apps/ia`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment** : Python 3.11

4. Configurer les variables d'environnement
5. Déployer

#### Tester le backend
```bash
curl https://your-api-url.onrender.com/health
```

### 3. Déploiement Frontend (Vercel)

#### Méthode 1 : Via CLI Vercel
```bash
# Installer Vercel CLI
npm i -g vercel

# Se connecter
vercel login

# Déployer
vercel --prod
```

#### Méthode 2 : Via interface Vercel
1. Aller sur [vercel.com](https://vercel.com)
2. Importer le repository GitHub
3. Configuration automatique détectée (Next.js)
4. Configurer les variables d'environnement
5. Déployer

#### Variables d'environnement Vercel
```
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
NEXT_PUBLIC_IA_API_URL=https://la-vida-luca-api.onrender.com
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33 1 23 45 67 89
```

## 🔍 Vérification et monitoring

### Tests de santé
```bash
# Test du frontend
curl https://la-vida-luca.vercel.app/

# Test du backend
curl https://la-vida-luca-api.onrender.com/health

# Test des APIs
curl https://la-vida-luca-api.onrender.com/api/v1/activities/
```

### Monitoring automatique
```bash
# Exécuter le script de monitoring
python scripts/monitor.py
```

### Logs et debugging
```bash
# Logs Render
vercel logs --app=la-vida-luca-api

# Logs Vercel  
vercel logs
```

## 🛠️ Maintenance

### Mises à jour
```bash
# Déployer une nouvelle version
git push origin main  # Déclenche CI/CD

# Ou déploiement manuel
./scripts/deploy.sh production
```

### Rollback
```bash
# Vercel
vercel --prod --alias previous-deployment-url

# Render (via interface web)
# Aller dans Deployments > Rollback
```

### Migrations de base de données
```bash
cd apps/ia
alembic upgrade head
```

## 🔐 Sécurité

### Checklist sécurité
- [ ] Variables d'environnement sécurisées (pas de clés dans le code)
- [ ] HTTPS activé sur tous les domaines
- [ ] CORS configuré correctement
- [ ] Headers de sécurité activés (via vercel.json)
- [ ] Authentification API configurée
- [ ] Logs de sécurité activés

### Sauvegarde
```bash
# Backup Supabase (automatique)
# Backup manuel via interface Supabase

# Export des données
curl -H "Authorization: Bearer $SUPABASE_SERVICE_KEY" \
     https://your-project.supabase.co/rest/v1/activities?select=*
```

## 📞 Support et dépannage

### Problèmes courants

#### 1. Erreur de build Next.js
```bash
# Vérifier Node.js version
node --version  # Doit être 18+

# Nettoyer le cache
rm -rf .next node_modules package-lock.json
npm install
npm run build
```

#### 2. Erreur de démarrage FastAPI
```bash
# Vérifier Python version
python --version  # Doit être 3.11+

# Vérifier les dépendances
pip install -r requirements.txt

# Test local
uvicorn main:app --reload
```

#### 3. Erreur de connexion base de données
```bash
# Vérifier DATABASE_URL
echo $DATABASE_URL

# Test connexion
python -c "from config import settings; print(settings.database_url)"
```

### Contacts
- **Technique** : tech@lavidaluca.fr
- **Général** : contact@lavidaluca.fr
- **Documentation** : [GitHub Issues](https://github.com/vidaluca77-cloud/LaVidaLuca-App/issues)

### Ressources utiles
- [Documentation Vercel](https://vercel.com/docs)
- [Documentation Render](https://render.com/docs)
- [Documentation Supabase](https://supabase.com/docs)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation Next.js](https://nextjs.org/docs)

---

**Dernière mise à jour** : Janvier 2024  
**Version** : 1.0.0