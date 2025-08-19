from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, activities, bookings, analytics, recommendations

api_router = APIRouter()

# Include all route modules
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(activities.router, prefix="/activities", tags=["activities"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])