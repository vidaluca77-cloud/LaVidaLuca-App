# Documentation API

## APIs disponibles

### Frontend API Routes

#### Contact API
- **Endpoint**: `POST /api/contact`
- **Description**: Envoi de messages de contact
- **Body**:
  ```json
  {
    "name": "string",
    "email": "string", 
    "message": "string",
    "phone": "string (optional)"
  }
  ```
- **Response**: 
  ```json
  {
    "success": true,
    "message": "Message envoyé avec succès"
  }
  ```

### Backend IA API

#### Recommandations d'activités
- **Endpoint**: `POST /api/recommendations`
- **Description**: Obtenir des recommandations personnalisées
- **Body**:
  ```json
  {
    "profile": {
      "skills": ["string"],
      "availability": ["string"],
      "location": "string",
      "preferences": ["string"]
    },
    "activities": [
      {
        "id": "string",
        "category": "agri|transfo|artisanat|nature|social",
        "skill_tags": ["string"],
        "duration_min": 0,
        "safety_level": 0,
        "seasonality": ["string"]
      }
    ]
  }
  ```
- **Response**:
  ```json
  {
    "suggestions": [
      {
        "activity": {...},
        "score": 0.95,
        "reasons": ["string"]
      }
    ]
  }
  ```

## Authentication

Les APIs utilisent l'authentification Supabase pour les endpoints protégés.

Headers requis:
```
Authorization: Bearer <supabase_token>
```

## Rate Limiting

- 100 requêtes par minute par IP
- 1000 requêtes par heure par utilisateur authentifié

## Error Handling

Format standard des erreurs:
```json
{
  "error": true,
  "message": "Description de l'erreur",
  "code": "ERROR_CODE",
  "details": {}
}
```

## Codes d'erreur

- `400` - Bad Request
- `401` - Unauthorized  
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error