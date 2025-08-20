"""
Gamification system routes for La Vida Luca.
Handles achievements, points, badges, and leaderboards.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from ..database import get_db
from ..auth.dependencies import get_current_user
from ..models.user import User
from ..models.gamification import Achievement, UserAchievement, Badge, UserBadge
from ..schemas.gamification import (
    AchievementCreate, AchievementResponse, UserAchievementResponse,
    BadgeCreate, BadgeResponse, UserBadgeResponse,
    LeaderboardResponse, UserStatsResponse
)
from ..services.gamification_service import gamification_service
from ..monitoring import context_logger

router = APIRouter()

# Achievements endpoints
@router.get("/achievements", response_model=List[AchievementResponse])
async def get_achievements(
    category: Optional[str] = Query(None, description="Filter by category"),
    completed_only: bool = Query(False, description="Show only completed achievements"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all achievements, optionally filtered by category or completion status."""
    context_logger.info("Fetching achievements", user_id=current_user.id, category=category)
    
    try:
        achievements = await gamification_service.get_user_achievements(
            db, current_user.id, category, completed_only
        )
        return achievements
    except Exception as e:
        context_logger.error("Error fetching achievements", error=str(e))
        raise HTTPException(status_code=500, detail="Error fetching achievements")

@router.post("/achievements/{achievement_id}/claim")
async def claim_achievement(
    achievement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Claim an achievement and award points."""
    context_logger.info("Claiming achievement", user_id=current_user.id, achievement_id=achievement_id)
    
    try:
        result = await gamification_service.claim_achievement(db, current_user.id, achievement_id)
        if not result:
            raise HTTPException(
                status_code=400, 
                detail="Achievement already claimed or not eligible"
            )
        return {"message": "Achievement claimed successfully", "points_awarded": result}
    except Exception as e:
        context_logger.error("Error claiming achievement", error=str(e))
        raise HTTPException(status_code=500, detail="Error claiming achievement")

# Badges endpoints
@router.get("/badges", response_model=List[BadgeResponse])
async def get_badges(
    earned_only: bool = Query(False, description="Show only earned badges"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all badges, optionally filtered by earned status."""
    context_logger.info("Fetching badges", user_id=current_user.id, earned_only=earned_only)
    
    try:
        badges = await gamification_service.get_user_badges(db, current_user.id, earned_only)
        return badges
    except Exception as e:
        context_logger.error("Error fetching badges", error=str(e))
        raise HTTPException(status_code=500, detail="Error fetching badges")

# User stats and progress
@router.get("/stats", response_model=UserStatsResponse)
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's gamification statistics."""
    context_logger.info("Fetching user stats", user_id=current_user.id)
    
    try:
        stats = await gamification_service.get_user_stats(db, current_user.id)
        return stats
    except Exception as e:
        context_logger.error("Error fetching user stats", error=str(e))
        raise HTTPException(status_code=500, detail="Error fetching user stats")

@router.get("/leaderboard", response_model=List[LeaderboardResponse])
async def get_leaderboard(
    period: str = Query("monthly", regex="^(weekly|monthly|all_time)$"),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get leaderboard for specified period."""
    context_logger.info("Fetching leaderboard", period=period, limit=limit)
    
    try:
        leaderboard = await gamification_service.get_leaderboard(db, period, limit)
        return leaderboard
    except Exception as e:
        context_logger.error("Error fetching leaderboard", error=str(e))
        raise HTTPException(status_code=500, detail="Error fetching leaderboard")

# Points system
@router.post("/points/award")
async def award_points(
    points: int,
    reason: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Award points to current user for an action."""
    context_logger.info("Awarding points", user_id=current_user.id, points=points, reason=reason)
    
    try:
        new_total = await gamification_service.award_points(db, current_user.id, points, reason)
        return {
            "message": f"Awarded {points} points",
            "reason": reason,
            "new_total": new_total
        }
    except Exception as e:
        context_logger.error("Error awarding points", error=str(e))
        raise HTTPException(status_code=500, detail="Error awarding points")

# Activity tracking for achievements
@router.post("/track-activity")
async def track_activity(
    activity_type: str,
    activity_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Track user activity for achievement progress."""
    context_logger.info("Tracking activity", user_id=current_user.id, activity_type=activity_type)
    
    try:
        achievements_unlocked = await gamification_service.track_activity(
            db, current_user.id, activity_type, activity_data
        )
        
        return {
            "message": "Activity tracked successfully",
            "achievements_unlocked": achievements_unlocked
        }
    except Exception as e:
        context_logger.error("Error tracking activity", error=str(e))
        raise HTTPException(status_code=500, detail="Error tracking activity")

# Admin endpoints (for creating achievements/badges)
@router.post("/admin/achievements", response_model=AchievementResponse)
async def create_achievement(
    achievement: AchievementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new achievement (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    context_logger.info("Creating achievement", admin_id=current_user.id, name=achievement.name)
    
    try:
        new_achievement = await gamification_service.create_achievement(db, achievement)
        return new_achievement
    except Exception as e:
        context_logger.error("Error creating achievement", error=str(e))
        raise HTTPException(status_code=500, detail="Error creating achievement")

@router.post("/admin/badges", response_model=BadgeResponse)
async def create_badge(
    badge: BadgeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new badge (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    context_logger.info("Creating badge", admin_id=current_user.id, name=badge.name)
    
    try:
        new_badge = await gamification_service.create_badge(db, badge)
        return new_badge
    except Exception as e:
        context_logger.error("Error creating badge", error=str(e))
        raise HTTPException(status_code=500, detail="Error creating badge")