# LaVidaLuca-App
Plateforme interactive pour le projet La Vida Luca : formation des jeunes en MFR, développement d'une agriculture nouvelle et insertion sociale.

## 🎯 Vision
- Former et accompagner les jeunes en MFR via un catalogue de 30 activités agricoles, artisanales et environnementales.
- Développer une agriculture nouvelle : durable, autonome, innovante.
- Favoriser l'insertion sociale par la pratique et la responsabilité.
- Créer un outil numérique qui connecte les lieux d'action et les participants.

## 📦 Architecture Monorepo

```
LaVidaLuca-App/
├── src/app/                 # Frontend Next.js (Vercel)
│   ├── page.tsx            # Page d'accueil
│   ├── catalogue/          # Catalogue d'activités
│   ├── test-ia/            # Interface de test IA
│   └── ...
├── apps/ia/                # Backend FastAPI (Render)
│   ├── main.py             # API IA endpoints
│   ├── requirements.txt    # Dépendances Python
│   ├── .env.example        # Configuration
│   └── tests/              # Tests API
├── .github/workflows/      # CI/CD GitHub Actions
├── render.yaml            # Configuration déploiement
└── package.json           # Scripts monorepo
```

## 🚀 Déploiement

### Frontend (Vercel)
- Site web Next.js
- Hébergement statique optimisé
- Intégration continue depuis GitHub

### Backend IA (Render)
- API FastAPI avec endpoints IA
- Déploiement automatique
- Gestion des variables d'environnement

### Base de données (Supabase)
- Authentification et données
- Schéma SQL pour le catalogue
- Intégration temps réel

## 🛠️ Installation et Développement

### Prérequis
- Node.js 18+
- Python 3.11+
- Git

### Installation complète
```bash
# Cloner le projet
git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
cd LaVidaLuca-App

# Installer toutes les dépendances
npm run setup

# Copier les fichiers d'environnement
cp .env.local.example .env.local
cp apps/ia/.env.example apps/ia/.env
```

### Développement

#### Frontend seul
```bash
npm run dev
# ➜ http://localhost:3000
```

#### Backend IA seul
```bash
npm run dev:ia
# ➜ http://localhost:8000
# Documentation: http://localhost:8000/docs
```

#### Développement complet (frontend + backend)
```bash
npm run dev:all
```

### Tests
```bash
# Tous les tests
npm test

# Tests backend seulement
npm run test:ia

# Lint frontend
npm run lint
```

## 🔧 Configuration

### Variables d'environnement Frontend (.env.local)
```env
NEXT_PUBLIC_SITE_URL=https://la-vida-luca.vercel.app
NEXT_PUBLIC_IA_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_key
NEXT_PUBLIC_CONTACT_EMAIL=vidaluca77@gmail.com
```

### Variables d'environnement Backend (apps/ia/.env)
```env
PORT=8000
DEBUG=true
ALLOWED_ORIGINS=http://localhost:3000,https://la-vida-luca.vercel.app
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

## 🤖 API IA - Endpoints

### Health Check
```bash
GET /health
# Statut de l'API
```

### Guide d'activité
```bash
POST /guide
Content-Type: application/json

{
  "activite_id": "semis-plantation",
  "profil_utilisateur": {
    "niveau": "debutant"
  },
  "contexte": "Formation MFR"
}
```

### Chat IA
```bash
POST /chat
Content-Type: application/json

{
  "message": "Quelles activités puis-je faire ?",
  "contexte": "Nouveau participant",
  "historique": []
}
```

## 📋 Catalogue des Activités

### Agriculture (agri)
- Semis & plantation
- Soins aux animaux d'élevage
- Tonte & entretien du troupeau
- Soins basse-cour

### Transformation (transfo)
- Fabrication de fromage
- Conserves et confitures
- Panification artisanale

### Artisanat
- Menuiserie de base
- Construction d'abris
- Peinture & décoration
- Aménagement d'espaces verts

### Environnement (nature)
- Plantation d'arbres
- Compostage et recyclage
- Nichoirs & hôtels à insectes

### Animation sociale
- Journées portes ouvertes
- Ateliers enfants
- Visites guidées

## 🧪 Tests et Qualité

### Frontend
- ESLint pour la qualité du code
- Tests de build Next.js
- Validation TypeScript

### Backend
- Tests unitaires avec pytest
- Tests d'intégration API
- Validation des endpoints

### CI/CD
- Tests automatiques sur PR
- Déploiement automatique sur main
- Scan de sécurité avec Trivy

## 🚀 Scripts Disponibles

```bash
# Développement
npm run dev              # Frontend seul
npm run dev:ia          # Backend IA seul
npm run dev:all         # Frontend + Backend

# Installation
npm run setup           # Installer tout
npm run install:ia      # Backend Python seulement

# Tests et qualité
npm test               # Tous les tests
npm run test:ia        # Tests backend
npm run lint           # Lint frontend

# Build
npm run build          # Build frontend pour production
```

## 🌐 URLs de Production

- **Frontend**: https://la-vida-luca.vercel.app
- **API IA**: https://lavidaluca-ia-api.onrender.com
- **Documentation API**: https://lavidaluca-ia-api.onrender.com/docs
- **Test IA**: https://la-vida-luca.vercel.app/test-ia

## 🔑 Secrets GitHub Actions

Pour le déploiement automatique, configurer ces secrets :

```
NEXT_PUBLIC_IA_API_URL
NEXT_PUBLIC_SITE_URL
RENDER_DEPLOY_HOOK_PRODUCTION
RENDER_DEPLOY_HOOK_STAGING
```

## 🛡️ Règles & Pacte

- Pas de vente directe sur la plateforme
- Respect de l'éthique du projet La Vida Luca
- Formation avant profit
- Collaboration et partage des connaissances
- Respect de l'environnement et des pratiques durables

## 👨‍💻 Instructions de Déploiement

### 1. Déployer le Frontend (Vercel)
1. Connecter le repo GitHub à Vercel
2. Configurer les variables d'environnement
3. Déploiement automatique sur push main

### 2. Déployer l'API IA (Render)
1. Créer un service Web sur Render
2. Connecter le repo GitHub
3. Configurer : `apps/ia` comme répertoire racine
4. Build command: `pip install -r requirements.txt`
5. Start command: `python main.py`

### 3. Configurer Supabase
1. Créer un projet Supabase
2. Importer le schéma SQL
3. Configurer l'authentification
4. Ajouter les variables d'environnement

### 4. Tests de déploiement
1. Vérifier l'API : `/health`
2. Tester l'interface : `/test-ia`
3. Valider l'intégration frontend-backend