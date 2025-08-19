"""
API v1 router configuration.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import users, activities

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    users.router, 
    prefix="/users", 
    tags=["users"]
)

api_router.include_router(
    activities.router, 
    prefix="/activities", 
    tags=["activities"]
)