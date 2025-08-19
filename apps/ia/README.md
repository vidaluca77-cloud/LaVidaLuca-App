# La Vida Luca - API Backend

API FastAPI pour les recommandations d'activités La Vida Luca.

## 🚀 Fonctionnalités

- **Authentification JWT** - Système d'authentification sécurisé
- **Gestion des utilisateurs** - Inscription, connexion, profils utilisateur
- **Recommandations IA** - Suggestions d'activités personnalisées
- **Intégration OpenAI** - Explications intelligentes des recommandations
- **Base de données** - Modèles SQLAlchemy pour données persistantes
- **Tests complets** - Suite de tests unitaires et d'intégration
- **Documentation API** - Documentation Swagger/OpenAPI automatique

## 📦 Installation

### Prérequis

- Python 3.8+
- pip ou poetry
- Base de données PostgreSQL (ou SQLite pour le développement)

### Configuration

1. **Cloner le repository**
```bash
cd apps/ia
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configuration des variables d'environnement**
```bash
cp .env.example .env
# Editer .env avec vos paramètres
```

4. **Initialiser la base de données**
```bash
python -m app.init_db
```

## 🏃‍♂️ Utilisation

### Développement

```bash
# Démarrer le serveur de développement
python run.py

# Ou avec uvicorn directement
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera disponible sur : http://localhost:8000

- **Documentation API** : http://localhost:8000/docs
- **API Alternative** : http://localhost:8000/redoc
- **Health Check** : http://localhost:8000/health

### Production

```bash
# Avec gunicorn (recommandé)
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Ou avec uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Tests avec couverture
pytest --cov=app

# Tests spécifiques
pytest app/tests/test_auth.py
pytest app/tests/test_recommendations.py
```

## 📚 API Endpoints

### Authentification
- `POST /api/v1/auth/register` - Inscription
- `POST /api/v1/auth/login` - Connexion

### Utilisateurs
- `GET /api/v1/users/me` - Profil utilisateur
- `PUT /api/v1/users/me` - Mise à jour profil
- `POST /api/v1/users/me/profile` - Créer profil détaillé
- `PUT /api/v1/users/me/profile` - Modifier profil détaillé

### Activités et Recommandations
- `GET /api/v1/activities/activities` - Liste des activités
- `GET /api/v1/activities/activities/{id}` - Détails d'une activité
- `POST /api/v1/activities/recommendations` - Recommandations (anonyme)
- `POST /api/v1/activities/recommendations/me` - Mes recommandations

## 🎯 Architecture

```
apps/ia/
├── app/
│   ├── api/              # Endpoints API
│   │   ├── auth.py       # Authentification
│   │   ├── users.py      # Gestion utilisateurs
│   │   └── activities.py # Activités et recommandations
│   ├── core/             # Configuration centrale
│   │   ├── config.py     # Paramètres
│   │   ├── database.py   # Base de données
│   │   ├── security.py   # Sécurité JWT
│   │   └── deps.py       # Dépendances
│   ├── models/           # Modèles SQLAlchemy
│   │   └── models.py     # User, Activity, etc.
│   ├── schemas/          # Schémas Pydantic
│   │   └── schemas.py    # Validation API
│   ├── services/         # Logique métier
│   │   ├── recommendation_service.py
│   │   └── openai_service.py
│   ├── tests/            # Tests unitaires
│   └── main.py           # Application FastAPI
├── requirements.txt      # Dépendances
├── .env.example         # Variables d'environnement
└── run.py               # Point d'entrée
```

## 🔧 Configuration

### Variables d'environnement

```env
# Base de données
DATABASE_URL=postgresql://user:pass@localhost/lavidaluca

# JWT
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-3.5-turbo

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://la-vida-luca.vercel.app
```

## 🤖 Intelligence Artificielle

L'API intègre OpenAI pour générer des explications personnalisées des recommandations d'activités. Le système :

1. **Analyse le profil utilisateur** (compétences, préférences, expérience)
2. **Calcule des scores de correspondance** avec chaque activité
3. **Génère des explications IA** contextualisées
4. **Retourne des recommandations classées** avec justifications

### Algorithme de recommandation

- **Compétences correspondantes** (+20 points par compétence)
- **Préférences de catégorie** (+25 points)
- **Niveau d'expérience** (+5-15 points selon adaptation)
- **Durée adaptée** (+10 points si < 2h)
- **Niveau de sécurité** (+10 points si sécurisé)
- **Disponibilités** (+15 points si compatible)

## 🚀 Déploiement

### Render (recommandé)

1. Connecter le repository GitHub
2. Configurer les variables d'environnement
3. Utiliser le Dockerfile ou build command :
   ```bash
   pip install -r requirements.txt && python -m app.init_db
   ```
4. Start command :
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

### Docker

```bash
# Build
docker build -t lavidaluca-api .

# Run
docker run -p 8000:8000 --env-file .env lavidaluca-api
```

## 📄 Licence

Projet La Vida Luca - Tous droits réservés.