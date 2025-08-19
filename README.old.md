# LaVidaLuca-App

Plateforme interactive pour le projet La Vida Luca : formation des jeunes en MFR, développement
d’une agriculture nouvelle et insertion sociale. La Vida Luca – Application IA interactive

Plateforme collaborative basée sur IA pour le projet La Vida Luca, dédiée à la formation des jeunes
en MFR, au développement d’une agriculture nouvelle et à l’insertion sociale. Objectif : permettre à
chacun de contribuer à sa manière au projet, dans le respect du pacte initial.

⸻

🎯 Vision • Former et accompagner les jeunes en MFR via un catalogue de 30 activités agricoles,
artisanales et environnementales. • Développer une agriculture nouvelle : durable, autonome,
innovante. • Favoriser l’insertion sociale par la pratique et la responsabilité. • Créer un outil
numérique qui connecte les lieux d’action et les participants.

⸻

📦 Structure du projet • /apps/web → Site Next.js (Vercel) • /apps/ia → API FastAPI pour l’IA
(Render) • /infra/supabase → Base de données et schéma SQL • /assets → Médias (logos, visuels,
documents) • README.md → Documentation

⸻

🚀 Déploiement prévu 1. Vercel – héberge le site web (Next.js) 2. Render – héberge l’IA et l’API 3.
Supabase – base de données et authentification

⸻

🔑 Variables d’environnement

À configurer pour le déploiement :NEXT_PUBLIC_SUPABASE_URL= NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_IA_API_URL= NEXT_PUBLIC_CONTACT_EMAIL= NEXT_PUBLIC_CONTACT_PHONE=
ALLOWED_ORIGINS=https://<site-vercel>.vercel.app

⸻

🛡️ Règles & Pacte • Pas de vente directe sur la plateforme • Page “Nos lieux d’action” au lieu de
“Localisation” • Section “Catalogue d’activités” réservée aux élèves MFR • Ton et design orientés
cœur et mission, pas argent

⸻

📋 Catalogue des 30 activités MFR

Voir /apps/web/pages/catalogue-activites.tsx pour la liste complète et la présentation des
activités.

⸻

👨‍💻 Instructions pour Claude 1. Déployer l’app web (Vercel) 2. Déployer l’IA (Render) 3. Créer et
connecter la base Supabase 4. Importer schema.sql puis seeds.sql 5. Configurer les variables
d’environnement 6. Tester l’accès aux pages protégées
