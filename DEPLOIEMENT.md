# Instructions de déploiement - La Vida Luca

Ce fichier contient toutes les configurations nécessaires pour déployer immédiatement l'application La Vida Luca sur Vercel, Render et Supabase.

## 📁 Fichiers de configuration créés

### 1. Vercel (Frontend Next.js)
- **Fichier:** `vercel.json`
- **Description:** Configuration complète pour le déploiement du site web Next.js
- **Inclut:** Variables d'environnement, headers de sécurité, redirections

### 2. Render (API IA FastAPI) 
- **Fichier:** `render.yaml`
- **Description:** Configuration pour déployer l'API IA sur Render
- **Inclut:** Configuration Python, variables d'environnement, health checks

### 3. Supabase (Base de données)
- **Fichiers:** 
  - `infra/supabase/schema.sql` - Schéma de base de données complet
  - `infra/supabase/seeds.sql` - Données initiales
- **Inclut:** Tables, policies RLS, triggers, données de test

## 🚀 Déploiement étape par étape

### Étape 1: Supabase (Base de données)

1. Créer un projet sur [supabase.com](https://supabase.com)
2. Dans l'éditeur SQL, exécuter dans l'ordre :
   ```sql
   -- 1. Copier/coller le contenu de infra/supabase/schema.sql
   -- 2. Copier/coller le contenu de infra/supabase/seeds.sql
   ```
3. Noter les informations du projet :
   - URL du projet Supabase
   - Clé publique anonyme (anon key)

### Étape 2: Render (API IA)

1. Créer un compte sur [render.com](https://render.com)
2. Connecter votre repository GitHub
3. Créer un nouveau service Web en utilisant `render.yaml`
4. Configurer les variables d'environnement :
   ```
   SUPABASE_URL=https://votre-projet.supabase.co
   SUPABASE_KEY=votre_clé_supabase
   ALLOWED_ORIGINS=https://votre-app.vercel.app
   ```
5. Noter l'URL de déploiement Render (ex: `https://votre-app.onrender.com`)

### Étape 3: Vercel (Frontend)

1. Créer un compte sur [vercel.com](https://vercel.com)
2. Connecter votre repository GitHub
3. Déployer le projet (Vercel détectera automatiquement `vercel.json`)
4. Configurer les variables d'environnement dans le dashboard Vercel :
   ```
   NEXT_PUBLIC_SUPABASE_URL=https://votre-projet.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=votre_clé_anonyme_supabase
   NEXT_PUBLIC_IA_API_URL=https://votre-app.onrender.com
   NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
   NEXT_PUBLIC_CONTACT_PHONE=+33.XX.XX.XX.XX
   ```

## 🔧 Configuration supplémentaire

### Authentification Supabase
- Configurer les URLs de redirection dans Supabase :
  - `https://votre-app.vercel.app/**`
- Activer les providers d'authentification souhaités

### API IA (Optionnel)
Pour créer l'API IA mentionnée dans `render.yaml`, créer un projet FastAPI avec :

```python
# main.py exemple
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://votre-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/suggestions")
def get_activity_suggestions(profile: dict):
    # Logique IA pour suggérer des activités
    return {"suggestions": []}
```

Avec `requirements.txt` :
```
fastapi==0.104.1
uvicorn==0.24.0
supabase==2.0.0
```

## 📋 Checklist de déploiement

- [ ] **Supabase configuré**
  - [ ] Projet créé
  - [ ] schema.sql exécuté
  - [ ] seeds.sql exécuté
  - [ ] Variables notées (URL + clé)

- [ ] **Render configuré** (si API IA)
  - [ ] Service créé
  - [ ] Variables d'environnement configurées
  - [ ] Déploiement réussi
  - [ ] Health check OK

- [ ] **Vercel configuré**
  - [ ] Projet connecté
  - [ ] Variables d'environnement configurées
  - [ ] Build successful
  - [ ] Site accessible

- [ ] **Tests finaux**
  - [ ] Pages du site accessibles
  - [ ] Catalogue fonctionnel
  - [ ] Formulaires opérationnels
  - [ ] Connexion base de données OK

## 🔍 Résolution de problèmes

### Erreur de build Next.js
- Vérifier que toutes les variables d'environnement sont configurées
- S'assurer que les chemins dans `vercel.json` sont corrects

### Erreur de connexion Supabase
- Vérifier l'URL et la clé dans les variables d'environnement
- S'assurer que les policies RLS permettent les opérations nécessaires

### Erreur CORS
- Vérifier que `ALLOWED_ORIGINS` dans Render contient l'URL Vercel
- Configurer les CORS dans FastAPI si API personnalisée

## 📞 Support

Pour toute question sur le déploiement, consulter :
- [Documentation Vercel](https://vercel.com/docs)
- [Documentation Render](https://render.com/docs)
- [Documentation Supabase](https://supabase.com/docs)