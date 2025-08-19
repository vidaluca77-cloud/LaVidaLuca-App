# 🌐 Guides de Déploiement - La Vida Luca

Ce document fournit des guides détaillés pour déployer La Vida Luca sur différentes plateformes.

## 📋 Vue d'ensemble des déploiements

| Composant | Plateforme | Status | Guide |
|-----------|------------|--------|-------|
| Frontend Next.js | Vercel | ✅ Prêt | [Guide Vercel](#vercel) |
| API IA FastAPI | Render | 🔄 Planifié | [Guide Render](#render) |
| Base de données | Supabase | 🔄 Planifié | [Guide Supabase](#supabase) |
| Monitoring | Custom Scripts | ✅ Prêt | [Guide Monitoring](#monitoring) |

---

## 🚀 Guide Vercel (Frontend)

### Prérequis
- Compte Vercel
- Repository GitHub
- Node.js 18+

### Déploiement automatique

1. **Connexion GitHub**
   ```bash
   # Aller sur vercel.com
   # Cliquer "New Project"
   # Importer depuis GitHub: vidaluca77-cloud/LaVidaLuca-App
   ```

2. **Configuration automatique**
   - Framework Preset: **Next.js** (détecté automatiquement)
   - Build Command: `npm run build`
   - Output Directory: `out` (pour static export)
   - Install Command: `npm install`

3. **Variables d'environnement**
   ```bash
   # Dans Vercel Dashboard > Settings > Environment Variables
   NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
   NEXT_PUBLIC_CONTACT_PHONE=+33123456789
   NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
   NEXT_PUBLIC_IA_API_URL=https://your-api.render.com
   ```

### Déploiement via CLI

```bash
# Installer Vercel CLI
npm i -g vercel

# Se connecter
vercel login

# Configuration initiale (première fois)
vercel

# Déploiement en production
vercel --prod
```

### Configuration avancée

**vercel.json**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "out",
  "framework": "nextjs",
  "redirects": [
    {
      "source": "/admin",
      "destination": "/login",
      "permanent": false
    }
  ],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "s-maxage=3600"
        }
      ]
    }
  ]
}
```

### Domaine personnalisé

```bash
# Via CLI
vercel domains add lavidaluca.fr

# Configuration DNS requise:
# A record: @ -> 76.76.19.61
# CNAME record: www -> cname.vercel-dns.com
```

### Monitoring Vercel

- **Analytics** : Activé par défaut
- **Logs** : `vercel logs <deployment-url>`
- **Performance** : Dashboard Vercel > Analytics

---

## ⚙️ Guide Render (API IA)

### Prérequis
- Compte Render
- Repository avec API FastAPI
- Python 3.9+

### Structure du projet API

```
apps/ia/
├── main.py              # Point d'entrée FastAPI
├── requirements.txt     # Dépendances Python
├── Dockerfile          # Image Docker (optionnel)
├── .env.example        # Exemple de variables
├── models/             # Modèles ML
├── routers/            # Routes API
└── services/           # Services métier
```

### Configuration Render

1. **Créer un Web Service**
   ```bash
   # Sur render.com
   # New > Web Service
   # Connect Repository: LaVidaLuca-App/apps/ia
   ```

2. **Configuration Build**
   ```bash
   # Build Command
   pip install -r requirements.txt

   # Start Command
   uvicorn main:app --host 0.0.0.0 --port $PORT

   # Environment
   Python 3.9
   ```

3. **Variables d'environnement**
   ```bash
   DATABASE_URL=postgresql://user:pass@host:port/db
   JWT_SECRET=your-jwt-secret
   OPENAI_API_KEY=your-openai-key
   REDIS_URL=redis://user:pass@host:port
   ```

### Exemple main.py

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="La Vida Luca IA API",
    description="API d'intelligence artificielle pour recommandations",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://la-vida-luca.vercel.app",
        "https://lavidaluca.fr"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "La Vida Luca IA API", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/api/v1/recommendations")
async def get_recommendations(user_profile: dict):
    # Logique de recommandation IA
    return {"recommendations": [], "metadata": {}}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### requirements.txt

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.1
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
openai==1.6.1
numpy==1.25.2
pandas==2.1.4
scikit-learn==1.3.2
```

### Auto-déploiement

```yaml
# .github/workflows/deploy-api.yml
name: Deploy API to Render

on:
  push:
    branches: [main]
    paths: ['apps/ia/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Render
        uses: render-deploy-action@v1
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}
```

---

## 🗄️ Guide Supabase (Base de données)

### Configuration initiale

1. **Créer un projet**
   ```bash
   # Sur supabase.com
   # New Project
   # Nom: la-vida-luca
   # Région: West Europe (eu-west-1)
   ```

