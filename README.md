# LaVidaLuca-App

Plateforme interactive pour le projet La Vida Luca : formation des jeunes en MFR, développement d'une agriculture nouvelle et insertion sociale.

## 🎯 Vision

Plateforme collaborative basée sur IA pour le projet La Vida Luca, dédiée à :
- Former et accompagner les jeunes en MFR via un catalogue de 30 activités agricoles, artisanales et environnementales
- Développer une agriculture nouvelle : durable, autonome, innovante
- Favoriser l'insertion sociale par la pratique et la responsabilité
- Créer un outil numérique qui connecte les lieux d'action et les participants

## 📦 Structure du monorepo

```
LaVidaLuca-App/
├── src/app/                    # Frontend Next.js (Vercel)
│   ├── page.tsx               # Page d'accueil avec catalogue d'activités
│   ├── test-ia/               # Interface de test pour l'IA
│   ├── contact/               # Page de contact
│   └── rejoindre/             # Page pour devenir relais
├── apps/
│   ├── ia/                    # Backend FastAPI (Render)
│   │   ├── main.py           # API endpoints /health, /guide, /chat
│   │   ├── requirements.txt   # Dépendances Python
│   │   ├── .env.example      # Configuration d'exemple
│   │   └── test_api.py       # Tests unitaires
│   └── web/                  # (Legacy - migration vers src/app)
├── .github/workflows/         # CI/CD GitHub Actions
├── public/                   # Assets statiques
├── render.yaml              # Configuration déploiement Render
└── README.md               # Documentation complète
```

## 🚀 Installation et développement

### Prérequis
- Node.js 18+
- Python 3.11+
- npm ou yarn

### Installation complète
```bash
# Clone du repository
git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
cd LaVidaLuca-App

# Installation de toutes les dépendances
npm run setup
```

### Scripts de développement

```bash
# Développement frontend seul
npm run dev:frontend

# Développement backend seul
npm run dev:backend

# Développement full-stack (frontend + backend)
npm run dev:full

# Tests
npm run test:frontend    # Build Next.js
npm run test:backend     # Tests FastAPI avec pytest
npm run test             # Tests complets

# Build de production
npm run build
```

## 🔧 Configuration

### Frontend (.env.local)
```env
NEXT_PUBLIC_IA_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_key
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
```

### Backend (apps/ia/.env)
```env
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000,https://la-vida-luca.vercel.app
OPENAI_API_KEY=your_openai_key
LOG_LEVEL=INFO
```

## 🤖 API IA - Endpoints

### GET /health
Vérification de l'état de l'API
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "version": "1.0.0"
}
```

### POST /guide
Génération de guide personnalisé basé sur le profil utilisateur
```json
{
  "profile": {
    "skills": ["elevage", "hygiene"],
    "availability": ["weekend", "matin"],
    "location": "Lyon",
    "preferences": ["agri"]
  }
}
```

### POST /chat
Chat avec l'IA pour questions sur les activités
```json
{
  "message": "Comment puis-je commencer en agriculture ?",
  "context": {}
}
```

## 🧪 Tests et qualité

### Tests backend
```bash
cd apps/ia
python -m pytest test_api.py -v
```

### Interface de test
Accessible à `/test-ia` pour tester tous les endpoints de l'API en mode interactif.

## 🚀 Déploiement

### Vercel (Frontend)
1. Connecter le repository à Vercel
2. Configurer les variables d'environnement
3. Déploiement automatique sur push `main`

### Render (Backend)
1. Utiliser le fichier `render.yaml` 
2. Configurer les variables d'environnement sensibles
3. Déploiement automatique via GitHub integration

### CI/CD
Pipeline GitHub Actions automatique :
- Tests frontend et backend
- Vérifications sécurité
- Déploiement automatique sur `main`

## 📋 Catalogue des 30 activités MFR

Les activités sont organisées en 4 catégories :

### 🌱 Agriculture (agri)
- Nourrir les poules, ramasser les œufs
- Préparer le sol, bêcher, retourner
- Planter des graines, repiquer, arroser
- Récolter légumes, fruits, herbes
- Soigner les animaux, vermifuger
- Tonte des moutons, taille des sabots
- Traite des chèvres, fabrication fromage
- Compostage, gestion des déchets verts

### 🔨 Artisanat (artisanat)
- Menuiserie simple, ponçage, montage
- Tissage, tricot, couture
- Poterie, modelage, cuisson
- Réparation outils, maintenance
- Construction abris, clôtures
- Travail du cuir, maroquinerie
- Forge simple, travail du métal
- Vannerie, tressage osier

### 🌿 Nature (nature)
- Observation oiseaux, relevés
- Entretien sentiers, débroussaillage
- Plantation arbres, haies
- Nichoirs, hôtels à insectes
- Récolte graines, boutures
- Gestion mare, écosystème aquatique
- Herbier, identification plantes
- Mesures environnementales

### 👥 Social (social)
- Journée portes ouvertes, accueil
- Animation enfants, jeux éducatifs
- Marché fermier, vente directe
- Cuisine collective, préparation repas
- Goûter fermier, service
- Communication, réseaux sociaux
- Formation, transmission savoirs
- Organisation événements

## 🔑 Variables d'environnement déploiement

```env
# Frontend (Vercel)
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx
NEXT_PUBLIC_IA_API_URL=https://lavidaluca-ia-api.onrender.com
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789

# Backend (Render)
PORT=10000
HOST=0.0.0.0
ENVIRONMENT=production
ALLOWED_ORIGINS=https://la-vida-luca.vercel.app
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
DATABASE_URL=postgresql://xxx
LOG_LEVEL=INFO
```

## 🛡️ Règles & Pacte

- Pas de vente directe sur la plateforme
- Respect du pacte initial La Vida Luca
- Priorité à la formation et l'insertion
- Valeurs : autonomie, durabilité, solidarité

## 👨‍💻 Instructions de déploiement

1. **Déployer l'app web (Vercel)**
   - Connecter GitHub → Vercel
   - Configurer variables d'environnement
   - Build automatique

2. **Déployer l'IA (Render)**
   - Utiliser `render.yaml`
   - Configurer variables sensibles
   - Connexion GitHub

3. **Base de données (optionnel)**
   - Créer projet Supabase
   - Importer schémas SQL
   - Configurer authentification

4. **Tests et validation**
   - Tester `/test-ia` pour vérifier connexions
   - Valider endpoints API
   - Vérifier CORS et sécurité