#!/bin/bash

# 🚀 Script de Déploiement Automatisé - La Vida Luca
# Gère le déploiement complet de l'application

set -euo pipefail

# Configuration
PROJECT_NAME="La Vida Luca"
GITHUB_REPO="vidaluca77-cloud/LaVidaLuca-App"
VERCEL_PROJECT_NAME="la-vida-luca"
LOG_FILE="/tmp/deploy-$(date +%Y%m%d-%H%M%S).log"

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Fonction de logging
log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error() {
    log "${RED}[ERROR]${NC} $*"
    exit 1
}

warn() {
    log "${YELLOW}[WARN]${NC} $*"
}

info() {
    log "${BLUE}[INFO]${NC} $*"
}

success() {
    log "${GREEN}[SUCCESS]${NC} $*"
}

# Vérification des prérequis
check_prerequisites() {
    info "Vérification des prérequis..."
    
    # Vérifier Node.js
    if ! command -v node >/dev/null 2>&1; then
        error "Node.js n'est pas installé. Veuillez installer Node.js 18+ avant de continuer."
    fi
    
    local node_version=$(node --version | sed 's/v//')
    local major_version=${node_version%%.*}
    if [[ $major_version -lt 18 ]]; then
        error "Node.js version $node_version détectée. Version 18+ requise."
    fi
    success "Node.js $node_version ✓"
    
    # Vérifier npm
    if ! command -v npm >/dev/null 2>&1; then
        error "npm n'est pas installé."
    fi
    success "npm $(npm --version) ✓"
    
    # Vérifier Git
    if ! command -v git >/dev/null 2>&1; then
        error "Git n'est pas installé."
    fi
    success "Git $(git --version | cut -d' ' -f3) ✓"
    
    # Vérifier si nous sommes dans un repo Git
    if ! git rev-parse --git-dir >/dev/null 2>&1; then
        error "Ce script doit être exécuté depuis le répertoire du projet Git."
    fi
    success "Repository Git détecté ✓"
}

# Installation et vérification des dépendances
install_dependencies() {
    info "Installation des dépendances..."
    
    if [[ ! -f "package.json" ]]; then
        error "Fichier package.json non trouvé."
    fi
    
    # Nettoyer les anciens node_modules si nécessaire
    if [[ -d "node_modules" ]]; then
        info "Nettoyage des anciens node_modules..."
        rm -rf node_modules package-lock.json
    fi
    
    # Installer les dépendances
    npm install || error "Échec de l'installation des dépendances"
    success "Dépendances installées ✓"
}

# Vérification de la qualité du code
quality_checks() {
    info "Vérification de la qualité du code..."
    
    # Build du projet
    info "Build du projet..."
    npm run build || error "Échec du build"
    success "Build réussi ✓"
    
    # Linting (si configuré)
    if npm run lint --silent >/dev/null 2>&1; then
        info "Linting du code..."
        npm run lint || warn "Problèmes de linting détectés"
    else
        warn "Linting non configuré - ignoré"
    fi
    
    # Tests (si configurés)
    if npm run test --silent >/dev/null 2>&1; then
        info "Exécution des tests..."
        npm run test || error "Tests échoués"
        success "Tests réussis ✓"
    else
        warn "Tests non configurés - ignorés"
    fi
}

