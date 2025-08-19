# 📡 Documentation API - La Vida Luca

## Vue d'ensemble

L'API La Vida Luca fournit des endpoints pour interagir avec la plateforme de formation agricole et artisanale. Cette API est construite avec Next.js API Routes et sera étendue avec FastAPI pour les fonctionnalités IA.

## 🏗️ Architecture API

### Stack technique actuel
- **Framework** : Next.js 14 API Routes
- **Runtime** : Node.js 18+
- **Base de données** : Supabase (PostgreSQL) - *à venir*
- **Authentification** : Supabase Auth - *à venir*
- **Validation** : TypeScript + Zod - *à implémenter*

### Stack technique prévu
- **API IA** : FastAPI (Python)
- **ML/AI** : TensorFlow/PyTorch pour les recommandations
- **Cache** : Redis pour les performances
- **Queue** : Celery pour les tâches asynchrones

## 🔗 Endpoints Disponibles

### Base URL
- **Production** : `https://la-vida-luca.vercel.app/api`
- **Développement** : `http://localhost:3000/api`

---

## 📝 Contact API

### `POST /api/contact`

Envoie un message de contact depuis le formulaire du site.

#### Paramètres de requête

```json
{
  "name": "string (requis, 2-100 caractères)",
  "email": "string (requis, format email valide)",
  "message": "string (requis, 10-1000 caractères)"
}
```

#### Exemple de requête

```bash
curl -X POST https://la-vida-luca.vercel.app/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jean Dupont",
    "email": "jean.dupont@example.com",
    "message": "Bonjour, je souhaite rejoindre votre réseau de fermes pédagogiques."
  }'
```

#### Réponses

**Succès (200 OK)**
```json
{
  "ok": true,
  "message": "Message envoyé avec succès"
}
```

**Erreur de validation (400 Bad Request)**
```json
{
  "error": "Validation failed",
  "details": {
    "name": "Le nom est requis",
    "email": "Format d'email invalide",
    "message": "Le message doit contenir au moins 10 caractères"
  }
}
```

**Erreur serveur (500 Internal Server Error)**
```json
{
  "error": "Erreur interne du serveur"
}
```

#### Implémentation actuelle

```typescript
// src/app/api/contact/route.ts
import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    
    // TODO: Validation avec Zod
    // TODO: Sanitisation des données
    // TODO: Envoi par email/Discord/Slack
    // TODO: Sauvegarde en base de données
    
    console.log("Contact:", body);
    
    return NextResponse.json({ ok: true });
  } catch (error) {
    return NextResponse.json(
      { error: "Erreur lors du traitement" },
      { status: 500 }
    );
  }
}
```

---

## 🎯 API Activités (Planifiée)

### `GET /api/activities`

Récupère la liste des activités disponibles.

#### Paramètres de requête (optionnels)

| Paramètre | Type | Description |
|-----------|------|-------------|
| `category` | string | Filtrer par catégorie (`agri`, `transfo`, `artisanat`, `nature`, `social`) |
| `safety_level` | number | Filtrer par niveau de sécurité (1, 2, 3) |
| `duration_min` | number | Durée minimale en minutes |
| `duration_max` | number | Durée maximale en minutes |
| `seasonality` | string | Saison (`printemps`, `ete`, `automne`, `hiver`) |
| `page` | number | Numéro de page (défaut: 1) |
| `limit` | number | Nombre d'éléments par page (défaut: 20, max: 100) |

#### Exemple de requête

```bash
curl "https://la-vida-luca.vercel.app/api/activities?category=agri&safety_level=1"
```

#### Réponse

```json
{
  "activities": [
    {
      "id": "1",
      "slug": "soins-animaux",
      "title": "Soins aux animaux de ferme",
      "category": "agri",
      "summary": "Alimentation, observation, soins de base.",
      "description": "Apprendre les gestes essentiels pour s'occuper des animaux de ferme...",
      "duration_min": 60,
      "skill_tags": ["patience", "observation"],
      "seasonality": ["toutes"],
      "safety_level": 1,
      "materials": ["bottes", "gants"],
      "prerequisites": [],
      "learning_objectives": [
        "Identifier les besoins nutritionnels",
        "Reconnaître les signes de maladie",
        "Appliquer les gestes de soin"
      ],
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-20T15:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 30,
    "pages": 2
  },
  "filters": {
    "category": "agri",
    "safety_level": 1
  }
}
```

