"""
API v1 router
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, activities, recommendations

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(activities.router, prefix="/activities", tags=["activities"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])