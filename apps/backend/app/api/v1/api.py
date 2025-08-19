from fastapi import APIRouter
from app.api.v1.endpoints import users, activities

api_router = APIRouter()

# Inclure les routes des différents endpoints
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(activities.router, prefix="/activities", tags=["activities"])

@api_router.get("/")
def read_api_info():
    """Informations sur l'API v1"""
    return {
        "message": "La Vida Luca API v1",
        "version": "1.0.0",
        "endpoints": {
            "users": "/api/v1/users",
            "activities": "/api/v1/activities"
        }
    }