### `GET /api/activities/:id`

Récupère les détails d'une activité spécifique.

#### Paramètres d'URL

| Paramètre | Type | Description |
|-----------|------|-------------|
| `id` | string | ID ou slug de l'activité |

#### Réponse

```json
{
  "activity": {
    "id": "1",
    "slug": "soins-animaux",
    "title": "Soins aux animaux de ferme",
    "category": "agri",
    "summary": "Alimentation, observation, soins de base.",
    "description": "Description complète de l'activité...",
    "duration_min": 60,
    "skill_tags": ["patience", "observation"],
    "seasonality": ["toutes"],
    "safety_level": 1,
    "materials": ["bottes", "gants"],
    "prerequisites": [],
    "steps": [
      {
        "order": 1,
        "title": "Préparation",
        "description": "Préparer le matériel nécessaire",
        "duration_min": 10
      },
      {
        "order": 2,
        "title": "Observation",
        "description": "Observer le comportement des animaux",
        "duration_min": 20
      }
    ],
    "safety_guide": {
      "rules": [
        "Respecter les consignes de l'encadrant",
        "Porter les équipements de protection"
      ],
      "checklist": [
        "Vérifier la présence de l'encadrant",
        "S'assurer d'avoir tout le matériel"
      ]
    },
    "resources": [
      {
        "type": "video",
        "title": "Introduction aux soins",
        "url": "https://example.com/video"
      },
      {
        "type": "document",
        "title": "Guide pratique",
        "url": "https://example.com/guide.pdf"
      }
    ]
  }
}
```

---

## 👤 API Utilisateurs (Planifiée)

### Authentification

L'API utilisera Supabase Auth pour l'authentification. Tous les endpoints protégés nécessiteront un token JWT.

#### Headers requis pour les endpoints protégés

```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### `POST /api/auth/register`

Inscription d'un nouveau utilisateur.

#### Paramètres

```json
{
  "email": "string (requis)",
  "password": "string (requis, min 8 caractères)",
  "name": "string (requis)",
  "role": "string (optionnel, défaut: 'student')"
}
```

### `POST /api/auth/login`

Connexion utilisateur.

#### Paramètres

```json
{
  "email": "string (requis)",
  "password": "string (requis)"
}
```

### `GET /api/user/profile`

Récupère le profil de l'utilisateur connecté.

### `PUT /api/user/profile`

Met à jour le profil utilisateur.

---

## 🤖 API IA (Planifiée - FastAPI)

### Base URL
- **Production** : `https://la-vida-luca-ia.render.com/api/v1`
- **Développement** : `http://localhost:8000/api/v1`

### `POST /api/v1/recommendations`

Obtient des recommandations d'activités personnalisées.

#### Paramètres

```json
{
  "user_profile": {
    "skills": ["string"],
    "preferences": ["string"],
    "experience_level": "beginner | intermediate | advanced",
    "available_time": "number (minutes)",
    "location": "string"
  },
  "constraints": {
    "seasonality": ["string"],
    "safety_level_max": "number",
    "categories": ["string"]
  }
}
```

#### Réponse

```json
{
  "recommendations": [
    {
      "activity": {
        "id": "1",
        "title": "Soins aux animaux de ferme",
        "category": "agri"
      },
      "score": 0.85,
      "reasons": [
        "Correspond à votre niveau débutant",
        "Activité de saison",
        "Matche vos préférences"
      ],
      "confidence": 0.92
    }
  ],
  "metadata": {
    "algorithm_version": "1.0.0",
    "processed_at": "2024-01-20T15:30:00Z",
    "processing_time_ms": 150
  }
}
```

---

## 📊 API Analytics (Planifiée)

### `GET /api/analytics/activities/popular`

Activités les plus populaires.

### `GET /api/analytics/users/engagement`

Métriques d'engagement utilisateur.

---

## 🔒 Sécurité

### Authentification
- JWT tokens via Supabase Auth
- Refresh tokens pour les sessions longues
- Rate limiting par IP et par utilisateur

### Validation des données
- Validation stricte avec Zod
- Sanitisation des inputs
- Protection contre les injections

