# La Vida Luca API

## FastAPI Backend pour le projet La Vida Luca

API RESTful pour la gestion des utilisateurs, activités et candidatures du projet La Vida Luca.

### Installation

1. **Créer un environnement virtuel**
```bash
cd apps/ia
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configuration**
Copier `.env.example` vers `.env` et configurer les variables :
```bash
cp .env.example .env
```

4. **Base de données**
```bash
# Initialiser Alembic
alembic init alembic

# Créer et appliquer les migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Peupler avec des données d'exemple
python create_sample_data.py
```

### Lancement

```bash
# Mode développement
uvicorn app.main:app --reload

# Mode production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Tests

```bash
pytest app/tests/
```

### Documentation API

Une fois l'application lancée :
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

### Structure

```
apps/ia/
├── app/
│   ├── api/routes/          # Routes API
│   │   ├── auth.py          # Authentification
│   │   ├── users.py         # Gestion utilisateurs
│   │   ├── activities.py    # Catalogue d'activités
│   │   └── applications.py  # Candidatures
│   ├── core/               # Configuration centrale
│   │   ├── config.py       # Paramètres
│   │   ├── database.py     # Base de données
│   │   └── security.py     # JWT & sécurité
│   ├── crud/              # Opérations base de données
│   ├── models/            # Modèles SQLAlchemy
│   ├── schemas/           # Schémas Pydantic
│   ├── tests/            # Tests unitaires
│   └── main.py           # Application FastAPI
├── alembic/              # Migrations base de données
├── requirements.txt      # Dépendances Python
├── Dockerfile           # Container Docker
└── .env.example        # Variables d'environnement
```

### Endpoints principaux

#### Authentification
- `POST /auth/register` - Inscription
- `POST /auth/login` - Connexion
- `POST /auth/token` - Token OAuth2
- `GET /auth/me` - Profil utilisateur

#### Utilisateurs
- `GET /api/users/` - Liste des utilisateurs
- `GET /api/users/{id}` - Détails utilisateur
- `PUT /api/users/{id}` - Mise à jour

#### Activités
- `GET /api/activities/` - Catalogue d'activités
- `GET /api/activities/{id}` - Détails activité
- `POST /api/activities/` - Créer activité (admin)
- `PUT /api/activities/{id}` - Modifier (admin)

#### Candidatures
- `GET /api/applications/` - Liste candidatures
- `GET /api/applications/me` - Mes candidatures
- `POST /api/applications/` - Nouvelle candidature
- `PUT /api/applications/{id}` - Mettre à jour

### Variables d'environnement

```bash
# Base de données
DATABASE_URL=postgresql://username:password@localhost/lavidaluca

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.vercel.app

# Application
DEBUG=True
```