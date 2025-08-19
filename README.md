# LaVidaLuca-App

Plateforme interactive pour le projet La Vida Luca : formation des jeunes en MFR, développement d'une agriculture nouvelle et insertion sociale.

![LaVidaLuca Logo](public/icons/icon-192.png)

## 🎯 Vision

**La Vida Luca** est une plateforme collaborative basée sur l'IA pour :
- Former et accompagner les jeunes en MFR via un catalogue de 30 activités agricoles, artisanales et environnementales
- Développer une agriculture nouvelle : durable, autonome, innovante
- Favoriser l'insertion sociale par la pratique et la responsabilité
- Créer un outil numérique qui connecte les lieux d'action et les participants

## 🚀 Architecture Technique

### Frontend (Next.js 14)
- **Framework** : Next.js 14 avec App Router
- **UI** : React 18 + TypeScript + Tailwind CSS
- **État** : React Context + Custom Hooks
- **Authentification** : JWT avec React Context
- **Composants** : Design system modulaire et réutilisable

### Backend (FastAPI)
- **API** : FastAPI avec SQLAlchemy ORM
- **Base de données** : PostgreSQL
- **Cache** : Redis
- **Authentification** : JWT avec PassLib
- **IA** : OpenAI API pour recommandations personnalisées
- **Tests** : Pytest avec couverture complète

### Infrastructure
- **Frontend** : Déployé sur Vercel
- **Backend** : Déployé sur Render
- **Base de données** : PostgreSQL managé
- **Cache** : Redis managé
- **CI/CD** : GitHub Actions

## 📦 Structure du Projet

```
LaVidaLuca-App/
├── src/                          # Frontend Next.js
│   ├── app/                     # Pages et layouts
│   ├── components/              # Composants React réutilisables
│   ├── contexts/               # Contextes React (Auth, etc.)
│   ├── hooks/                  # Hooks personnalisés
│   └── lib/                    # Utilitaires et API client
├── apps/api/                   # Backend FastAPI
│   ├── app/
│   │   ├── models/            # Modèles SQLAlchemy
│   │   ├── routers/           # Routes API
│   │   ├── schemas/           # Schémas Pydantic
│   │   ├── services/          # Services métier
│   │   └── utils/             # Utilitaires
│   ├── tests/                 # Tests backend
│   └── requirements.txt       # Dépendances Python
├── .github/workflows/         # CI/CD GitHub Actions
├── docker-compose.yml         # Configuration Docker locale
└── README.md                  # Cette documentation
```

## 🛠️ Installation et Développement

### Prérequis
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker (optionnel)

### Installation Rapide avec Docker

1. **Cloner le repository**
```bash
git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
cd LaVidaLuca-App
```

2. **Démarrer avec Docker Compose**
```bash
docker-compose up -d
```

3. **Accéder à l'application**
- Frontend : http://localhost:3000
- Backend API : http://localhost:8000
- API Documentation : http://localhost:8000/docs

### Installation Manuelle

#### Backend FastAPI

1. **Créer l'environnement virtuel**
```bash
cd apps/api
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configuration**
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

4. **Démarrer le serveur**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Next.js

1. **Installer les dépendances**
```bash
npm install
```

2. **Configuration**
```bash
cp .env.example .env.local
# Éditer .env.local avec vos configurations
```

3. **Démarrer le serveur de développement**
```bash
npm run dev
```

## 🔧 Configuration

### Variables d'Environnement Backend
```env
DATABASE_URL=postgresql://user:password@localhost:5432/lavidaluca
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-super-secret-jwt-key
OPENAI_API_KEY=your-openai-api-key
ALLOWED_ORIGINS=["http://localhost:3000"]
```

### Variables d'Environnement Frontend
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789
```

## 📋 Fonctionnalités Principales

### 🔐 Authentification et Autorisation
- Inscription/connexion sécurisée avec JWT
- Gestion des rôles (utilisateur, administrateur)
- Protection des routes et endpoints

### 🏃‍♂️ Gestion des Activités
- Catalogue de 30 activités agricoles et artisanales
- Recherche et filtrage avancés
- Système d'inscription et de participation
- Évaluations et commentaires

### 🤖 Recommandations IA
- Analyse des profils utilisateurs
- Algorithme de matching intelligent
- Suggestions personnalisées basées sur OpenAI
- Suivi des progrès et compétences

### 👥 Gestion des Utilisateurs
- Profils détaillés avec compétences et préférences
- Dashboard personnel avec progression
- Historique des participations

### 📊 Administration
- Interface d'administration complète
- Gestion des utilisateurs et activités
- Métriques et analyses
- Modération du contenu

## 🧪 Tests

### Backend
```bash
cd apps/api
pytest tests/ -v --cov=app
```

### Frontend
```bash
npm test
```

### Tests E2E
```bash
npm run test:e2e
```

## 🚀 Déploiement

### Déploiement Automatique (Recommandé)

Le projet est configuré pour un déploiement automatique via GitHub Actions :

1. **Fork** le repository
2. **Configurer** les secrets GitHub :
   - `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`
   - `RENDER_API_KEY`, `RENDER_SERVICE_ID`
3. **Push** sur la branche `main` pour déclencher le déploiement

### Déploiement Manuel

#### Frontend (Vercel)
```bash
npm install -g vercel
vercel --prod
```

#### Backend (Render)
1. Connecter votre repository à Render
2. Configurer les variables d'environnement
3. Déployer automatiquement

## 🔒 Sécurité

- **Authentification** : JWT avec rotation des tokens
- **Validation** : Validation stricte des données avec Pydantic
- **Rate Limiting** : Protection contre les abus
- **CORS** : Configuration sécurisée
- **Chiffrement** : Mots de passe hashés avec bcrypt
- **Audit** : Logs de sécurité et monitoring

## 📈 Performance

- **Cache Redis** : Mise en cache des requêtes fréquentes
- **Optimisations React** : Lazy loading et mémorisation
- **Images optimisées** : Compression et formats modernes
- **CDN** : Distribution globale via Vercel

## 🤝 Contribution

1. **Fork** le projet
2. **Créer** une branche feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrir** une Pull Request

### Standards de Code
- **Frontend** : ESLint + Prettier + TypeScript strict
- **Backend** : Black + Flake8 + MyPy + Bandit
- **Tests** : Couverture minimale de 80%
- **Documentation** : JSDoc/Docstrings pour les fonctions publiques

## 📚 Documentation API

La documentation interactive de l'API est disponible à :
- **Swagger UI** : `/docs`
- **ReDoc** : `/redoc`
- **OpenAPI JSON** : `/openapi.json`

## 🛡️ Règles & Pacte

- Pas de vente directe sur la plateforme
- Respect des valeurs d'agriculture durable
- Priorité à la formation et à l'insertion
- Collaboration et partage des connaissances

## 📞 Contact

- **Email** : contact@lavidaluca.fr
- **Site web** : https://la-vida-luca.vercel.app
- **Documentation** : https://vidaluca77-cloud.github.io/LaVidaLuca-App

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- **MFR** (Maisons Familiales Rurales) pour l'inspiration pédagogique
- **OpenAI** pour les capacités d'IA
- **Communauté Open Source** pour les outils exceptionnels

---

**La Vida Luca** - *Former, cultiver, insérer* 🌱