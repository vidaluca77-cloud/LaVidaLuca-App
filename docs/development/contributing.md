# Guide de contribution

## Bienvenue contributeur !

Merci de votre intérêt pour contribuer au projet La Vida Luca. Ce guide vous explique comment participer au développement de la plateforme.

## Code de conduite

En participant à ce projet, vous vous engagez à respecter notre code de conduite basé sur les valeurs de La Vida Luca :
- Respect et bienveillance envers tous les contributeurs
- Collaboration constructive
- Engagement pour l'impact social et environnemental
- Transparence dans les échanges

## Types de contributions

### 🐛 Signaler un bug
1. Vérifiez que le bug n'est pas déjà signalé dans les issues
2. Créez une issue avec le template "Bug report"
3. Incluez : 
   - Description claire du problème
   - Étapes pour reproduire
   - Comportement attendu vs observé
   - Screenshots si applicable
   - Environnement (OS, navigateur, version)

### ✨ Proposer une fonctionnalité
1. Ouvrez une issue avec le template "Feature request"
2. Décrivez la fonctionnalité et sa valeur ajoutée
3. Proposez une implémentation si possible
4. Attendez les retours avant de développer

### 📚 Améliorer la documentation
- Corriger des typos
- Clarifier des explications
- Ajouter des exemples
- Traduire en d'autres langues

### 💻 Contribuer au code
Consultez les issues taggées `good first issue` pour commencer.

## Processus de développement

### 1. Setup initial
```bash
# Fork le repository
git clone https://github.com/VOTRE_USERNAME/LaVidaLuca-App.git
cd LaVidaLuca-App

# Ajouter le repository upstream
git remote add upstream https://github.com/vidaluca77-cloud/LaVidaLuca-App.git

# Installer les dépendances
npm install

# Créer le fichier d'environnement
cp .env.local.example .env.local
```

### 2. Créer une branche
```bash
# Mettre à jour main
git checkout main
git pull upstream main

# Créer une branche pour votre feature
git checkout -b type/description-courte
```

Exemples de noms de branches :
- `feat/user-authentication`
- `fix/mobile-navigation`
- `docs/api-documentation`
- `refactor/monitoring-system`

### 3. Développer
- Suivez les [standards de code](./README.md#standards-de-code)
- Écrivez des tests pour les nouvelles fonctionnalités
- Mettez à jour la documentation si nécessaire
- Committez régulièrement avec des messages clairs

### 4. Tests et validation
```bash
# Lancer les tests
npm test

# Vérifier le linting
npm run lint

# Construire le projet
npm run build
```

### 5. Soumettre la Pull Request
1. Poussez votre branche
   ```bash
   git push origin type/description-courte
   ```

2. Créez une Pull Request vers `main`
3. Remplissez le template de PR
4. Demandez une revue de code

## Template de Pull Request

```markdown
## Description
Brève description des changements

## Type de changement
- [ ] Bug fix
- [ ] Nouvelle fonctionnalité
- [ ] Breaking change
- [ ] Documentation

## Tests
- [ ] Tests unitaires ajoutés/mis à jour
- [ ] Tests d'intégration ajoutés/mis à jour
- [ ] Tests manuels effectués

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings introduced
```

## Standards techniques

### Commits
Utilisez le format conventional commits :
```
type(scope): description

body (optionnel)

footer (optionnel)
```

Types acceptés :
- `feat`: nouvelle fonctionnalité
- `fix`: correction de bug
- `docs`: documentation
- `style`: formatage, missing semi colons, etc.
- `refactor`: refactoring
- `perf`: amélioration de performance
- `test`: ajout de tests
- `build`: changements du système de build
- `ci`: changements CI
- `chore`: autres changements

### Code Review

Critères de review :
- ✅ Fonctionnalité correctement implémentée
- ✅ Tests couvrent les cas d'usage
- ✅ Code lisible et maintenable
- ✅ Performance acceptable
- ✅ Sécurité respectée
- ✅ Accessibilité prise en compte
- ✅ Documentation à jour

### Merge

Conditions pour merger :
- ✅ 1 approbation minimum (2 pour les changements majeurs)
- ✅ Tous les tests passent
- ✅ Pas de conflits
- ✅ Build réussi
- ✅ Documentation mise à jour si nécessaire

## Ressources

### Documentation
- [Guide de développement](./README.md)
- [Standards de code](./code-standards.md)
- [Architecture](../architecture/README.md)

### Communication
- Email : [vidaluca77@gmail.com](mailto:vidaluca77@gmail.com)
- Issues GitHub pour les discussions techniques

### Outils recommandés
- VS Code avec les extensions listées
- GitHub Desktop ou GitKraken pour l'interface Git
- Postman pour tester les APIs

## Questions fréquentes

**Q: Comment configurer l'environnement de développement ?**
R: Suivez le [guide de démarrage rapide](../guides/quick-start.md)

**Q: Puis-je travailler sur plusieurs issues en même temps ?**
R: Préférez vous concentrer sur une issue à la fois pour des reviews plus efficaces

**Q: Comment tester mes changements ?**
R: Consultez la section Testing du guide de développement

**Q: Que faire si ma PR est rejetée ?**
R: Lisez les commentaires, appliquez les changements demandés et re-soumettez

## Remerciements

Chaque contribution compte pour faire avancer le projet La Vida Luca. Merci de votre engagement pour une agriculture et une société plus durables ! 🌱