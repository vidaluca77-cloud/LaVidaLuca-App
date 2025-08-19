# Variables d'environnement pour le déploiement

## Configuration Vercel (Frontend)

### Variables automatiquement configurées dans vercel.json
- `NEXT_PUBLIC_API_URL`: https://lavidaluca-backend.onrender.com
- `NEXT_PUBLIC_ENVIRONMENT`: production

### Variables à configurer manuellement dans Vercel Dashboard
```bash
# Sentry Configuration
NEXT_PUBLIC_SENTRY_DSN=your-sentry-dsn-here
SENTRY_ORG=your-sentry-org
SENTRY_PROJECT=your-sentry-project

# Build Configuration
SENTRY_AUTH_TOKEN=your-sentry-auth-token
```

## Configuration Render (Backend)

### Variables automatiquement configurées dans render.yaml
- Toutes les variables de base (DATABASE_URL, CORS_ORIGINS, etc.)

### Variables à configurer manuellement dans Render Dashboard
```bash
# OpenAI Integration
OPENAI_API_KEY=your-openai-api-key

# Sentry Monitoring
SENTRY_DSN=your-backend-sentry-dsn

# Email Configuration (optionnel pour formulaires de contact)
SMTP_HOST=smtp.gmail.com
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Validation des variables

Pour vérifier que toutes les variables sont correctement configurées:

### Frontend (Vercel)
```bash
curl https://lavidaluca.fr/api/health
```

### Backend (Render)
```bash
curl https://lavidaluca-backend.onrender.com/health
```

## URLs de déploiement

- **Frontend Production**: https://lavidaluca.fr
- **Backend Production**: https://lavidaluca-backend.onrender.com
- **API Documentation**: https://lavidaluca-backend.onrender.com/docs (si activée)
- **Monitoring**: Accès via Sentry dashboard

## Notes de sécurité

1. **JWT_SECRET_KEY**: Généré automatiquement par Render
2. **CORS**: Configuré pour autoriser uniquement les domaines de production
3. **Rate Limiting**: 100 req/min pour les utilisateurs authentifiés, 20 pour les anonymes
4. **Headers de sécurité**: CSP, XSS Protection, etc. configurés dans vercel.json