### Rate Limiting

| Endpoint | Limite |
|----------|--------|
| `/api/contact` | 5 requêtes/minute |
| `/api/activities` | 100 requêtes/minute |
| `/api/auth/*` | 10 requêtes/minute |
| `/api/v1/recommendations` | 20 requêtes/minute |

### CORS

```javascript
// Configuration CORS
const allowedOrigins = [
  'https://la-vida-luca.vercel.app',
  'https://lavidaluca.fr',
  process.env.NODE_ENV === 'development' ? 'http://localhost:3000' : null
].filter(Boolean);
```

---

## 🐛 Gestion des erreurs

### Format standard des erreurs

```json
{
  "error": "string (message d'erreur)",
  "code": "string (code d'erreur)",
  "details": "object (détails optionnels)",
  "timestamp": "string (ISO 8601)",
  "request_id": "string (UUID)"
}
```

### Codes d'erreur communs

| Code | Status | Description |
|------|--------|-------------|
| `VALIDATION_ERROR` | 400 | Données invalides |
| `UNAUTHORIZED` | 401 | Authentification requise |
| `FORBIDDEN` | 403 | Permissions insuffisantes |
| `NOT_FOUND` | 404 | Ressource introuvable |
| `RATE_LIMITED` | 429 | Trop de requêtes |
| `INTERNAL_ERROR` | 500 | Erreur serveur |

---

## 🧪 Tests

### Tests automatisés
- Tests unitaires avec Jest
- Tests d'intégration avec Supertest
- Tests E2E avec Playwright

### Environnement de test
- Base de données de test Supabase
- Mocks pour les services externes
- CI/CD avec GitHub Actions

---

## 📈 Monitoring

### Métriques surveillées
- Temps de réponse par endpoint
- Taux d'erreur par statut
- Utilisation des ressources
- Performances des requêtes DB

### Outils de monitoring
- Vercel Analytics
- Supabase Dashboard
- Custom scripts dans `/scripts/monitoring/`

---

## 🔄 Versioning

### Stratégie de versioning
- **API v1** : Version actuelle stable
- **API v2** : Prochaines fonctionnalités majeures
- Rétrocompatibilité maintenue pendant 12 mois

### Headers de version

```
Accept: application/json
API-Version: v1
```

---

## 📚 Exemples d'utilisation

### JavaScript/TypeScript

```typescript
// Client API typé
import { LaVidaLucaAPI } from '@/lib/api';

const api = new LaVidaLucaAPI({
  baseURL: 'https://la-vida-luca.vercel.app/api',
  apiKey: process.env.API_KEY
});

// Envoyer un contact
const contact = await api.contact.send({
  name: 'Jean Dupont',
  email: 'jean@example.com',
  message: 'Intéressé par le programme'
});

// Récupérer les activités
const activities = await api.activities.list({
  category: 'agri',
  safety_level: 1
});
```

### Python

```python
import requests

# Envoyer un contact
response = requests.post(
    'https://la-vida-luca.vercel.app/api/contact',
    json={
        'name': 'Jean Dupont',
        'email': 'jean@example.com',
        'message': 'Intéressé par le programme'
    }
)

if response.status_code == 200:
    print("Message envoyé avec succès")
```

---

## 🚀 Feuille de route

### Version 1.1 (Q2 2024)
- [ ] Authentification Supabase
- [ ] API Activités complète
- [ ] Validation avec Zod
- [ ] Rate limiting

### Version 1.2 (Q3 2024)
- [ ] API IA avec FastAPI
- [ ] Recommandations personnalisées
- [ ] Analytics avancés
- [ ] WebSockets pour temps réel

### Version 2.0 (Q4 2024)
- [ ] API mobile dédiée
- [ ] Système de notifications
- [ ] API de gamification
- [ ] Intégrations tierces

---

## 📞 Support

### Documentation
- **Guide complet** : [DEPLOY.md](../DEPLOY.md)
- **README** : [README.md](../README.md)

### Contact technique
- **Issues GitHub** : Pour les bugs et améliorations
- **Email** : dev@lavidaluca.fr
- **Discord** : Serveur de développement

---

*Dernière mise à jour : $(date +'%d/%m/%Y') | Version API : 1.0.0*