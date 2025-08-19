# Guide de Déploiement - La Vida Luca App

## 🚀 Instructions de Déploiement

### 1. Déploiement Frontend (Vercel)

#### Configuration Vercel
1. Connecter le repository GitHub à Vercel
2. Configurer les variables d'environnement dans Vercel Dashboard :
   ```
   NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
   NEXT_PUBLIC_IA_API_URL=https://your-render-service.onrender.com
   NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
   NEXT_PUBLIC_CONTACT_PHONE=+33123456789
   ```

#### Commandes de déploiement
```bash
# Build & Deploy automatique via Git push
git push origin main

# Ou déploiement manuel via Vercel CLI
npm install -g vercel
vercel --prod
```

### 2. Déploiement Backend (Render)

#### Configuration Render
1. Connecter le repository à Render
2. Le fichier `render.yaml` configure automatiquement :
   - Service web Python
   - Base de données PostgreSQL
   - Variables d'environnement

#### Variables d'environnement Render
Configurer dans le dashboard Render :
```
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
SECRET_KEY=generate-a-secure-key
ENVIRONMENT=production
```

### 3. Configuration Base de Données (Supabase)

#### Étapes d'installation
1. Créer un projet Supabase
2. Exécuter les fichiers SQL :
   ```sql
   -- 1. Créer le schéma
   -- Copier/coller le contenu de infra/supabase/schema.sql
   
   -- 2. Insérer les données initiales
   -- Copier/coller le contenu de infra/supabase/seeds.sql
   ```

3. Configurer l'authentification :
   - Activer Email/Password auth
   - Configurer les URLs de redirection
   - Personnaliser les templates d'email

#### Configuration RLS (Row Level Security)
Les politiques sont automatiquement créées par le schema SQL pour :
- Accès sécurisé aux profils utilisateurs
- Protection des données personnelles
- Accès public aux activités

### 4. Tests de Déploiement

#### Vérifications Frontend
```bash
# Test local
npm run dev
# Visiter: http://localhost:3000

# Test build production
npm run build
npm run start
```

#### Vérifications Backend
```bash
# Test local API
cd apps/ia
pip install -r requirements.txt
uvicorn main:app --reload
# Visiter: http://localhost:8000/docs
```

#### Tests d'intégration
1. Tester l'inscription/connexion utilisateur
2. Vérifier les recommandations IA
3. Tester le formulaire de contact
4. Valider les pages protégées

### 5. Monitoring et Maintenance

#### Logs et Monitoring
- **Vercel** : Dashboard > Functions > Logs
- **Render** : Dashboard > Logs
- **Supabase** : Dashboard > Logs

#### Mise à jour des dépendances
```bash
# Frontend
npm update

# Backend
pip install -r requirements.txt --upgrade
```

### 6. URLs Finales

Une fois déployé :
- **Frontend** : `https://your-app.vercel.app`
- **Backend API** : `https://your-service.onrender.com`
- **Documentation API** : `https://your-service.onrender.com/docs`
- **Base de données** : Dashboard Supabase

### 7. Variables d'Environnement Récapitulatif

#### Vercel (Frontend)
```env
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_IA_API_URL=
NEXT_PUBLIC_CONTACT_EMAIL=
NEXT_PUBLIC_CONTACT_PHONE=
```

#### Render (Backend)
```env
ALLOWED_ORIGINS=
DATABASE_URL=    # Auto-configuré
SECRET_KEY=      # Généré automatiquement
ENVIRONMENT=production
```

### 8. Sécurité

#### Points de vigilance
- [ ] Variables sensibles jamais dans le code
- [ ] CORS configuré restrictement
- [ ] RLS activé sur Supabase
- [ ] HTTPS uniquement en production
- [ ] Validation des inputs côté serveur

#### Secrets à ne jamais exposer
- Clés privées Supabase
- Tokens d'API tiers
- Mots de passe base de données
- Clés de session

---

## 🔧 Dépannage

### Erreurs communes

**Build Next.js échoue**
```bash
# Nettoyer le cache
rm -rf .next
npm run build
```

**API CORS errors**
- Vérifier `ALLOWED_ORIGINS` dans Render
- Contrôler la configuration CORS dans `main.py`

**Base de données inaccessible**
- Vérifier les variables d'environnement Supabase
- Contrôler les politiques RLS

**Variables d'environnement non prises en compte**
- Redémarrer les services après modification
- Vérifier la syntaxe des noms de variables