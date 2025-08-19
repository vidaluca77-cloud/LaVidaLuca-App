# Scripts de Monitoring - La Vida Luca

Ce dossier contient les scripts de surveillance et de monitoring pour la plateforme La Vida Luca.

## Scripts disponibles

### 1. health-check.sh
Script de vérification de santé rapide des services déployés.

**Usage:**
```bash
./scripts/monitoring/health-check.sh
```

**Fonctionnalités:**
- Vérifie la disponibilité de l'application web
- Test l'API IA et ses endpoints de santé
- Contrôle la connectivité à la base de données
- Affiche un résumé coloré des statuts
- Code de sortie adapté pour l'intégration CI/CD

### 2. performance-monitor.js
Script de monitoring de performance avancé avec génération de rapports.

**Usage:**
```bash
node scripts/monitoring/performance-monitor.js
```

**Fonctionnalités:**
- Mesure les temps de réponse des endpoints
- Calcule la disponibilité des services
- Génère des rapports HTML et JSON
- Supporte les tentatives multiples
- Historique des performances

**Rapports générés:**
- `monitoring-reports/latest-monitoring.html` - Rapport visuel
- `monitoring-reports/latest-monitoring.json` - Données brutes
- `monitoring-reports/monitoring-TIMESTAMP.*` - Archives horodatées

### 3. test-deployment.sh
Script de validation de l'infrastructure de déploiement.

**Usage:**
```bash
./scripts/test-deployment.sh
```

**Validations:**
- Présence des fichiers de configuration
- Syntaxe JSON des configurations
- Build Next.js et compilation TypeScript
- Structure de l'API FastAPI
- Validité des migrations SQL
- Permissions des scripts

## Intégration CI/CD

Ces scripts sont intégrés dans le pipeline GitHub Actions :

- **health-check.sh** : Vérifications post-déploiement
- **performance-monitor.js** : Monitoring continu (optionnel)
- **test-deployment.sh** : Validation pré-déploiement

## Configuration

Les scripts utilisent les variables d'environnement suivantes :

```bash
VERCEL_PRODUCTION_URL=https://votre-app.vercel.app
RENDER_SERVICE_URL=https://votre-api.onrender.com
NEXT_PUBLIC_SUPABASE_URL=https://votre-projet.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=votre_cle_anonyme
```

## Monitoring automatique

Pour un monitoring automatique, vous pouvez utiliser cron :

```bash
# Vérification de santé toutes les 5 minutes
*/5 * * * * /path/to/scripts/monitoring/health-check.sh

# Rapport de performance quotidien à 6h
0 6 * * * /usr/bin/node /path/to/scripts/monitoring/performance-monitor.js
```

## Alertes

Les scripts supportent l'intégration avec des systèmes d'alerte :

- Codes de sortie standardisés (0=OK, 1=Warning, 2=Critical)
- Sortie JSON pour l'intégration avec des outils de monitoring
- Support des webhooks (à configurer via MONITORING_WEBHOOK_URL)

## Personnalisation

Les scripts peuvent être étendus pour :

- Ajouter de nouveaux endpoints à surveiller
- Configurer des seuils d'alerte personnalisés
- Intégrer des métriques métier spécifiques
- Envoyer des notifications personnalisées