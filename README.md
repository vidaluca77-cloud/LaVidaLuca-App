# LaVidaLuca-App
Plateforme interactive pour le projet La Vida Luca : formation des jeunes en MFR, développement d'une agriculture nouvelle et insertion sociale.

## 🎯 Vision
• Former et accompagner les jeunes en MFR via un catalogue de 30 activités agricoles, artisanales et environnementales.
• Développer une agriculture nouvelle : durable, autonome, innovante.
• Favoriser l'insertion sociale par la pratique et la responsabilité.
• Créer un outil numérique qui connecte les lieux d'action et les participants.

## 📦 Structure du projet
• `/apps/web` → Site Next.js (Vercel)
• `/apps/ia` → API FastAPI pour l'IA (Render)
• `/infra/supabase` → Base de données et schéma SQL
• `/assets` → Médias (logos, visuels, documents)
• `README.md` → Documentation
• `DEPLOYMENT.md` → Guide de déploiement détaillé

## 🚀 Déploiement

### Configuration rapide
1. **Vercel** – héberge le site web (Next.js)
2. **Render** – héberge l'IA et l'API (FastAPI)
3. **Supabase** – base de données et authentification

### Variables d'environnement à configurer

**Frontend (Vercel):**
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_IA_API_URL=https://your-render-service.onrender.com
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789
```

**Backend (Render):**
```env
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
DATABASE_URL=postgresql://... # Auto-configuré par Render
SECRET_KEY=your-secret-key
ENVIRONMENT=production
```

### Étapes de déploiement
1. Déployer l'app web (Vercel) → Connecter repo + configurer variables
2. Déployer l'IA (Render) → Utiliser `render.yaml`
3. Créer et connecter la base Supabase → Projet + Auth
4. Importer `schema.sql` puis `seeds.sql` → Dans SQL Editor
5. Configurer les variables d'environnement → Dans les dashboards
6. Tester l'accès aux pages protégées → Inscription/connexion

📋 **Voir `DEPLOYMENT.md` pour le guide détaillé.**

## 📋 Catalogue des 30 activités MFR

**Agriculture (6):** Soins aux animaux, traite, pâtures, cultures, maraîchage, clôtures
**Transformation (6):** Fromage, conserves, laine, boulangerie, charcuterie, brassage  
**Artisanat (6):** Poterie, outils, menuiserie, peinture, espaces verts, signalétique
**Nature (6):** Rivière, haies, forêt, compost, faune, nichoirs
**Social (6):** Portes ouvertes, visites, ateliers enfants, cuisine, goûter, marché

## 🛡️ Règles & Pacte
• Pas de vente directe sur la plateforme
• Page "Nos lieux d'action" au lieu de "Localisation"
• Section "Catalogue d'activités" réservée aux élèves MFR
• Ton et design orientés cœur et mission, pas argent

## 🔧 Développement Local

```bash
# Frontend
npm install
npm run dev

# Backend  
cd apps/ia
pip install -r requirements.txt
uvicorn main:app --reload
```

## 📱 URLs de Production
- **Frontend:** https://la-vida-luca.vercel.app
- **API Backend:** https://lavidaluca-api.onrender.com
- **Documentation API:** https://lavidaluca-api.onrender.com/docs