"""
Main API router combining all endpoints
"""
from fastapi import APIRouter

from app.api.endpoints import (
    auth,
    activities,
    bookings,
    users,
    recommendations,
    analytics
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(activities.router, prefix="/activities", tags=["activities"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["ai-recommendations"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])