# LaVidaLuca Backend API

API FastAPI pour la plateforme LaVidaLuca - Formation des jeunes en MFR et développement d'une agriculture nouvelle.

## 🚀 Installation

### Prérequis
- Python 3.11+
- PostgreSQL ou SQLite (pour les tests)
- Docker (optionnel)

### Installation locale

1. **Cloner le projet et accéder au backend**
```bash
cd apps/backend
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration**
```bash
cp .env.example .env
# Éditer le fichier .env avec vos paramètres
```

5. **Initialiser la base de données**
```bash
# Créer les migrations initiales
alembic revision --autogenerate -m "Initial migration"

# Appliquer les migrations
alembic upgrade head
```

6. **Démarrer le serveur**
```bash
uvicorn main:app --reload
```

L'API sera accessible sur `http://localhost:8000`

## 🐳 Docker

### Construire l'image
```bash
docker build -t lavidaluca-backend .
```

### Lancer le conteneur
```bash
docker run -p 8000:8000 --env-file .env lavidaluca-backend
```

## 📋 Documentation API

Une fois le serveur démarré, la documentation interactive est disponible :
- **Swagger UI** : http://localhost:8000/api/v1/docs
- **ReDoc** : http://localhost:8000/api/v1/redoc

## 🔧 Structure du projet

```
apps/backend/
├── alembic/                 # Migrations de base de données
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py      # Routes d'authentification
│   │   │   ├── users.py     # Routes utilisateurs
│   │   │   └── activities.py # Routes activités
│   │   └── deps.py          # Dépendances FastAPI
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   └── security.py      # Sécurité JWT
│   ├── models/
│   │   ├── base.py          # Base SQLAlchemy
│   │   ├── user.py          # Modèle utilisateur
│   │   └── activity.py      # Modèle activité
│   └── services/
│       └── auth.py          # Services d'authentification
├── tests/                   # Tests
├── Dockerfile              # Configuration Docker
├── requirements.txt        # Dépendances Python
└── main.py                 # Application FastAPI
```

## 🔐 Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification :

1. **Inscription** : `POST /api/v1/auth/register`
2. **Connexion** : `POST /api/v1/auth/login/json`
3. **Profil** : `GET /api/v1/auth/me` (avec token)

### Exemple d'utilisation

```python
import requests

# Inscription
response = requests.post("http://localhost:8000/api/v1/auth/register", json={
    "email": "user@example.com",
    "password": "motdepasse",
    "full_name": "Nom Utilisateur"
})

# Connexion
response = requests.post("http://localhost:8000/api/v1/auth/login/json", json={
    "email": "user@example.com",
    "password": "motdepasse"
})
token = response.json()["access_token"]

# Utilisation du token
headers = {"Authorization": f"Bearer {token}"}
profile = requests.get("http://localhost:8000/api/v1/auth/me", headers=headers)
```

## 📊 Modèles de données

### Utilisateur
- Informations de base (email, nom, mot de passe)
- Profil (compétences, disponibilités, préférences)
- Statut MFR (étudiant, institution)

### Activité
- Informations générales (titre, catégorie, description)
- Propriétés pédagogiques (durée, compétences, saisonnalité)
- Sécurité et matériel
- Disponibilité et restrictions

## 🧪 Tests

```bash
# Lancer les tests
pytest

# Avec couverture
pytest --cov=app tests/
```

## 🚀 Déploiement

### Variables d'environnement de production

```bash
PROJECT_NAME="LaVidaLuca Backend API"
DATABASE_URL="postgresql://user:password@host:port/database"
SECRET_KEY="your-secret-key-very-long-and-random"
ALLOWED_ORIGINS="https://your-frontend-domain.vercel.app"
```

### Render

1. Connecter le repository GitHub
2. Configurer les variables d'environnement
3. Déployer automatiquement

### Migration de base de données

```bash
# Créer une nouvelle migration
alembic revision --autogenerate -m "Description des changements"

# Appliquer les migrations
alembic upgrade head
```

## 📞 Support

Pour toute question ou problème, créer une issue sur le repository GitHub.