#!/usr/bin/env python3
"""
Test des Configurations de Déploiement

Ce script teste la validité des fichiers de configuration pour le déploiement.
"""

import json
import yaml
import os
import sys
from pathlib import Path

def test_vercel_json():
    """Teste la validité du fichier vercel.json"""
    try:
        with open('vercel.json', 'r') as f:
            config = json.load(f)
        
        # Vérifications de base
        assert 'version' in config, "Version manquante dans vercel.json"
        assert config['version'] == 2, "Version doit être 2"
        assert 'buildCommand' in config, "buildCommand manquant"
        assert 'outputDirectory' in config, "outputDirectory manquant"
        
        print("✅ vercel.json valide")
        return True
    except Exception as e:
        print(f"❌ vercel.json invalide: {e}")
        return False

def test_render_yaml():
    """Teste la validité du fichier render.yaml"""
    try:
        with open('render.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Vérifications de base
        assert 'services' in config, "Services manquants dans render.yaml"
        assert len(config['services']) > 0, "Au moins un service requis"
        
        service = config['services'][0]
        assert 'type' in service, "Type de service manquant"
        assert service['type'] == 'web', "Type doit être 'web'"
        assert 'runtime' in service, "Runtime manquant"
        
        print("✅ render.yaml valide")
        return True
    except Exception as e:
        print(f"❌ render.yaml invalide: {e}")
        return False

def test_python_api():
    """Teste la validité syntaxique de l'API Python"""
    try:
        import py_compile
        py_compile.compile('apps/ia/main.py', doraise=True)
        print("✅ apps/ia/main.py syntaxe valide")
        return True
    except Exception as e:
        print(f"❌ apps/ia/main.py syntaxe invalide: {e}")
        return False

def test_env_files():
    """Teste la présence et le format des fichiers .env.example"""
    try:
        # Test du .env.example principal
        with open('.env.example', 'r') as f:
            lines = f.readlines()
        
        required_vars = [
            'NEXT_PUBLIC_SUPABASE_URL',
            'NEXT_PUBLIC_SUPABASE_ANON_KEY',
            'NEXT_PUBLIC_IA_API_URL',
            'NEXT_PUBLIC_CONTACT_EMAIL',
            'NEXT_PUBLIC_CONTACT_PHONE',
            'ALLOWED_ORIGINS'
        ]
        
        content = ''.join(lines)
        for var in required_vars:
            assert var in content, f"Variable {var} manquante dans .env.example"
        
        # Test du .env.example de l'API IA
        with open('apps/ia/.env.example', 'r') as f:
            ia_content = f.read()
        
        assert 'SUPABASE_URL' in ia_content, "SUPABASE_URL manquant dans apps/ia/.env.example"
        assert 'ALLOWED_ORIGINS' in ia_content, "ALLOWED_ORIGINS manquant dans apps/ia/.env.example"
        
        print("✅ Fichiers .env.example valides")
        return True
    except Exception as e:
        print(f"❌ Fichiers .env.example invalides: {e}")
        return False

def test_requirements_txt():
    """Teste la présence du fichier requirements.txt"""
    try:
        with open('apps/ia/requirements.txt', 'r') as f:
            content = f.read()
        
        required_packages = ['fastapi', 'uvicorn', 'python-dotenv']
        for package in required_packages:
            assert package in content, f"Package {package} manquant dans requirements.txt"
        
        print("✅ apps/ia/requirements.txt valide")
        return True
    except Exception as e:
        print(f"❌ apps/ia/requirements.txt invalide: {e}")
        return False

def main():
    """Lance tous les tests"""
    print("🧪 Test des configurations de déploiement\n")
    
    tests = [
        test_vercel_json,
        test_render_yaml,
        test_python_api,
        test_env_files,
        test_requirements_txt
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print(f"\n📊 Résultats: {sum(results)}/{len(results)} tests réussis")
    
    if all(results):
        print("🎉 Toutes les configurations sont valides pour le déploiement!")
        return 0
    else:
        print("⚠️  Certaines configurations nécessitent des corrections.")
        return 1

if __name__ == "__main__":
    sys.exit(main())