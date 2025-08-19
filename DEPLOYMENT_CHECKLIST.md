# Checklist de déploiement La Vida Luca

## Pré-déploiement

### Frontend (Vercel)
- [ ] Vérifier que `vercel.json` est présent et configuré
- [ ] Configurer les variables d'environnement dans Vercel Dashboard:
  - [ ] `NEXT_PUBLIC_SENTRY_DSN`
  - [ ] `SENTRY_ORG`
  - [ ] `SENTRY_PROJECT`
  - [ ] `SENTRY_AUTH_TOKEN`
- [ ] Tester le build local: `npm run build`
- [ ] Vérifier les tests: `npm test`
- [ ] Connecter le repository GitHub à Vercel
- [ ] Configurer le domaine personnalisé: `lavidaluca.fr`

### Backend (Render)
- [ ] Vérifier que `render.yaml` est présent et configuré
- [ ] Configurer les variables d'environnement dans Render Dashboard:
  - [ ] `OPENAI_API_KEY`
  - [ ] `SENTRY_DSN`
  - [ ] `SMTP_HOST`, `SMTP_USERNAME`, `SMTP_PASSWORD` (si email activé)
- [ ] Tester les tests backend: `npm run backend:test`
- [ ] Connecter le repository GitHub à Render
- [ ] Configurer le domaine personnalisé (si nécessaire)

## Post-déploiement

### Tests de connectivité
- [ ] Exécuter le script de vérification: `npm run deploy:check`
- [ ] Vérifier la page d'accueil: https://lavidaluca.fr
- [ ] Vérifier l'API backend: https://lavidaluca-backend.onrender.com/health
- [ ] Tester les routes API via le frontend: https://lavidaluca.fr/api/health

### Tests de sécurité
- [ ] Vérifier les headers de sécurité:
  ```bash
  curl -I https://lavidaluca.fr | grep -i security
  ```
- [ ] Tester CORS depuis le frontend
- [ ] Vérifier que les endpoints sensibles nécessitent l'authentification
- [ ] Contrôler le rate limiting

### Tests de monitoring
- [ ] Vérifier que Sentry reçoit les événements frontend
- [ ] Vérifier que Sentry reçoit les événements backend
- [ ] Contrôler les métriques dans Render Dashboard
- [ ] Tester les alertes de monitoring

### Tests fonctionnels
- [ ] Tester l'inscription/connexion utilisateur
- [ ] Tester la navigation entre les pages
- [ ] Tester les formulaires de contact
- [ ] Tester l'intégration OpenAI (si configurée)
- [ ] Vérifier la base de données via les endpoints API

## Rollback Plan

### En cas de problème frontend
1. Revenir à la version précédente dans Vercel Dashboard
2. Ou déployer la branche `main` précédente
3. Vérifier que le rollback fonctionne

### En cas de problème backend
1. Revenir à la version précédente dans Render Dashboard
2. Vérifier la connectivité à la base de données
3. Redémarrer les services si nécessaire

## Monitoring post-déploiement

### À surveiller pendant 24h
- [ ] Temps de réponse des API
- [ ] Erreurs 5xx dans Sentry
- [ ] Utilisation des ressources (CPU, mémoire)
- [ ] Connexions à la base de données

### À surveiller pendant 1 semaine
- [ ] Trafic utilisateur
- [ ] Performance générale
- [ ] Erreurs utilisateur
- [ ] Feedback utilisateur

## Contacts d'urgence
- **Équipe technique**: [contact technique]
- **Vercel Support**: support via dashboard
- **Render Support**: support via dashboard
- **Sentry**: support via dashboard

## Documentation
- Configuration: `DEPLOYMENT.md`
- Scripts: `scripts/check-deployment.sh`
- Tests: `tests/deployment/`