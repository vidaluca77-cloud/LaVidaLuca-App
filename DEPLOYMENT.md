# 🚀 Guide de Déploiement La Vida Luca

Ce guide vous permettra de déployer l'application La Vida Luca sur Vercel (frontend), Render (backend) et Supabase (base de données).

## 📋 Prérequis

- Compte GitHub
- Compte Vercel
- Compte Render  
- Compte Supabase

## 🗄️ 1. Configuration Supabase (Base de données)

### Créer le projet Supabase
1. Connectez-vous à [supabase.com](https://supabase.com)
2. Créez un nouveau projet
3. Notez votre `Project URL` et `anon public key`

### Importer le schéma
1. Dans le dashboard Supabase, allez dans `SQL Editor`
2. Copiez le contenu de `infra/supabase/schema.sql` et exécutez-le
3. Copiez le contenu de `infra/supabase/seeds.sql` et exécutez-le

### Configurer l'authentification
1. Allez dans `Authentication > Settings`
2. Activez les méthodes de connexion souhaitées (email/password recommandé)
3. Configurez les URLs de redirection selon votre domaine Vercel

## 🖥️ 2. Déploiement Frontend (Vercel)

### Déployer sur Vercel
1. Connectez-vous à [vercel.com](https://vercel.com)
2. Importez votre repository GitHub
3. Vercel détectera automatiquement Next.js
4. Configurez les variables d'environnement :

```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_IA_API_URL=https://your-render-app.onrender.com
NEXT_PUBLIC_CONTACT_EMAIL=contact@la-vida-luca.com
NEXT_PUBLIC_CONTACT_PHONE=+33 1 23 45 67 89
NEXT_PUBLIC_SITE_URL=https://your-app.vercel.app
```

5. Déployez le projet

## 🔧 3. Déploiement Backend (Render)

### Préparer le backend
1. Assurez-vous que le dossier `apps/ia/` contient tous les fichiers nécessaires
2. Le fichier `render.yaml` est déjà configuré

### Déployer sur Render
1. Connectez-vous à [render.com](https://render.com)
2. Créez un nouveau Web Service
3. Connectez votre repository GitHub
4. Configurez :
   - **Root Directory**: `apps/ia`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. Ajoutez les variables d'environnement :

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your_service_role_key
JWT_SECRET=your_secure_jwt_secret_here
ALLOWED_ORIGINS=https://your-app.vercel.app
```

### Obtenir la Service Role Key Supabase
1. Dans Supabase, allez dans `Settings > API`
2. Copiez la `service_role` key (pas la `anon public`)
3. ⚠️ **ATTENTION**: Cette clé est secrète, ne la partagez jamais

## 🔒 4. Configuration de l'authentification

### JWT Secret
Générez une clé secrète forte pour JWT :
```bash
openssl rand -base64 32
```

### Supabase Auth Triggers
Ajoutez cette fonction dans Supabase SQL Editor pour créer automatiquement les profils utilisateur :

```sql
-- Function to handle new user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.users (id, email, full_name, role)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'full_name', ''),
    COALESCE(NEW.raw_user_meta_data->>'role', 'user')
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to call the function on signup
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

## 🔗 5. Liens entre services

### Mettre à jour les URLs
1. Une fois Render déployé, copiez l'URL de votre API
2. Mettez à jour `NEXT_PUBLIC_IA_API_URL` dans Vercel
3. Mettez à jour `ALLOWED_ORIGINS` dans Render avec l'URL Vercel

### Test de connectivité
1. Testez la connexion Vercel → Render → Supabase
2. Vérifiez les logs pour identifier les erreurs éventuelles

## ✅ 6. Vérifications finales

### Tests à effectuer
- [ ] Page d'accueil accessible
- [ ] Inscription utilisateur fonctionne
- [ ] Connexion utilisateur fonctionne
- [ ] Contact form sauvegarde en base
- [ ] API Render répond aux requêtes
- [ ] Catalogue d'activités s'affiche
- [ ] Pages protégées redirigent vers login

### Monitoring
- Configurez les alertes Render pour les erreurs API
- Surveillez les métriques Supabase
- Activez les logs d'erreur Vercel

## 🐛 Dépannage

### Erreurs communes
1. **CORS Error**: Vérifiez `ALLOWED_ORIGINS` dans Render
2. **Auth Error**: Vérifiez les clés Supabase et JWT_SECRET
3. **Build Error**: Vérifiez les dépendances dans package.json/requirements.txt
4. **DB Error**: Vérifiez que le schéma a été importé correctement

### Logs utiles
- Vercel: Functions logs dans le dashboard
- Render: Application logs en temps réel
- Supabase: Auth et Database logs

## 📞 Support

En cas de problème, vérifiez :
1. Les logs de chaque service
2. Les variables d'environnement
3. La connectivité réseau entre services
4. Les politiques RLS Supabase

---

🎉 **Félicitations !** Votre application La Vida Luca est maintenant déployée et prête à accompagner les jeunes dans leur formation agricole et leur insertion sociale.