# Configuration monitoring et observabilité

## Vue d'ensemble

Le système de monitoring La Vida Luca combine plusieurs outils pour une observabilité complète :

- **Sentry** : Error tracking et performance monitoring
- **Vercel Analytics** : Métriques frontend et Web Vitals
- **Render Metrics** : Monitoring infrastructure API
- **Supabase Dashboard** : Métriques base de données
- **Custom metrics** : Métriques business spécifiques

## Configuration Sentry

### Installation et setup

1. **Créer un projet Sentry**
   ```bash
   # Via web : https://sentry.io
   # Ou CLI
   npm install -g @sentry/cli
   sentry-cli login
   sentry-cli projects create
   ```

2. **Variables d'environnement**
   ```bash
   NEXT_PUBLIC_SENTRY_DSN=https://your-key@sentry.io/project-id
   SENTRY_ORG=your-org
   SENTRY_PROJECT=la-vida-luca
   SENTRY_AUTH_TOKEN=your-auth-token
   ```

3. **Configuration releases**
   ```bash
   # Dans next.config.js - déjà configuré
   # Création automatique de release à chaque déploiement
   ```

### Dashboards Sentry

#### Dashboard Erreurs
- Errors by page/route
- Error frequency trends  
- Error impact (users affected)
- Error resolution status

#### Dashboard Performance
- Page load times
- API response times
- Database query performance
- Transaction trends

#### Dashboard Releases
- Release health
- New errors introduced
- Performance regressions
- Adoption rate

### Alertes configurées

```yaml
# Alertes email/Slack
error_rate:
  threshold: "> 5% in 5 minutes"
  channels: ["email", "slack"]

performance_regression:
  threshold: "> 20% slower than baseline"
  channels: ["email"]

new_error:
  threshold: "New error affecting > 10 users"
  channels: ["slack"]

memory_usage:
  threshold: "> 80% for 10 minutes"
  channels: ["email", "slack"]
```

## Métriques custom

### Performance tracking

```typescript
// Exemple d'utilisation dans le code
import { performanceMonitor } from '@/lib/monitoring';

// Mesurer une fonction
const recommendations = await performanceMonitor.measureAsync(
  'get_recommendations',
  () => getRecommendations(profile),
  { userId: user.id, profileType: profile.type }
);

// Métrique business
performanceMonitor.recordBusinessMetric('activity_viewed', {
  activityId: activity.id,
  category: activity.category,
  userType: user.type
});
```

### Métriques collectées

#### Métriques techniques
```typescript
interface TechnicalMetrics {
  page_load_time: number;
  api_response_time: number;
  database_query_time: number;
  cache_hit_rate: number;
  error_rate: number;
  memory_usage: number;
  cpu_usage: number;
}
```

#### Métriques business
```typescript
interface BusinessMetrics {
  // Engagement
  page_views: number;
  unique_visitors: number;
  session_duration: number;
  bounce_rate: number;
  
  // Fonctionnalités
  activities_viewed: number;
  recommendations_requested: number;
  contact_forms_submitted: number;
  relais_applications: number;
  
  // Conversion
  catalog_engagement_rate: number;
  application_completion_rate: number;
  user_retention_rate: number;
}
```

## Health checks

### Endpoints configurés

```typescript
// /api/health - Déjà implémenté
{
  "status": "healthy|degraded|unhealthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "services": {
    "database": "healthy",
    "ai_api": "healthy", 
    "cache": "healthy"
  },
  "uptime": 123456,
  "version": "1.0.0"
}
```

### Monitoring external

```bash
# Pingdom/UptimeRobot checks
GET https://la-vida-luca.vercel.app/api/health
Interval: 1 minute
Timeout: 30 seconds
Expected: 200 OK

GET https://api-ia.render.com/health  
Interval: 2 minutes
Timeout: 30 seconds
Expected: 200 OK
```

## Dashboards personnalisés

### Dashboard opérationnel

**Métriques en temps réel** :
- Status global (healthy/degraded/down)
- Temps de réponse API (P50, P95, P99)
- Erreurs par minute
- Utilisateurs actifs
- Déploiements récents

