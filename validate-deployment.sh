#!/bin/bash

# Script de validation de la configuration de déploiement
# Usage: ./validate-deployment.sh

echo "🚀 Validation de la configuration de déploiement La Vida Luca"
echo "============================================================"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction de vérification
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 existe"
        return 0
    else
        echo -e "${RED}✗${NC} $1 manquant"
        return 1
    fi
}

# Fonction de vérification JSON
check_json() {
    if command -v jq >/dev/null 2>&1; then
        if jq empty "$1" >/dev/null 2>&1; then
            echo -e "${GREEN}✓${NC} $1 est un JSON valide"
            return 0
        else
            echo -e "${RED}✗${NC} $1 contient du JSON invalide"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠${NC} jq non installé, impossible de valider $1"
        return 0
    fi
}

echo -e "\n📁 Vérification des fichiers de configuration..."

# Vérifier les fichiers de configuration
errors=0

check_file "vercel.json" && check_json "vercel.json" || errors=$((errors+1))
check_file "apps/backend/render.yaml" || errors=$((errors+1))
check_file "DEPLOYMENT.md" || errors=$((errors+1))
check_file "package.json" && check_json "package.json" || errors=$((errors+1))
check_file "next.config.js" || errors=$((errors+1))

echo -e "\n📦 Vérification des dépendances..."

# Vérifier si les dépendances sont installées
if [ -d "node_modules" ]; then
    echo -e "${GREEN}✓${NC} node_modules existe"
else
    echo -e "${RED}✗${NC} node_modules manquant - exécuter 'npm install'"
    errors=$((errors+1))
fi

echo -e "\n🔧 Vérification des scripts package.json..."

# Vérifier les scripts essentiels
required_scripts=("build" "start" "lint" "backend:dev" "backend:test" "deploy:check")

for script in "${required_scripts[@]}"; do
    if npm run | grep -q "$script"; then
        echo -e "${GREEN}✓${NC} Script '$script' disponible"
    else
        echo -e "${RED}✗${NC} Script '$script' manquant"
        errors=$((errors+1))
    fi
done

echo -e "\n⚙️ Vérification de la configuration Vercel..."

# Vérifier la structure vercel.json
if [ -f "vercel.json" ]; then
    if grep -q '"version"' vercel.json && grep -q '"buildCommand"' vercel.json; then
        echo -e "${GREEN}✓${NC} Configuration Vercel basique présente"
    else
        echo -e "${YELLOW}⚠${NC} Configuration Vercel incomplète"
    fi
fi

echo -e "\n🐍 Vérification de la configuration Render..."

# Vérifier la structure render.yaml
if [ -f "apps/backend/render.yaml" ]; then
    if grep -q 'type: web' apps/backend/render.yaml && grep -q 'name: lavidaluca-backend' apps/backend/render.yaml; then
        echo -e "${GREEN}✓${NC} Configuration Render basique présente"
    else
        echo -e "${YELLOW}⚠${NC} Configuration Render incomplète"
    fi
fi

echo -e "\n📝 Résumé de la validation"
echo "========================="

if [ $errors -eq 0 ]; then
    echo -e "${GREEN}✅ Toutes les vérifications sont passées !${NC}"
    echo -e "La configuration de déploiement est prête."
    echo ""
    echo "Prochaines étapes :"
    echo "1. Vercel : Connecter le repo et déployer"
    echo "2. Render : Connecter le repo et configurer les variables d'env"
    echo "3. Tester le déploiement avec 'npm run deploy:check'"
    exit 0
else
    echo -e "${RED}❌ $errors erreur(s) détectée(s)${NC}"
    echo -e "Veuillez corriger les problèmes avant de déployer."
    exit 1
fi