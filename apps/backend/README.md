# La Vida Luca - Backend FastAPI

## Vue d'ensemble
Backend FastAPI pour la plateforme collaborative La Vida Luca, dédiée à la formation des jeunes en MFR (Maisons Familiales Rurales) et au développement d'une agriculture nouvelle.

## Architecture Backend

### Technologies
- **Framework**: FastAPI 0.100+
- **Python**: 3.11+
- **Base de données**: PostgreSQL 12+ avec SQLAlchemy
- **Authentification**: JWT (JSON Web Tokens)
- **Migrations**: Alembic
- **Tests**: pytest + pytest-asyncio
- **ORM**: SQLAlchemy (version 1.4.x compatible)

### Structure du projet
```
apps/backend/
├── main.py              # Point d'entrée FastAPI
├── config.py            # Configuration et settings
├── database.py          # Connexion PostgreSQL
├── middleware.py        # Middlewares personnalisés
├── exceptions.py        # Gestionnaires d'exceptions
├── models/              # Modèles SQLAlchemy
│   ├── __init__.py
│   ├── user.py
│   ├── activity.py
│   └── contact.py
├── routes/              # Routes API
│   ├── __init__.py
│   ├── auth.py
│   ├── users.py
│   ├── activities.py
│   ├── contacts.py
│   └── suggestions.py
├── schemas/             # Schémas Pydantic
│   ├── __init__.py
│   ├── common.py
│   ├── auth.py
│   ├── user.py
│   ├── activity.py
│   └── contact.py
├── auth/                # Authentification
├── services/            # Logique métier
├── tests/               # Tests unitaires
│   ├── conftest.py
│   ├── test_main.py
│   ├── test_auth.py
│   └── test_activities.py
├── migrations/          # Migrations Alembic
├── requirements.txt     # Dépendances Python
└── README.md           # Cette documentation
```

## Installation

### Prérequis
- **Python**: 3.11 ou supérieur
- **PostgreSQL**: 12 ou supérieur
- **pip**: Pour l'installation des dépendances
- **Optionnel**: Virtual environment (venv/conda)

### 1. Installation des dépendances
```bash
# Depuis le répertoire apps/backend/
pip install -r requirements.txt
```

### 2. Configuration de l'environnement
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer les variables d'environnement
# Variables principales :
# - DATABASE_URL=postgresql://user:password@localhost:5432/lavidaluca
# - JWT_SECRET_KEY=your-secret-key-here
# - ENVIRONMENT=development
```

### 3. Configuration de la base de données
```bash
# Créer la base de données PostgreSQL
createdb lavidaluca_dev

# Appliquer les migrations
alembic upgrade head

# (Optionnel) Peupler avec des données d'exemple
python seed.py
```

### 4. Lancement du serveur de développement
```bash
# Méthode 1: Uvicorn direct
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Méthode 2: Script npm (depuis la racine du projet)
npm run backend:dev
```

L'API sera accessible sur :
- **Serveur**: http://localhost:8000
- **Documentation interactive**: http://localhost:8000/docs
- **Documentation ReDoc**: http://localhost:8000/redoc

## Variables d'environnement

### Configuration de base
```env
# Environnement (development/testing/production)
ENVIRONMENT=development
DEBUG=true

# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/lavidaluca
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# JWT Authentication
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS
CORS_ORIGINS=["http://localhost:3000", "https://lavidaluca.fr"]
CORS_ALLOW_CREDENTIALS=true

# OpenAI (optionnel)
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-3.5-turbo

# Email (pour les formulaires de contact)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@domain.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@lavidaluca.fr
```

## Tests

### Exécution des tests
```bash
# Tests unitaires
pytest

# Tests avec couverture
pytest --cov=. --cov-report=html

# Tests spécifiques
pytest tests/test_main.py

# Tests en mode watch (nécessite pytest-watch)
pytest-watch
```

### Configuration des tests
Les tests utilisent une base de données de test séparée configurée dans `conftest.py`. 
Assurez-vous d'avoir créé la base de données de test :
```bash
createdb lavidaluca_test
```

## API Endpoints

### Authentification
- `POST /api/v1/auth/login` - Connexion utilisateur
- `POST /api/v1/auth/register` - Inscription utilisateur
- `POST /api/v1/auth/refresh` - Renouvellement du token

### Utilisateurs
- `GET /api/v1/users/me` - Profil utilisateur actuel
- `PUT /api/v1/users/me` - Mise à jour du profil

### Activités
- `GET /api/v1/activities` - Liste des activités
- `GET /api/v1/activities/{id}` - Détails d'une activité

### Contact
- `POST /api/v1/contacts` - Envoi d'un message de contact

### Suggestions IA
- `GET /api/v1/suggestions` - Suggestions personnalisées

### Système
- `GET /` - Informations de l'API
- `GET /health` - Vérification de santé

## Développement

### Structure des modèles
Les modèles SQLAlchemy sont dans `models/` et suivent une structure standard avec :
- Clés primaires UUID
- Timestamps automatiques (created_at, updated_at)
- Relations appropriées entre entités

### Schémas Pydantic
Les schémas de validation sont dans `schemas/` et incluent :
- Validation des entrées
- Sérialisation des sorties
- Documentation automatique de l'API

### Authentification
Le système d'authentification utilise :
- JWT tokens avec expiration
- Hashage sécurisé des mots de passe (bcrypt)
- Middleware de vérification automatique

### Middleware
- **CORS** : Configuration pour le frontend
- **Process Time** : Mesure du temps de traitement
- **Request Logging** : Logs des requêtes
- **Trusted Host** : Protection en production

## Déploiement

### Production
```bash
# Variables d'environnement en production
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://user:pass@prod-host:5432/db
JWT_SECRET_KEY=strong-production-secret

# Serveur ASGI avec Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker (optionnel)
```bash
# Build
docker build -t lavidaluca-backend .

# Run
docker run -p 8000:8000 --env-file .env lavidaluca-backend
```

## Scripts npm disponibles (depuis la racine)

- `npm run backend:dev` - Serveur de développement
- `npm run backend:install` - Installation des dépendances
- `npm run backend:test` - Exécution des tests
- `npm run backend:migrate` - Application des migrations
- `npm run backend:migration` - Création d'une nouvelle migration

## Support et Contribution

### Logs et Debugging
Les logs sont configurés avec différents niveaux selon l'environnement.
En développement, les requêtes SQL sont loggées automatiquement.

### Convention de code
- **PEP 8** pour le style Python
- **Type hints** obligatoires
- **Docstrings** pour les fonctions publiques
- **Tests** pour les nouvelles fonctionnalités

---

Pour plus d'informations, consultez la documentation principale du projet.