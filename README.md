# LaVidaLuca-App

Plateforme interactive pour le projet La Vida Luca : formation des jeunes en MFR, développement d'une agriculture nouvelle et insertion sociale.

La Vida Luca – Application IA interactive

Plateforme collaborative basée sur IA pour le projet La Vida Luca, dédiée à la formation des jeunes en MFR, au développement d'une agriculture nouvelle et à l'insertion sociale.
Objectif : permettre à chacun de contribuer à sa manière au projet, dans le respect du pacte initial.

⸻

## 🎯 Vision

- Former et accompagner les jeunes en MFR via un catalogue de 30 activités agricoles, artisanales et environnementales.
- Développer une agriculture nouvelle : durable, autonome, innovante.
- Favoriser l'insertion sociale par la pratique et la responsabilité.
- Créer un outil numérique qui connecte les lieux d'action et les participants.

⸻

## 📦 Structure du projet

- `/src` → Frontend Next.js (Vercel)
- `/apps/ia` → API FastAPI pour l'IA (Render)
- `/infra/supabase` → Base de données et schéma SQL
- `/docs` → Documentation complète
- `/.github/workflows` → CI/CD pipelines
- `/assets` → Médias (logos, visuels, documents)

⸻

## 🚀 Déploiement

1. **Vercel** – héberge le site web (Next.js)
2. **Render** – héberge l'IA et l'API
3. **Supabase** – base de données et authentification

## Environnements

- **Production**: https://la-vida-luca.vercel.app
- **Staging**: https://la-vida-luca-staging.vercel.app
- **Backend Production**: https://la-vida-luca-ia.onrender.com
- **Backend Staging**: https://la-vida-luca-ia-staging.onrender.com

⸻

## 🔑 Variables d'environnement

Principales variables à configurer :

```env
NEXT_PUBLIC_SUPABASE_URL=your-supabase-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
NEXT_PUBLIC_IA_API_URL=your-backend-api-url
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789
```

Pour plus de détails, voir [docs/ENVIRONMENT_VARIABLES.md](docs/ENVIRONMENT_VARIABLES.md)

⸻

## 🛠️ Installation et développement

### Prérequis
- Node.js 18+
- Python 3.11+
- Poetry
- Docker (optionnel)

### Configuration rapide

```bash
# Cloner le repository
git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
cd LaVidaLuca-App

# Configuration frontend
npm install
cp .env.example .env.local
# Éditer .env.local avec vos valeurs

# Configuration backend
cd apps/ia
poetry install
cp .env.example .env
# Éditer .env avec vos valeurs

# Démarrer en développement
npm run dev  # Frontend sur :3000
cd apps/ia && poetry run uvicorn main:app --reload  # Backend sur :8000
```

### Développement avec Docker

```bash
# Démarrer tous les services
docker-compose up -d

# Arrêter les services
docker-compose down
```

⸻

## 📋 CI/CD Pipeline

### GitHub Actions Workflows

- **Frontend CI/CD**: Tests, build, déploiement automatique
- **Backend CI/CD**: Tests, Docker build, déploiement
- **Database Operations**: Migrations, backups, restore
- **Monitoring**: Health checks, performance, sécurité

### Processus de déploiement

1. **Développement**: Feature branches → PR vers `develop`
2. **Staging**: Merge vers `develop` → Déploiement auto staging
3. **Production**: Merge `develop` → `main` → Déploiement auto production

### Health Checks

- Frontend: `/api/health`
- Backend: `/health`
- Metrics: `/api/metrics`

⸻

## 📊 Monitoring et sécurité

### Monitoring
- Health checks automatiques (toutes les 5 minutes)
- Performance monitoring (Lighthouse CI)
- Error tracking (Sentry)
- Uptime monitoring

### Sécurité
- Vulnerability scanning (Snyk, Trivy)
- Automated dependency updates (Dependabot)
- Security headers (CSP, HSTS, etc.)
- Database RLS policies
- Container security best practices

### Backups
- Database backups quotidiens
- Retention 30 jours
- Stockage chiffré S3
- Tests de restore mensuels

⸻

## 📋 Catalogue des 30 activités MFR

Activités organisées par catégories :

### Agriculture (6 activités)
- Soins aux animaux
- Préparation des sols  
- Semis en potager
- Plantation de cultures
- Initiation maraîchage
- Gestion des clôtures & abris

### Transformation (6 activités)
- Fabrication de fromage
- Confitures & conserves
- Transformation de la laine
- Fabrication de jus
- Séchage d'herbes aromatiques
- Pain traditionnel

### Artisanat (6 activités)
- Menuiserie simple
- Poterie & terre cuite
- Réparation d'outils
- Peinture & décoration d'espaces
- Aménagement d'espaces verts
- Panneaux & orientation

### Nature (6 activités)
- Entretien de la rivière
- Création de sentiers
- Plantation d'arbres
- Compostage
- Observation de la faune locale
- Création d'une mare

### Social (6 activités)
- Accueil de visiteurs
- Organisation d'événements
- Cuisine collective
- Goûter fermier
- Nettoyage collectif d'espaces
- Communication sur les réseaux

Pour la liste complète avec détails, voir le catalogue intégré dans l'application.

⸻

## 📚 Documentation

Documentation complète disponible dans `/docs` :

- [Setup Instructions](docs/SETUP.md) - Installation et configuration
- [CI/CD Documentation](docs/CICD.md) - Pipeline et déploiements
- [Environment Variables](docs/ENVIRONMENT_VARIABLES.md) - Variables d'environnement
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md) - Résolution de problèmes
- [Security Policy](SECURITY.md) - Politique de sécurité

⸻

## 🛡️ Règles & Pacte

- Pas de vente directe sur la plateforme
- Respect du pacte initial du projet La Vida Luca
- Formation et insertion comme priorités
- Approche collaborative et bienveillante
- Page "Nos lieux d'action" au lieu de "Localisation"
- Section "Catalogue d'activités" réservée aux élèves MFR
- Ton et design orientés cœur et mission, pas argent

⸻

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

⸻

## 📄 License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

⸻

## 🔗 Links utiles

- **Documentation API**: https://la-vida-luca-ia.onrender.com/docs
- **Status Page**: Monitoring des services
- **Roadmap**: Issues GitHub du projet