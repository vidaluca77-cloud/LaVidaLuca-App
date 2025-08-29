# La Vida Luca App

[![CI/CD Pipeline](https://github.com/vidaluca77-cloud/LaVidaLuca-App/actions/workflows/ci.yml/badge.svg)](https://github.com/vidaluca77-cloud/LaVidaLuca-App/actions/workflows/ci.yml)
[![Deploy](https://github.com/vidaluca77-cloud/LaVidaLuca-App/actions/workflows/deploy.yml/badge.svg)](https://github.com/vidaluca77-cloud/LaVidaLuca-App/actions/workflows/deploy.yml)

Plateforme collaborative pour l'entraide et les échanges locaux, axée sur le jardinage, la permaculture et la vie durable.

## 🏗️ Architecture

- **Frontend**: Next.js 15 + React 19 + TypeScript
- **Backend**: FastAPI + Python 3.12
- **Base de données**: PostgreSQL avec AsyncPG
- **Authentification**: JWT
- **IA**: OpenAI Integration pour conseils personnalisés
- **Déploiement**: Vercel (frontend) + Render (backend)
- **Monitoring**: Sentry + Prometheus metrics

## 🚀 Lancement Local

### Prérequis

- Node.js 20+
- Python 3.12+
- PostgreSQL 15+
- Git

### Installation rapide

```bash
# 1. Cloner le repository
git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
cd LaVidaLuca-App

# 2. Configuration environnement
cp .env.example .env
cp apps/backend/.env.example apps/backend/.env
cp apps/web/.env.local.example apps/web/.env.local

# 3. Installer les dépendances
npm run setup

# 4. Configurer la base de données
createdb lavidaluca_dev
cd apps/backend
python -m alembic upgrade head

# 5. Lancer l'application complète
npm run dev:full
```

### Lancement séparé

#### Backend (port 8000)
```bash
cd apps/backend
pip install -r requirements.txt
cp .env.example .env
# Configurer DATABASE_URL dans .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend (port 3000)
```bash
cd apps/web
npm install
cp .env.local.example .env.local
# Configurer NEXT_PUBLIC_API_URL dans .env.local
npm run dev
```

## 📡 API Endpoints

### Endpoints principaux

- `GET /` - Informations de l'API
- `GET /health` - Health check (base de données + statut)
- `GET /docs` - Documentation Swagger (développement uniquement)

### Authentification
- `POST /api/v1/auth/register` - Inscription utilisateur
- `POST /api/v1/auth/login` - Connexion
- `POST /api/v1/auth/refresh` - Renouvellement token

### Guide IA
- `POST /api/v1/guide` - Conseils personnalisés IA
- `GET /api/v1/guide/health` - Statut service guide

### Utilisateurs
- `GET /api/v1/users/me` - Profil utilisateur
- `PUT /api/v1/users/me` - Mise à jour profil

### Activités
- `GET /api/v1/activities` - Liste des activités
- `POST /api/v1/activities` - Créer une activité
- `GET /api/v1/activities/{id}` - Détails activité

### Contacts & Suggestions
- `POST /api/v1/contacts` - Formulaire de contact
- `POST /api/v1/suggestions` - Proposer une amélioration

## 🧪 Tests

### Backend
```bash
cd apps/backend
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html  # Avec couverture
```

### Frontend
```bash
cd apps/web
npm run test
npm run test:coverage
```

### Test de l'API Guide
Visitez `http://localhost:3000/test-ia` pour tester l'endpoint `/guide` avec une interface utilisateur.

## 🚀 Déploiement Automatique

Le déploiement est automatisé via GitHub Actions :

### Configuration des secrets

Dans les settings GitHub du repository, configurer :

#### Backend (Render)
- `RENDER_DEPLOY_HOOK_IA` : URL de déploiement Render

#### Frontend (Netlify)
- `NETLIFY_SITE_ID` : ID du site Netlify
- `NETLIFY_AUTH_TOKEN` : Token d'authentification Netlify

### Processus de déploiement

1. **Push sur `main`** déclenche automatiquement :
   - Tests backend avec PostgreSQL
   - Build frontend
   - Tests d'intégration
   - Déploiement backend sur Render
   - Déploiement frontend sur Netlify

2. **Pull Requests** exécutent les tests CI sans déploiement

## 🔧 Configuration Environnement

### Variables Backend (.env)
```bash
ENVIRONMENT=development|production
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db
JWT_SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Variables Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME=La Vida Luca
SENTRY_DSN=your-sentry-dsn
```

## 📁 Structure du Projet

```
LaVidaLuca-App/
├── .github/workflows/     # GitHub Actions CI/CD
├── apps/
│   ├── backend/          # API FastAPI
│   │   ├── routes/       # Endpoints API
│   │   ├── tests/        # Tests backend
│   │   ├── models/       # Modèles SQLAlchemy
│   │   └── main.py       # Application principale
│   └── web/              # Frontend Next.js
│       ├── app/          # Pages et composants
│       ├── public/       # Assets statiques
│       └── src/          # Code source
├── .env.example          # Configuration globale
└── package.json          # Scripts npm globaux
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Standards de code
- **Backend**: Black (formatage) + isort + flake8
- **Frontend**: ESLint + Prettier + TypeScript strict
- **Tests**: Coverage minimum 80%
- **Commits**: Convention Conventional Commits

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

- **Issues GitHub**: [github.com/vidaluca77-cloud/LaVidaLuca-App/issues](https://github.com/vidaluca77-cloud/LaVidaLuca-App/issues)
- **Email**: support@lavidaluca.fr
- **Documentation**: Disponible à `/docs` en mode développement

---

Développé avec ❤️ pour promouvoir l'entraide locale et la vie durable.
    Frontend --> Backend[FastAPI Backend]
    Backend --> Database[(PostgreSQL)]
    Backend --> OpenAI[OpenAI API]
    Frontend --> Sentry[Sentry Monitoring]
    Backend --> Sentry
    
    subgraph "Déploiement"
        Frontend --> Vercel[Vercel Hosting]
        Backend --> Render[Render Hosting]
    end
    
    subgraph "Fonctionnalités"
        Backend --> Activities[Catalogue d'activités]
        Backend --> IA[Suggestions IA]
        Backend --> Contact[Contact & Rejoindre]
        Backend --> Auth[Authentification JWT]
    end
```

## Installation

### Prérequis
- Node.js 18.x ou supérieur
- Python 3.11+
- PostgreSQL 12+
- npm ou yarn
- Git

### 1. Cloner le repository
```bash
git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
cd LaVidaLuca-App
```

### 2. Installation complète
```bash
# Installation frontend et backend
npm run setup

# Ou installation séparée:
npm install                    # Frontend
npm run backend:install       # Backend
```

### 3. Configuration Backend
```bash
cd apps/backend
cp .env.example .env
# Éditer .env avec vos valeurs
```

### 4. Configuration Base de données
```bash
# Créer la base de données
createdb lavidaluca_dev

# Appliquer les migrations
npm run backend:migrate

# (Optionnel) Peupler avec des données d'exemple
cd apps/backend && python seed.py
```

### 5. Configuration Frontend
Créer un fichier `.env.local` à la racine avec les variables suivantes :
```env
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Sentry (monitoring - requis pour la surveillance des erreurs)
NEXT_PUBLIC_SENTRY_DSN=votre_dsn_sentry

# Sentry Backend (pour le monitoring backend)
SENTRY_DSN=votre_dsn_sentry_backend

# Contact
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789
```

### 6. Lancement en développement
```bash
# Frontend seul
npm run dev

# Backend seul  
npm run backend:dev

# Frontend + Backend simultanément
npm run dev:full
```

L'application sera accessible sur :
- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **Documentation API**: `http://localhost:8000/docs`
- **Monitoring Dashboard**: `http://localhost:3000/monitoring` (développement uniquement)
- **Métriques Prometheus**: `http://localhost:8000/metrics`

## Scripts disponibles

### Frontend
| Script | Description |
|--------|-------------|
| `npm run dev` | Lance le serveur de développement frontend |
| `npm run build` | Compile l'application pour la production |
| `npm run start` | Lance l'application compilée |
| `npm run lint` | Vérifie la qualité du code |
| `npm run type-check` | Vérifie les types TypeScript |
| `npm test` | Lance les tests frontend |

### Backend
| Script | Description |
|--------|-------------|
| `npm run backend:dev` | Lance le serveur de développement backend |
| `npm run backend:install` | Installe les dépendances Python |
| `npm run backend:test` | Lance les tests backend |
| `npm run backend:migrate` | Applique les migrations de base de données |
| `npm run backend:migration` | Crée une nouvelle migration |

### Full-stack
| Script | Description |
|--------|-------------|
| `npm run setup` | Installation complète (frontend + backend) |
| `npm run dev:full` | Lance frontend et backend simultanément |

## Structure du projet

```
├── apps/
│   ├── backend/            # API FastAPI
│   │   ├── main.py         # Point d'entrée de l'API
│   │   ├── config.py       # Configuration
│   │   ├── database.py     # Connexion base de données
│   │   ├── auth/           # Authentification JWT
│   │   ├── models/         # Modèles SQLAlchemy
│   │   ├── schemas/        # Schémas Pydantic
│   │   ├── routes/         # Points de terminaison API
│   │   ├── services/       # Logique métier
│   │   ├── migrations/     # Migrations Alembic
│   │   └── tests/          # Tests backend
│   └── web/                # Application frontend Next.js
├── public/                 # Fichiers statiques
│   ├── icons/             # Icônes PWA
│   └── manifest.webmanifest
├── src/
│   ├── app/               # App Router Next.js 13+
│   │   ├── api/           # Routes API (legacy)
│   │   ├── catalogue/     # Page catalogue d'activités
│   │   ├── contact/       # Page contact
│   │   ├── rejoindre/     # Page rejoindre
│   │   ├── layout.tsx     # Layout principal
│   │   └── page.tsx       # Page d'accueil
│   ├── components/        # Composants réutilisables
│   ├── lib/              # Utilitaires et configurations
│   ├── monitoring/       # Outils de monitoring
│   └── types/            # Types TypeScript
├── monitoring/            # Configuration monitoring backend
├── docs/                 # Documentation additionnelle
└── tests/                # Tests frontend
```

## Déploiement

### Production sur Netlify

1. **Connexion du repository**
   - Connecter le repository GitHub à Netlify
   - Sélectionner la branche `main` pour les déploiements automatiques
   - Configuration automatique via `netlify.toml`

2. **Configuration des variables d'environnement**
   Dans le dashboard Netlify, ajouter toutes les variables du fichier `.env.local`

3. **Déploiement**
   ```bash
   # Déploiement automatique via Git
   git push origin main
   
   # Ou déploiement manuel via CLI
   npm install -g netlify-cli
   netlify login
   cd apps/web
   npm run build
   netlify deploy --prod --dir=out
   ```

### Optimisations de production
- **Static Export** : Site statique optimisé
- **Compression** : Gzip automatique par Netlify
- **CDN** : Distribution globale automatique
- **Images** : Optimisation via Next.js (pré-build)
- **Fonts** : Optimisation automatique des Google Fonts
- **Bundle** : Tree-shaking et minification
- **PWA** : Manifest et service worker
- **Headers** : Configuration de sécurité via `netlify.toml`

## Monitoring et Observabilité

### Sentry (Monitoring d'erreurs)
- Capture automatique des erreurs frontend
- Monitoring des performances
- Alertes en temps réel
- Session Replay pour le debugging

### Métriques personnalisées
- Temps de chargement des pages
- Interactions utilisateur
- Erreurs API
- Performances des suggestions IA

### Logs structurés
```javascript
// Exemple d'utilisation
import { logger } from '@/lib/logger';

logger.info('Action utilisateur', {
  action: 'view_activity',
  activityId: 'abc123',
  userId: 'user456'
});
```

## API et Intégrations

### Routes API principales
- `GET /api/activities` - Liste des activités
- `POST /api/contact` - Envoi de messages de contact
- `GET /api/suggestions` - Suggestions IA personnalisées

### Intégrations externes
- **Supabase** : Base de données et authentification
- **OpenAI** : Génération de suggestions personnalisées
- **Sentry** : Monitoring et alertes

## Tests

### Exécution des tests
```bash
# Tests unitaires
npm test

# Tests avec coverage
npm run test:coverage

# Tests en mode watch
npm run test:watch
```

### Types de tests
- **Unitaires** : Composants et fonctions utilitaires
- **Intégration** : Flux utilisateur complets
- **E2E** : Tests de bout en bout avec Playwright

## Contribution

### Workflow de développement
1. **Fork** du repository
2. **Branche** : `git checkout -b feature/ma-fonctionnalite`
3. **Développement** avec tests
4. **Commit** : `git commit -m 'feat: ajouter ma fonctionnalité'`
5. **Push** : `git push origin feature/ma-fonctionnalite`
6. **Pull Request** avec description détaillée

### Standards de code
- **ESLint** : Configuration stricte Next.js
- **TypeScript** : Typage strict activé
- **Prettier** : Formatage automatique
- **Conventional Commits** : Messages de commit standardisés

### Review checklist
- [ ] Tests passent (`npm test`)
- [ ] Build réussit (`npm run build`)
- [ ] Lint sans erreur (`npm run lint`)
- [ ] Types corrects (`npm run type-check`)
- [ ] Documentation mise à jour
- [ ] Changements testés manuellement

## Sécurité

### Bonnes pratiques
- Variables d'environnement pour les secrets
- Validation des inputs côté client et serveur
- CSP (Content Security Policy) configuré
- HTTPS obligatoire en production

### Authentification
- JWT tokens via Supabase
- Refresh tokens automatiques
- Logout sécurisé

## Monitoring et Observabilité

### Surveillance des erreurs
- **Sentry** : Capture et suivi des erreurs frontend et backend
- **Error Boundaries** : Gestion des erreurs React avec fallback UI
- **Filtrage intelligent** : Les erreurs sensibles sont automatiquement filtrées
- **Contexte utilisateur** : Tracking des actions utilisateur pour debugging

### Métriques de performance
- **Web Vitals** : FCP, LCP, FID, CLS en temps réel
- **API Performance** : Latence, taux de succès/échec des appels API
- **Métriques système** : CPU, mémoire, connexions base de données
- **Métriques métier** : Actions utilisateur, utilisation des fonctionnalités

### Dashboard de monitoring
- **Interface temps réel** : `/monitoring` (développement uniquement)
- **Statut de santé** : Aperçu global de l'état de l'application
- **Alertes** : Système d'alertes configurables pour les problèmes critiques
- **Export des données** : Téléchargement des métriques au format JSON

### Logging structuré
- **Frontend** : JSON structuré avec contexte utilisateur
- **Backend** : Logs contextuels avec request ID unique
- **Activités utilisateur** : Tracking des interactions pour analytics
- **API calls** : Log complet des requêtes/réponses avec durée

### Configuration monitoring
```bash
# Frontend (.env.local)
NEXT_PUBLIC_SENTRY_DSN=your_sentry_dsn

# Backend (.env)
SENTRY_DSN=your_sentry_backend_dsn
```

### Endpoints de monitoring
- **Health check** : `GET /health`
- **Métriques Prometheus** : `GET /metrics`
- **Dashboard monitoring** : `http://localhost:3000/monitoring`

## Performance

### Optimisations
- **Code splitting** automatique par Next.js
- **Lazy loading** des composants
- **Image optimization** avec next/image
- **Font optimization** avec next/font

### Métriques cibles
- **FCP** < 1.5s (First Contentful Paint)
- **LCP** < 2.5s (Largest Contentful Paint)
- **CLS** < 0.1 (Cumulative Layout Shift)
- **FID** < 100ms (First Input Delay)

## Support et Contact

### Documentation
- **API Docs** : `/docs` (à venir avec backend)
- **Storybook** : Composants UI (à venir)
- **Wiki** : Documentation étendue

### Contact technique
- **Email** : tech@lavidaluca.fr
- **Issues** : GitHub Issues pour les bugs
- **Discussions** : GitHub Discussions pour les questions

## Roadmap

### À venir
- [ ] Backend FastAPI pour l'IA
- [ ] Authentification complète
- [ ] Dashboard utilisateur
- [ ] Mobile app (React Native)
- [ ] API publique
- [ ] Intégration calendrier
- [ ] Notifications push

---

**La Vida Luca** - Plateforme collaborative pour la formation des jeunes en MFR et le développement d'une agriculture nouvelle.

*Dernière mise à jour : 2024*