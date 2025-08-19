# La Vida Luca - Application Web

Plateforme interactive pour le projet La Vida Luca : formation des jeunes en MFR, développement d'une agriculture nouvelle et insertion sociale.

## 🎯 Vision

- Former et accompagner les jeunes en MFR via un catalogue de 30 activités agricoles, artisanales et environnementales
- Développer une agriculture nouvelle : durable, autonome, innovante
- Favoriser l'insertion sociale par la pratique et la responsabilité
- Créer un outil numérique qui connecte les lieux d'action et les participants

## 📁 Structure du Projet

```
src/
├── app/                    # Pages Next.js (App Router)
│   ├── layout.tsx         # Layout principal
│   ├── page.tsx           # Page d'accueil
│   ├── contact/           # Page de contact
│   ├── catalogue/         # Catalogue des activités
│   └── api/               # API routes
├── components/            # Composants réutilisables
│   ├── Header.tsx         # En-tête de navigation
│   └── __tests__/         # Tests des composants
├── utils/                 # Utilitaires et helpers
│   ├── activities.ts      # Données des activités
│   ├── matching.ts        # Algorithme de matching IA
│   ├── formatters.ts      # Fonctions de formatage
│   └── __tests__/         # Tests des utilitaires
└── types/                 # Types TypeScript
    └── index.ts           # Types partagés
```

## 🚀 Installation

```bash
# Installer les dépendances
npm install

# Démarrer en mode développement
npm run dev

# Construire pour la production
npm run build

# Démarrer en mode production
npm start
```

## 🧪 Tests

```bash
# Lancer tous les tests
npm test

# Tests en mode watch
npm run test:watch

# Tests avec coverage
npm run test:coverage
```

## 🎨 Code Quality

```bash
# Linter le code
npm run lint

# Corriger automatiquement les erreurs de lint
npm run lint:fix

# Formater le code avec Prettier
npm run format

# Vérifier le formatage
npm run format:check
```

## 🛠️ Technologies

- **Framework**: Next.js 15+ (App Router)
- **Langage**: TypeScript
- **Styling**: Tailwind CSS
- **Tests**: Jest + React Testing Library
- **Linting**: ESLint + Prettier
- **Icons**: Heroicons

## 📦 Dépendances Principales

### Production

- `next`: Framework React
- `react` / `react-dom`: Librairie React
- `@heroicons/react`: Icônes

### Développement

- `typescript`: Support TypeScript
- `eslint` / `prettier`: Linting et formatage
- `jest` / `@testing-library/*`: Tests
- `tailwindcss`: Framework CSS

## 🔧 Configuration

### ESLint + Prettier

- Configuration stricte Next.js
- Intégration Prettier pour le formatage automatique
- Règles personnalisées pour le projet

### Jest

- Configuration Next.js intégrée
- Support TypeScript
- Coverage reporting configuré

### TypeScript

- Configuration stricte
- Path mapping (`@/*` → `src/*`)
- Support Next.js App Router

## 📊 Catalogue des Activités

Le projet inclut 30 activités organisées en 5 catégories :

1. **Agriculture** (6 activités) - Élevage, cultures, soins aux animaux
2. **Transformation** (6 activités) - Fromage, conserves, pain...
3. **Artisanat** (6 activités) - Menuiserie, construction, réparation
4. **Environnement** (6 activités) - Plantation, compostage, écologie
5. **Animation** (6 activités) - Accueil, visites, ateliers enfants

Chaque activité comprend :

- Description et objectifs
- Durée et niveau de sécurité
- Compétences développées
- Matériel nécessaire
- Saisonnalité

## 🤖 IA de Matching

Algorithme de recommandation personnalisée basé sur :

- Compétences actuelles de l'utilisateur
- Préférences de catégories d'activités
- Disponibilités temporelles
- Niveau de sécurité adapté
- Localisation géographique

## 🚀 Déploiement

Le projet est configuré pour un déploiement statique :

```bash
# Build de production
npm run build

# Les fichiers statiques sont générés dans /out
```

Configuration pour Vercel/Netlify :

- Export statique activé
- Optimisations d'images désactivées
- Trailing slashes configurés

## 🛡️ Règles & Pacte

- Pas de vente directe sur la plateforme
- Focus sur la mission éducative et sociale
- Respect de l'éthique "le cœur avant l'argent"
- Design orienté impact et humanité

## 📋 Scripts Disponibles

- `npm run dev` - Développement local
- `npm run build` - Build de production
- `npm run start` - Serveur de production
- `npm run lint` - Vérification du code
- `npm run lint:fix` - Correction automatique
- `npm run format` - Formatage Prettier
- `npm run format:check` - Vérification formatage
- `npm test` - Tests unitaires
- `npm run test:watch` - Tests en mode watch
- `npm run test:coverage` - Tests avec coverage

## 🤝 Contribution

1. Respecter les conventions de code (ESLint + Prettier)
2. Écrire des tests pour les nouvelles fonctionnalités
3. Maintenir la couverture de tests > 80%
4. Suivre l'architecture établie (composants, utils, types)
5. Documenter les changements importants

## 📄 License

Projet dédié à la formation et à l'insertion sociale des jeunes en MFR.
