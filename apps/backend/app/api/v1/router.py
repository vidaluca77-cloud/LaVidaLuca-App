from fastapi import APIRouter
from app.api.v1 import activities, users, auth

api_router = APIRouter()

# Include all route modules
api_router.include_router(activities.router, tags=["activities"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(auth.router, tags=["auth"])