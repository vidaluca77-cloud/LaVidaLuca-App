"""
API router for all v1 endpoints.
"""
from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .activities import router as activities_router
from .recommendations import router as recommendations_router

api_router = APIRouter()

# Include all routers with their prefixes
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(activities_router, prefix="/activities", tags=["Activities"])
api_router.include_router(recommendations_router, prefix="/recommendations", tags=["Recommendations"])