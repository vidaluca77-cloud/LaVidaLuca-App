# Fichiers de Configuration de Déploiement

Cette configuration complète permet un déploiement immédiat de La Vida Luca sur les plateformes Vercel, Render et Supabase.

## 📁 Structure des fichiers

```
├── vercel.json                     # Configuration Vercel (Frontend)
├── render.yaml                     # Configuration Render (API IA)
├── .env.example                    # Variables d'environnement exemple
├── DEPLOY.md                       # Guide de déploiement complet
├── supabase/                       # Configuration base de données
│   ├── README.md                   # Guide Supabase
│   ├── config.json                 # Configuration projet
│   └── migrations/
│       ├── 001_initial_schema.sql  # Schéma initial
│       └── 002_seed_data.sql       # Données d'amorçage
├── apps/ia/                        # API FastAPI pour l'IA
│   ├── main.py                     # Application FastAPI
│   ├── requirements.txt            # Dépendances Python
│   └── .env.example                # Variables d'environnement API
└── scripts/
    └── validate-deployment.sh      # Script de validation
```

## 🚀 Déploiement rapide

### 1. Prérequis
- Compte Vercel ✅ (existant)
- Compte Render ✅ (existant)  
- Compte Supabase (à créer - gratuit)

### 2. Variables d'environnement requises

**Frontend (Vercel):**
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `NEXT_PUBLIC_IA_API_URL` 
- `NEXT_PUBLIC_CONTACT_EMAIL`
- `NEXT_PUBLIC_CONTACT_PHONE`

**API IA (Render):**
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_KEY`
- `ALLOWED_ORIGINS`
- `OPENAI_API_KEY`

### 3. Ordre de déploiement

1. **Supabase** : Créer le projet et exécuter les migrations SQL
2. **Render** : Déployer l'API IA avec les variables d'environnement
3. **Vercel** : Déployer le frontend avec les variables d'environnement

## ✅ Validation

Exécuter le script de validation avant le déploiement :

```bash
./scripts/validate-deployment.sh
```

## 📖 Documentation complète

Voir `DEPLOY.md` pour les instructions détaillées étape par étape.

## 🛠️ Fonctionnalités incluses

- **Configuration Vercel** : Optimisée pour Next.js avec gestion des APIs
- **Configuration Render** : Service web Python avec auto-déploiement
- **Base de données Supabase** : Schéma complet avec 30 activités MFR
- **Variables d'environnement** : Complètement documentées
- **Script de validation** : Vérification automatique de la configuration
- **Documentation** : Guide complet pour chaque plateforme