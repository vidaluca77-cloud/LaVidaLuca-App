#!/bin/bash

# Script de validation des configurations de déploiement
# À exécuter avant le déploiement final

set -e

echo "🔍 Validation des configurations de déploiement La Vida Luca"
echo "============================================================"

# Vérifier la structure des fichiers
echo "📁 Vérification de la structure des fichiers..."

required_files=(
    "vercel.json"
    "render.yaml"
    ".env.example"
    "DEPLOY.md"
    "supabase/README.md"
    "supabase/config.json"
    "supabase/migrations/001_initial_schema.sql"
    "supabase/migrations/002_seed_data.sql"
    "apps/ia/main.py"
    "apps/ia/requirements.txt"
    "apps/ia/.env.example"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file manquant"
        exit 1
    fi
done

# Vérifier que Next.js compile
echo ""
echo "🏗️ Test de compilation Next.js..."
if npm run build > /dev/null 2>&1; then
    echo "✅ Build Next.js réussi"
else
    echo "❌ Échec du build Next.js"
    exit 1
fi

# Vérifier les variables d'environnement dans .env.example
echo ""
echo "🔑 Vérification des variables d'environnement..."

required_env_vars=(
    "NEXT_PUBLIC_SUPABASE_URL"
    "NEXT_PUBLIC_SUPABASE_ANON_KEY"
    "NEXT_PUBLIC_IA_API_URL"
    "NEXT_PUBLIC_CONTACT_EMAIL"
    "NEXT_PUBLIC_CONTACT_PHONE"
)

for var in "${required_env_vars[@]}"; do
    if grep -q "$var" .env.example; then
        echo "✅ $var définie"
    else
        echo "❌ $var manquante"
        exit 1
    fi
done

# Vérifier la syntaxe JSON
echo ""
echo "📋 Vérification de la syntaxe JSON..."

json_files=(
    "vercel.json"
    "supabase/config.json"
    "package.json"
)

for file in "${json_files[@]}"; do
    if python3 -m json.tool "$file" > /dev/null 2>&1; then
        echo "✅ $file (JSON valide)"
    else
        echo "❌ $file (JSON invalide)"
        exit 1
    fi
done

# Vérifier la syntaxe YAML
echo ""
echo "📋 Vérification de la syntaxe YAML..."
if python3 -c "import yaml; yaml.safe_load(open('render.yaml'))" > /dev/null 2>&1; then
    echo "✅ render.yaml (YAML valide)"
else
    echo "❌ render.yaml (YAML invalide)"
    exit 1
fi

# Vérifier la syntaxe SQL
echo ""
echo "🗄️ Vérification de base de la syntaxe SQL..."
sql_files=(
    "supabase/migrations/001_initial_schema.sql"
    "supabase/migrations/002_seed_data.sql"
)

for file in "${sql_files[@]}"; do
    if [ -s "$file" ]; then
        echo "✅ $file (non vide)"
    else
        echo "❌ $file (vide ou inexistant)"
        exit 1
    fi
done

# Vérifier que l'API IA a les dépendances
echo ""
echo "🐍 Vérification des dépendances Python..."
required_deps=(
    "fastapi"
    "uvicorn"
    "pydantic"
    "python-dotenv"
    "supabase"
)

for dep in "${required_deps[@]}"; do
    if grep -q "$dep" apps/ia/requirements.txt; then
        echo "✅ $dep"
    else
        echo "❌ $dep manquante"
        exit 1
    fi
done

echo ""
echo "🎉 Toutes les validations sont passées !"
echo ""
echo "📝 Prochaines étapes :"
echo "1. Créer un projet Supabase et récupérer les clés"
echo "2. Configurer les variables d'environnement dans Vercel"
echo "3. Déployer l'API sur Render"
echo "4. Tester le déploiement complet"
echo ""
echo "📖 Consultez DEPLOY.md pour les instructions détaillées"