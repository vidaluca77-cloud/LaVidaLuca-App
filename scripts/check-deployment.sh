#!/bin/bash
# Script de vérification des déploiements La Vida Luca

set -e

# Configuration
FRONTEND_URL="https://lavidaluca.fr"
BACKEND_URL="https://lavidaluca-backend.onrender.com"
TIMEOUT=30

echo "🚀 Vérification des déploiements La Vida Luca..."
echo "================================="

# Fonction de vérification HTTP
check_endpoint() {
    local url=$1
    local description=$2
    local expected_status=${3:-200}
    
    echo "Vérification: $description"
    echo "URL: $url"
    
    if response=$(curl -s -w "%{http_code}" --connect-timeout $TIMEOUT "$url" -o /tmp/response.txt); then
        status_code="${response: -3}"
        if [ "$status_code" = "$expected_status" ]; then
            echo "✅ OK ($status_code)"
            echo ""
            return 0
        else
            echo "❌ ERREUR - Code: $status_code"
            echo "Réponse:"
            cat /tmp/response.txt
            echo ""
            return 1
        fi
    else
        echo "❌ ERREUR - Connexion impossible"
        echo ""
        return 1
    fi
}

# Tests Frontend
echo "🌐 FRONTEND CHECKS"
echo "-----------------"
check_endpoint "$FRONTEND_URL" "Page d'accueil"
check_endpoint "$FRONTEND_URL/contact" "Page de contact"

# Tests Backend
echo "🔧 BACKEND CHECKS"
echo "-----------------"
check_endpoint "$BACKEND_URL/health" "Health check backend"
check_endpoint "$BACKEND_URL" "API root"

# Tests API (si accessible)
echo "🔗 API INTEGRATION CHECKS"
echo "-------------------------"
check_endpoint "$FRONTEND_URL/api/health" "Proxy API health"

# Tests de sécurité de base
echo "🔒 SECURITY CHECKS"
echo "-----------------"
echo "Vérification des headers de sécurité..."

# Vérification CSP
if curl -s -I "$FRONTEND_URL" | grep -i "content-security-policy" > /dev/null; then
    echo "✅ Content-Security-Policy présent"
else
    echo "⚠️  Content-Security-Policy manquant"
fi

# Vérification X-Frame-Options
if curl -s -I "$FRONTEND_URL" | grep -i "x-frame-options" > /dev/null; then
    echo "✅ X-Frame-Options présent"
else
    echo "⚠️  X-Frame-Options manquant"
fi

echo ""
echo "🎯 RESUME"
echo "========="
echo "Frontend: $FRONTEND_URL"
echo "Backend: $BACKEND_URL"
echo ""

# Nettoyage
rm -f /tmp/response.txt

echo "✅ Vérifications terminées!"