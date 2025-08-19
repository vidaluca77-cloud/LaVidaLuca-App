# LaVidaLuca-App

Plateforme interactive pour le projet La Vida Luca : formation des jeunes en MFR, développement d'une agriculture nouvelle et insertion sociale.

## 🎯 Vision

- **Former et accompagner** les jeunes en MFR via un catalogue de 30 activités agricoles, artisanales et environnementales
- **Développer une agriculture nouvelle** : durable, autonome, innovante
- **Favoriser l'insertion sociale** par la pratique et la responsabilité
- **Créer un outil numérique** qui connecte les lieux d'action et les participants

## 🏗️ Architecture

```
/
├── apps/
│   ├── backend/              # API FastAPI
│   │   ├── src/
│   │   │   ├── api/         # Routes API
│   │   │   ├── auth/        # Authentification JWT
│   │   │   ├── db/          # Modèles et base de données
│   │   │   └── services/    # Services (IA, recommandations)
│   │   ├── tests/           # Tests unitaires
│   │   └── Dockerfile
│   └── frontend/            # Application Next.js
│       ├── src/
│       │   ├── app/         # Pages (App Router)
│       │   ├── components/  # Composants réutilisables
│       │   ├── hooks/       # Hooks React
│       │   └── utils/       # Utilitaires et types
│       ├── tests/           # Tests frontend
│       └── Dockerfile
├── infra/                   # Infrastructure
│   ├── supabase/           # Schéma et données PostgreSQL
│   └── docker-compose.yml  # Configuration Docker
├── scripts/                 # Scripts de déploiement
└── .github/workflows/       # CI/CD GitHub Actions
```

## 🚀 Technologies

### Backend
- **FastAPI** - API moderne et performante
- **SQLAlchemy** - ORM pour PostgreSQL
- **JWT** - Authentification sécurisée
- **OpenAI** - IA pour recommandations personnalisées
- **PostgreSQL** - Base de données robuste

### Frontend
- **Next.js 14** - Framework React moderne
- **Tailwind CSS** - Design system responsive
- **React Context** - Gestion d'état globale
- **TypeScript** - Typage statique

### Infrastructure
- **Docker** - Containerisation
- **Supabase** - Base de données PostgreSQL hébergée
- **Vercel** - Déploiement frontend
- **Render** - Déploiement backend

## 🛠️ Développement Local

### Prérequis
- Docker et Docker Compose
- Node.js 18+ (pour le frontend)
- Python 3.11+ (pour le backend)

### Installation Rapide

```bash
# Cloner le repository
git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
cd LaVidaLuca-App

# Configuration automatique
./scripts/setup-dev.sh

# Démarrer tous les services
cd infra
docker-compose up
```

### Services Disponibles
- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs
- **Base de données** : localhost:5432

### Développement Manuel

#### Backend
```bash
cd apps/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend
```bash
cd apps/frontend
npm install
npm run dev
```

## 📋 Catalogue des 30 Activités MFR

### Agriculture (6 activités)
- Nourrir et soigner les moutons
- Tonte & entretien du troupeau
- Soins basse-cour
- Plantation de cultures
- Initiation maraîchage
- Gestion des clôtures & abris

### Transformation (6 activités)
- Fabrication de fromage
- Confitures & conserves
- Transformation de la laine
- Fabrication de jus
- Séchage d'herbes aromatiques
- Pain au four à bois

### Artisanat (6 activités)
- Poterie (terre locale)
- Tissage simple
- Vannerie
- Fabrication de savon
- Menuiserie simple
- Teinture naturelle

### Nature (6 activités)
- Reconnaissance des plantes
- Compost & permaculture
- Apiculture (découverte)
- Gestion de l'eau
- Graines & semences
- Gestion forestière

### Social (6 activités)
- Accueil de visiteurs
- Pédagogie avec les enfants
- Organisation d'un événement
- Cuisine collective
- Goûter fermier
- Participation à un marché local

## 🔑 Variables d'Environnement

### Backend
```env
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key-for-jwt
OPENAI_API_KEY=sk-your-openai-api-key
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Frontend
```env
NEXT_PUBLIC_IA_API_URL=https://your-backend-api.com
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789
```

## 🚀 Déploiement

### Production
1. **Frontend** → Vercel
2. **Backend** → Render
3. **Base de données** → Supabase

### Script de déploiement
```bash
./scripts/deploy.sh
```

## 🧪 Tests

### Backend
```bash
cd apps/backend
pytest tests/ -v
```

### Frontend
```bash
cd apps/frontend
npm run test
```

## 📚 API Documentation

L'API REST est documentée automatiquement avec FastAPI :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

### Endpoints principaux
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion
- `GET /api/activities/` - Liste des activités
- `GET /api/activities/recommendations/{user_id}` - Recommandations IA
- `GET /api/users/me` - Profil utilisateur

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajoute nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 🛡️ Règles & Pacte

- **Pas de vente directe** sur la plateforme
- **Respect du pacte initial** du projet La Vida Luca
- **Bienveillance** et entraide entre participants
- **Valorisation** des savoir-faire traditionnels
- **Développement durable** et éco-responsabilité

## 📄 License

Ce projet est sous licence [MIT](LICENSE).

---

**La Vida Luca** - *Cultiver l'avenir ensemble* 🌱