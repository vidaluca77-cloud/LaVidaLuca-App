"""
Gamification service for La Vida Luca.
Handles all gamification logic including points, achievements, badges, and leveling.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_

from ..models.gamification import (
    Achievement, UserAchievement, Badge, UserBadge, 
    UserPoints, UserLevel, ActivityCompletion
)
from ..models.user import User
from ..models.activity import Activity
from ..schemas.gamification import (
    AchievementCreate, AchievementResponse, BadgeCreate, BadgeResponse,
    UserStatsResponse, LeaderboardResponse, ProgressResponse
)
from ..monitoring import context_logger

class GamificationService:
    """Service class for gamification operations."""

    def __init__(self):
        self.level_thresholds = [0, 100, 250, 500, 1000, 2000, 4000, 8000, 15000, 30000]
        self.achievement_categories = [
            "agriculture", "engagement", "learning", "community", "completion"
        ]

    async def get_user_achievements(
        self, 
        db: Session, 
        user_id: int, 
        category: Optional[str] = None,
        completed_only: bool = False
    ) -> List[AchievementResponse]:
        """Get user's achievements with progress."""
        query = db.query(Achievement, UserAchievement).outerjoin(
            UserAchievement, 
            and_(Achievement.id == UserAchievement.achievement_id, 
                 UserAchievement.user_id == user_id)
        )

        if category:
            query = query.filter(Achievement.category == category)
        
        if completed_only:
            query = query.filter(UserAchievement.is_completed == True)

        results = query.all()
        
        achievements = []
        for achievement, user_achievement in results:
            achievement_data = AchievementResponse(
                id=achievement.id,
                name=achievement.name,
                description=achievement.description,
                category=achievement.category,
                points=achievement.points,
                icon=achievement.icon,
                criteria=achievement.criteria,
                is_active=achievement.is_active,
                created_at=achievement.created_at,
                progress=user_achievement.progress if user_achievement else 0,
                max_progress=user_achievement.max_progress if user_achievement else 1,
                is_completed=user_achievement.is_completed if user_achievement else False,
                completed_at=user_achievement.completed_at if user_achievement else None
            )
            achievements.append(achievement_data)

        return achievements

    async def claim_achievement(self, db: Session, user_id: int, achievement_id: int) -> Optional[int]:
        """Claim an achievement and award points."""
        user_achievement = db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_id == achievement_id,
            UserAchievement.is_completed == True
        ).first()

        if not user_achievement or user_achievement.completed_at:
            return None  # Already claimed or not eligible

        achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()
        if not achievement:
            return None

        # Mark as claimed
        user_achievement.completed_at = datetime.utcnow()
        
        # Award points
        await self.award_points(db, user_id, achievement.points, f"Achievement: {achievement.name}")
        
        db.commit()
        context_logger.info("Achievement claimed", user_id=user_id, achievement_id=achievement_id, points=achievement.points)
        
        return achievement.points

    async def get_user_badges(
        self, 
        db: Session, 
        user_id: int, 
        earned_only: bool = False
    ) -> List[BadgeResponse]:
        """Get user's badges."""
        if earned_only:
            query = db.query(Badge, UserBadge).join(
                UserBadge, Badge.id == UserBadge.badge_id
            ).filter(UserBadge.user_id == user_id)
        else:
            query = db.query(Badge, UserBadge).outerjoin(
                UserBadge, 
                and_(Badge.id == UserBadge.badge_id, UserBadge.user_id == user_id)
            )

        results = query.all()
        
        badges = []
        for badge, user_badge in results:
            badge_data = BadgeResponse(
                id=badge.id,
                name=badge.name,
                description=badge.description,
                icon=badge.icon,
                rarity=badge.rarity,
                requirements=badge.requirements,
                is_active=badge.is_active,
                created_at=badge.created_at,
                earned_at=user_badge.earned_at if user_badge else None
            )
            badges.append(badge_data)

        return badges

    async def get_user_stats(self, db: Session, user_id: int) -> UserStatsResponse:
        """Get comprehensive user statistics."""
        # Get or create user level info
        user_level = db.query(UserLevel).filter(UserLevel.user_id == user_id).first()
        if not user_level:
            user_level = UserLevel(user_id=user_id)
            db.add(user_level)
            db.commit()

        # Count achievements
        total_achievements = db.query(Achievement).filter(Achievement.is_active == True).count()
        completed_achievements = db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id,
            UserAchievement.is_completed == True
        ).count()

        # Count badges
        total_badges = db.query(Badge).filter(Badge.is_active == True).count()
        earned_badges = db.query(UserBadge).filter(UserBadge.user_id == user_id).count()

        # Count completed activities
        activities_completed = db.query(ActivityCompletion).filter(
            ActivityCompletion.user_id == user_id
        ).count()

        # Calculate current streak (simplified)
        current_streak = await self._calculate_streak(db, user_id)

        # Get rank
        rank = await self._get_user_rank(db, user_id)

        return UserStatsResponse(
            user_id=user_id,
            level=user_level.level,
            experience_points=user_level.experience_points,
            total_points=user_level.total_points,
            total_achievements=total_achievements,
            completed_achievements=completed_achievements,
            total_badges=total_badges,
            earned_badges=earned_badges,
            activities_completed=activities_completed,
            current_streak=current_streak,
            rank=rank
        )

    async def get_leaderboard(
        self, 
        db: Session, 
        period: str = "monthly", 
        limit: int = 10
    ) -> List[LeaderboardResponse]:
        """Get leaderboard for specified period."""
        # Calculate date range based on period
        now = datetime.utcnow()
        if period == "weekly":
            start_date = now - timedelta(weeks=1)
        elif period == "monthly":
            start_date = now - timedelta(days=30)
        else:  # all_time
            start_date = datetime.min

        # Query for leaderboard
        query = db.query(
            User.id,
            User.username,
            User.full_name,
            func.coalesce(func.sum(UserPoints.points), 0).label('total_points'),
            func.coalesce(UserLevel.level, 1).label('level'),
            func.count(UserAchievement.id).label('achievements_count'),
            func.count(UserBadge.id).label('badges_count')
        ).outerjoin(UserPoints, User.id == UserPoints.user_id)\
         .outerjoin(UserLevel, User.id == UserLevel.user_id)\
         .outerjoin(UserAchievement, and_(
             User.id == UserAchievement.user_id,
             UserAchievement.is_completed == True
         ))\
         .outerjoin(UserBadge, User.id == UserBadge.user_id)

        if period != "all_time":
            query = query.filter(UserPoints.created_at >= start_date)

        results = query.group_by(
            User.id, User.username, User.full_name, UserLevel.level
        ).order_by(desc('total_points')).limit(limit).all()

        leaderboard = []
        for rank, result in enumerate(results, 1):
            leaderboard.append(LeaderboardResponse(
                user_id=result.id,
                username=result.username,
                full_name=result.full_name,
                total_points=result.total_points,
                level=result.level,
                achievements_count=result.achievements_count,
                badges_count=result.badges_count,
                rank=rank
            ))

        return leaderboard

    async def award_points(
        self, 
        db: Session, 
        user_id: int, 
        points: int, 
        reason: str,
        activity_type: Optional[str] = None,
        activity_id: Optional[int] = None
    ) -> int:
        """Award points to a user and update their level."""
        # Create points transaction
        points_transaction = UserPoints(
            user_id=user_id,
            points=points,
            reason=reason,
            activity_type=activity_type,
            activity_id=activity_id
        )
        db.add(points_transaction)

        # Get or create user level
        user_level = db.query(UserLevel).filter(UserLevel.user_id == user_id).first()
        if not user_level:
            user_level = UserLevel(user_id=user_id)
            db.add(user_level)

        # Update points and experience
        user_level.total_points += points
        user_level.experience_points += points

        # Check for level up
        new_level = self._calculate_level(user_level.experience_points)
        if new_level > user_level.level:
            user_level.level = new_level
            context_logger.info("User leveled up", user_id=user_id, new_level=new_level)

        db.commit()
        return user_level.total_points

    async def track_activity(
        self, 
        db: Session, 
        user_id: int, 
        activity_type: str, 
        activity_data: Dict[str, Any]
    ) -> List[str]:
        """Track user activity and check for achievement progress."""
        achievements_unlocked = []

        # Award base points for activity
        base_points = self._get_activity_points(activity_type)
        if base_points > 0:
            await self.award_points(db, user_id, base_points, f"Activity: {activity_type}")

        # Check for achievement progress
        achievements = db.query(Achievement).filter(Achievement.is_active == True).all()
        
        for achievement in achievements:
            if self._check_achievement_criteria(achievement, activity_type, activity_data):
                # Update or create user achievement
                user_achievement = db.query(UserAchievement).filter(
                    UserAchievement.user_id == user_id,
                    UserAchievement.achievement_id == achievement.id
                ).first()

                if not user_achievement:
                    user_achievement = UserAchievement(
                        user_id=user_id,
                        achievement_id=achievement.id,
                        max_progress=achievement.criteria.get('target', 1)
                    )
                    db.add(user_achievement)

                # Update progress
                if not user_achievement.is_completed:
                    user_achievement.progress += 1
                    if user_achievement.progress >= user_achievement.max_progress:
                        user_achievement.is_completed = True
                        achievements_unlocked.append(achievement.name)

        db.commit()
        return achievements_unlocked

    async def create_achievement(self, db: Session, achievement_data: AchievementCreate) -> Achievement:
        """Create a new achievement."""
        achievement = Achievement(**achievement_data.dict())
        db.add(achievement)
        db.commit()
        db.refresh(achievement)
        return achievement

    async def create_badge(self, db: Session, badge_data: BadgeCreate) -> Badge:
        """Create a new badge."""
        badge = Badge(**badge_data.dict())
        db.add(badge)
        db.commit()
        db.refresh(badge)
        return badge

    def _calculate_level(self, experience_points: int) -> int:
        """Calculate user level based on experience points."""
        for level, threshold in enumerate(self.level_thresholds):
            if experience_points < threshold:
                return max(1, level)
        return len(self.level_thresholds)

    def _get_activity_points(self, activity_type: str) -> int:
        """Get base points for different activity types."""
        point_map = {
            "activity_completion": 50,
            "quiz_completion": 30,
            "forum_post": 10,
            "daily_login": 5,
            "profile_update": 15
        }
        return point_map.get(activity_type, 10)

    def _check_achievement_criteria(
        self, 
        achievement: Achievement, 
        activity_type: str, 
        activity_data: Dict[str, Any]
    ) -> bool:
        """Check if activity meets achievement criteria."""
        if not achievement.criteria:
            return False

        criteria = achievement.criteria
        if criteria.get('activity_type') != activity_type:
            return False

        # Add more sophisticated criteria checking here
        return True

    async def _calculate_streak(self, db: Session, user_id: int) -> int:
        """Calculate user's current activity streak."""
        # Simplified streak calculation - count consecutive days with activity
        # In a real implementation, this would be more sophisticated
        recent_activities = db.query(ActivityCompletion).filter(
            ActivityCompletion.user_id == user_id
        ).order_by(desc(ActivityCompletion.completed_at)).limit(30).all()

        if not recent_activities:
            return 0

        # Simple consecutive day counting
        streak = 1
        current_date = recent_activities[0].completed_at.date()
        
        for activity in recent_activities[1:]:
            activity_date = activity.completed_at.date()
            if (current_date - activity_date).days == 1:
                streak += 1
                current_date = activity_date
            else:
                break

        return streak

    async def _get_user_rank(self, db: Session, user_id: int) -> Optional[int]:
        """Get user's rank in the overall leaderboard."""
        user_level = db.query(UserLevel).filter(UserLevel.user_id == user_id).first()
        if not user_level:
            return None

        rank = db.query(func.count(UserLevel.id)).filter(
            UserLevel.total_points > user_level.total_points
        ).scalar()

        return rank + 1 if rank is not None else 1

# Global service instance
gamification_service = GamificationService()