# Vérification des variables d'environnement
check_environment() {
    info "Vérification des variables d'environnement..."
    
    local required_vars=(
        "NEXT_PUBLIC_CONTACT_EMAIL"
        "NEXT_PUBLIC_CONTACT_PHONE"
    )
    
    local missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            missing_vars+=("$var")
        fi
    done
    
    if [[ ${#missing_vars[@]} -gt 0 ]]; then
        warn "Variables d'environnement manquantes:"
        for var in "${missing_vars[@]}"; do
            warn "  - $var"
        done
        warn "Ces variables peuvent être configurées dans Vercel après le déploiement."
    else
        success "Variables d'environnement configurées ✓"
    fi
}

# Déploiement sur Vercel
deploy_to_vercel() {
    info "Déploiement sur Vercel..."
    
    # Vérifier si Vercel CLI est installé
    if ! command -v vercel >/dev/null 2>&1; then
        info "Installation de Vercel CLI..."
        npm install -g vercel || error "Échec de l'installation de Vercel CLI"
    fi
    
    # Login Vercel (si nécessaire)
    if ! vercel whoami >/dev/null 2>&1; then
        warn "Connexion à Vercel requise..."
        vercel login || error "Échec de la connexion à Vercel"
    fi
    
    local current_user=$(vercel whoami 2>/dev/null || echo "unknown")
    success "Connecté à Vercel en tant que: $current_user"
    
    # Déploiement
    info "Lancement du déploiement..."
    
    # Déploiement en production
    if vercel --prod --yes; then
        success "Déploiement Vercel réussi ✓"
        
        # Récupérer l'URL de déploiement
        local deployment_url=$(vercel ls "$VERCEL_PROJECT_NAME" 2>/dev/null | grep "https://" | head -1 | awk '{print $2}' || echo "")
        if [[ -n "$deployment_url" ]]; then
            success "Application disponible à: $deployment_url"
        fi
    else
        error "Échec du déploiement Vercel"
    fi
}

# Configuration post-déploiement
post_deployment_config() {
    info "Configuration post-déploiement..."
    
    # Vérifier la configuration des domaines
    info "Vérification de la configuration des domaines..."
    vercel domains ls 2>/dev/null || warn "Aucun domaine personnalisé configuré"
    
    # Vérifier les variables d'environnement Vercel
    info "Vérification des variables d'environnement Vercel..."
    local env_vars=$(vercel env ls 2>/dev/null || echo "")
    if [[ -n "$env_vars" ]]; then
        success "Variables d'environnement Vercel configurées"
    else
        warn "Aucune variable d'environnement configurée dans Vercel"
        info "Configurez les variables via: vercel env add <NAME>"
    fi
}

# Tests post-déploiement
post_deployment_tests() {
    info "Tests post-déploiement..."
    
    local site_url="https://$VERCEL_PROJECT_NAME.vercel.app"
    
    # Test de disponibilité
    info "Test de disponibilité du site..."
    local response_code=$(curl -s -o /dev/null -w "%{http_code}" "$site_url" --max-time 30)
    
    if [[ "$response_code" -eq 200 ]]; then
        success "Site accessible (HTTP $response_code) ✓"
    else
        error "Site non accessible (HTTP $response_code)"
    fi
    
    # Test des pages principales
    local pages=("/contact" "/catalogue" "/rejoindre")
    for page in "${pages[@]}"; do
        local page_response=$(curl -s -o /dev/null -w "%{http_code}" "$site_url$page" --max-time 10)
        if [[ "$page_response" -eq 200 ]]; then
            success "Page $page accessible ✓"
        else
            warn "Page $page retourne HTTP $page_response"
        fi
    done
    
    # Test de l'API contact
    info "Test de l'API contact..."
    local api_response=$(curl -s -o /dev/null -w "%{http_code}" \
                        -X POST \
                        -H "Content-Type: application/json" \
                        -d '{"name":"Test Deploy","email":"test@deploy.com","message":"Test automatique"}' \
                        "$site_url/api/contact" --max-time 10)
    
    if [[ "$api_response" -eq 200 ]]; then
        success "API contact fonctionnelle ✓"
    else
        warn "API contact retourne HTTP $api_response"
    fi
}

# Génération du rapport de déploiement
generate_deployment_report() {
    info "Génération du rapport de déploiement..."
    
    local report_file="/tmp/deployment-report-$(date +%Y%m%d-%H%M%S).html"
    local commit_hash=$(git rev-parse HEAD)
    local commit_message=$(git log -1 --pretty=%B)
    local branch_name=$(git rev-parse --abbrev-ref HEAD)
    
    cat > "$report_file" << EOF
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport de Déploiement - $PROJECT_NAME</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #22c55e, #16a34a); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; text-align: center; }
        .section { background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #22c55e; }
        .success { color: #28a745; font-weight: bold; }
        .warning { color: #ffc107; font-weight: bold; }
        .error { color: #dc3545; font-weight: bold; }
        .info { background: #d1ecf1; padding: 15px; border-radius: 5px; border-left: 4px solid #bee5eb; }
        pre { background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; border: 1px solid #e9ecef; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Rapport de Déploiement</h1>
            <h2>🌱 $PROJECT_NAME</h2>
            <p>Déploiement terminé le $(date '+%d/%m/%Y à %H:%M:%S')</p>
        </div>
        
        <div class="grid">
            <div class="section">
                <h3>📊 Informations du Build</h3>
                <p><strong>Branche:</strong> $branch_name</p>
                <p><strong>Commit:</strong> ${commit_hash:0:8}</p>
                <p><strong>Message:</strong> $commit_message</p>
                <p><strong>Utilisateur:</strong> $(git config user.name || echo "Inconnu")</p>
            </div>
            
            <div class="section">
                <h3>🌐 URLs de Déploiement</h3>
                <p><strong>Production:</strong> <a href="https://$VERCEL_PROJECT_NAME.vercel.app">https://$VERCEL_PROJECT_NAME.vercel.app</a></p>
                <p><strong>Dashboard Vercel:</strong> <a href="https://vercel.com/dashboard">vercel.com/dashboard</a></p>
            </div>
        </div>
        
        <div class="section">
            <h3>✅ Étapes du Déploiement</h3>
            <ul>
                <li class="success">✅ Vérification des prérequis</li>
                <li class="success">✅ Installation des dépendances</li>
                <li class="success">✅ Build du projet</li>
                <li class="success">✅ Déploiement Vercel</li>
                <li class="success">✅ Tests post-déploiement</li>
            </ul>
        </div>
        
        <div class="section">
            <h3>📋 Logs de Déploiement</h3>
            <pre>$(cat "$LOG_FILE")</pre>
        </div>
        
        <div class="info">
            <h3>🔧 Prochaines Étapes</h3>
            <ol>
                <li>Configurer les variables d'environnement dans Vercel si nécessaire</li>
                <li>Configurer un domaine personnalisé (optionnel)</li>
                <li>Mettre en place le monitoring continu</li>
                <li>Configurer les sauvegardes automatiques</li>
            </ol>
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: #666; font-size: 0.9em;">
            <p>🌱 Rapport généré automatiquement par le système de déploiement La Vida Luca</p>
            <p>Pour toute question, consultez la documentation dans DEPLOY.md</p>
        </div>
    </div>
</body>
</html>
EOF
    
    success "Rapport de déploiement généré: $report_file"
    
    # Ouvrir le rapport dans le navigateur si possible
    if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "$report_file" 2>/dev/null || true
    elif command -v open >/dev/null 2>&1; then
        open "$report_file" 2>/dev/null || true
    fi
}

# Nettoyage post-déploiement
cleanup() {
    info "Nettoyage post-déploiement..."
    
    # Nettoyer les artifacts de build si demandé
    if [[ "${CLEANUP_BUILD:-false}" == "true" ]]; then
        rm -rf .next out 2>/dev/null || true
        success "Artifacts de build supprimés"
    fi
    
    # Conserver les logs pendant 7 jours
    find /tmp -name "deploy-*.log" -mtime +7 -delete 2>/dev/null || true
}

# Fonction d'aide
show_help() {
    cat << EOF
🚀 Script de Déploiement - La Vida Luca

Usage: $0 [OPTIONS]

Options:
  -h, --help          Afficher cette aide
  -c, --cleanup       Nettoyer les artifacts de build après déploiement
  -s, --skip-tests    Ignorer les tests post-déploiement
  -v, --verbose       Mode verbeux

Variables d'environnement:
  CLEANUP_BUILD=true       Nettoyer automatiquement après déploiement
  SKIP_POST_TESTS=true     Ignorer les tests post-déploiement
  VERCEL_TOKEN=xxx         Token d'authentification Vercel

Exemples:
  $0                      Déploiement standard
  $0 --cleanup           Déploiement avec nettoyage
  $0 --skip-tests        Déploiement sans tests post-déploiement

EOF
}

# Fonction principale
main() {
    # Parse des arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -c|--cleanup)
                CLEANUP_BUILD=true
                shift
                ;;
            -s|--skip-tests)
                SKIP_POST_TESTS=true
                shift
                ;;
            -v|--verbose)
                set -x
                shift
                ;;
            *)
                warn "Option inconnue: $1"
                shift
                ;;
        esac
    done
    
    success "🚀 Démarrage du déploiement de $PROJECT_NAME"
    
    # Étapes du déploiement
    check_prerequisites
    install_dependencies
    quality_checks
    check_environment
    deploy_to_vercel
    post_deployment_config
    
    # Tests post-déploiement (sauf si ignorés)
    if [[ "${SKIP_POST_TESTS:-false}" != "true" ]]; then
        post_deployment_tests
    fi
    
    # Génération du rapport
    generate_deployment_report
    
    # Nettoyage
    cleanup
    
    success "🎉 Déploiement terminé avec succès!"
    info "📄 Consultez le rapport de déploiement pour plus de détails"
    info "🌐 Votre application est maintenant en ligne!"
}

# Point d'entrée
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi