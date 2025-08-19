# LaVidaLuca FastAPI Backend

API backend pour le projet La Vida Luca - Formation des jeunes en MFR.

## 🚀 Fonctionnalités Implémentées

### ✅ Core Features
- ✅ **Base de données** : Configuration PostgreSQL/SQLite avec SQLAlchemy
- ✅ **Authentification** : Système JWT complet avec inscription/connexion
- ✅ **Intégration OpenAI** : Recommandations IA personnalisées
- ✅ **API Routes** : Endpoints pour activités, utilisateurs et recommandations
- ✅ **Gestion d'erreurs** : Middleware complet et gestion d'exceptions
- ✅ **Sécurité** : CORS, validation des données, protection JWT

### ✅ Main Components
- ✅ **Modèles de données** : User, Activity, UserActivity, Recommendation
- ✅ **Endpoints API** : 20+ endpoints REST documentés
- ✅ **Middleware de sécurité** : CORS, logging, timing
- ✅ **Configuration d'environnement** : Gestion centralisée des variables
- ✅ **Structure de tests** : Tests automatisés avec pytest

### ✅ Backend Support
- ✅ **Authentification et autorisation** : JWT complet
- ✅ **Gestion d'activités** : CRUD complet pour 31 activités
- ✅ **Recommandations IA** : Algorithme basique + OpenAI
- ✅ **Intégration frontend** : Helper TypeScript fourni

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

## Intégration Frontend

Un helper TypeScript est fourni dans `frontend-integration.ts` pour faciliter l'intégration avec Next.js :

```typescript
import { api, UserProfile } from './api/lavidaluca';

// Obtenir des activités
const activities = await api.getActivities();

// Obtenir des recommandations
const userProfile: UserProfile = {
  skills: ['agriculture', 'elevage'],
  availability: ['weekend'],
  location: 'France',
  preferences: ['agri']
};

const suggestions = await api.getRecommendations(userProfile, 5);
```

## Tests

Le backend inclut une suite de tests couvrant :
- ✅ Endpoints d'authentification
- ✅ CRUD des activités
- ✅ Système de recommandations
- ✅ Validation des données
- ✅ Gestion d'erreurs

Tous les tests passent avec succès (6/6).

## Données de Test

31 activités sont pré-configurées et seedées automatiquement :
- **Agriculture** : 6 activités (moutons, chèvres, légumes, etc.)
- **Transformation** : 6 activités (fromage, conserves, pain, etc.)
- **Artisanat** : 7 activités (menuiserie, réparation, poterie, etc.)
- **Nature** : 6 activités (cueillette, plantation, observation, etc.)
- **Social** : 6 activités (accueil, animation, marché, etc.)

## Déploiement

Le backend est conçu pour être déployé sur **Render** avec PostgreSQL.

Configuration Render :
- Service : Web Service
- Build Command : `pip install -r requirements.txt`
- Start Command : `python main.py`
- Environment Variables : Configurer selon .env.example

## Structure du Projet

```
apps/ia/
├── auth/                 # Système d'authentification
│   └── security.py      # JWT, hashing, validation
├── database/            # Configuration base de données
│   ├── __init__.py      # Session et connexion
│   └── models.py        # Modèles SQLAlchemy
├── routers/             # Endpoints API
│   ├── auth.py         # Routes d'authentification
│   ├── users.py        # Routes utilisateurs
│   ├── activities.py   # Routes activités
│   └── recommendations.py # Routes recommandations
├── schemas/             # Schémas Pydantic
│   ├── user.py         # Schémas utilisateur
│   ├── activity.py     # Schémas activité
│   ├── recommendation.py # Schémas recommandation
│   └── auth.py         # Schémas authentification
├── services/            # Services métier
│   └── recommendation.py # Service IA/recommandations
├── tests/               # Tests automatisés
│   └── test_main.py    # Tests principaux
├── main.py             # Application FastAPI principale
├── config.py           # Configuration centralisée
├── seed_data.py        # Script de seeding
├── requirements.txt    # Dépendances Python
├── .env.example        # Template variables d'environnement
├── render.yaml         # Configuration déploiement
└── README.md           # Documentation
```

## Status de Développement

🟢 **Terminé** : Backend FastAPI complet et fonctionnel
- Toutes les fonctionnalités core implémentées
- Tests passants
- Documentation complète
- Prêt pour intégration frontend et déploiement