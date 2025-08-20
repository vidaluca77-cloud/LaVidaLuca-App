"""
Pydantic schemas for gamification system.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# Achievement schemas
class AchievementBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    category: str = Field(..., max_length=50)
    points: int = Field(default=0, ge=0)
    icon: Optional[str] = Field(None, max_length=100)
    criteria: Optional[Dict[str, Any]] = None

class AchievementCreate(AchievementBase):
    pass

class AchievementResponse(AchievementBase):
    id: int
    is_active: bool
    created_at: datetime
    progress: Optional[int] = None  # User's progress towards this achievement
    max_progress: Optional[int] = None
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# User Achievement schemas
class UserAchievementResponse(BaseModel):
    id: int
    achievement_id: int
    progress: int
    max_progress: int
    is_completed: bool
    completed_at: Optional[datetime]
    achievement: AchievementResponse

    class Config:
        from_attributes = True

# Badge schemas
class BadgeBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=100)
    rarity: str = Field(default="common", regex="^(common|rare|epic|legendary)$")
    requirements: Optional[Dict[str, Any]] = None

class BadgeCreate(BadgeBase):
    pass

class BadgeResponse(BadgeBase):
    id: int
    is_active: bool
    created_at: datetime
    earned_at: Optional[datetime] = None  # When user earned this badge

    class Config:
        from_attributes = True

# User Badge schemas
class UserBadgeResponse(BaseModel):
    id: int
    badge_id: int
    earned_at: datetime
    badge: BadgeResponse

    class Config:
        from_attributes = True

# Points schemas
class PointsTransaction(BaseModel):
    points: int
    reason: str = Field(..., max_length=200)
    activity_type: Optional[str] = Field(None, max_length=50)
    activity_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

# User stats schemas
class UserStatsResponse(BaseModel):
    user_id: int
    level: int
    experience_points: int
    total_points: int
    total_achievements: int
    completed_achievements: int
    total_badges: int
    earned_badges: int
    activities_completed: int
    current_streak: int  # Days of consecutive activity
    rank: Optional[int] = None  # User's rank in leaderboard

# Leaderboard schemas
class LeaderboardResponse(BaseModel):
    user_id: int
    username: str
    full_name: Optional[str]
    total_points: int
    level: int
    achievements_count: int
    badges_count: int
    rank: int

# Activity completion schemas
class ActivityCompletionCreate(BaseModel):
    activity_id: int
    rating: Optional[int] = Field(None, ge=1, le=5)
    feedback: Optional[str] = None

class ActivityCompletionResponse(BaseModel):
    id: int
    activity_id: int
    completed_at: datetime
    rating: Optional[int]
    feedback: Optional[str]
    points_awarded: int

    class Config:
        from_attributes = True

# Progress tracking schemas
class ProgressUpdate(BaseModel):
    activity_type: str
    activity_data: Dict[str, Any]
    points_awarded: Optional[int] = None

class ProgressResponse(BaseModel):
    achievements_unlocked: List[AchievementResponse]
    badges_earned: List[BadgeResponse]
    points_awarded: int
    level_up: bool
    new_level: Optional[int] = None