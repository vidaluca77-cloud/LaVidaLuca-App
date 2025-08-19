# API IA - La Vida Luca

API FastAPI pour l'intelligence artificielle de matching d'activités pédagogiques.

## 🚀 Déploiement

Cette API est configurée pour être déployée automatiquement sur Render via le fichier `render.yaml` à la racine du projet.

## 📋 Fonctionnalités

- **Matching d'activités** : Suggestions personnalisées basées sur le profil utilisateur
- **Assistant conversationnel** : Aide contextuelle pour les activités
- **Health checks** : Surveillance de l'état du service

## 🛠 Développement local

```bash
# Installer les dépendances
pip install -r requirements.txt

# Copier le fichier d'environnement
cp .env.example .env

# Remplir les variables dans .env

# Lancer le serveur
python main.py
```

L'API sera accessible sur `http://localhost:8000`

## 📚 Documentation

- API docs: `/docs`
- Health check: `/health`
- Suggestions: `POST /api/suggestions`
- Chat assistant: `POST /api/chat`

## 🔧 Variables d'environnement

Voir `.env.example` pour la liste complète des variables nécessaires.