from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Activity Schemas
class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    difficulty_level: str = "beginner"
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    equipment_needed: Optional[str] = None
    learning_objectives: Optional[str] = None
    is_published: bool = False


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    equipment_needed: Optional[str] = None
    learning_objectives: Optional[str] = None
    is_published: Optional[bool] = None


class Activity(ActivityBase):
    id: int
    creator_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


# Activity Suggestion Schemas
class ActivitySuggestionBase(BaseModel):
    suggestion_reason: str
    ai_generated: bool = True


class ActivitySuggestion(ActivitySuggestionBase):
    id: int
    user_id: int
    activity_id: int
    created_at: datetime
    activity: Activity

    class Config:
        from_attributes = True


# Gamification Schemas

# Skill Schemas
class SkillBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str


class SkillCreate(SkillBase):
    pass


class Skill(SkillBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# User Skill Schemas
class UserSkillBase(BaseModel):
    skill_id: int
    level: int = 1
    experience: int = 0


class UserSkillCreate(UserSkillBase):
    pass


class UserSkill(UserSkillBase):
    id: int
    user_id: int
    obtained_at: datetime
    skill: Skill

    class Config:
        from_attributes = True


# Achievement Schemas
class AchievementBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    points_reward: int = 50
    category: Optional[str] = None
    criteria: Optional[dict] = None
    is_active: bool = True


class AchievementCreate(AchievementBase):
    pass


class Achievement(AchievementBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# User Achievement Schemas
class UserAchievementBase(BaseModel):
    achievement_id: int


class UserAchievementCreate(UserAchievementBase):
    pass


class UserAchievement(UserAchievementBase):
    id: int
    user_id: int
    earned_at: datetime
    achievement: Achievement

    class Config:
        from_attributes = True


# Activity Completion Schemas
class ActivityCompletionBase(BaseModel):
    activity_id: int
    rating: Optional[int] = None
    feedback: Optional[str] = None


class ActivityCompletionCreate(ActivityCompletionBase):
    pass


class ActivityCompletion(ActivityCompletionBase):
    id: int
    user_id: int
    completion_date: datetime
    points_earned: int
    activity: Activity

    class Config:
        from_attributes = True


# User Progress Schemas
class UserProgressBase(BaseModel):
    activities_completed: int = 0
    points_earned: int = 0
    skills_learned: int = 0
    achievements_unlocked: int = 0


class UserProgress(UserProgressBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        from_attributes = True


# Enhanced User Schema with gamification
class UserWithStats(User):
    total_points: int = 0
    current_level: int = 1
    experience_points: int = 0
    user_skills: List[UserSkill] = []
    achievements: List[UserAchievement] = []