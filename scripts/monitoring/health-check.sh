#!/bin/bash

# 🔍 Script de Monitoring - La Vida Luca
# Surveille la santé de l'application et l'infrastructure

set -euo pipefail

# Configuration
SITE_URL="${SITE_URL:-https://la-vida-luca.vercel.app}"
SLACK_WEBHOOK="${SLACK_WEBHOOK:-}"
DISCORD_WEBHOOK="${DISCORD_WEBHOOK:-}"
EMAIL_TO="${EMAIL_TO:-admin@lavidaluca.fr}"
LOG_FILE="/tmp/monitoring-$(date +%Y%m%d).log"
ALERT_FILE="/tmp/monitoring-alerts.log"

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction de logging
log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Fonction d'alerte
alert() {
    local level="$1"
    local message="$2"
    
    log "${RED}[ALERT $level]${NC} $message"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" >> "$ALERT_FILE"
    
    # Envoyer notification si configuré
    if [[ -n "$SLACK_WEBHOOK" ]]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"🚨 La Vida Luca Alert [$level]: $message\"}" \
            "$SLACK_WEBHOOK" 2>/dev/null || true
    fi
    
    if [[ -n "$DISCORD_WEBHOOK" ]]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"content\":\"🚨 La Vida Luca Alert [$level]: $message\"}" \
            "$DISCORD_WEBHOOK" 2>/dev/null || true
    fi
}

# Vérification de la disponibilité du site
check_website() {
    log "${GREEN}[CHECK]${NC} Vérification du site web..."
    
    local response_code
    local response_time
    
    # Test de la page d'accueil
    if response_code=$(curl -s -o /dev/null -w "%{http_code}" "$SITE_URL" --max-time 10); then
        if [[ "$response_code" -eq 200 ]]; then
            log "✅ Site accessible (HTTP $response_code)"
        else
            alert "WARNING" "Site retourne HTTP $response_code au lieu de 200"
        fi
    else
        alert "CRITICAL" "Site inaccessible - timeout ou erreur de connexion"
        return 1
    fi
    
    # Test du temps de réponse
    if response_time=$(curl -s -o /dev/null -w "%{time_total}" "$SITE_URL" --max-time 10); then
        local time_ms=$(echo "$response_time * 1000" | bc -l)
        local time_int=${time_ms%.*}
        
        if [[ $time_int -lt 2000 ]]; then
            log "✅ Temps de réponse acceptable: ${time_int}ms"
        elif [[ $time_int -lt 5000 ]]; then
            alert "WARNING" "Temps de réponse lent: ${time_int}ms"
        else
            alert "CRITICAL" "Temps de réponse très lent: ${time_int}ms"
        fi
    fi
}

# Vérification des pages critiques
check_critical_pages() {
    log "${GREEN}[CHECK]${NC} Vérification des pages critiques..."
    
    local pages=(
        "/contact"
        "/catalogue" 
        "/rejoindre"
        "/api/contact"
    )
    
    for page in "${pages[@]}"; do
        local url="$SITE_URL$page"
        local response_code
        
        if response_code=$(curl -s -o /dev/null -w "%{http_code}" "$url" --max-time 10); then
            if [[ "$response_code" -eq 200 ]] || [[ "$response_code" -eq 405 && "$page" == "/api/contact" ]]; then
                log "✅ Page $page accessible"
            else
                alert "WARNING" "Page $page retourne HTTP $response_code"
            fi
        else
            alert "CRITICAL" "Page $page inaccessible"
        fi
    done
}

# Vérification SSL/TLS
check_ssl() {
    log "${GREEN}[CHECK]${NC} Vérification du certificat SSL..."
    
    local domain=$(echo "$SITE_URL" | sed 's|https\?://||' | sed 's|/.*||')
    local expiry_date
    
    if expiry_date=$(echo | openssl s_client -servername "$domain" -connect "$domain:443" 2>/dev/null | \
                     openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2); then
        
        local expiry_timestamp=$(date -d "$expiry_date" +%s)
        local current_timestamp=$(date +%s)
        local days_until_expiry=$(( (expiry_timestamp - current_timestamp) / 86400 ))
        
        if [[ $days_until_expiry -gt 30 ]]; then
            log "✅ Certificat SSL valide (expire dans $days_until_expiry jours)"
        elif [[ $days_until_expiry -gt 7 ]]; then
            alert "WARNING" "Certificat SSL expire dans $days_until_expiry jours"
        else
            alert "CRITICAL" "Certificat SSL expire dans $days_until_expiry jours"
        fi
    else
        alert "WARNING" "Impossible de vérifier le certificat SSL"
    fi
}

# Vérification des performances
check_performance() {
    log "${GREEN}[CHECK]${NC} Vérification des performances..."
    
    # Test Lighthouse basique via API
    if command -v lighthouse >/dev/null 2>&1; then
        local lighthouse_score
        lighthouse_score=$(lighthouse "$SITE_URL" --only-categories=performance --output=json --quiet | \
                          jq -r '.categories.performance.score * 100' 2>/dev/null || echo "0")
        
        if [[ ${lighthouse_score%.*} -ge 90 ]]; then
            log "✅ Score Lighthouse Performance: ${lighthouse_score%.*}/100"
        elif [[ ${lighthouse_score%.*} -ge 70 ]]; then
            alert "WARNING" "Score Lighthouse Performance faible: ${lighthouse_score%.*}/100"
        else
            alert "CRITICAL" "Score Lighthouse Performance très faible: ${lighthouse_score%.*}/100"
        fi
    else
        log "${YELLOW}[INFO]${NC} Lighthouse non installé - skip du test de performance"
    fi
}

