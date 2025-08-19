# La Vida Luca - Backend API

FastAPI backend pour la plateforme La Vida Luca.

## Installation

1. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer l'environnement :
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

## Démarrage

### Mode développement
```bash
python main.py
```

### Mode production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Base de données

### Migrations avec Alembic
```bash
# Créer une nouvelle migration
alembic revision --autogenerate -m "Description de la migration"

# Appliquer les migrations
alembic upgrade head
```

## Documentation API

Une fois le serveur démarré, accédez à :
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc
- OpenAPI JSON : http://localhost:8000/api/v1/openapi.json

## Structure des endpoints

### Activités
- `GET /api/v1/activities/` - Liste des activités
- `POST /api/v1/activities/` - Créer une activité
- `GET /api/v1/activities/{id}` - Détails d'une activité
- `GET /api/v1/activities/slug/{slug}` - Activité par slug
- `PUT /api/v1/activities/{id}` - Modifier une activité
- `DELETE /api/v1/activities/{id}` - Supprimer une activité
- `POST /api/v1/activities/suggestions` - Suggestions basées sur profil

### Utilisateurs
- `GET /api/v1/users/` - Liste des utilisateurs
- `POST /api/v1/users/` - Créer un utilisateur
- `GET /api/v1/users/{id}` - Détails d'un utilisateur
- `PUT /api/v1/users/{id}` - Modifier un utilisateur
- `DELETE /api/v1/users/{id}` - Supprimer un utilisateur
- `POST /api/v1/users/auth/login` - Authentification

## Tests

```bash
pytest
```

## Configuration

Variables d'environnement principales dans `.env` :

- `DATABASE_URL` - URL de connexion à la base de données
- `SECRET_KEY` - Clé secrète pour JWT
- `ALLOWED_ORIGINS` - Origines autorisées pour CORS
- `DEBUG` - Mode debug (true/false)