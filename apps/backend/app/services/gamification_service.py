"""
Gamification service for managing user progress, points, achievements, and skills.
"""

from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.models import (
    User, Activity, UserSkill, Skill, Achievement, UserAchievement,
    ActivityCompletion, UserProgress
)
from ..schemas.schemas import (
    ActivityCompletionCreate, UserSkillCreate, UserAchievementCreate
)


class GamificationService:
    """Service for handling gamification logic."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_level(self, experience_points: int) -> int:
        """Calculate user level based on experience points."""
        # Level formula: level = 1 + floor(sqrt(xp / 100))
        # This means: Level 1: 0-99 XP, Level 2: 100-399 XP, Level 3: 400-899 XP, etc.
        import math
        return 1 + int(math.sqrt(experience_points / 100))
    
    def get_xp_for_next_level(self, current_level: int) -> int:
        """Get the XP required to reach the next level."""
        return (current_level ** 2) * 100
    
    def complete_activity(
        self, 
        user_id: int, 
        activity_id: int, 
        rating: Optional[int] = None,
        feedback: Optional[str] = None
    ) -> Dict:
        """
        Mark an activity as completed by a user and award points/skills.
        Returns summary of rewards earned.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        activity = self.db.query(Activity).filter(Activity.id == activity_id).first()
        
        if not user or not activity:
            raise ValueError("User or activity not found")
        
        # Check if already completed
        existing_completion = self.db.query(ActivityCompletion).filter(
            ActivityCompletion.user_id == user_id,
            ActivityCompletion.activity_id == activity_id
        ).first()
        
        if existing_completion:
            raise ValueError("Activity already completed by this user")
        
        # Calculate points earned
        base_points = activity.points_reward or 10
        bonus_points = 0
        
        # Bonus for rating
        if rating and rating >= 4:
            bonus_points += 5
        
        total_points = base_points + bonus_points
        
        # Create completion record
        completion = ActivityCompletion(
            user_id=user_id,
            activity_id=activity_id,
            rating=rating,
            feedback=feedback,
            points_earned=total_points
        )
        self.db.add(completion)
        
        # Update user points and experience
        user.total_points += total_points
        user.experience_points += total_points
        
        # Check for level up
        old_level = user.current_level
        new_level = self.calculate_level(user.experience_points)
        level_up = new_level > old_level
        user.current_level = new_level
        
        # Award skills taught by this activity
        new_skills = []
        if activity.skills_taught:
            for skill_id in activity.skills_taught:
                self._award_skill_experience(user_id, skill_id, 10)
                new_skills.append(skill_id)
        
        # Check for new achievements
        new_achievements = self._check_achievements(user_id)
        
        self.db.commit()
        
        return {
            "points_earned": total_points,
            "total_points": user.total_points,
            "level_up": level_up,
            "new_level": new_level if level_up else None,
            "new_skills": new_skills,
            "new_achievements": new_achievements
        }
    
    def _award_skill_experience(self, user_id: int, skill_id: int, experience: int):
        """Award experience points to a specific skill."""
        user_skill = self.db.query(UserSkill).filter(
            UserSkill.user_id == user_id,
            UserSkill.skill_id == skill_id
        ).first()
        
        if user_skill:
            user_skill.experience += experience
            # Level up skill if threshold reached
            new_level = min(5, 1 + (user_skill.experience // 50))  # 50 XP per skill level
            user_skill.level = new_level
        else:
            # Create new skill entry
            user_skill = UserSkill(
                user_id=user_id,
                skill_id=skill_id,
                level=1,
                experience=experience
            )
            self.db.add(user_skill)
    
    def _check_achievements(self, user_id: int) -> List[int]:
        """Check and award new achievements for a user."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return []
        
        # Get all achievements not yet earned by user
        earned_achievement_ids = self.db.query(UserAchievement.achievement_id).filter(
            UserAchievement.user_id == user_id
        ).subquery()
        
        available_achievements = self.db.query(Achievement).filter(
            Achievement.is_active == True,
            ~Achievement.id.in_(earned_achievement_ids)
        ).all()
        
        new_achievements = []
        
        for achievement in available_achievements:
            if self._meets_achievement_criteria(user_id, achievement):
                user_achievement = UserAchievement(
                    user_id=user_id,
                    achievement_id=achievement.id
                )
                self.db.add(user_achievement)
                
                # Award achievement points
                user.total_points += achievement.points_reward
                user.experience_points += achievement.points_reward
                
                new_achievements.append(achievement.id)
        
        return new_achievements
    
    def _meets_achievement_criteria(self, user_id: int, achievement: Achievement) -> bool:
        """Check if user meets the criteria for an achievement."""
        criteria = achievement.criteria or {}
        
        # Example achievement criteria checks
        if achievement.category == "completion":
            completed_count = self.db.query(ActivityCompletion).filter(
                ActivityCompletion.user_id == user_id
            ).count()
            
            required_completions = criteria.get("completions", 1)
            return completed_count >= required_completions
        
        elif achievement.category == "points":
            required_points = criteria.get("points", 100)
            user = self.db.query(User).filter(User.id == user_id).first()
            return user.total_points >= required_points
        
        elif achievement.category == "level":
            required_level = criteria.get("level", 2)
            user = self.db.query(User).filter(User.id == user_id).first()
            return user.current_level >= required_level
        
        elif achievement.category == "skill":
            required_skill_id = criteria.get("skill_id")
            required_skill_level = criteria.get("skill_level", 3)
            if required_skill_id:
                user_skill = self.db.query(UserSkill).filter(
                    UserSkill.user_id == user_id,
                    UserSkill.skill_id == required_skill_id
                ).first()
                return user_skill and user_skill.level >= required_skill_level
        
        return False
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get comprehensive gamification stats for a user."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Get completion stats
        total_completions = self.db.query(ActivityCompletion).filter(
            ActivityCompletion.user_id == user_id
        ).count()
        
        # Get skill stats
        skills_count = self.db.query(UserSkill).filter(
            UserSkill.user_id == user_id
        ).count()
        
        # Get achievement stats
        achievements_count = self.db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id
        ).count()
        
        # Calculate XP for next level
        xp_for_next_level = self.get_xp_for_next_level(user.current_level)
        xp_progress = user.experience_points - ((user.current_level - 1) ** 2) * 100
        xp_needed = xp_for_next_level - ((user.current_level - 1) ** 2) * 100
        
        return {
            "total_points": user.total_points,
            "current_level": user.current_level,
            "experience_points": user.experience_points,
            "xp_for_next_level": xp_for_next_level,
            "xp_progress": xp_progress,
            "xp_needed": xp_needed,
            "activities_completed": total_completions,
            "skills_learned": skills_count,
            "achievements_earned": achievements_count
        }
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top users by points for leaderboard."""
        top_users = self.db.query(User).filter(
            User.is_active == True
        ).order_by(User.total_points.desc()).limit(limit).all()
        
        return [
            {
                "user_id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "total_points": user.total_points,
                "current_level": user.current_level
            }
            for user in top_users
        ]
    
    def recommend_activities_by_skills(self, user_id: int, limit: int = 5) -> List[Dict]:
        """Recommend activities based on user's current skills."""
        # Get user's skills
        user_skills = self.db.query(UserSkill).filter(
            UserSkill.user_id == user_id
        ).all()
        
        user_skill_ids = [us.skill_id for us in user_skills]
        
        # Find activities that teach new skills or match current skills
        if not user_skill_ids:
            # For new users, recommend beginner activities
            activities = self.db.query(Activity).filter(
                Activity.is_published == True,
                Activity.difficulty_level == "beginner"
            ).limit(limit).all()
        else:
            # Find activities with skills the user has (as prerequisites)
            # This is a simplified recommendation - in practice you'd want more sophisticated logic
            activities = self.db.query(Activity).filter(
                Activity.is_published == True
            ).limit(limit).all()
        
        return [
            {
                "activity_id": activity.id,
                "title": activity.title,
                "category": activity.category,
                "difficulty_level": activity.difficulty_level,
                "points_reward": activity.points_reward,
                "skills_taught": activity.skills_taught or []
            }
            for activity in activities
        ]


def create_default_skills(db: Session):
    """Create default skills for the system."""
    default_skills = [
        # Agriculture skills
        {"name": "Jardinage Bio", "description": "Techniques de jardinage biologique", "category": "agriculture"},
        {"name": "Compostage", "description": "Création et gestion de compost", "category": "agriculture"},
        {"name": "Permaculture", "description": "Principes de permaculture", "category": "agriculture"},
        {"name": "Élevage", "description": "Soins aux animaux de ferme", "category": "agriculture"},
        
        # Artisanat skills
        {"name": "Menuiserie", "description": "Travail du bois", "category": "artisanat"},
        {"name": "Poterie", "description": "Travail de l'argile", "category": "artisanat"},
        {"name": "Textile", "description": "Tissage et couture", "category": "artisanat"},
        {"name": "Métallurgie", "description": "Travail des métaux", "category": "artisanat"},
        
        # Social skills
        {"name": "Communication", "description": "Communication interpersonnelle", "category": "social"},
        {"name": "Leadership", "description": "Capacités de leadership", "category": "social"},
        {"name": "Travail d'équipe", "description": "Collaboration en équipe", "category": "social"},
        {"name": "Enseignement", "description": "Transmission de connaissances", "category": "social"},
        
        # Nature skills
        {"name": "Botanique", "description": "Connaissance des plantes", "category": "nature"},
        {"name": "Écologie", "description": "Compréhension des écosystèmes", "category": "nature"},
        {"name": "Orientation", "description": "Navigation et orientation", "category": "nature"},
        {"name": "Observation", "description": "Observation de la nature", "category": "nature"},
    ]
    
    for skill_data in default_skills:
        existing_skill = db.query(Skill).filter(Skill.name == skill_data["name"]).first()
        if not existing_skill:
            skill = Skill(**skill_data)
            db.add(skill)
    
    db.commit()


def create_default_achievements(db: Session):
    """Create default achievements for the system."""
    default_achievements = [
        {
            "name": "Premier Pas",
            "description": "Complétez votre première activité",
            "category": "completion",
            "points_reward": 25,
            "criteria": {"completions": 1}
        },
        {
            "name": "Explorateur",
            "description": "Complétez 5 activités",
            "category": "completion",
            "points_reward": 50,
            "criteria": {"completions": 5}
        },
        {
            "name": "Expert",
            "description": "Complétez 20 activités",
            "category": "completion",
            "points_reward": 150,
            "criteria": {"completions": 20}
        },
        {
            "name": "Centurion",
            "description": "Accumulez 100 points",
            "category": "points",
            "points_reward": 50,
            "criteria": {"points": 100}
        },
        {
            "name": "Millionnaire",
            "description": "Accumulez 1000 points",
            "category": "points",
            "points_reward": 200,
            "criteria": {"points": 1000}
        },
        {
            "name": "Montée en Grade",
            "description": "Atteignez le niveau 5",
            "category": "level",
            "points_reward": 100,
            "criteria": {"level": 5}
        },
        {
            "name": "Maître Artisan",
            "description": "Atteignez le niveau 10",
            "category": "level",
            "points_reward": 300,
            "criteria": {"level": 10}
        }
    ]
    
    for achievement_data in default_achievements:
        existing_achievement = db.query(Achievement).filter(
            Achievement.name == achievement_data["name"]
        ).first()
        if not existing_achievement:
            achievement = Achievement(**achievement_data)
            db.add(achievement)
    
    db.commit()