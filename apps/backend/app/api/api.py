from fastapi import APIRouter
from .endpoints import auth, activities, users, suggestions, contacts, agri_assistant


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(activities.router, prefix="/activities", tags=["activities"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(suggestions.router, prefix="/suggestions", tags=["suggestions"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
api_router.include_router(agri_assistant.router, prefix="/agri-assistant", tags=["agri-assistant"])