# 🌱 La Vida Luca - Plateforme Interactive

**Plateforme collaborative dédiée à la formation des jeunes en MFR, au développement d'une agriculture nouvelle et à l'insertion sociale.**

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/vidaluca77-cloud/LaVidaLuca-App)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Next.js](https://img.shields.io/badge/Next.js-14.0.4-black.svg)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3.3-blue.svg)](https://www.typescriptlang.org/)

## 🎯 Vision et Mission

### Objectifs principaux
- **Former et accompagner** les jeunes en MFR via un catalogue de 30 activités agricoles, artisanales et environnementales
- **Développer une agriculture nouvelle** : durable, autonome, innovante
- **Favoriser l'insertion sociale** par la pratique et la responsabilité
- **Créer un outil numérique** qui connecte les lieux d'action et les participants

### Valeurs fondamentales
- 🌿 **Durabilité** : Respect de l'environnement et des écosystèmes
- 🤝 **Solidarité** : Entraide et collaboration entre les participants  
- 📚 **Pédagogie** : Apprentissage par la pratique et l'expérience
- 🎨 **Innovation** : Nouvelles approches agricoles et artisanales
- ❤️ **Bienveillance** : Ton et design orientés cœur et mission, pas profit

## 🏗️ Architecture du Projet

### Structure technique
```
LaVidaLuca-App/
├── src/                    # Code source Next.js
│   ├── app/               # App Router (Next.js 14)
│   │   ├── page.tsx       # Page d'accueil avec catalogue d'activités
│   │   ├── contact/       # Formulaire de contact
│   │   ├── catalogue/     # Catalogue des produits/services
│   │   ├── rejoindre/     # Devenir relais La Vida Luca
│   │   └── api/           # Routes API
│   └── components/        # Composants réutilisables
├── apps/                  # Applications tierces
│   ├── web/              # Site Next.js (Vercel) - EN COURS
│   └── ia/               # API FastAPI IA (Render) - PRÉVU
├── infra/                # Infrastructure
│   └── supabase/         # Schémas et migrations DB - PRÉVU
├── docs/                 # Documentation
├── scripts/              # Scripts de monitoring et déploiement
└── public/               # Assets statiques
```

### Stack technologique

**Frontend**
- **Next.js 14** avec App Router
- **TypeScript** pour la sécurité des types
- **Tailwind CSS** pour le styling
- **React 18** avec les derniers hooks

**Backend** (Prévu)
- **FastAPI** pour l'API IA
- **Python** pour les algorithmes d'apprentissage
- **Supabase** pour la base de données et l'authentification

**Déploiement**
- **Vercel** pour le frontend
- **Render** pour l'API IA
- **Supabase** pour la base de données

## 🚀 Installation et Développement

### Prérequis
- Node.js 18+ et npm
- Git

### Installation rapide
```bash
# Cloner le repository
git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
cd LaVidaLuca-App

# Installer les dépendances
npm install

# Lancer en mode développement
npm run dev
```

### Variables d'environnement
Créer un fichier `.env.local` :
```bash
# Supabase (à configurer)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# API IA (à venir)
NEXT_PUBLIC_IA_API_URL=https://your-api.render.com

# Contact
NEXT_PUBLIC_CONTACT_EMAIL=contact@lavidaluca.fr
NEXT_PUBLIC_CONTACT_PHONE=+33123456789

# Sécurité
ALLOWED_ORIGINS=https://your-site.vercel.app
```

### Scripts disponibles
```bash
npm run dev          # Développement local
npm run build        # Build de production
npm run start        # Serveur de production
npm run lint         # Linting du code
npm run monitor      # Scripts de monitoring (à venir)
```

## 📋 Catalogue des 30 Activités MFR

### Catégories d'activités

**🌾 Agriculture (8 activités)**
- Soins aux animaux de ferme
- Tonte & entretien du troupeau  
- Soins basse-cour
- Plantation de cultures
- Initiation maraîchage
- Gestion des clôtures & abris

**🥕 Transformation (6 activités)**
- Fabrication de fromage
- Boulangerie artisanale
- Conserves & confitures
- Fabrication de savon
- Séchage & tisanes
- Fermentation

**🔨 Artisanat (8 activités)**
- Menuiserie de base
- Poterie & céramique
- Tissage & tricot
- Travail du cuir
- Vannerie
- Forge artistique
- Réparation objets
- Panneaux & orientation

**🌳 Nature (4 activités)**
- Entretien de la rivière
- Plantation d'arbres
- Gestion des déchets verts
- Observation de la biodiversité

**👥 Social (4 activités)**
- Accueil des visiteurs
- Animation d'ateliers
- Visites guidées de la ferme
- Ateliers pour enfants

### Niveaux de sécurité
- 🟢 **Niveau 1** : Facile - Activités sécurisées pour débutants
- 🟡 **Niveau 2** : Attention - Surveillance renforcée requise
- 🔴 **Niveau 3** : Expert - Encadrement professionnel obligatoire

## 🎨 Design et UX

### Principes de design
- **Simplicité** : Interface claire et intuitive
- **Accessibilité** : Conforme aux standards WCAG
- **Responsive** : Adapté mobile, tablette et desktop
- **Performance** : Temps de chargement optimisés

### Palette de couleurs
```css
:root {
  --vida-green: #22c55e;    /* Vert nature */
  --vida-earth: #a3744e;    /* Terre */
  --vida-sky: #7dd3fc;      /* Ciel */
  --vida-warm: #fbbf24;     /* Chaleur */
}
```

## 🔧 Configuration et Déploiement

### Déploiement en production

1. **Site web (Vercel)**
   - Build automatique depuis GitHub
   - Variables d'environnement configurées
   - Domaine personnalisé

2. **API IA (Render)** - À venir
   - Déploiement automatique
   - Base de données connectée
   - Monitoring inclus

3. **Base de données (Supabase)** - À configurer
   - Schéma SQL importé
   - Authentification configurée
   - Politiques de sécurité activées

Pour plus de détails : voir [DEPLOY.md](./DEPLOY.md)

## 🛡️ Règles et Pacte

### Principes fondamentaux
- ❌ **Pas de vente directe** sur la plateforme
- 🏡 **"Nos lieux d'action"** au lieu de "Localisation"
- 🎓 **Section "Catalogue d'activités"** réservée aux élèves MFR
- ❤️ **Ton et design orientés cœur et mission**, pas argent
- 🤝 **Respect du pacte initial** dans toutes les décisions

### Modération et gouvernance
- Validation des contenus par l'équipe pédagogique
- Charte d'utilisation respectueuse
- Signalement des abus
- Communauté bienveillante

## 📊 Monitoring et Analytics

### Métriques suivies
- **Performance** : Core Web Vitals, temps de chargement
- **Usage** : Pages vues, parcours utilisateur
- **Qualité** : Taux d'erreur, disponibilité
- **Sécurité** : Tentatives d'intrusion, vulnérabilités

### Outils de monitoring
- Vercel Analytics (intégré)
- Supabase Dashboard (à venir)
- Scripts de surveillance personnalisés (voir `/scripts/`)

## 🤝 Contribution

### Comment contribuer
1. Fork le repository
2. Créer une branche feature (`git checkout -b feature/amelioration`)
3. Commit les changements (`git commit -m 'feat: nouvelle fonctionnalité'`)
4. Push la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

### Guidelines de contribution
- Code en TypeScript avec types stricts
- Tests unitaires pour les nouvelles fonctionnalités
- Documentation à jour
- Respect des conventions ESLint
- Messages de commit conventionnels

### Équipe de développement
- **Développement principal** : [Équipe La Vida Luca]
- **UI/UX** : Design centré utilisateur
- **Backend** : Architecture scalable
- **DevOps** : Déploiement automatisé

## 📞 Support et Contact

### Channels de communication
- **Issues GitHub** : Pour les bugs et demandes de fonctionnalités
- **Discussions** : Pour les questions générales
- **Email** : contact@lavidaluca.fr
- **Documentation** : Wiki du projet

### Feuille de route

**Version 1.0** (Actuelle)
- [x] Interface Next.js de base
- [x] Catalogue d'activités intégré
- [x] Formulaire de contact
- [x] Pages de navigation
- [x] Design responsive

**Version 1.1** (Prochaine)
- [ ] Authentification Supabase
- [ ] Profils utilisateur
- [ ] Système de réservation
- [ ] API IA pour recommandations

**Version 2.0** (Future)
- [ ] Application mobile
- [ ] Système de notation
- [ ] Communauté intégrée
- [ ] Gamification

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](./LICENSE) pour plus de détails.

## 🙏 Remerciements

Merci à tous les contributeurs qui rendent ce projet possible :
- Les équipes pédagogiques des MFR
- Les agriculteurs partenaires
- La communauté open-source
- Les familles et jeunes impliqués

---

**Ensemble, cultivons l'avenir ! 🌱**

---

*Dernière mise à jour : $(date +'%d/%m/%Y') | Version 1.0.0*