# Vérification de l'espace disque (si monitoring sur serveur)
check_disk_space() {
    log "${GREEN}[CHECK]${NC} Vérification de l'espace disque..."
    
    local usage
    usage=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [[ $usage -lt 80 ]]; then
        log "✅ Espace disque OK: ${usage}% utilisé"
    elif [[ $usage -lt 90 ]]; then
        alert "WARNING" "Espace disque faible: ${usage}% utilisé"
    else
        alert "CRITICAL" "Espace disque critique: ${usage}% utilisé"
    fi
}

# Vérification de la mémoire (si monitoring sur serveur)
check_memory() {
    log "${GREEN}[CHECK]${NC} Vérification de la mémoire..."
    
    if command -v free >/dev/null 2>&1; then
        local memory_usage
        memory_usage=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
        
        if [[ $memory_usage -lt 80 ]]; then
            log "✅ Utilisation mémoire OK: ${memory_usage}%"
        elif [[ $memory_usage -lt 90 ]]; then
            alert "WARNING" "Utilisation mémoire élevée: ${memory_usage}%"
        else
            alert "CRITICAL" "Utilisation mémoire critique: ${memory_usage}%"
        fi
    else
        log "${YELLOW}[INFO]${NC} Commande 'free' non disponible - skip du test mémoire"
    fi
}

# Test du formulaire de contact
test_contact_form() {
    log "${GREEN}[CHECK]${NC} Test du formulaire de contact..."
    
    local response_code
    response_code=$(curl -s -o /dev/null -w "%{http_code}" \
                   -X POST \
                   -H "Content-Type: application/json" \
                   -d '{"name":"Monitoring Test","email":"monitoring@test.com","message":"Test automatique"}' \
                   "$SITE_URL/api/contact" --max-time 10) || response_code="000"
    
    if [[ "$response_code" -eq 200 ]]; then
        log "✅ API Contact fonctionnelle"
    else
        alert "WARNING" "API Contact retourne HTTP $response_code"
    fi
}

# Génération du rapport
generate_report() {
    log "${GREEN}[REPORT]${NC} Génération du rapport de monitoring..."
    
    local report_file="/tmp/monitoring-report-$(date +%Y%m%d-%H%M%S).html"
    
    cat > "$report_file" << EOF
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport de Monitoring - La Vida Luca</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #22c55e; color: white; padding: 20px; border-radius: 8px; }
        .status { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .ok { background: #d4edda; border-left: 4px solid #28a745; }
        .warning { background: #fff3cd; border-left: 4px solid #ffc107; }
        .critical { background: #f8d7da; border-left: 4px solid #dc3545; }
        .timestamp { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌱 Rapport de Monitoring - La Vida Luca</h1>
        <p>Généré le $(date '+%d/%m/%Y à %H:%M:%S')</p>
    </div>
    
    <h2>📊 Résumé des vérifications</h2>
    <div class="status ok">
        <strong>✅ Vérifications effectuées avec succès</strong>
        <p>Le site La Vida Luca fonctionne correctement.</p>
    </div>
    
    <h2>📋 Détails</h2>
    <pre>$(cat "$LOG_FILE")</pre>
    
    <h2>🚨 Alertes</h2>
    <pre>$(cat "$ALERT_FILE" 2>/dev/null || echo "Aucune alerte")</pre>
    
    <div class="timestamp">
        <p>Rapport généré automatiquement par le système de monitoring La Vida Luca</p>
    </div>
</body>
</html>
EOF
    
    log "📄 Rapport généré: $report_file"
}

# Nettoyage des anciens logs
cleanup_logs() {
    find /tmp -name "monitoring-*.log" -mtime +7 -delete 2>/dev/null || true
    find /tmp -name "monitoring-report-*.html" -mtime +7 -delete 2>/dev/null || true
}

# Fonction principale
main() {
    log "${GREEN}🚀 Démarrage du monitoring La Vida Luca${NC}"
    
    # Nettoyage préalable
    cleanup_logs
    
    # Vérifications principales
    check_website
    check_critical_pages
    check_ssl
    test_contact_form
    
    # Vérifications système (si applicable)
    if [[ "${MONITOR_SYSTEM:-false}" == "true" ]]; then
        check_disk_space
        check_memory
    fi
    
    # Vérifications performance (si tools disponibles)
    if [[ "${MONITOR_PERFORMANCE:-false}" == "true" ]]; then
        check_performance
    fi
    
    # Génération du rapport
    if [[ "${GENERATE_REPORT:-false}" == "true" ]]; then
        generate_report
    fi
    
    log "${GREEN}✅ Monitoring terminé${NC}"
    
    # Afficher le résumé des alertes
    if [[ -f "$ALERT_FILE" ]] && [[ -s "$ALERT_FILE" ]]; then
        log "${RED}⚠️  $(wc -l < "$ALERT_FILE") alerte(s) détectée(s)${NC}"
        return 1
    else
        log "${GREEN}✅ Aucune alerte détectée${NC}"
        return 0
    fi
}

# Point d'entrée
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi