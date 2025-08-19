#!/bin/bash

# Script de développement local pour LaVidaLuca-App
# Usage: ./dev.sh [frontend|backend|all]

set -e

function start_frontend() {
    echo "🚀 Démarrage du frontend Next.js..."
    npm install
    npm run dev
}

function start_backend() {
    echo "🚀 Démarrage du backend FastAPI..."
    cd apps/ia
    
    # Vérifier si Python est installé
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 n'est pas installé"
        exit 1
    fi
    
    # Installer les dépendances
    if [ -f "requirements.txt" ]; then
        echo "📦 Installation des dépendances Python..."
        pip install -r requirements.txt
    fi
    
    # Démarrer le serveur
    echo "🌟 API disponible sur: http://localhost:8000"
    echo "📖 Documentation: http://localhost:8000/docs"
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
}

function show_help() {
    echo "Script de développement LaVidaLuca-App"
    echo ""
    echo "Usage:"
    echo "  ./dev.sh frontend    - Démarre uniquement le frontend Next.js"
    echo "  ./dev.sh backend     - Démarre uniquement le backend FastAPI"
    echo "  ./dev.sh all         - Démarre frontend et backend (recommandé)"
    echo "  ./dev.sh help        - Affiche cette aide"
    echo ""
    echo "URLs de développement:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend:  http://localhost:8000"
    echo "  API Docs: http://localhost:8000/docs"
}

case "${1:-all}" in
    "frontend")
        start_frontend
        ;;
    "backend")
        start_backend
        ;;
    "all")
        echo "🎯 Démarrage complet de l'application..."
        echo "📌 Pour démarrer les services séparément:"
        echo "   Frontend: npm run dev"
        echo "   Backend:  cd apps/ia && uvicorn main:app --reload"
        echo ""
        start_frontend
        ;;
    "help")
        show_help
        ;;
    *)
        echo "❌ Option inconnue: $1"
        show_help
        exit 1
        ;;
esac