2. **Configuration de sécurité**
   ```sql
   -- Activer Row Level Security
   ALTER TABLE users ENABLE ROW LEVEL SECURITY;
   ALTER TABLE activities ENABLE ROW LEVEL SECURITY;
   ```

### Schéma de base de données

```sql
-- Utilisateurs
CREATE TABLE users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'student' CHECK (role IN ('student', 'teacher', 'admin')),
  profile JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Activités
CREATE TABLE activities (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  slug VARCHAR(255) UNIQUE NOT NULL,
  title VARCHAR(255) NOT NULL,
  category VARCHAR(100) NOT NULL CHECK (category IN ('agri', 'transfo', 'artisanat', 'nature', 'social')),
  summary TEXT,
  description TEXT,
  duration_min INTEGER NOT NULL,
  safety_level INTEGER DEFAULT 1 CHECK (safety_level IN (1, 2, 3)),
  skill_tags TEXT[] DEFAULT '{}',
  seasonality TEXT[] DEFAULT '{}',
  materials TEXT[] DEFAULT '{}',
  prerequisites TEXT[] DEFAULT '{}',
  learning_objectives TEXT[] DEFAULT '{}',
  content JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Participation aux activités
CREATE TABLE user_activities (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  activity_id UUID REFERENCES activities(id) ON DELETE CASCADE,
  status VARCHAR(50) DEFAULT 'registered' CHECK (status IN ('registered', 'in_progress', 'completed', 'cancelled')),
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  rating INTEGER CHECK (rating >= 1 AND rating <= 5),
  feedback TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, activity_id)
);

-- Messages de contact
CREATE TABLE contact_messages (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  status VARCHAR(50) DEFAULT 'new' CHECK (status IN ('new', 'read', 'replied', 'archived')),
  replied_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Index pour les performances
CREATE INDEX idx_activities_category ON activities(category);
CREATE INDEX idx_activities_safety_level ON activities(safety_level);
CREATE INDEX idx_user_activities_user_id ON user_activities(user_id);
CREATE INDEX idx_user_activities_status ON user_activities(status);
CREATE INDEX idx_contact_messages_status ON contact_messages(status);
CREATE INDEX idx_contact_messages_created_at ON contact_messages(created_at DESC);
```

### Politiques de sécurité (RLS)

```sql
-- Utilisateurs peuvent lire leur propre profil
CREATE POLICY "Users can read own profile" ON users
  FOR SELECT USING (auth.uid() = id);

-- Utilisateurs peuvent mettre à jour leur propre profil
CREATE POLICY "Users can update own profile" ON users
  FOR UPDATE USING (auth.uid() = id);

-- Tout le monde peut lire les activités
CREATE POLICY "Activities are publicly readable" ON activities
  FOR SELECT USING (true);

-- Utilisateurs connectés peuvent voir leurs propres participations
CREATE POLICY "Users can read own activities" ON user_activities
  FOR SELECT USING (auth.uid() = user_id);

-- Utilisateurs connectés peuvent s'inscrire aux activités
CREATE POLICY "Users can register for activities" ON user_activities
  FOR INSERT WITH CHECK (auth.uid() = user_id);
```

### Seeds de données

```sql
-- Insérer les 30 activités
INSERT INTO activities (slug, title, category, summary, duration_min, safety_level, skill_tags, seasonality, materials) VALUES
('soins-animaux', 'Soins aux animaux de ferme', 'agri', 'Alimentation, observation, soins de base.', 60, 1, ARRAY['patience', 'observation'], ARRAY['toutes'], ARRAY['bottes', 'gants']),
('tonte-troupeau', 'Tonte & entretien du troupeau', 'agri', 'Hygiène, tonte (démo), soins courants.', 90, 2, ARRAY['elevage', 'hygiene'], ARRAY['printemps'], ARRAY['bottes', 'gants']),
('basse-cour', 'Soins basse-cour', 'agri', 'Poules/canards/lapins : alimentation, abris, propreté.', 60, 1, ARRAY['soins_animaux'], ARRAY['toutes'], ARRAY['bottes', 'gants']),
-- ... autres activités
;
```

### Configuration client

```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Types générés automatiquement
export type Database = {
  public: {
    Tables: {
      users: {
        Row: {
          id: string
          email: string
          name: string
          role: string
          created_at: string
        }
        Insert: {
          email: string
          name: string
          role?: string
        }
        Update: {
          name?: string
          role?: string
        }
      }
      // ... autres tables
    }
  }
}
```

---

## 📊 Guide Monitoring

### Scripts de monitoring

