# LaVidaLuca-App

Plateforme interactive pour le projet La Vida Luca : formation des jeunes en MFR, développement d'une agriculture nouvelle et insertion sociale.

## 📦 Structure du projet

```
LaVidaLuca-App/
├── apps/
│   ├── web/                    # Frontend Next.js (Vercel)
│   │   ├── src/
│   │   │   ├── app/           # Pages et routes App Router
│   │   │   └── types/         # Types TypeScript
│   │   ├── public/            # Assets statiques
│   │   └── package.json
│   └── ia/                     # Backend FastAPI (Render)
│       ├── app/
│       │   ├── models/        # Modèles SQLAlchemy
│       │   ├── schemas/       # Schémas Pydantic
│       │   ├── routes/        # Routes API
│       │   └── core/          # Configuration
│       ├── alembic/           # Migrations de base de données
│       ├── tests/             # Tests unitaires
│       ├── main.py            # Point d'entrée FastAPI
│       └── requirements.txt
├── infra/
│   ├── supabase/              # Configuration base de données
│   │   ├── schema.sql         # Schéma de base de données
│   │   └── seeds.sql          # Données initiales
│   ├── deploy/                # Scripts de déploiement
│   │   └── deploy.sh          # Script de déploiement principal
│   └── monitoring/            # Configuration monitoring
│       ├── health-check.sh    # Script de vérification santé
│       └── README.md
├── assets/                    # Médias (logos, visuels, documents)
├── .github/workflows/         # CI/CD GitHub Actions
└── README.md                  # Documentation principale
```

## 🚀 Déploiement

### Prérequis
- Node.js 18+
- Python 3.11+
- Base de données PostgreSQL (Supabase recommandé)

### Installation

1. **Cloner le repository**
   ```bash
   git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
   cd LaVidaLuca-App
   ```

2. **Frontend (Next.js)**
   ```bash
   cd apps/web
   npm install
   npm run dev
   ```

3. **Backend (FastAPI)**
   ```bash
   cd apps/ia
   python -m venv .venv
   source .venv/bin/activate  # ou .venv\Scripts\activate sur Windows
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

4. **Base de données**
   - Créer un projet Supabase
   - Exécuter `infra/supabase/schema.sql`
   - Exécuter `infra/supabase/seeds.sql`

### Déploiement automatisé

```bash
./infra/deploy/deploy.sh
```

### Variables d'environnement

**Frontend (apps/web/.env.local)**
```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_IA_API_URL=your_render_api_url
NEXT_PUBLIC_CONTACT_EMAIL=vidaluca77@gmail.com
NEXT_PUBLIC_CONTACT_PHONE=@lavidaluca77
```

**Backend (apps/ia/.env)**
```env
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
ENVIRONMENT=production
```

## 🧪 Tests

**Frontend**
```bash
cd apps/web
npm test
```

**Backend**
```bash
cd apps/ia
python -m pytest tests/ -v
```

## 📊 Monitoring

Le système inclut un monitoring automatique :

```bash
./infra/monitoring/health-check.sh
```

Pour un monitoring continu, ajouter à crontab :
```bash
*/5 * * * * /path/to/infra/monitoring/health-check.sh
```

## 🎯 Fonctionnalités

### Frontend (Next.js)
- ✅ Page d'accueil avec présentation du projet
- ✅ Catalogue d'activités MFR interactif
- ✅ Système de contact et candidature
- ✅ Design responsive et accessible
- ✅ Types TypeScript complets
- ✅ Tests unitaires

### Backend (FastAPI)
- ✅ API REST complète
- ✅ Système de matching IA pour activités
- ✅ Modèles de données structurés
- ✅ Migrations Alembic
- ✅ Tests unitaires
- ✅ Documentation API automatique

### Infrastructure
- ✅ Configuration CI/CD GitHub Actions
- ✅ Scripts de déploiement automatisés
- ✅ Monitoring et health checks
- ✅ Configuration Supabase
- ✅ Security scanning

## 🏗️ Architecture

- **Frontend** : Next.js 14 avec App Router, TypeScript, Tailwind CSS
- **Backend** : FastAPI avec SQLAlchemy, Alembic, PostgreSQL
- **Base de données** : Supabase (PostgreSQL)
- **Déploiement** : Vercel (frontend) + Render (backend)
- **Monitoring** : Scripts personnalisés + intégrations natives

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add: AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Documentation API

Une fois le backend démarré, la documentation API est disponible à :
- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`

## 🛡️ Sécurité

- Scan automatique de vulnérabilités avec Trivy
- Variables d'environnement sécurisées
- CORS configuré
- Validation des données avec Pydantic

## 📞 Contact

- **Email** : vidaluca77@gmail.com
- **Snapchat** : @lavidaluca77

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.