# Guide de développement

## Table des matières

- [Configuration de l'environnement](#configuration-environnement)
- [Standards de code](#standards-de-code)
- [Architecture du code](#architecture-du-code)
- [Testing](#testing)
- [Contribution](#contribution)

## Configuration environnement

### Prérequis
- Node.js 18+
- npm 9+
- Git
- VS Code (recommandé)

### Extensions VS Code recommandées
- ES7+ React/Redux/React-Native snippets
- TypeScript Importer
- Tailwind CSS IntelliSense
- Prettier - Code formatter
- ESLint

### Configuration Git
```bash
git config user.name "Votre Nom"
git config user.email "votre@email.com"
```

## Standards de code

### TypeScript
- Utiliser TypeScript strict mode
- Définir des interfaces pour tous les objets
- Éviter `any`, préférer `unknown`
- Utiliser des types union quand approprié

### React/Next.js
- Composants fonctionnels avec hooks
- Props typées avec interfaces
- Gestion d'état avec useState/useReducer
- Server Components quand possible

### Styling
- Tailwind CSS pour le styling
- Classes utilitaires plutôt que CSS custom
- Composants réutilisables pour les patterns communs
- Dark mode support (à venir)

### Structure des fichiers
```
src/
├── app/                 # App Router (Next.js 13+)
│   ├── (routes)/       # Groupes de routes
│   ├── api/            # API routes
│   └── globals.css     # Styles globaux
├── components/         # Composants réutilisables
│   ├── ui/            # Composants UI de base
│   └── features/      # Composants métier
├── lib/               # Utilitaires et configurations
│   ├── utils.ts       # Fonctions utilitaires
│   ├── constants.ts   # Constantes
│   └── types.ts       # Types globaux
└── hooks/             # Custom hooks
```

### Naming conventions
- **Fichiers** : kebab-case (`user-profile.tsx`)
- **Composants** : PascalCase (`UserProfile`)
- **Variables** : camelCase (`userName`)
- **Constantes** : SCREAMING_SNAKE_CASE (`API_BASE_URL`)
- **Types/Interfaces** : PascalCase (`UserProfile`, `ApiResponse`)

## Architecture du code

### Composants
```tsx
// ✅ Bon exemple
interface UserProfileProps {
  user: User;
  onUpdate: (user: User) => void;
}

export function UserProfile({ user, onUpdate }: UserProfileProps) {
  const [isEditing, setIsEditing] = useState(false);
  
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      {/* Contenu */}
    </div>
  );
}
```

### API Routes
```tsx
// src/app/api/example/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

export async function GET(request: NextRequest) {
  try {
    // Logique métier
    logger.info('API call successful');
    return NextResponse.json({ data: 'success' });
  } catch (error) {
    logger.error('API error', error as Error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

### Gestion d'erreur
```tsx
// Utiliser le logger structuré
import { logger } from '@/lib/logger';

try {
  // Code risqué
} catch (error) {
  logger.error('Erreur dans le composant', error as Error, {
    component: 'UserProfile',
    userId: user.id
  });
}
```

## Testing

### Structure des tests
```
src/
├── __tests__/          # Tests unitaires
├── components/
│   └── __tests__/     # Tests des composants
└── lib/
    └── __tests__/     # Tests des utilitaires
```

### Types de tests
- **Unit tests** : Fonctions utilitaires, hooks
- **Component tests** : Rendu et interactions
- **Integration tests** : API routes
- **E2E tests** : Parcours utilisateur complets

### Exemple de test
```tsx
// components/__tests__/UserProfile.test.tsx
import { render, screen } from '@testing-library/react';
import { UserProfile } from '../UserProfile';

describe('UserProfile', () => {
  it('renders user name', () => {
    const user = { id: '1', name: 'John Doe' };
    render(<UserProfile user={user} onUpdate={() => {}} />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });
});
```

## Contribution

### Workflow Git
1. Créer une branche depuis `main`
   ```bash
   git checkout -b feature/nouvelle-fonctionnalite
   ```

2. Développer avec des commits atomiques
   ```bash
   git add .
   git commit -m "feat: ajouter authentification utilisateur"
   ```

3. Pousser et créer une Pull Request
   ```bash
   git push origin feature/nouvelle-fonctionnalite
   ```

### Messages de commit
Format : `type(scope): description`

Types :
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatting, point-virgules manquants, etc.
- `refactor`: Refactoring du code
- `test`: Ajout de tests
- `chore`: Maintenance

Exemples :
```
feat(auth): ajouter connexion Google
fix(api): corriger validation email
docs(readme): mettre à jour guide installation
```

### Pull Requests
- Titre descriptif
- Description détaillée des changements
- Tests ajoutés/mis à jour
- Screenshots pour les changements UI
- Revue de code requise

### Standards de qualité
- ✅ Tests passent
- ✅ Lint sans erreurs
- ✅ Build réussi
- ✅ Types TypeScript corrects
- ✅ Performance acceptable
- ✅ Accessibilité respectée