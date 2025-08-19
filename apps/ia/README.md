# LaVidaLuca FastAPI Backend

API backend pour le projet La Vida Luca - Formation des jeunes en MFR.

## Architecture

- **FastAPI** : Framework web moderne et rapide
- **PostgreSQL** : Base de données pour production 
- **SQLAlchemy** : ORM pour la gestion de base de données
- **JWT** : Authentification sécurisée
- **OpenAI** : Intégration IA pour les recommandations
- **Pydantic** : Validation des données

## Installation

1. Créer un environnement virtuel :
```bash
cd apps/ia
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configuration :
```bash
cp .env.example .env
# Éditer .env avec vos valeurs
```

4. Variables d'environnement requises :
- `DATABASE_URL` : URL de connexion PostgreSQL
- `SECRET_KEY` : Clé secrète pour JWT
- `OPENAI_API_KEY` : Clé API OpenAI
- `ALLOWED_ORIGINS` : Origines CORS autorisées

## Utilisation

### Développement
```bash
python main.py
```

L'API sera disponible sur http://localhost:8000

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Seeding des données
```bash
python seed_data.py
```

### Tests
```bash
pytest
```

## Documentation API

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## Endpoints principaux

### Authentification
- `POST /auth/register` : Créer un compte
- `POST /auth/login` : Se connecter
- `POST /auth/token` : Obtenir un token (OAuth2)

### Utilisateurs
- `GET /users/me` : Profil utilisateur
- `PUT /users/me` : Modifier le profil
- `GET /users/me/profile` : Profil de préférences
- `PUT /users/me/profile` : Modifier les préférences

### Activités
- `GET /activities/` : Liste des activités
- `POST /activities/` : Créer une activité
- `GET /activities/{id}` : Détail d'une activité
- `PUT /activities/{id}` : Modifier une activité
- `DELETE /activities/{id}` : Supprimer une activité
- `GET /activities/categories/list` : Catégories d'activités

### Recommandations IA
- `POST /recommendations/suggest` : Obtenir des recommandations IA
- `POST /recommendations/generate` : Générer des recommandations pour l'utilisateur connecté
- `GET /recommendations/me` : Mes recommandations sauvegardées
- `POST /recommendations/save` : Sauvegarder une recommandation

## Modèles de données

### User
- Informations personnelles
- Compétences et préférences
- Historique d'activités

### Activity
- Métadonnées de l'activité
- Compétences requises
- Niveau de sécurité
- Saisonnalité

### Recommendation
- Score de correspondance
- Raisons de la recommandation
- Générée par IA ou algorithme

## Sécurité

- Authentification JWT
- Validation des données avec Pydantic
- Middleware CORS configuré
- Protection contre les attaques communes

## Déploiement

Le backend est conçu pour être déployé sur **Render** avec PostgreSQL.

Configuration Render :
- Service : Web Service
- Build Command : `pip install -r requirements.txt`
- Start Command : `python main.py`
- Environment Variables : Configurer selon .env.example