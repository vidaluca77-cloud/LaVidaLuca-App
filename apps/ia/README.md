# La Vida Luca - FastAPI Backend

API backend pour la plateforme La Vida Luca - Formation des jeunes en MFR, développement d'une agriculture nouvelle et insertion sociale.

## Fonctionnalités

### Sécurité et Middleware
- ✅ Gestion d'erreurs centralisée
- ✅ Configuration CORS
- ✅ Middleware de sécurité (TrustedHost)
- ✅ Rate limiting
- ✅ Authentification JWT
- ✅ Validation des tokens

### API Endpoints
- ✅ Authentification (register, login, refresh token)
- ✅ Gestion des activités
- ✅ Protection par JWT
- ✅ Documentation automatique (Swagger/OpenAPI)

### Base de données
- ✅ Modèles SQLAlchemy optimisés
- ✅ Configuration Alembic pour les migrations
- ✅ Pooling de connexions
- ✅ Support PostgreSQL avec asyncpg

### Tests
- ✅ Configuration pytest
- ✅ Tests unitaires (auth, middleware)
- ✅ Tests d'intégration (API endpoints)
- ✅ Couverture de code configurée

## Installation

1. Installer les dépendances:
```bash
pip install -r requirements.txt
```

2. Configurer les variables d'environnement:
```bash
cp .env.example .env
# Éditer .env avec vos paramètres
```

3. Initialiser la base de données:
```bash
alembic init
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Utilisation

### Développement
```bash
python main.py
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Tests
```bash
# Tests unitaires
pytest tests/test_auth.py -v

# Tests d'intégration
pytest tests/test_integration.py -v

# Tous les tests avec couverture
pytest --cov=app
```

## Documentation API

Une fois l'application lancée:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

Voir `.env.example` pour les variables d'environnement disponibles:
- Configuration de base de données
- Clés de sécurité JWT
- Paramètres CORS
- Limites de taux

## Architecture

```
app/
├── auth/           # Service d'authentification JWT
├── api/endpoints/  # Endpoints API
├── core/           # Configuration
├── db/             # Configuration base de données
├── middleware/     # Middleware personnalisés
└── models/         # Modèles SQLAlchemy
```