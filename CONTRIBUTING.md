# Guide de Contribution

Merci de votre intérêt pour contribuer au projet La Vida Luca ! Ce guide vous aidera à comprendre notre processus de développement et nos standards.

## 🚀 Démarrage Rapide

1. **Fork** le repository
2. **Clone** votre fork localement
3. **Installer** les dépendances : `npm install`
4. **Créer** une branche pour votre fonctionnalité : `git checkout -b feature/ma-fonctionnalite`
5. **Développer** votre fonctionnalité
6. **Tester** : `npm test`
7. **Formater** : `npm run format`
8. **Commit** et **Push**
9. **Créer** une Pull Request

## 📁 Architecture du Code

### Structure des Dossiers

```
src/
├── app/           # Pages Next.js (App Router)
├── components/    # Composants réutilisables
├── utils/         # Fonctions utilitaires
├── types/         # Types TypeScript
└── hooks/         # Custom React hooks (à venir)
```

### Conventions de Nommage

- **Composants** : PascalCase (`Header.tsx`)
- **Utilitaires** : camelCase (`formatters.ts`)
- **Types** : PascalCase (`UserProfile`)
- **Variables** : camelCase (`userName`)
- **Constants** : SCREAMING_SNAKE_CASE (`ACTIVITIES`)

## 🧪 Tests

### Obligations

- **Couverture minimale** : 80%
- **Tests unitaires** pour toutes les fonctions utilitaires
- **Tests de composants** pour l'interface utilisateur
- **Tests d'intégration** pour les fonctionnalités critiques

### Structure des Tests

```
src/
├── components/
│   ├── Header.tsx
│   └── __tests__/
│       └── Header.test.tsx
└── utils/
    ├── formatters.ts
    └── __tests__/
        └── formatters.test.ts
```

### Commandes de Test

```bash
npm test                # Tests unitaires
npm run test:watch      # Mode watch
npm run test:coverage   # Avec coverage
```

## 🎨 Standards de Code

### ESLint + Prettier

Tous les fichiers doivent respecter nos règles :

```bash
npm run lint            # Vérification
npm run lint:fix        # Correction automatique
npm run format          # Formatage Prettier
```

### TypeScript

- **Mode strict** activé
- **Types explicites** pour les paramètres de fonction
- **Interfaces** pour les objets complexes
- **Pas de `any`** - utiliser des types spécifiques

## 📝 Commits et Messages

### Format des Commits

Utiliser le format conventionnel :

```
type(scope): description

feat(components): add Header component with navigation
fix(utils): correct duration formatting for hours
docs(readme): update installation instructions
test(utils): add tests for matching algorithm
```

### Types de Commits

- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage, point-virgules
- `refactor`: Refactoring sans changement fonctionnel
- `test`: Ajout/modification de tests
- `chore`: Maintenance, outils

## 🔄 Processus de Pull Request

### Avant de Soumettre

1. ✅ Tests passent : `npm test`
2. ✅ Build réussit : `npm run build`
3. ✅ Linting OK : `npm run lint`
4. ✅ Formatage OK : `npm run format:check`
5. ✅ Couverture maintenue : `npm run test:coverage`

### Description de la PR

Inclure :

- **Résumé** des changements
- **Motivation** et contexte
- **Types de changements** (feat, fix, etc.)
- **Tests** ajoutés ou modifiés
- **Screenshots** pour les changements UI

### Template PR

```markdown
## Résumé

[Description concise des changements]

## Type de changement

- [ ] Bug fix
- [ ] Nouvelle fonctionnalité
- [ ] Breaking change
- [ ] Documentation

## Tests

- [ ] Tests unitaires ajoutés/modifiés
- [ ] Tests manuels effectués
- [ ] Couverture maintenue > 80%

## Checklist

- [ ] Code formaté avec Prettier
- [ ] ESLint sans erreurs
- [ ] Build réussit
- [ ] Tests passent
```

## 🎯 Bonnes Pratiques

### Composants React

```tsx
// ✅ Bon
interface HeaderProps {
  onHomeClick?: () => void;
  className?: string;
}

export const Header: React.FC<HeaderProps> = ({
  onHomeClick,
  className = "",
}) => {
  return <header className={`bg-white ${className}`}>{/* ... */}</header>;
};

// ❌ Éviter
export default function Header(props: any) {
  // ...
}
```

### Utilitaires

```ts
// ✅ Bon
export const formatDuration = (minutes: number): string => {
  if (minutes < 0) {
    throw new Error("Duration cannot be negative");
  }

  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;

  return hours > 0 ? `${hours}h${mins || ""}` : `${mins}min`;
};

// ❌ Éviter
export function formatDuration(minutes) {
  return minutes > 60 ? minutes / 60 + "h" : minutes + "min";
}
```

### Tests

```tsx
// ✅ Bon
describe("formatDuration", () => {
  it("formats minutes correctly", () => {
    expect(formatDuration(30)).toBe("30min");
    expect(formatDuration(60)).toBe("1h");
    expect(formatDuration(90)).toBe("1h30");
  });

  it("throws error for negative values", () => {
    expect(() => formatDuration(-10)).toThrow();
  });
});

// ❌ Éviter
test("test duration", () => {
  expect(formatDuration(30)).toBe("30min");
});
```

## 🐛 Signalement de Bugs

### Template d'Issue

```markdown
## Description

[Description claire et concise du bug]

## Étapes pour Reproduire

1. Aller à '...'
2. Cliquer sur '....'
3. Faire défiler jusqu'à '....'
4. Voir l'erreur

## Comportement Attendu

[Description de ce qui devrait se passer]

## Comportement Actuel

[Description de ce qui se passe réellement]

## Environnement

- OS: [ex. macOS]
- Navigateur: [ex. Chrome, Safari]
- Version: [ex. 22]

## Screenshots

[Si applicable, ajouter des captures d'écran]
```

## 🆕 Propositions de Fonctionnalités

Avant de développer une nouvelle fonctionnalité :

1. **Créer une issue** pour discussion
2. **Attendre validation** de l'équipe
3. **Définir l'approche** technique
4. **Commencer le développement**

## 📞 Support

- **Issues GitHub** : Pour bugs et fonctionnalités
- **Discussions** : Pour questions générales
- **Email** : vidaluca77@gmail.com pour questions urgentes

## 🤝 Code de Conduite

- Être respectueux envers tous les contributeurs
- Utiliser un langage inclusif
- Accepter les critiques constructives
- Se concentrer sur l'amélioration du projet
- Respecter la mission éducative et sociale

---

Merci de contribuer à La Vida Luca ! 🌱
