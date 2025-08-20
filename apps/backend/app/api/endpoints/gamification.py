"""
Gamification API endpoints for skills, achievements, and user progress.
"""

from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from ...db.database import get_db
from ...api.deps import get_current_active_user
from ...models.models import User, Skill, Achievement, UserSkill, UserAchievement, ActivityCompletion
from ...schemas.schemas import (
    Skill as SkillSchema, SkillCreate,
    Achievement as AchievementSchema, AchievementCreate,
    UserSkill as UserSkillSchema,
    UserAchievement as UserAchievementSchema,
    ActivityCompletion as ActivityCompletionSchema, ActivityCompletionCreate,
    UserProgress as UserProgressSchema
)
from ...services.gamification_service import GamificationService

router = APIRouter()


# Skills endpoints
@router.get("/skills/", response_model=List[SkillSchema], summary="Get all skills")
def get_skills(
    category: str = Query(None, description="Filter by skill category"),
    db: Session = Depends(get_db)
):
    """Get all available skills, optionally filtered by category."""
    query = db.query(Skill)
    if category:
        query = query.filter(Skill.category == category)
    
    skills = query.all()
    return skills


@router.get("/skills/categories/", response_model=List[str], summary="Get skill categories")
def get_skill_categories(db: Session = Depends(get_db)):
    """Get all available skill categories."""
    categories = db.query(Skill.category).distinct().all()
    return [cat[0] for cat in categories]


@router.post("/skills/", response_model=SkillSchema, summary="Create new skill")
def create_skill(
    skill: SkillCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new skill (admin only)."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Check if skill already exists
    existing_skill = db.query(Skill).filter(Skill.name == skill.name).first()
    if existing_skill:
        raise HTTPException(status_code=400, detail="Skill already exists")
    
    db_skill = Skill(**skill.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


# Achievements endpoints
@router.get("/achievements/", response_model=List[AchievementSchema], summary="Get all achievements")
def get_achievements(
    category: str = Query(None, description="Filter by achievement category"),
    db: Session = Depends(get_db)
):
    """Get all available achievements, optionally filtered by category."""
    query = db.query(Achievement).filter(Achievement.is_active == True)
    if category:
        query = query.filter(Achievement.category == category)
    
    achievements = query.all()
    return achievements


@router.post("/achievements/", response_model=AchievementSchema, summary="Create new achievement")
def create_achievement(
    achievement: AchievementCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new achievement (admin only)."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Check if achievement already exists
    existing_achievement = db.query(Achievement).filter(Achievement.name == achievement.name).first()
    if existing_achievement:
        raise HTTPException(status_code=400, detail="Achievement already exists")
    
    db_achievement = Achievement(**achievement.model_dump())
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement


# User progress and stats endpoints
@router.get("/users/me/stats", summary="Get current user's gamification stats")
def get_user_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive gamification stats for the current user."""
    gamification_service = GamificationService(db)
    return gamification_service.get_user_stats(current_user.id)


@router.get("/users/me/skills", response_model=List[UserSkillSchema], summary="Get current user's skills")
def get_user_skills(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all skills acquired by the current user."""
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()
    return user_skills


@router.get("/users/me/achievements", response_model=List[UserAchievementSchema], summary="Get current user's achievements")
def get_user_achievements(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all achievements earned by the current user."""
    user_achievements = db.query(UserAchievement).filter(UserAchievement.user_id == current_user.id).all()
    return user_achievements


@router.get("/users/me/completions", response_model=List[ActivityCompletionSchema], summary="Get current user's completed activities")
def get_user_completions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all activities completed by the current user."""
    completions = db.query(ActivityCompletion).filter(ActivityCompletion.user_id == current_user.id).all()
    return completions


@router.post("/activities/{activity_id}/complete", summary="Mark activity as completed")
def complete_activity(
    activity_id: int,
    completion_data: ActivityCompletionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Mark an activity as completed by the current user.
    Awards points, skills, and checks for achievements.
    """
    gamification_service = GamificationService(db)
    
    try:
        result = gamification_service.complete_activity(
            user_id=current_user.id,
            activity_id=activity_id,
            rating=completion_data.rating,
            feedback=completion_data.feedback
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/leaderboard", summary="Get points leaderboard")
def get_leaderboard(
    limit: int = Query(10, ge=1, le=50, description="Number of top users to return"),
    db: Session = Depends(get_db)
):
    """Get the top users by points for the leaderboard."""
    gamification_service = GamificationService(db)
    return {
        "leaderboard": gamification_service.get_leaderboard(limit),
        "limit": limit
    }


@router.get("/recommendations", summary="Get personalized activity recommendations")
def get_activity_recommendations(
    limit: int = Query(5, ge=1, le=20, description="Number of recommendations to return"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get personalized activity recommendations based on user's skills and progress."""
    gamification_service = GamificationService(db)
    recommendations = gamification_service.recommend_activities_by_skills(current_user.id, limit)
    
    return {
        "recommendations": recommendations,
        "user_id": current_user.id,
        "limit": limit
    }


# Analytics endpoints
@router.get("/analytics/overview", summary="Get gamification analytics overview")
def get_analytics_overview(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get overview analytics for gamification system (admin only)."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Total users with gamification data
    active_users = db.query(User).filter(User.is_active == True).count()
    users_with_completions = db.query(ActivityCompletion.user_id).distinct().count()
    
    # Activity completion stats
    total_completions = db.query(ActivityCompletion).count()
    avg_rating = db.query(func.avg(ActivityCompletion.rating)).filter(
        ActivityCompletion.rating.isnot(None)
    ).scalar() or 0
    
    # Skill and achievement stats
    total_skills = db.query(Skill).count()
    total_achievements = db.query(Achievement).filter(Achievement.is_active == True).count()
    
    # Points distribution
    max_points = db.query(func.max(User.total_points)).scalar() or 0
    avg_points = db.query(func.avg(User.total_points)).scalar() or 0
    
    return {
        "users": {
            "total_active": active_users,
            "with_completions": users_with_completions,
            "engagement_rate": (users_with_completions / active_users * 100) if active_users > 0 else 0
        },
        "activities": {
            "total_completions": total_completions,
            "average_rating": round(avg_rating, 2)
        },
        "content": {
            "total_skills": total_skills,
            "total_achievements": total_achievements
        },
        "points": {
            "max_points": max_points,
            "average_points": round(avg_points, 2)
        }
    }


@router.get("/analytics/user/{user_id}", summary="Get detailed user analytics")
def get_user_analytics(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed analytics for a specific user (admin only or own data)."""
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Verify user exists
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    gamification_service = GamificationService(db)
    user_stats = gamification_service.get_user_stats(user_id)
    
    # Additional detailed analytics
    completions_by_category = db.query(
        Activity.category,
        func.count(ActivityCompletion.id).label('count')
    ).join(ActivityCompletion).filter(
        ActivityCompletion.user_id == user_id
    ).group_by(Activity.category).all()
    
    skills_by_category = db.query(
        Skill.category,
        func.count(UserSkill.id).label('count')
    ).join(UserSkill).filter(
        UserSkill.user_id == user_id
    ).group_by(Skill.category).all()
    
    return {
        "user_id": user_id,
        "username": target_user.username,
        "stats": user_stats,
        "completions_by_category": [
            {"category": cat, "count": count} for cat, count in completions_by_category
        ],
        "skills_by_category": [
            {"category": cat, "count": count} for cat, count in skills_by_category
        ]
    }