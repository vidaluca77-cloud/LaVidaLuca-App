from fastapi import APIRouter
from .endpoints import users, activities, recommendations

api_router = APIRouter()

# Include all endpoint routers
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

api_router.include_router(
    recommendations.router, 
    prefix="/recommendations", 
    tags=["recommendations"]
)