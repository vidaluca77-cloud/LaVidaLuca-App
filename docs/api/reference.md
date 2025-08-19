# API Reference

## Table des matières

- [Contact API](#contact-api)
- [Recommendations API](#recommendations-api)
- [Health Check API](#health-check-api)

## Contact API

### POST /api/contact

Permet d'envoyer un message de contact depuis le formulaire du site.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | ✅ | Nom de la personne |
| email | string | ✅ | Email de contact |
| message | string | ✅ | Message |
| phone | string | ❌ | Numéro de téléphone |

**Example Request:**

```bash
curl -X POST https://la-vida-luca.vercel.app/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jean Dupont",
    "email": "jean@example.com",
    "message": "Je souhaite rejoindre le projet",
    "phone": "+33123456789"
  }'
```

**Example Response:**

```json
{
  "success": true,
  "message": "Message envoyé avec succès"
}
```

## Recommendations API

### POST /api/recommendations

Obtient des recommendations d'activités personnalisées basées sur le profil utilisateur.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| profile | ProfileObject | ✅ | Profil utilisateur |
| activities | ActivityObject[] | ✅ | Liste des activités disponibles |

**ProfileObject:**

```typescript
interface ProfileObject {
  skills: string[];
  availability: string[];
  location: string;
  preferences: string[];
}
```

**ActivityObject:**

```typescript
interface ActivityObject {
  id: string;
  slug: string;
  title: string;
  category: 'agri' | 'transfo' | 'artisanat' | 'nature' | 'social';
  summary: string;
  duration_min: number;
  skill_tags: string[];
  seasonality: string[];
  safety_level: number;
  materials: string[];
}
```

**Example Request:**

```bash
curl -X POST https://api-ia.render.com/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "profile": {
      "skills": ["patience", "créativité"],
      "availability": ["weekend"],
      "location": "france",
      "preferences": ["artisanat"]
    },
    "activities": [...]
  }'
```

**Example Response:**

```json
{
  "suggestions": [
    {
      "activity": {
        "id": "9",
        "title": "Transformation de la laine",
        "category": "transfo",
        "summary": "Lavage, cardage, petite création textile."
      },
      "score": 0.95,
      "reasons": [
        "Correspond à vos compétences en créativité",
        "Activité disponible le weekend",
        "Niveau de sécurité adapté"
      ]
    }
  ]
}
```

## Health Check API

### GET /api/health

Vérification de l'état de santé des services.

**Example Response:**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "services": {
    "database": "healthy",
    "ai_api": "healthy",
    "cache": "healthy"
  },
  "version": "1.0.0"
}
```