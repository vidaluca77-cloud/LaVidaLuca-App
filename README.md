# LaVidaLuca-App

Plateforme interactive pour le projet La Vida Luca : formation des jeunes en MFR, développement d'une agriculture nouvelle et insertion sociale.

## 🎯 Vision

- **Former et accompagner** les jeunes en MFR via un catalogue de 30 activités agricoles, artisanales et environnementales
- **Développer une agriculture nouvelle** : durable, autonome, innovante
- **Favoriser l'insertion sociale** par la pratique et la responsabilité
- **Créer un outil numérique** qui connecte les lieux d'action et les participants

## 📦 Architecture Monorepo

```
LaVidaLuca-App/
├── src/                    # Frontend Next.js (racine)
│   ├── app/               # Pages et composants Next.js 14
│   └── ...
├── apps/
│   └── ia/                # Backend FastAPI pour l'IA agricole
│       ├── main.py        # Application FastAPI
│       ├── requirements.txt
│       ├── .env.example
│       └── tests/
├── .github/workflows/     # CI/CD
├── render.yaml           # Configuration déploiement Render
└── README.md
```

## 🚀 Démarrage Rapide

### Prérequis

- Node.js 18+ et npm
- Python 3.11+
- Git

### Installation complète

```bash
# Cloner le repository
git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
cd LaVidaLuca-App

# Installation automatique (frontend + backend)
npm run setup
```

### Développement

```bash
# Démarrer frontend et backend simultanément
npm run dev:full

# Ou séparément :
npm run dev          # Frontend sur http://localhost:3000
npm run dev:api      # API sur http://localhost:8000
```

### Tests

```bash
# Tests de l'API FastAPI
npm run test:api

# Tests frontend (si configurés)
npm test

# Page de test de l'API
# Aller sur http://localhost:3000/test-ia
```

## 🤖 API IA Agricole

### Endpoints Disponibles

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/health` | GET | Vérification de la santé de l'API |
| `/guide` | POST | Guide agricole personnalisé |
| `/chat` | POST | Chat interactif avec l'IA |
| `/docs` | GET | Documentation interactive Swagger |

### Exemples d'utilisation

#### Guide agricole
```bash
curl -X POST "http://localhost:8000/guide" \
  -H "Content-Type: application/json" \
  -d '{
    "culture": "tomates",
    "saison": "printemps",
    "region": "Provence",
    "niveau": "débutant"
  }'
```

#### Chat IA
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Comment débuter en permaculture ?",
    "contexte": "formation MFR"
  }'
```

## 🔧 Configuration

### Variables d'environnement

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_IA_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-key
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
```

#### Backend (apps/ia/.env)
```bash
ALLOWED_ORIGINS=http://localhost:3000,https://la-vida-luca.vercel.app
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true
```

## 🚀 Déploiement

### Architecture de Production

- **Frontend** : Vercel (Next.js)
- **API IA** : Render (FastAPI)
- **Base de données** : Supabase (PostgreSQL)
- **CI/CD** : GitHub Actions

### Déploiement sur Render

1. **Connecter le repository** à Render
2. **Utiliser render.yaml** pour la configuration automatique
3. **Configurer les variables d'environnement** :
   ```
   ALLOWED_ORIGINS=https://la-vida-luca.vercel.app
   API_DEBUG=false
   ```

### Déploiement sur Vercel

```bash
# Installer Vercel CLI
npm install -g vercel

# Déployer
vercel

# Configurer les variables d'environnement
vercel env add NEXT_PUBLIC_IA_API_URL production
# Valeur: https://lavidaluca-ia-api.onrender.com
```

## 🧪 Tests et Qualité

### Tests automatisés

```bash
# Tests de l'API
cd apps/ia && pytest tests/ -v

# Linting
npm run lint

# Audit de sécurité
npm audit
```

### CI/CD Pipeline

Le pipeline GitHub Actions exécute automatiquement :

- ✅ Tests frontend (Node.js 18, 20)
- ✅ Tests backend (Python 3.11, 3.12)
- ✅ Linting et formatage
- ✅ Audit de sécurité
- 🚀 Déploiement automatique (main branch)

## 📋 Catalogue des Activités MFR

L'application propose **30 activités agricoles et artisanales** pour la formation des jeunes :

### 🌱 Agriculture (10 activités)
- Maraîchage bio et permaculture
- Élevage de petits animaux
- Apiculture et production de miel
- Culture de champignons
- Compostage et fertilisation naturelle

### 🔨 Artisanat (10 activités)  
- Menuiserie et construction bois
- Poterie et céramique
- Tissage et textile naturel
- Vannerie et osier
- Forge et métallurgie

### 🌍 Environnement (10 activités)
- Gestion de l'eau et irrigation
- Énergies renouvelables
- Biodiversité et écosystèmes
- Restauration de paysages
- Gestion des déchets

## 🛡️ Règles et Engagement

- ❌ **Pas de vente directe** sur la plateforme
- 🏡 Page **"Nos lieux d'action"** au lieu de "Localisation"
- 🎓 Section **"Catalogue d'activités"** réservée aux élèves MFR
- ❤️ Ton et design orientés **cœur et mission**, pas argent

## 🤝 Contribution

### Structure de développement

```bash
# Créer une branche feature
git checkout -b feature/nouvelle-fonctionnalite

# Développer et tester
npm run dev:full
npm run test:api

# Commit et push
git add .
git commit -m "feat: nouvelle fonctionnalité"
git push origin feature/nouvelle-fonctionnalite
```

### Standards de code

- **Frontend** : ESLint + Prettier, TypeScript strict
- **Backend** : Black + Flake8, type hints obligatoires
- **Tests** : Coverage minimum 80%
- **Documentation** : JSDoc pour le frontend, docstrings pour l'API

## 📞 Support

- **Email** : contact@lavidaluca.fr
- **Documentation** : [API Docs](http://localhost:8000/docs)
- **Issues** : GitHub Issues pour bugs et améliorations

## 📄 Licence

MIT - Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

**La Vida Luca** - *Cultivons l'avenir ensemble* 🌱