**Alertes** :
- Service down (immédiat)
- Error rate > 5% (5min)
- Response time > 2s (10min)
- Memory usage > 80% (15min)

### Dashboard business

**Engagement** :
- Visiteurs uniques (jour/semaine/mois)
- Pages vues les plus populaires
- Durée de session moyenne
- Taux de rebond

**Conversion** :
- Formulaires de contact soumis
- Candidatures relais
- Engagement catalogue d'activités
- Recommandations générées

**Géographie** :
- Répartition des visiteurs par région
- Performance par région
- Adoption par département

### Dashboard technique

**Performance** :
- Core Web Vitals (LCP, FID, CLS)
- Temps de construction (build time)
- Taille des bundles JavaScript
- Cache hit ratio

**Qualité** :
- Code coverage des tests
- Vulnérabilités de sécurité
- Debt technique (SonarQube)
- Performance score (Lighthouse)

## Configuration logs

### Logs structurés

```typescript
// Format standardisé - déjà implémenté
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "info|warn|error|debug",
  "message": "User logged in",
  "metadata": {
    "userId": "123",
    "sessionId": "abc-def",
    "userAgent": "Mozilla/5.0...",
    "ip": "192.168.1.1"
  }
}
```

### Aggregation et recherche

**Vercel** : Logs disponibles via dashboard
**Render** : Logs disponibles via dashboard  
**Supabase** : Logs SQL via dashboard

En production, considérer :
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Grafana + Loki**
- **Datadog Logs**

## Tracing distribué

### Configuration

```typescript
// Sentry tracing - déjà configuré
import * as Sentry from "@sentry/nextjs";

// Tracer une transaction
const transaction = Sentry.startTransaction({
  name: "Get Recommendations",
  op: "ai.recommendation"
});

try {
  // Code tracé
  const result = await getRecommendations();
  transaction.setStatus("ok");
} catch (error) {
  transaction.setStatus("internal_error");
} finally {
  transaction.finish();
}
```

### Spans personnalisés

```typescript
// Tracer des opérations spécifiques
const span = transaction.startChild({
  op: "db.query",
  description: "Fetch user activities"
});

try {
  const activities = await db.getActivities(userId);
  span.setData("activity_count", activities.length);
} finally {
  span.finish();
}
```

## Alertes et notifications

### Canaux configurés

**Email** :
- Erreurs critiques
- Déploiements
- Rapports hebdomadaires

**Slack** (optionnel) :
- Erreurs en temps réel
- Déploiements
- Métriques anormales

**SMS** (urgences uniquement) :
- Service complètement down
- Perte de données

### Escalation

1. **Niveau 1** (immédiat) : Slack
2. **Niveau 2** (5 min) : Email
3. **Niveau 3** (15 min) : SMS
4. **Niveau 4** (30 min) : Appel

### Règles d'alertes

```yaml
critical:
  - service_down: "immediate"
  - error_rate_>10%: "immediate"
  - data_loss: "immediate"

warning:
  - error_rate_>5%: "5 minutes"
  - response_time_>2s: "10 minutes" 
  - memory_usage_>80%: "15 minutes"

info:
  - deployment_complete: "immediate"
  - weekly_report: "monday 9am"
```

## Maintenance et optimisation

### Révisions régulières

**Quotidien** :
- Vérifier les alertes de la nuit
- Contrôler les métriques clés
- Valider les déploiements

**Hebdomadaire** :
- Analyser les tendances
- Optimiser les alertes (réduire le bruit)
- Réviser les performances

**Mensuel** :
- Rapport de disponibilité
- Optimisation des coûts monitoring
- Mise à jour des dashboards

### Optimisations automatiques

```typescript
// Auto-scaling basé sur les métriques
// (à configurer côté infrastructure)

// Nettoyage automatique des logs
// Rétention : 30 jours en développement, 90 jours en production

// Compression automatique des métriques anciennes
// Granularité réduite après 7 jours
```

### SLI/SLO

**Service Level Indicators** :
- Availability: 99.9%
- Response time P95: < 2s
- Error rate: < 1%

**Service Level Objectives** :
- Uptime mensuel: 99.9%
- Temps de résolution incidents: < 4h
- Temps de déploiement: < 10min