#!/bin/bash

# Scripts de déploiement pour La Vida Luca
# Usage: ./scripts/deploy.sh [environment]

set -e

ENVIRONMENT=${1:-production}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Déploiement La Vida Luca - Environnement: $ENVIRONMENT"

# Fonction de logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Vérification des prérequis
check_prerequisites() {
    log "📋 Vérification des prérequis..."
    
    # Vérifier Node.js
    if ! command -v node &> /dev/null; then
        log "❌ Node.js non trouvé. Installation requise."
        exit 1
    fi
    
    # Vérifier Python
    if ! command -v python3 &> /dev/null; then
        log "❌ Python 3 non trouvé. Installation requise."
        exit 1
    fi
    
    # Vérifier les variables d'environnement
    if [[ "$ENVIRONMENT" == "production" ]]; then
        required_vars=(
            "VERCEL_TOKEN"
            "RENDER_API_KEY"
            "RENDER_SERVICE_ID"
            "NEXT_PUBLIC_SUPABASE_URL"
            "NEXT_PUBLIC_SUPABASE_ANON_KEY"
        )
        
        for var in "${required_vars[@]}"; do
            if [[ -z "${!var}" ]]; then
                log "❌ Variable d'environnement manquante: $var"
                exit 1
            fi
        done
    fi
    
    log "✅ Prérequis validés"
}

# Build du frontend
build_frontend() {
    log "🔨 Build du frontend Next.js..."
    cd "$PROJECT_ROOT"
    
    npm ci
    npm run lint
    npm run build
    
    log "✅ Frontend buildé avec succès"
}

# Préparation du backend
prepare_backend() {
    log "🔨 Préparation du backend FastAPI..."
    cd "$PROJECT_ROOT/apps/ia"
    
    # Créer un environnement virtuel si nécessaire
    if [[ ! -d ".venv" ]]; then
        python3 -m venv .venv
    fi
    
    source .venv/bin/activate
    pip install -r requirements.txt
    
    # Exécuter les tests
    python -m pytest tests/ -v
    
    log "✅ Backend préparé avec succès"
}

# Déploiement vers Vercel
deploy_to_vercel() {
    log "🚀 Déploiement vers Vercel..."
    cd "$PROJECT_ROOT"
    
    if [[ "$ENVIRONMENT" == "production" ]]; then
        npx vercel --prod --token "$VERCEL_TOKEN" --yes
    else
        npx vercel --token "$VERCEL_TOKEN" --yes
    fi
    
    log "✅ Déployé sur Vercel"
}

# Déploiement vers Render
deploy_to_render() {
    log "🚀 Déploiement vers Render..."
    
    # Trigger deployment via API
    curl -X POST \
        -H "Authorization: Bearer $RENDER_API_KEY" \
        -H "Accept: application/json" \
        "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys"
    
    log "✅ Déploiement Render déclenché"
}

# Migration de la base de données
run_migrations() {
    log "🗃️ Exécution des migrations..."
    cd "$PROJECT_ROOT/apps/ia"
    
    source .venv/bin/activate
    alembic upgrade head
    
    log "✅ Migrations exécutées"
}

# Tests post-déploiement
run_health_checks() {
    log "🏥 Tests de santé post-déploiement..."
    
    cd "$PROJECT_ROOT"
    python scripts/monitor.py
    
    log "✅ Tests de santé terminés"
}

# Notification
send_notification() {
    log "📢 Envoi de notification..."
    
    if [[ -n "$DISCORD_WEBHOOK_URL" ]]; then
        curl -H "Content-Type: application/json" \
             -X POST \
             -d "{\"content\":\"🚀 Déploiement $ENVIRONMENT terminé avec succès !\"}" \
             "$DISCORD_WEBHOOK_URL"
    fi
}

# Fonction principale
main() {
    log "🎯 Début du déploiement $ENVIRONMENT"
    
    check_prerequisites
    build_frontend
    prepare_backend
    
    if [[ "$ENVIRONMENT" == "production" ]]; then
        run_migrations
        deploy_to_vercel
        deploy_to_render
        sleep 30  # Attendre que les déploiements se stabilisent
        run_health_checks
        send_notification
    else
        deploy_to_vercel
        log "🎯 Déploiement de test terminé"
    fi
    
    log "🎉 Déploiement $ENVIRONMENT terminé avec succès !"
}

# Gestion des erreurs
trap 'log "❌ Erreur pendant le déploiement. Arrêt."; exit 1' ERR

# Exécution
main "$@"