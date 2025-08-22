# FastAPI Backend - La Vida Luca

## Description

API complète pour la plateforme La Vida Luca, développée avec FastAPI pour gérer l'authentification, les activités agricoles, les profils utilisateurs et les inscriptions.

## Fonctionnalités

### 🔐 Authentification
- Inscription et connexion utilisateur
- JWT tokens (access + refresh)
- Middleware de sécurité
- Gestion des rôles (utilisateur, étudiant MFR)

### 👥 Gestion des utilisateurs
- Profils utilisateur complets
- Gestion des compétences et disponibilités
- Préférences d'activités
- Informations médicales et d'urgence

### 🌱 Gestion des activités
- 30 activités pré-définies (agriculture, transformation, artisanat, environnement, social)
- Système de recommandation basé sur les profils
- Sessions d'activités avec gestion des places
- Filtres par catégorie, niveau, saison

### 📝 Inscriptions
- Inscription aux activités et sessions
- Gestion des statuts (en attente, confirmé, annulé)
- Historique des participations

### 🛡️ Sécurité
- Validation Pydantic
- Rate limiting
- CORS sécurisé
- Hachage sécurisé des mots de passe

## Installation

### Prérequis
- Python 3.11+
- PostgreSQL
- Docker (optionnel)

### Installation locale

1. **Installer les dépendances**
```bash
cd apps/api
pip install -r requirements.txt
```

2. **Configuration**
```bash
cp .env.example .env
# Éditer .env avec vos paramètres
```

3. **Base de données**
```bash
# Créer la base de données
createdb lavidaluca

# Migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Données de test
python seed_data.py
```

4. **Lancer l'API**
```bash
python run.py
# ou
uvicorn main:app --reload
```

### Installation Docker

```bash
cd apps/api
docker-compose up -d
```

## API Documentation

Une fois l'API lancée, la documentation interactive est disponible :
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

## Tests

```bash
# Tous les tests
pytest

# Tests unitaires seulement
pytest tests/unit/

# Tests d'intégration seulement
pytest tests/integration/

# Avec couverture
pytest --cov=app
```

## Structure du projet

```
apps/api/
├── app/
│   ├── api/v1/            # Routes API
│   ├── auth/              # Authentification
│   ├── core/              # Configuration et modèles
│   ├── schemas/           # Schémas Pydantic
│   └── services/          # Logique métier
├── alembic/               # Migrations
├── tests/                 # Tests
├── main.py                # Point d'entrée
├── requirements.txt       # Dépendances
└── docker-compose.yml     # Configuration Docker
```

## Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `DATABASE_URL` | URL de la base de données | postgresql://... |
| `SECRET_KEY` | Clé secrète JWT | - |
| `ENVIRONMENT` | Environnement (dev/prod) | development |
| `ALLOWED_ORIGINS` | Origines CORS autorisées | localhost:3000 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiration token access | 30 |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Expiration token refresh | 7 |

## Déploiement

### Render.com

1. Connecter le repository
2. Configurer les variables d'environnement
3. Définir la commande de build : `pip install -r requirements.txt`
4. Définir la commande de start : `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`

### Autres plateformes

L'API est containerisée et peut être déployée sur n'importe quelle plateforme supportant Docker.

## Sécurité

- Tokens JWT avec expiration
- Rate limiting (100 req/min par défaut)
- Validation stricte des données
- Hachage bcrypt des mots de passe
- CORS configuré
- Headers de sécurité

## Support

Pour toute question ou problème, créer une issue sur le repository GitHub.