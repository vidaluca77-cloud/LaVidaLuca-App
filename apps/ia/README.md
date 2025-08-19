# FastAPI Backend pour La Vida Luca

API backend pour le système de recommandations d'activités et gestion des profils utilisateurs.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Créer un fichier `.env` avec les variables d'environnement requises:

```env
DATABASE_URL=postgresql://user:password@localhost/lavidaluca
JWT_SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-url.vercel.app
```

## Développement

```bash
# Démarrer le serveur de développement
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Migrations de base de données
alembic upgrade head

# Tests
pytest
```

## API Documentation

Une fois l'application lancée, la documentation interactive est disponible à:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)