```bash
# Monitoring de base
./scripts/monitoring/health-check.sh

# Monitoring de performance
SITE_URL=https://la-vida-luca.vercel.app \
RUN_LIGHTHOUSE=true \
./scripts/monitoring/performance-check.sh

# Monitoring avec alertes
SLACK_WEBHOOK=https://hooks.slack.com/... \
./scripts/monitoring/health-check.sh
```

### Configuration des alertes

**Slack/Discord**
```bash
# Variables d'environnement
export SLACK_WEBHOOK="https://hooks.slack.com/services/..."
export DISCORD_WEBHOOK="https://discord.com/api/webhooks/..."

# Test d'alerte
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"🚨 Test alerte La Vida Luca"}' \
  $SLACK_WEBHOOK
```

**Cron jobs pour monitoring automatique**
```bash
# Ajouter au crontab
crontab -e

# Monitoring toutes les 5 minutes
*/5 * * * * /path/to/scripts/monitoring/health-check.sh >/dev/null 2>&1

# Rapport de performance quotidien
0 6 * * * /path/to/scripts/monitoring/performance-check.sh
```

### Dashboard de monitoring

```html
<!-- Exemple de dashboard simple -->
<!DOCTYPE html>
<html>
<head>
    <title>Monitoring La Vida Luca</title>
    <meta http-equiv="refresh" content="60">
</head>
<body>
    <h1>🌱 Status La Vida Luca</h1>
    <div id="status">
        <div class="metric">
            <h3>Site Principal</h3>
            <span class="status-ok">✅ Opérationnel</span>
        </div>
        <div class="metric">
            <h3>API IA</h3>
            <span class="status-pending">🔄 En développement</span>
        </div>
        <div class="metric">
            <h3>Base de données</h3>
            <span class="status-pending">🔄 Configuration</span>
        </div>
    </div>
</body>
</html>
```

---

## 🔧 Déploiement multi-environnements

### Environnements

| Environnement | Frontend | API | DB | Usage |
|---------------|----------|-----|----|-------|
| **Development** | localhost:3000 | localhost:8000 | local | Développement |
| **Staging** | staging-*.vercel.app | staging-*.render.com | staging DB | Tests |
| **Production** | lavidaluca.fr | api.lavidaluca.fr | prod DB | Live |

### Configuration par environnement

**Development (.env.local)**
```bash
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=local-anon-key
NEXT_PUBLIC_IA_API_URL=http://localhost:8000
```

**Staging (Vercel)**
```bash
NEXT_PUBLIC_SUPABASE_URL=https://staging-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=staging-anon-key
NEXT_PUBLIC_IA_API_URL=https://staging-api.render.com
```

**Production (Vercel)**
```bash
NEXT_PUBLIC_SUPABASE_URL=https://prod-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=prod-anon-key
NEXT_PUBLIC_IA_API_URL=https://api.lavidaluca.fr
```

---

## 🚨 Troubleshooting

### Problèmes courants Vercel

**Build fails**
```bash
# Nettoyer le cache
rm -rf .next node_modules
npm install
npm run build
```

**Environment variables not working**
```bash
# Vérifier dans Vercel Dashboard
# Redéployer après modification des env vars
vercel --prod
```

### Problèmes courants Render

**Service won't start**
```bash
# Vérifier les logs
curl https://api.render.com/v1/services/srv-xxx/logs

# Vérifier le health check
curl https://your-service.render.com/health
```

**Database connection issues**
```bash
# Tester la connexion
psql $DATABASE_URL -c "SELECT 1"
```

### Problèmes courants Supabase

**RLS blocking queries**
```sql
-- Désactiver temporairement pour debug
ALTER TABLE table_name DISABLE ROW LEVEL SECURITY;

-- Vérifier les politiques
SELECT * FROM pg_policies WHERE tablename = 'table_name';
```

---

## 📈 Optimisations de performance

### Frontend (Vercel)
- Images optimisées avec Next.js Image
- Bundle splitting automatique
- Edge caching avec Vercel Edge Network
- Compression gzip/brotli

### API (Render)
- Connection pooling PostgreSQL
- Cache Redis pour requêtes fréquentes
- Pagination des résultats
- Rate limiting

### Base de données (Supabase)
- Index sur colonnes fréquemment requêtées
- Requêtes optimisées avec EXPLAIN ANALYZE
- Connection pooling
- Read replicas si nécessaire

---

## 🔐 Sécurité

### Frontend
- CSP headers configurés
- Validation côté client et serveur
- Sanitisation des données utilisateur
- HTTPS forcé

### API
- Rate limiting par IP/utilisateur
- Validation des tokens JWT
- CORS configuré strictement
- Logging des accès

### Base de données
- Row Level Security activé
- Connexions chiffrées
- Backups automatiques chiffrés
- Audit logs activés

---

*Dernière mise à jour : $(date +'%d/%m/%Y') | Version : 1.0.0*