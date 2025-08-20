from fastapi import APIRouter
from .endpoints import auth, activities, users, suggestions, contacts


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(activities.router, prefix="/activities", tags=["activities"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(suggestions.router, prefix="/suggestions", tags=["suggestions"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])